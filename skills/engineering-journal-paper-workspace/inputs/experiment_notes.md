# Experiment notes (lab log)

Platform: treadmill cart moving at 0.3 m/s, AprilTag 36h11 (160 mm) on deck.
Drone: 450 mm quad, PX4 1.14, downward global-shutter camera 640x480 @ 8 fps.
Motion capture (OptiTrack, 120 Hz) gives ground-truth touchdown offset.

Ran N=12 landings per mode:
- baro_vision mode: touchdown offset mean 46 mm, sd 18 mm. All 12 within deck.
- baro_only mode: mean 187 mm, sd 92 mm. 3 of 12 missed the 300 mm deck radius.

Vision mode offsets by direction: downwind trials 41 +/- 15 mm, upwind 52 +/- 20 mm.
Paired t-test on offsets p = 0.0002. Paired diff 141 mm, CI [98, 184].
Descent time: vision 14.2 +/- 1.9 s vs baro 9.8 +/- 0.7 s.
One vision trial had 2 tag dropouts > 0.4 s (decay-hold engaged, recovered).
