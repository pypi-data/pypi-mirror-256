import os
import numpy as np
from scipy.spatial.transform import Rotation as R


def attributes(target, source):
    for a in dir(source):
            if not a.startswith("__"):
                if not callable(a):
                    setattr(target, a, getattr(source, a))

    return target


def struct_input(argvs, typ, nums, err):
    
    # right len
    if len(argvs) == 0:
        return None
        
    elif len(argvs) == nums:
        args = argvs

    elif len(argvs) == 1 and len(argvs[0]) == nums:
        args = argvs[0]
    
    else:
        raise err
    

    # right types
    if isinstance(typ, list):
        for i in range(len(typ)):
            if not isinstance(args[i], typ[i]):
                raise err

    else:
        try:
            args = list(map(typ, args))
        except:
            raise err
    
    return args


def get_datapath():

    path = os.getcwd()
    dataPath = path + "/data"

    return dataPath


def struct_change(pose, target):

    if isinstance(pose, np.ndarray):
            pose = pose.tolist()
    if isinstance(pose, list):
        pose = target(pose)

    return pose


def pose_change(pose, now="zyx", target="ZYX"):

    pos = pose.ret[:3]
    if isinstance(pos, np.ndarray):
        pos = pos.tolist()

    rot = R.from_euler(now, pose.ret[3:], degrees=True)
    rot = rot.as_euler(target, degrees=True)
    if isinstance(rot, np.ndarray):
        rot = rot.tolist()

    pose.ret = pos + rot

    return pose