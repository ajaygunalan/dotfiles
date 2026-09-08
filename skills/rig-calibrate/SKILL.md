---
name: rig-calibrate
description: Calibrate the US rig position by reading 4 corner TCP positions from the robot, computing the correct placement, and updating the overlay code.
user-invocable: true
---

# Rig Position Calibration

Calibrate the position of the US calibration rig (water tank) for Rerun visualization. The user freedrives the robot to touch 4 corners of the rig's top opening, and this skill computes the correct placement.

## Convention

The 4 corners of the rig top opening, viewed from above:

```
    D --------- C
    |           |
    |   (box)   |
    |           |
    A --------- B
      (front)
```

- **A** = front-left
- **B** = front-right
- **C** = back-right (diagonal of A)
- **D** = back-left (diagonal of B)

Front = the side facing the operator/robot base.

## Rig Geometry

- STL: `models/rig/us_cal_rig_m.stl` (meters)
- Top opening: 136mm x 136mm square
- Height: 103mm
- STL origin: bottom corner below D (STL coordinates [0, 0, 0])
- After +90° X rotation, the open top faces Z-up

## Workflow

1. User runs `python -m rcm_qp.pose_control --ip 169.254.120.1`
2. User presses `v` for vertical pose, then `f` for freedrive
3. User touches probe tip to corner A, tells Claude "corner A"
4. Claude reads joint angles via `rtde_receive` and computes TCP (FK yellow point)
5. Repeat for B, C, D
6. Claude computes:
   - Snap corners to 136mm grid (box is a known square)
   - Average Z across all 4 (box top is level)
   - Center = average of all 4 corners
   - STL origin = D_world - [0, 0, 0.103] (D is above STL origin, subtract box height)
   - Validate: edges should be ~130-136mm (probe tip is ~3-4mm inside actual edge)
   - Diagonal should be ~185-192mm
7. Claude updates `rcm_qp/perception/cal_poses.py` — the ABCD corners
   (`RIG_CORNER_A/B/C/D`). Both MeshCat and Rerun import from here.
   - `rig_transform()` derives (R, t) from `RIG_CORNER_D`
   - `us_rerun_overlay.py` imports `RIG_CORNER_*` directly
8. Commit and push

## Reading TCP

```python
import rtde_receive, numpy as np
from rcm_qp.perception.us_common import create_fk_plant, fk

r = rtde_receive.RTDEReceiveInterface('169.254.120.1')
q = np.array(r.getActualQ())
r.disconnect()

plant, ctx, world, tcp = create_fk_plant()
R, t = fk(plant, ctx, world, tcp, q)
# t is the TCP (yellow point) in robot base frame
```

## Computing Position

```python
# Measured corners (from TCP readings)
A = np.array([...])  # front-left
B = np.array([...])  # front-right
C = np.array([...])  # back-right
D = np.array([...])  # back-left

# Snap to geometry
center = (A + B + C + D) / 4
z_avg = center[2]  # box top is level

# STL origin is directly below D by box height
D_world = np.array([D[0], D[1], z_avg])
rig_origin = D_world - np.array([0, 0, 0.103])
```

## Rerun Logging (in us_rerun_overlay.py)

```python
from scipy.spatial.transform import Rotation

D_world = np.array([...])  # from calibration
rig_origin = D_world - np.array([0, 0, 0.103])
rot_x90 = Rotation.from_euler("x", 90, degrees=True).as_quat()

rr.log("world/rig",
    rr.Asset3D(path=str(rig_stl_m)),
    rr.InstancePoses3D(
        translations=[rig_origin.tolist()],
        quaternions=[rr.Quaternion(xyzw=rot_x90)],
    ),
    rr.CoordinateFrame("world"),  # REQUIRED — connects to URDF spatial graph
)
```

## Key Traps

- **CoordinateFrame("world")** is required on any entity alongside URDF robot
- **InstancePoses3D** (not Transform3D) to position Asset3D
- **Log in loop** (not static before loop) when using spawn(connect=False) + set_sinks()
- **STL in meters** — use `us_cal_rig_m.stl`, not the mm version
- **+90° X rotation** — makes the box opening face Z-up
