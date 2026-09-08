"""Autonomous landing controller for quadrotor on a moving ground platform."""

import time
import zmq
import numpy as np
from mavsdk_shim import send_velocity_setpoint, get_telemetry

CONTROL_RATE_HZ = 50
CAMERA_RATE_HZ = 8          # AprilTag detections from downward camera
EMA_ALPHA = 0.35
KP_XY = 0.9
KD_XY = 0.15
KP_Z = 0.6
V_MAX_XY = 1.2              # m/s
V_MAX_Z = 0.5               # m/s
DESCEND_GATE_PX = 40        # start descending when tag center within this radius
TAG_TIMEOUT_S = 0.4
MAX_CONSECUTIVE_MISSES = 3
FLARE_ALT_M = 0.35
TOUCHDOWN_VZ = 0.25
HSV_LOWER = (35, 60, 90)    # platform marker color gate
HSV_UPPER = (85, 255, 255)
ZMQ_ADDR = "tcp://127.0.0.1:6001"


class ComplementaryAltitude:
    """Fuse barometer (drifty, 50 Hz) with rangefinder (noisy near ground, 20 Hz)."""

    def __init__(self, tau=0.8):
        self.tau = tau
        self.alt = None

    def update(self, baro_alt, range_alt, dt):
        if self.alt is None:
            self.alt = range_alt if range_alt is not None else baro_alt
            return self.alt
        pred = self.alt + (baro_alt - self.alt)  # baro tracks fast motion
        if range_alt is not None:
            k = dt / (self.tau + dt)
            self.alt = (1 - k) * pred + k * range_alt
        else:
            self.alt = pred
        return self.alt


class LandingController:
    """mode: 'baro_only' (open-loop descent) or 'baro_vision' (tag-servoed)."""

    def __init__(self, mode="baro_vision"):
        self.mode = mode
        self.alt_filter = ComplementaryAltitude()
        self.ema_uv = None
        self.last_tag_t = 0.0
        self.misses = 0
        self.state = "SEARCH"   # SEARCH -> ALIGN -> DESCEND -> FLARE -> DONE
        self.last_good_cmd = np.zeros(3)
        ctx = zmq.Context()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.connect(ZMQ_ADDR)
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "tag/uv")

    def _smooth(self, uv):
        if self.ema_uv is None:
            self.ema_uv = np.array(uv, dtype=float)
        else:
            self.ema_uv = EMA_ALPHA * np.array(uv) + (1 - EMA_ALPHA) * self.ema_uv
        return self.ema_uv

    def step(self, dt):
        tel = get_telemetry()
        alt = self.alt_filter.update(tel.baro_alt, tel.range_alt, dt)
        uv = self._poll_tag()
        if uv is not None:
            self.last_tag_t = time.time()
            self.misses = 0
            uv = self._smooth(uv)
        else:
            self.misses += 1

        if self.mode == "baro_only":
            v_cmd = np.array([0.0, 0.0, -V_MAX_Z])
        else:
            if time.time() - self.last_tag_t > TAG_TIMEOUT_S:
                if self.misses > MAX_CONSECUTIVE_MISSES:
                    self.state = "SEARCH"
                v_cmd = self.last_good_cmd * 0.5   # decay hold
            else:
                err = self.ema_uv - np.array([320, 240])  # image center
                vx = np.clip(-KP_XY * err[1] / 240 - KD_XY * tel.vx, -V_MAX_XY, V_MAX_XY)
                vy = np.clip(-KP_XY * err[0] / 320 - KD_XY * tel.vy, -V_MAX_XY, V_MAX_XY)
                vz = -V_MAX_Z if np.linalg.norm(err) < DESCEND_GATE_PX else 0.0
                if alt < FLARE_ALT_M:
                    self.state = "FLARE"
                    vz = -TOUCHDOWN_VZ
                v_cmd = np.array([vx, vy, vz])
                self.last_good_cmd = v_cmd

        send_velocity_setpoint(*v_cmd)   # streamed at 50 Hz
        return v_cmd

    def _poll_tag(self):
        try:
            _, msg = self.sub.recv_multipart(flags=zmq.NOBLOCK)
            u, v = np.frombuffer(msg, dtype=np.float32)
            return (u, v)
        except zmq.Again:
            return None
