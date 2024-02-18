import math
import numpy as np
from scipy.spatial.transform import Rotation as R


from .helpers import struct_change
from .structs import LD90Joints, Pose
from .config import *
from .com import ARCL


class LD90:

    def __init__(self, ipLD90=ipLD90, portLD90=portLD90):

        self.ipLD90 = ipLD90
        self.portLD90 = portLD90
        
        self.arcl = ARCL(ipLD90, portLD90)


    def get_joints(self) -> LD90Joints:

        arg = "status"
        self.arcl.send_arcl(arg)

        loc = self.arcl.read_arcl("Location",
                                   print, "Failed")
        loc = loc.split(" ")

        cs = []
        for l in loc:
            if l not in ["", " ", ":", ": "]:
                cs.append(l)

        return LD90Joints(cs)
    

    def kinematics(self, q) -> Pose:

        q = struct_change(q, LD90Joints)

        pos = [q.x, q.y, 0]
        r = R.from_euler("z", q.phi, degrees=True)
        eul = r.as_euler("ZYX", degrees=True).tolist()

        pose = pos + eul

        p = Pose(pose)
        
        return p


    def state_of_charge(self) -> str:
        
        self.arcl.send_arcl("status")

        arg = "StateOfCharge"

        soc = self.arcl.read_arcl("StateOfCharge",
                                   print, "Failed")

        return soc


    def say(self, text: str):

        self.arcl.send_arcl("say " + text)

    
    def play_sound(self, name):

        self.arcl.send_arcl(f"play {name}")


    def dock(self):

        arg = "dock"
        self.arcl.send_arcl(arg)

        self.arcl.read_arcl("DockingState",
                            print, "Failed")


    def undock(self):

        arg = "undock"
        self.arcl.send_arcl(arg)

        self.arcl.read_arcl("Undocked",
                            print, "Failed")


    def goto(self, q):

        q = struct_change(q, LD90Joints)

        arg = "doTask gotoPoint " + str(int(q.x)) + " " + str(int(q.y))
        arg += " " + str(int(q.phi))
        self.arcl.send_arcl(arg)

        self.arcl.read_arcl("Completed doing task gotoPoint",
                            self.goto, q)
        

    def move(self, q):

        self.goto(q)


    def patrol(self, name):

        arg = "patrolOnce " + name
        self.arcl.send_arcl(arg)

        self.arcl.read_arcl("Finished patrolling route",
                            self.patrol, arg)