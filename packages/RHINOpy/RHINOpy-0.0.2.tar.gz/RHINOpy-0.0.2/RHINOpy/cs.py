import numpy as np
from scipy.spatial.transform import Rotation as R

from .helpers import pose_change, struct_change
from .structs import Pose, LD90Joints
from .LD90 import LD90
from .TM5 import TM5   



class CS_WORLD:

    def __new__(self) -> Pose:

        return Pose(0,0,0,0,0,0)


class CS_LD90:

    def __new__(self) -> Pose:

        ld90 = LD90()
        q = ld90.get_joints()
        return ld90.kinematics(q)


class CS_TM5_BASE:

    def __new__(self) -> Pose:

        return Pose(0,0, 833, 0,0,0)
    

class CS_TM5_FLANGE:

    def __new__(self) -> Pose:

        tm5 = TM5()
        p = Pose(tm5.get_pose_flange())
        p = pose_change(p, "ZYX", "zyx")

        return p
    

class CS_TM5_TCP:

    def __new__(self) -> Pose:

        tm5 = TM5()
        pFlange = tm5.get_pose_flange()
        pTool = tm5.get_pose_tcp()

        pDiff = np.array(pTool.ret) - np.array(pFlange.ret)
        p = Pose(pDiff)
        p = pose_change(p, "ZYX", "zyx")

        return p


class CS_CAMERA:

    def __new__(self) -> Pose:

        pDiff = CS_TM5_TCP()

        base2tcp = pose2matrix(pDiff)
        tcp2flange = np.linalg.inv(base2tcp)
        
        pos = [0, -79, 52.25 + 6]
        euler = [0, 0, 0]
        flange2cam = Pose(pos + euler)
        flange2cam = pose_change(flange2cam, "ZYX", "zyx")
        flange2cam = pose2matrix(flange2cam)

        T = np.dot(tcp2flange, flange2cam)

        return matrix2pose(T)
    

def pose2matrix(pose: Pose) -> np.ndarray:

    r = R.from_euler('zyx', pose.ret[3:], degrees=True)
    TR = r.as_matrix()
    T = np.identity(4)
    T[:3, :3] = TR
    T[:3, 3] = pose.ret[:3]

    return T


def matrix2pose(m: np.ndarray) -> Pose:

    pos = m[:3, 3].tolist()
    rot = R.from_matrix(m[:3, :3])
    euler = rot.as_euler('zyx', degrees=True).tolist()

    return Pose(pos + euler)


def transform(pose, current, target) -> Pose:

    cs = [CS_WORLD, CS_LD90, CS_TM5_BASE, 
            CS_TM5_FLANGE, CS_TM5_TCP, CS_CAMERA]
    
    pose = struct_change(pose, Pose)

    try:
        c = cs.index(current)
    except:
        raise ValueError(
            """"current" must be a defined coordinate system.""")
    
    try:
        t = cs.index(target)
    except:
        raise ValueError(
            """"target must be a defined coordinate system.""")
    

    if c == t:
        return pose
    elif c < t:
        t += 1
        rs = np.arange(c, t)[::-1]
        t -= 1
    else:
        c += 1
        rs = range(t, c)
        c -= 1
        
    T_n = np.identity(4)
    for i in rs:

        p = cs[i]()
            
        T_i = pose2matrix(p)

        T_n = np.dot(T_n, T_i)

    if c < t:
        T_n = np.linalg.inv(T_n)

    r = R.from_matrix(T_n[:3, :3])
    r = r.as_euler("zyx", degrees=True)

    point = np.array(pose.ret[:4])
    point[3] = 1
    point = np.dot(T_n, point)[:3].tolist()

    matPose = pose2matrix(pose)[:3, :3]
    mat = np.dot(T_n[:3, :3], matPose)
    rot = R.from_matrix(mat)
    euler = rot.as_euler("zyx", degrees=True)
    euler += np.array(pose.ret[3:])
    euler = euler.tolist()

    return Pose(point + euler)