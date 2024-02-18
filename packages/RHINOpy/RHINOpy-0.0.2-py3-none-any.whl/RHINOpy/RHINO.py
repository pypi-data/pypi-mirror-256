import techmanpy as tp

from .config import *
from .structs import *
from .customs import Joints
from .com import *
from .LD90 import LD90
from .TM5 import TM5



class RHINO:

    def __init__(self, speed=0.05, ipLD90=ipLD90, portLD90=portLD90, ipTM5=ipTM5):

        self.ipLD90 = ipLD90
        self.portLD90 = portLD90

        self.ipTM5 = ipTM5

        self.ld90 = LD90(ipLD90, portLD90)
        self.tm5 = TM5(ipTM5, speed=speed)


    def get_joints(self) -> RHINOJoints:

        l = self.ld90.get_joints()
        
        t = self.tm5.get_joints()

        return RHINOJoints(l, t)
    
    
    def publish_joints(self):

        async def _publish_joints():

            #pub = MQTTWrapperPublish(ipIOT, RHINOJoints)

            async with tp.connect_svr(robot_ip=self.ipTM5) as conn:

                while True:
                    l = self.ld90.get_joints()
                    t = await conn.get_value("Joint_Angle")
                    t = TM5Joints(t)

                    #pub.publish(RHINOJoints(l, t))

        asyncio.run(_publish_joints())


    def get_pose(self) -> RHINOPose:
        
        l = self.ld90.get_joints()

        t = self.tm5.get_pose_tcp()

        return RHINOPose(l, t)
    

    def move(self, name):

        js = Joints().import_joints(name)
        
        if js["type"] == "2":
            raise Exception("Use LD90().move() for the saved joints")
            
        if js["type"] == "3":
            raise Exception("Use TM5().move() for the saved joints")

        if not isinstance(js["joints"], list):
            js["joints"] = [js["joints"]]
        
        for j in js["joints"]:
        
            self.ld90.move(j.LD90Joints)
            self.tm5.ptp_joints(j[1].TM5Joints)    
            

    def LD90_move(self, name):

        js = Joints().import_joints(name)

        if js["type"] == "1":
            raise Exception("Use RHINO().move() for the saved joints")
        
        if js["type"] == "3":
            raise Exception("Use TM5().move() for the saved joints")

        if not isinstance(js["joints"], list):
            js["joints"] = [js["joints"]]
        
        for j in js["joints"]:

            self.ld90.move(j)


    def TM5_move(self, name):

        js = Joints().import_joints(name)

        if js["type"] == "1":
                raise Exception("Use RHINO().move() for the saved joints")

        if js["type"] == "2":
            raise Exception("Use LD90().move() for the saved joints")

        if not isinstance(js["joints"], list):
            js["joints"] = [js["joints"]]
        
        for j in js["joints"]:
            self.tm5.ptp_joints(j)