


class MyError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return self.message


class LD90JointsErr(MyError):

    def __init__(self):
        self.message = """

        The input to LD90Joints must be:
        
            A list of length 3 
            or 
            3 single inputs
            --> x, y, theta.
            """
                
        super().__init__()
    

class PoseErr(MyError):
    def __init__(self):
        self.message = """

        The input to TM5Pose must be:
        
            A list of length 6 
            or 
            6 single inputs
            x, y, z, alpha, beta, gamma.
            """
                
        super().__init__()


class TM5JointsErr(MyError):
    def __init__(self):
        self.message = """

        The input to TMJoints must be:
        
            list: [q1, q6]
            or 
            q1, ..., q6.
            """
        
        super().__init__()


class RHINOJointsErr(MyError):
    def __init__(self):
        self.message = """

        The input to RHINOJoints must be:
        
            list: [LD90Joints, TM5Joints]
            or 
            LD90Joints, TM5Joints.
            """
                
        super().__init__()


class RHINOPoseErr(MyError):
    def __init__(self):
        self.message = """

        The input to RHINOPose must be:
        
            list: [LD90Joints, Pose]
            or 
            LD90Joints, TM5Pose.
            """
                
        super().__init__()


class MessageTimeout(MyError):
    def __init__(self):
        self.message = "Value was not registered."
        
        super().__init__()