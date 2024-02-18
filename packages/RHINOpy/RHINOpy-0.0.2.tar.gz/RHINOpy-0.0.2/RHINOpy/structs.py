from .exceptions import *
from .helpers import struct_input



class topicsMQTT:

    def __init__(self, struct):

        self.struct = struct()
        self.name = self.struct.name
        self.titles = self.struct.titles

        self.topics = []
        if isinstance(self.name, list):
            self.__create("")
        else:
            self.__create(self.name)


    def __create(self, n):

        for t in self.titles:
            self.topics.append(n + t)


    def __str__(self) -> str:
        s = f"topicsMQTT([{self.name}, {self.topics}])"
        return s
    

class LD90Joints:

    def __init__(self, *argvs):

        self.NUMS = 3
        self.name = "RHINO/LD90/"
        self.typ = float
        self.err = LD90JointsErr
        self.titles = ["x", "y", "phi"]

        args = struct_input(argvs, self.typ, self.NUMS, self.err)
        if args == None: return
        
        self.x = args[0]
        self.y = args[1]
        self.phi = args[2]
        self.ret = [self.x, self.y, self.phi]
    
    
    def __str__(self) -> str:
        return f"LD90Joints([{self.x}, {self.y}, {self.phi} [degrees]])"""
    

class TM5Joints:

    def __init__(self, *argvs):
        
        self.NUMS = 6
        self.name = "RHINO/TM5/"
        self.typ = float
        self.err = TM5JointsErr
        self.titles = ["q" + str(s) for s in range(6)]
        
        args = struct_input(argvs, self.typ, self.NUMS, self.err)
        if args == None: return
        
        self.ret = []
        for a in args:
            self.ret.append(a)


    def __str__(self) -> str:
        s = f"TM5Joints({self.ret}; [degrees])"
        return s
    

class RHINOJoints:

    def __init__(self, *argvs):

        self.NUMS = 2
        self.name = ["RHINO/LD90/", "RHINO/TM5/"]
        self.typ = [LD90Joints, TM5Joints]
        self.err = RHINOJointsErr

        self.titles = []
        for i in range(len(self.typ)):
            n = self.name[i]
            ts = self.typ[i]().titles
            for t in ts:
                self.titles.append(n + t)

        args = struct_input(argvs, self.typ, self.NUMS, self.err)
        if args == None: return
        
        self.LD90Joints = args[0]
        self.TM5Joints = args[1]

        self.ret = self.LD90Joints.ret + self.TM5Joints.ret
        
    
    def __str__(self) -> str:
        s = f"RHINOJoints([{self.LD90Joints}, {self.TM5Joints}])"
        return s
    

class Pose:

    def __init__(self, *argvs):

        self.NUMS = 6
        self.name = "RHINO/TM5_TCP/"
        self.typ = float
        self.err = PoseErr
        self.titles = ["x", "y", "z", "rz", "ry'", "rx''"]
        
        args = struct_input(argvs, self.typ, self.NUMS, self.err)
        if args == None: return
        
        self.ret = []
        for a in args:
            self.ret.append(a)
        
        self.pose = {}
        for i in range(self.NUMS):
            self.pose[self.titles[i]] = self.ret[i]


    def __str__(self) -> str:
        s = f"Pose({self.ret}; [1-3: [mm], 4-6: Euler (zy'x'') [degrees])"
        return s
    

class RHINOPose:

    def __init__(self, *argvs):

        self.NUMS = 2
        self.name = ["RHINO/", "RHINO/"]
        self.typ = [LD90Joints, Pose]
        self.err = RHINOPoseErr

        self.titles = []
        for i in range(len(self.typ)):
            n = self.name[i]
            ts = self.typ[i]().titles
            for t in ts:
                self.titles.append(n + t)

        args = struct_input(argvs, self.typ, self.NUMS, self.err)
        if args == None: return
        
        self.LD90Joints = args[0]
        self.TM5Pose = args[1]

        self.ret = self.LD90Joints.ret + self.TM5Pose.ret
        
    
    def __str__(self) -> str:
        s = f"RHINOPose([{self.LD90Joints}, {self.TM5Pose}])"
        return s