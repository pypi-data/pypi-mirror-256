import os
import glob
import json

from .helpers import *
from .structs import *
# from .RHINO import RHINO
from .LD90 import LD90
from .TM5 import TM5


class Joints:

    def __init__(self) -> None:

        self.pathJoints = get_datapath() + "/joints"

        if not os.path.isdir(self.pathJoints):
            os.makedirs(self.pathJoints)


    def __save(self, name, typ, desc, joints):

        if typ == "1":
            if isinstance(joints, list):
                rhino = []
                for j in joints:
                    ld90 = j.LD90Joints.ret
                    tm5 = j.TM5Joints.ret
                    rhino.append([ld90, tm5])

            else:
                ld90 = joints.LD90Joints.ret
                tm5 = joints.TM5Joints.ret
                rhino = [ld90, tm5]

        if typ == "2":
            if isinstance(joints, list):
                rhino = []
                for j in joints:
                    ld90 = j.ret
                    rhino.append(ld90)

            else:
                ld90 = joints.ret

        if typ == "3":
            if isinstance(joints, list):
                rhino = []
                for j in joints:
                    tm5 = j.ret
                    rhino.append(tm5)

            else:
                tm5 = joints.ret
                rhino = [tm5]

        d = {"name": name,
             "type": typ,
             "description": desc,
             "joints": rhino}

        json.dump(d, open(f"{self.pathJoints}/{name}.txt",'w'))

        print()
        print(f"Saved {name}.")
        print("\n\n")


    def save_joints(self):
        
        print()
        name = input("Input the name of the joint combination: ")
        print()
        typ = input("What should be saved? 1 for RHINO, 2 for LD90, 3 for TM5: ")
        if typ not in ["1", "2", "3"]:
            raise ValueError("typ must be 1, 2 or 3")
        print()
        desc = input("Give a description of the joint combination: ")
        print("\n")
        print("Move the RHINO cobot to the wished Pose.")
        print()

        inp = input("Ready to add joint combination? y/n  ")

        if inp != "y" or inp != "Y":
            if typ == "1":
                l = LD90().get_joints()
                t = TM5().get_joints()
                j = RHINOJoints(l, t)
            elif typ == "2":
                j = LD90().get_joints()
            elif typ == "3":
                j = TM5().get_joints()            

            self.__save(name, typ, desc, j)

        else:
            print("Saved no joint combination.")
            print("Aborted the save function.\n")


    def save_multiple_joints(self):
        
        print()
        name = input("Input the name of the multiple joint combination: ")
        print()
        typ = input("What should be saved? 1 for RHINO, 2 for LD90, 3 for TM5: ")
        if typ not in ["1", "2", "3"]:
            raise ValueError("typ must be 1, 2 or 3")
        print()
        desc = input("Give a description of the joint combination: ")
        print("\n")
        print("Move the RHINO cobot to the wished Pose.")
        print()

        js = []
        inp = "y"
        while inp == "y" or inp == "Y":
            inp = input("Ready to add joint combination? y/n  ")

            if typ == "1":
                l = LD90().get_joints()
                t = TM5().get_joints()
                j = RHINOJoints(l, t)
            elif typ == "2":
                js.append(LD90().get_joints())
            elif typ == "3":
                js.append(TM5().get_joints())  
        

        if len(js) == 1:
            print("When saving only one joint combination, use save_joint.")
            print("Saved no joint combinations.")
            print("Aborted the save function.\n")

        elif len(js) > 0:
            self.__save(name, typ, desc, js)

        else:
            print("No joint combinations given.")
            print("Saved no joint combinations.")
            print("Aborted the save function.\n")

    
    def __files(self, name=None):

        paths = glob.glob(self.pathJoints + "\\*")
        files = [os.path.basename(f) for f in paths]
        fileNames = [os.path.splitext(f)[0] for f in files]

        try:
            index = fileNames.index(name)
        except:
            raise ValueError(
                f"{name} is not saved in the joint combinations.")
        
        return paths[index]


    def __import(self, path):

        js = json.load(open(path))

        if not isinstance(js["joints"][0][0], list):
        
            if js["type"] == "1":
                ld90 = LD90Joints(js["joints"][0])
                tm5 = TM5Joints(js["joints"][1])
                js["joints"] = RHINOJoints(ld90, tm5)
            
            if js["type"] == "2":
                js["joints"] = LD90Joints(js["joints"][0])

            if js["type"] == "3":
                js["joints"] = TM5Joints(js["joints"][0])
        
        else:
            a = []
            for j in js["joints"]:
                
                if js["type"] == "1":
                    ld90 = LD90Joints(j[0])
                    tm5 = TM5Joints(j[1])
                    a.append(RHINOJoints(ld90, tm5))

                if js["type"] == "2":
                    ld90 = LD90Joints(j[0])
                    a.append(ld90)

                if js["type"] == "1":
                    tm5 = TM5Joints(j[0])
                    a.append(tm5)

            js["joints"] = a
        
        return js
        
    
    def import_joints_all(self):

        paths = glob.glob(self.pathJoints + "/*")

        js = []
        for p in paths:
            j = self.__import(p)
            js.append(j)

        return js
    

    def import_joints(self, name):

        path = self.__files(name)

        j = self.__import(path)

        return j


    def list_joints(self):
        
        js = self.import_joints_all()
        
        print()
        for j in js:
            print(f"Name:", j["name"])
            print(f"Type:", j["type"])
            print(f"Description:", j["description"])
            print("\n")


    def delete_joints(self, name):

        path = self.__files(name)

        os.remove(path)

        print(f"\nRemoved {name}.\n\n")