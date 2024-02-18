import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.optimize import root, minimize
import techmanpy as tp
import asyncio

from .config import *
# from .customs import *
from .helpers import struct_change, pose_change
from .structs import Pose, TM5Joints


class TM5:

    def __init__(self, ipTM5=ipTM5, speed=0.1, acc=200):

        self.ipTM5 = ipTM5
        self.speed = speed
        self.acc = acc
        self.tagMove = 1


    def DH(self, theta, d, a, alpha):

        T_i = np.array(
            [[np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha),  a * np.cos(theta)],
             [np.sin(theta), np.cos(theta) * np.cos(alpha),  -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
             [0,               np.sin(alpha),                    np.cos(alpha),                    d],
             [0,               0,                                  0,                                  1]])
        
        return T_i


    def kinematics(self, q, rot="euler") -> Pose:

        q = struct_change(q, TM5Joints)

        theta = np.array(q.ret) * np.pi / 180
        theta[1] -= np.pi/2
        theta[3] += np.pi/2
        d =     [145.2, 146, -129.7, 106, 106, 113.2]
        a =     [0, 429, 411.5, 0, 0, 0]
        alpha = [-np.pi/2, 0, 0, np.pi/2, -np.pi/2, 0]

        T = np.identity(4)
        for p in zip(theta, d, a, alpha):
            T_i = self.DH(*p)
            T = np.dot(T, T_i)

        pos = np.array([0, 0, 0, 1])
        posT = np.dot(T, pos)[:3].tolist()
        r = R.from_matrix(T[:3, :3])

        if rot == "euler":
            euler = r.as_euler("zyx")
            euler = euler * 180 / np.pi
            euler = euler.tolist()
            return Pose(posT + euler)

        if rot == "quat":
            quat = r.as_quat().tolist()
            return posT + quat
        
        else:
            raise ValueError("""rot must be either "euler" or "quat".""")


    def inv_kinematics(self, p, q0=None) -> TM5Joints:   
        
        def func_root(q, p):
            q = TM5Joints(q)
            err = np.array(p) - np.array(self.kinematics(q, "quat"))
            return np.linalg.norm(err)
        
        if q0 == None:
            q0 = 6 * [0]

        p = struct_change(p, Pose)
        q0 = struct_change(q0, TM5Joints)

        r = R.from_euler("zyx", p.ret[3:])
        quat = r.as_quat()
        p = p.ret[:3] + quat.tolist()

        q = minimize(func_root, q0.ret, args=(p))

        return TM5Joints(q.x)


    def camera_light(self, val: bool):

        async def _camera_light(val):
            async with tp.connect_svr(robot_ip=self.ipTM5) as conn:

                if val: val = "1"
                else: val = "0"

                await conn.set_value("Camera_Light", val)

        asyncio.run(_camera_light(val))


    def get_joints(self) -> TM5Joints:
        
        async def _get_joints():
            async with tp.connect_svr(robot_ip=self.ipTM5) as conn:
                j = await conn.get_value("Joint_Angle")
            return TM5Joints(j)
        
        j = asyncio.run(_get_joints())
        
        return j
        

    def get_pose_flange(self) -> Pose:

        async def _get_pose_flange():
            async with tp.connect_svr(robot_ip=self.ipTM5) as conn:
                p = await conn.get_value("Coord_Base_Flange")
                p = pose_change(Pose(p), now="ZYX", target="zyx")
            return p
        
        p = asyncio.run(_get_pose_flange())
        
        return p


    def get_pose_basic_tcp(self) -> Pose:

        async def _get_pose_basic_tcp():
            async with tp.connect_svr(robot_ip=self.ipTM5) as conn:
                p = await conn.get_value("Coord_Base_Tool")
                p = pose_change(Pose(p), now="ZYX", target="zyx")
            return p
        
        p = asyncio.run(_get_pose_basic_tcp())
        
        return p
    

    def get_pose_tcp(self) -> Pose:

        async def _get_pose_tcp():
            async with tp.connect_svr(robot_ip=self.ipTM5) as conn:
                p = await conn.get_value("Coord_Robot_Tool")
                p = pose_change(Pose(p), now="ZYX", target="zyx")
            return p
        
        p = asyncio.run(_get_pose_tcp())
        
        return p


    def ptp_joints(self, q):

        async def _ptp_joints(q):

            q = struct_change(q, TM5Joints)

            async with tp.connect_sct(robot_ip=self.ipTM5) as move:
                await move.move_to_joint_angles_ptp(
                    q.ret, self.speed, self.acc)
                await move.set_queue_tag(self.tagMove, True)

        asyncio.run(_ptp_joints(q))



    def ptp_pose(self, pose):      

        async def _ptp_pose(pose):

            pose = struct_change(pose, Pose)
            pose = pose_change(pose)

            async with tp.connect_sct(robot_ip=self.ipTM5) as move:
                await move.move_to_point_ptp(pose.ret, self.speed, self.acc)
                await move.set_queue_tag(self.tagMove, True)

        asyncio.run(_ptp_pose(pose))
            
        
    def line(self, pose):

        pose = struct_change(pose, Pose)
        pose = pose_change(pose)
    
        async def _line(pose):
            async with tp.connect_sct(robot_ip=self.ipTM5) as move:
                await move.move_to_point_line(pose.ret, self.speed, self.acc)
                await move.set_queue_tag(self.tagMove, True)

        asyncio.run(_line(pose))


    def circle(self, poseTwo, poseThree):

        poseTwo = struct_change(poseTwo, Pose)
        poseTwo = pose_change(poseTwo)
        
        poseThree = struct_change(poseThree, Pose)
        poseThree = pose_change(poseThree)
        
        async def _circle(poseTwo, poseThree):
            async with tp.connect_sct(robot_ip=self.ipTM5) as move:
                await move.move_to_point_line(poseTwo.ret, poseThree.ret,
                                            self.speed, self.acc)
                await move.set_queue_tag(self.tagMove, True)

        asyncio.run(_circle(poseTwo, poseThree))