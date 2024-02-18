<p align="center">
  <img src='https://github.com/rhinocobot/RHINOpy/blob/f3817623ef7f71699fdf984e35efbac1ada68dc3/pictures/rhino.png' width="130" />
</p>

# General
## What is `RHINOpy`?
`RHINOpy` is a control library for the RHINO cobot of Esslingen University.

The RHINO Cobot is a combined system of the Omron LD90 logistics robot and the Omron TM5-900 6DOF-cobot. Future tasks of this cobot could be pick-and-place or assembly tasks in a futuristic factory.

Before the `RHINOpy` library there was the need to write two separate sequence programs in two different programs. Additionally controlling one robot after another was not possible.

`RHINOpy`solves both of these issues. The library is written in Python as an easy-to-use driver to control the whole system and to reduce the needed effort to create sequences.

This library consists of structural definitions, communication standards, coordinate system manipulation, image recognition and movement commmands for the cobot.

### Requirements
**TMFlow:** `1.80+`  
**Python:** &nbsp;`3.8+`

### Creators
This project was created by **Sascha Magerle**, **Moritz Muellerschoen** and **Niklas Wackerow** under the supervision of **Prof. Dr.-Ing Tobias Kempf**.


## Control Structure
### Omron LD90
The Omron LD90 logistics robot is controlled by sending commands in the internal scripting language `ARCL`. The `RHINOpy`library uses some hidden features to expand the use of the Omron LD90.

For further informations see: [Omron ARCL guide](https://assets.omron.eu/downloads/manual/en/v11/i617_advanced_robotics_command_language_(arcl)_reference_manual_en.pdf)

### Omron TM5
The Omron TM5 cobot is controlled by a preexisting library `techmanpy`. When simultaneously using `techmanpy` and the `ARCL` command structure it would be possible to move both robots at the same time. Therefore the `techmanpy` library was integrated to the `RHINOpy` library because of safety issues of the asynchronous script structure of `techmanpy`.

The documentation can be found here: [techmanpy documentation](https://github.com/jvdtoorn/techmanpy)


## Preparations of the robots
### Subnets
All components of the RHINO system (Omron LD90, Omron TM5 and the control computer) have to be in the same subnet. This subnet is chosen as: 
```
192.168.2.0/24
```

To get the IP addresses of the wanted device in Python code there are built in variables
This table shows the IP addresses of all devices in the subnet:
| Device | IP Address | IP Address Variable (`string`) in `RHINOpy` |
| --- | --- | --- |
| Omron LD90 | `192.168.2.10` | `RHINOpy.ipLD90` |
| Omron TM5 | `192.168.2.11` | `RHINOpy.ipTM5` |
| Raspberry Pi 4 (Private) | `192.168.2.52` | `RHINOpy.ipPiLAN` |
| Raspberry Pi 4 (Public) | `134.152.34.25` | `RHINOpy.ipPiWAN` |
| URL of the MQTT server VAL | `dtaasp.de` | `RHINOpy.urlVAL` |
| Engineering Laptop of Lab | `192.168.2.51` | - |
| Other Engineering Laptop | `192.168.2.xxx` (must be same subnet) | - |

To control the RHINO cobot with an engineering laptop there has to be an Ethernet connection to the switch placed on top of the RHINO cobot.


### Omron TM5
To prepare the Omron TM5 for usage, follow the steps of the `techmanpy` library: [Omron TM5 Preparations](https://github.com/jvdtoorn/techmanpy/wiki/Robot-Preparation)

For receiving data (like joint angles, ...) the Ethernet Slave has to be on. It is important to add the IP address of the control computer to the internal table with full read and send access to the Omron TM5. Otherwise it is not possible to receive data.

To send data (like movement commands, ...) the robot has to be in the 'Listen' mode. A program was created for this ("Listen" in programs list). Here is a link to the guide for creating and executing programs on the Omron TM5: [Programs on Omron TM5](https://assets.omron.eu/downloads/manual/en/v9/i626_tm_flow_software_installation_manual_en.pdf)

In the `techmanpy` library there is a good script for testing the preparations: [Test Script](https://github.com/jvdtoorn/techmanpy/blob/384ef92dc0601f93259e4a6e5a7e8b1c96876902/test_connection.py)

If all three services are 'connected', you are ready to go!


## Installation
Following


## Intended Execution of `RHINOpy` programs
Generally, it is possible to send commands with all devices which are connected to the subnet.

But for optimal use it is recommended to debug the execution of the program on an engineering computer and for production programs to run the Python script on the Raspberry Pi 4.

Tested scripts can be uploaded to the Raspberry Pi by WinSCP and then executed by the command line or by the preinstalled Thonny IDE.

Here is a tutorial on how to upload files by WinSCP. The IP address can be found above and the password to the Raspberry Pi 4 can be found in the project report.

[WinSCP uploading files](https://www.youtube.com/watch?v=xW0BQIaz7Ic)

<br>

# Code Documentation


## Structural definitions
For a better scripting experience here are some useful structural definitions. All are used to establish standard definitions of kinematic variables.

It is possible to print the structural definition with a simple `print` command.

To save all stored values into a Python `list` 'vals', the following command can be used:
```Python
vals = RHINOpy.someStruct.ret
```

<br>

### List of all structural definition

#### RHINOpy.LD90Joints
```Python
RHINOpy.LD90Joints(x, y, phi)
```

Structural definition of all joint variables of the Omron LD90.

**Parameters:**

  * x (`float`): x-coordinate [mm] of the LD90 in the world coordinate system. 

  * y (`float`): y-coordinate [mm] of the LD90 in the world coordinate system. 

  * phi (`float`): turning angle in the mathematical positive z-axis (upwards) [°] of the LD90 in the world coordinate system.

  **Returns:** RHINOpy.LD90Joints (`RHINOpy`)

  **Raises:** RHINOpy.LD90JointsErr

<br>

#### RHINOpy.TM5Joints
```Python
RHINOpy.TM5Joints(j1, j2, j3, j4, j5, j6)
```

Structural definition of all joint variables of the Omron TM5.

Joint description see: [TM5-900 Joints](https://assets.omron.eu/downloads/datasheet/en/v5/i837_collaborative_robots_datasheet_en.pdf)

**Parameters:**
  * j1 ... j6 (`float`): Six joint angles for joint 1 to Joint 6 [°].

&ensp;&ensp;or

  * joints (`list` or `np.ndarray`): List of length 6 of all joint angles [°].

**Returns:** RHINOpy.TM5Joints

**Raises:** RHINOpy.TM5JointsErr

<br>

#### RHINOpy.RHINOJoints
```Python
RHINOpy.RHINOJoints(ld90J, tm5J)
```

Structural definition of all joint variables of the RHINO cobot.

**Parameters:**
  * ld90J (`RHINOpy.LD90Joints` or `list` or `np.ndarray`): Omron LD90 joints definition (If `list` or `np.ndarray`, see above).

  * tm5J (`RHINOpy.LD90Joints` or `list` or `np.ndarray`): Omron TM5 joints definition (If `list` or `np.ndarray`, see above).

&ensp;&ensp;or

  * joints (`list`): List of both (`RHINOpy`) joint definitions.

&ensp;&ensp;or

  * joints (`list`): List of both joint definitions [[x, y, phi], [j1, ..., j6]].

**Returns:** RHINOpy.RHINOJoints

**Raises:** RHINOpy.RHINOJointsErr

<br>

#### RHINOpy.Pose
```Python
RHINOpy.Pose(x, y, z, alpha, beta, gamma)
```

Structural definition of a pose (position & orientation). The rotation is expressed in (intrinsic) zy'x''-euler angles.

**Parameters:**
  * x (`float`): x-coordinate [mm].

  * y (`float`): y-coordinate [mm].

  * y (`float`): z-coordinate [mm].

  * alpha (`float`): alpha oriention angle [°].

  * beta (`float`): beta oriention angle [°].

  * gamma (`float`): gamma oriention angle [°].


&ensp;&ensp;or

  * pose (`list` or `np.ndarray`): List of the position [all in mm] and orientation [all in °].

**Returns:** RHINOpy.Pose

**Raises:** RHINOpy.PoseErr

<br>

#### RHINOpy.RHINOPose
```Python
RHINOpy.RHINOPose(poseLD90, poseTM5)
```

Structural definition of the deterministic pose of the RHINO cobot.

**Parameters:**
  * poseLD90 (`RHINOpy.LD90Joints` or `list` or `np.ndarray`): Pose (joint) definition of the Omron LD90 (If `list` or `np.ndarray`, see above).

  * poseTM5 (`RHINOpy.LD90Joints` or `list` or `np.ndarray`): Pose (joint) definition of the Omron LD90 (If `list` or `np.ndarray`, see above).

&ensp;&ensp;or

  * pose (`list` or `np.ndarray`): List of the position [all in mm] and orientation [all in °].

&ensp;&ensp;or

  * pose (`list` or `np.ndarray`): List of the pose [[xLD90, y, phi], [xTM5, yTM5, zTM5, alpha, beta, gamma]].

**Returns:** RHINOpy.Pose

**Raises:** RHINOpy.RHINOPoseErr

<br><br>
## Omron LD90
This paragraph explains all functions to control the Omron LD90 logistics robot.

When you want to use the following functions, always connect to the Omron LD90 by using this code:

```Python
import RHINOpy

ld90 = RHINOpy.LD90(ipLD90=RHINOpy.ipLD90, portLD90=RHINOpy.portLD90)
```

**Parameters:**
  * ipLD90 (`string` | *optional*): Default `RHINOpy.ipLD90`, IP address of the Omron LD90.
  * portLD90 (`string` | *optional*): Default `RHINOpy.portLD90`, Port of the Omron LD90.
**Returns:** RHINOpy.LD90

You can then use functions by calling:
```Python
ld90.function()
```

<br>

### List of all function of the Omron LD90 in the `RHINOpy` library

#### RHINOpy.LD90.get_joints
```Python
RHINOpy.LD90.get_joints()
```

Requests the current joint angles of the Omron LD90.

**Parameters:** None

**Returns:** RHINOpy.LD90Joints

**Raises:** ConnectionError

<br>

#### RHINOpy.LD90.kinematics
```Python
RHINOpy.LD90.kinematics(q)
```

Computes the direct kinematic of the Omron LD90.

**Parameters:**
  * q (`RHINOpy.LD90Joints` or `list` or `np.ndarray`): Joint angles of the Omron LD90.

**Returns:** RHINOpy.Pose

**Raises:** ConnectionError

There is no inverse kinematics implemented, because of the simplicity of this transformation.

<br>

#### RHINOpy.LD90.state_of_charge
```Python
RHINOpy.LD90.state_of_charge()
```

Requests the state of charge of the Omron LD90.

**Parameters:** None

**Returns:** float (in percent)

**Raises:** ConnectionError

<br>

#### RHINOpy.LD90.say
```Python
RHINOpy.LD90.say(text)
```

Lets the Omron LD90 say the word of `text`.

**Parameters:**
  * text (`string`): Text what should be said.

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.LD90.play_sound
```Python
RHINOpy.LD90.play_sound(name)
```

Lets the Omron LD90 play the sound of the .wav file. Sound must be stored on the storage of the LD90.

How to store audio files on the Omron LD90: [Video Tutorial](https://www.youtube.com/watch?v=r5jYmbiXHeY)

**Parameters:**
  * name (`string`): Name of the .wav file of the sound. File type must not be included.

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.LD90.dock
```Python
RHINOpy.LD90.dock()
```

Sends the Omron LD90 to the charging station.

**Parameters:** None

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.LD90.undock
```Python
RHINOpy.LD90.undock()
```

Undocks the Omron LD90 from the charging station.

**Parameters:** None

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.LD90.goto
```Python
RHINOpy.LD90.goto(q)
```

Sends a movement command to drive the Omron LD90 to a specific pose/joint combination. In case of the Omron LD90 the pose and joint combination are the same.

**Parameters:**
  * q (`RHINOpy.LD90Joints` or `list` or `np.ndarray`): Wished target pose.

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.LD90.move
```Python
RHINOpy.LD90.move(q)
```

The same functionality as `RHINOpy.LD90.goto`.

<br>

#### RHINOpy.LD90.patrol
```Python
RHINOpy.LD90.patrol(routeName)
```

Sends a route request to the Omron LD90. The route must exist in Omron Motion Planner. It is possible to create more advanced movement commands with the route functionality.

How to create routes in Omron Motion Planner: [Video Tutorial](https://www.youtube.com/watch?v=EJZX7EsRhtQ)

**Parameters:**
  * routeName (`string`): Route name.

**Returns:** None

**Raises:** ConnectionError

<br><br>
## Omron TM5
This paragraph explains all functions to control the Omron TM5-900 6-DOF-cobot.

When you want to use the following functions, always connect to the Omron TM5-900 by using this code:

```Python
import RHINOpy

tm5 = RHINOpy.TM5(ipTM5=RHINOpy.ipTM5, speed=speed, acc=acc)
```

**Parameters:**
  * ipTM5 (`string` | *optional*): Default `RHINOpy.ipTM5`, IP address of the Omron TM5.
  * speed (`float` | *optional*): Default 0.1, Speed of the Omron TM5 in decimals, e.g. 1.0 is 100%.
  * acc (`float` | *optional*): Default 200.0, Duration [ms] until the cobot reaches the maximum accelaration.

**Returns:** RHINOpy.TM5

You can then use functions by calling:
```Python
tm5.function()
```

After the connection, the `speed` or the `acc` parameter can be changed by this pseudocode:
```Python
tm5.attribute = value
```

<br>

### List of all functions of the Omron TM5 in `RHINOpy`

#### RHINOpy.TM5.DH
```Python
RHINOpy.TM5.DH(theta, d, a, alpha)
```
Returns the general Denavit-Hartenberg matrix. For more information see: [Denavit Hartenberg matrix](https://de.wikipedia.org/wiki/Denavit-Hartenberg-Transformation)

**Parameters:**
  * theta (`float`): Theta angle [rad] of the Denavit Hartenberg transformation.
  * d (`float`): d distance [mm] of the Denavit Hartenberg transformation.
  * a (`float`): a distance [mm] of the Denavit Hartenberg transformation.
  * alpha (`float`): Alpha angle [rad] of the Denavit Hartenberg transformation.

**Returns:** (4, 4) np.ndarray

**Raises:** ValueError

<br>

#### RHINOpy.TM5.kinematics
```Python
RHINOpy.TM5.kinematics(q, rot=rot)
```
Computes the direct kinematics for the Omron TM5.

**Parameters:**
  * q (`RHINOpy.TM5Joints` or `list` or `np.ndarray`): (6, 1) elements of the joint angles [°] of the Omron TM5.
  * rot (`string` | *optional*): Default `"euler"`, will output the orientation (here last 3 elements) as (intrinsic) zy'x'' euler angles; other option `quat`, will output the orientation (here last 4 elements) as quaternions.

**Returns:** RHINOpy.Pose or (7, 1) list

**Raises:** ValueError

<br>

#### RHINOpy.TM5.inv_kinematics
```Python
RHINOpy.TM5.inv_kinematics(p, q0)
```
Computes the inverse kinematics of the Omron TM5.

**Parameters:**
  * p (`RHINOpy.Pose` or `list` or `np.ndarray`): (6, 1) elements of the description of the wished pose of the Omron TM5. The orientation (last 3 elements) must be in (intrinsic) zy'x'' euler angles.
  * q0 (`RHINOpy.TM5Joints` or `list` or `np.ndarray` | *optional*): Default `None`, The last joint angles [°] of the Omron TM5. When not given, it could result in a non realistic pose in the context of the starting pose of the Omron TM5 (Ambiguity of the inverse kinematic).

**Returns:** RHINOpy.TM5Joints

**Raises:** ValueError

<br>

#### RHINOpy.TM5.camera_light
```Python
RHINOpy.TM5.camera_light(val)
```
Turns the camera light of the Omron TM5 on or off.

**Parameters:**
  * val (`bool`): Wished state of the camera light, `True`: On, `False`: Off.

**Returns:** None

**Raises:** ValueError or ConnectionError

<br>

#### RHINOpy.TM5.get_joints
```Python
RHINOpy.TM5.get_joints()
```
Requests the current joint angles [°] of the Omron TM5.

**Parameters:** None 

**Returns:** RHINOpy.TM5Joints

**Raises:** ConnectionError

<br>

#### RHINOpy.TM5.get_pose_flange
```Python
RHINOpy.TM5.get_pose_flange()
```
Requests the current pose of the flange of the Omron TM5. The orientation (last 3 elements) is given in (intrinsic) zy'x'' euler angles. The reference coordinate system is the coordinate system in the base of the Omron TM5.

**Parameters:** None

**Returns:** RHINOpy.Pose

**Raises:** ConnectionError

<br>

#### RHINOpy.TM5.get_pose_basic_tcp
```Python
RHINOpy.TM5.get_pose_basic_tcp()
```
Requests the current pose of the basic gripper tool (TCP) of the Omron TM5. The orientation (last 3 elements) is given in (intrinsic) zy'x'' euler angles. The reference coordinate system is the coordinate system in the base of the Omron TM5.

**Parameters:** None

**Returns:** RHINOpy.Pose

**Raises:** ConnectionError

<br>

#### RHINOpy.TM5.get_pose_tcp
```Python
RHINOpy.TM5.get_pose_tcp()
```
Requests the current pose of the installed tool in TMFlow (TCP) of the Omron TM5. The orientation (last 3 elements) is given in (intrinsic) zy'x'' euler angles. The reference coordinate system is the coordinate system in the base of the Omron TM5.

**Parameters:** None

**Returns:** RHINOpy.Pose

**Raises:** ConnectionError

<br>

#### RHINOpy.TM5.ptp_joints
```Python
RHINOpy.TM5.ptp_joints(q)
```
Lets the Omron TM5 do a PTP motion from the current to the wished joint angles.

**Parameters:**
  * q (`RHINOpy.TM5Joints` or `list` or `np.ndarray`): Wished joint angles [°] combination of the PTP motion.

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.TM5.ptp_pose
```Python
RHINOpy.TM5.ptp_pose(p)
```
Lets the Omron TM5 do a PTP motion from the current to the wished pose.

**Parameters:**
  * p (`RHINOpy.Pose` or `list` or `np.ndarray`): Wished pose (first three [mm]; last three [°]) of the PTP motion. The orientation (last 3 elements) must be in (intrinsic) zy'x'' euler angles.

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.TM5.line
```Python
RHINOpy.TM5.line(p)
```
Lets the Omron TM5 do a line motion from the current to the wished pose.

**Parameters:**
  * p (`RHINOpy.Pose` or `list` or `np.ndarray`): Wished pose (first three [mm]; last three [°]) of the PTP motion. The orientation (last 3 elements) must be in (intrinsic) zy'x'' euler angles.

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.TM5.circle
```Python
RHINOpy.TM5.circle(poseTwo, poseThree)
```
Lets the Omron TM5 do a circle motion starting at the current pose.

**Parameters:**
  * poseTwo (`RHINOpy.Pose` or `list` or `np.ndarray`): The second pose to interpolate the circle. The orientation (last 3 elements) must be in (intrinsic) zy'x'' euler angles.
  * poseThree (`RHINOpy.Pose` or `list` or `np.ndarray`): The third pose to interpolate the circle. The orientation (last 3 elements) must be in (intrinsic) zy'x'' euler angles.

**Returns:** None

**Raises:** ConnectionError


<br><br>
## RHINO cobot
There are also features included to request data from the whole RHINO cobot (Omron LD90, Omron TM5):

To interact with the RHINO cobot, a connection to the RHINO is needed.
```Python
rhino = RHINOpy.RHINO(speed=speed, ipLD90=ipLD90, portLD90=portLD90, ipTM5=ipTM5)
```
**Parameters:**
  * speed (`string` | *optional*): Default 0.1, Speed of the Omron TM5 in decimals, e.g. 1.0 is 100%.
  * ipLD90 (`string` | *optional*): Default `RHINOpy.ipLD90`, IP address of the Omron LD90.
  * portLD90 (`string` | *optional*): Default `RHINOpy.portLD90`, Port of the Omron LD90.
  * ipTM5 (`string` | *optional*): Default `RHINOpy.ipTM5`, IP address of the Omron TM5.

**Returns:** RHINOpy.RHINO

**Raises:** ConnectionError

<br>

### List of RHINO functions

#### RHINOpy.RHINO.get_joints
```Python
RHINOpy.RHINO.get_joints()
```
Request the joint angles of the RHINO cobot.

**Parameters:** None

**Returns:** RHINOpy.RHINOJoints

**Raises:** ConnectionError

<br>

#### RHINOpy.RHINO.get_pose
```Python
RHINOpy.RHINO.get_pose()
```
Request the pose of the RHINO cobot.

**Parameters:** None

**Returns:** RHINOpy.RHINOPose

**Raises:** ConnectionError


<br><br>
## Coordinate Systems
Often times it is necessary to transform poses between different coordinate systems. To make this process easier `RHINOpy` delivers predefined coordinate systems (see picture below) and functions to transform points and poses.

<p align="left">
  <img src='https://github.com/rhinocobot/RHINOpy/blob/774714b5b61ed5dde0bdd1249eebcc1e017c7216/pictures/cs.png' width="600"/>
</p>

This table shows the number of the coordinate system and its specific name in `RHINOpy`:
| # | Name | Description |
| --- | --- | --- |
| 1 | `RHINOpy.CS_WORLD` | World coordinate system located at the charging station of the Omron LD90 |
| 2 | `RHINOpy.CS_LD90` | Coordinate system on the floor. Described by `RHINOpy.LD90.get_joints` |
| 3 | `RHINOpy.CS_TM5_BASE` | Coordinate system directly on top of `RHINOpy.CS_LD90` where the Omron TM5 is mounted |
| 4 | `RHINOpy.CS_TM5_FLANGE` | Coordinate system where the robot tool is mounted |
| 5 | `RHINOpy.CS_TM5_TCP` | Coordinate system of the gripper in the TCP |
| 6 | `RHINOpy.CS_TM5_CAMERA` | Coordinate system of the camera. Output coordinate system of the Image Recognition |

<br>

### List of all coordinate systems related functions

#### RHINOpy.transform
```Python
RHINOpy.transform(pose, current, target)
```
Transforms a pose to a different coordinate system.

**Parameters:**
  * pose (`RHINOpy.Pose` or `list` or `np.ndarray`): The pose which should be transformed to a different coordinate system.
  * current (`RHINOpy.CS_xxx`): The current coordinate system. The coordinate system must be defined in the table above.
  * target (`RHINOpy.CS_xxx`): The target coordinate system of the transformation. The coordinate system must be defined in the table above.
    
**Returns:** RHINOpy.Pose

**Raises:** ValueError

<br>

#### RHINOpy.pose2matrix
```Python
RHINOpy.pose2matrix(pose)
```
Transforms a pose into a (4, 4) transformation matrix.

**Parameters:**
  * pose (`RHINOpy.Pose`): Pose which should be transformed to a transformation matrix. The orientation must be in (intrinsic) zy'x'' euler angles.

**Returns:** (4, 4) np.ndarray

**Raises:** ValueError or RHINOpy.PoseErr

<br>

#### RHINOpy.matrix2pose
```Python
RHINOpy.matrix2pose(matrix)
```
Transforms a (4, 4) transformation matrix into a pose. The orientation is described in (intrinsic) zy'x'' euler angles.

**Parameters:**
  * matrix ((4, 4) `np.ndarray`): The transformation matrix (translation and rotation) to be transformed into a pose. 

**Returns:** RHINOpy.Pose

**Raises:** ValueError or RHINOpy.PoseErr


<br><br>
## Joint Saving
Especially, when using multiple joint angles in sequence scripts, it is not easy to remember all the numbers. Usually, there are teach in functions to save specific combinations into variables. With `RHINOpy`there is the possibility to save joint combinations and later to use them in scripts. There is no possibility to save poses, because a pose would be ambigous with the 9-DOF RHINO.

The first step is to call following Python function:
```Python
import RHINOpy

rhino = RHINOpy.RHINO()

rhino.save_joints()
```

Next there are multiple console output, which describe the necessary inputs to make:
```console
$ Input the name of the joint combination:
$ What should be saved? 1 for RHINO, 2 for LD90, 3 for TM5:
$ Give a description of the joint combination:
```

After the inputs the function tells to move the chosen part of the RHINO cobot to the joint combination:
```console
$ Move the RHINO cobot to the wished Pose.
```

To save the joint combination, press `y` when the RHINO cobot is in the right joint combination.

If everything is finished, there will be this output:
```console
$ Saved {name}.
```

Otherwise the terminal output will tell the exact error.

<br>

Often times it is necessary to move to close areas. For this purpose the next function was created:

#### RHINOpy.RHINO.save_multiple_joints
```Python
RHINOpy.RHINO.RHINO.save_multiple_joints()
```

It has the same behaviour like `RHINOpy.save_joints`, but after pressing `y` for saving, it will ask for the next joint combination to be saved. With this functionality it is possible to create small PTP motions to define the cobots path with a defined precision.

<br><br>

To interact with the defined motions there are multiple functions:

#### RHINOpy.RHINO.list_joints
```Python
RHINOpy.list_joints()
```
Lists all of the saved joint combination and prints information of all joint combinations.

**Parameters:** None

**Returns:** print output

**Raises:** None

<br> 

#### RHINOpy.RHINO.delete_joints
```Python
RHINOpy.RHINO.delete_joints(name)
```
Deletes the saved joint combination.

**Parameters:**
  * name (`string`): Name of the joint combination which should be deleted. 

**Returns:** None

**Raises:** ValueError

<br>

There are three functions to move the RHINO cobot to the saved joint combination(s). The reason for three function is to always make sure that the user knows the exact purpose of the joint combination(s). To move to the joint combination, a connection to the RHINO is needed.
#### RHINOpy.RHINO.move
```Python
RHINOpy.RHINO.move(name)
```
Moves the RHINO cobot to the joint combination(s). First, the Omron LD90 moves to its first joint angles. Secondly, the Omron TM5 moves to its first joint angles (PTP). If there are multiple joint combinations, the moving is repeated until it is the last joint combination.

#### RHINOpy.RHINO.LD90_move
```Python
RHINOpy.RHINO.LD90_move(name)
```
Moves the Omron LD90 to the joint combination(s). If there are multiple joint combinations, the movement is repeated until it is the last joint combination.


#### RHINOpy.RHINO.TM5_move
```Python
RHINOpy.RHINO.TM5_move(name)
```
Moves the Omron TM5 to the joint combination(s). If there are multiple joint combinations, the movement is repeated until it is the last joint combination.

**Parameters:**
  * name (`string`): Name of the joint combination(s) of the motion.

**Returns:** None

**Raises:** ConnectionError

<br>


<br><br>
## Communication
`RHINOpy` has specific communication protocols integrated. The `ARCL` communication protocol is integrated into `RHINOpy`, but will not be explained here, because it is only used by the backend of `RHINOpy`. The next paragraph will explain all functionality to use MQTT for e.g. the communication with a digital twin.

### Sending Data
To send data to a MQTT broker there are multiple ways to do so:

#### RHINOpy.MQTTPublisher
```Python
pub = RHINOpy.MQTTPublisher(broker)
pub.publish(topic, msg)
```
Sends single data `string` to a MQTT broker. The first line does not need to be called every time data should be sent.

**Parameters:**
  * broker (`string`): IP address/URL of the MQTT broker, e.g. `"192.168.2.52"`.
  * topic (`string`): Topic on which the data should be send.
  * msg (`string`): Message which should be send.

**Returns:** None

**Raises:** ConnectionError

<br>

#### RHINOpy.MQTTWrapperPublish
```Python
pub = RHINOpy.MQTTWrapperPublish(broker, generalStruct)
pub.publish(struct)
```
Sends data from a `RHINOpy` struct (e.g. `RHINOpy.LD90Joints`) to a MQTT broker. The first line does not need to be called every time data should be sent.

**Parameters:**
  * broker (`string`): IP address/URL of the MQTT broker, e.g. `"192.168.2.52"`.
  * generalStruct(`RHINOpy.struct`): General struct (can be empty) of what should be sent by this `pub`.
  * struct(`RHINOpy.struct`): Filled struct with the data that should be sent.

**Example:**
```Python
# Publish the LD90 joint angles to a digital twin

ld90 = RHINOpy.LD90()
pub = RHINOpy.MQTTWrapperPublish(RHINOpy.ipPiLAN, RHINOpy.LD90Joints)

while(True):
  joints = ld90.get_joints()
  
  pub.publish(joints)

  time.sleep(1/FPS)
```
    
**Returns:** None

**Raises:** ConnectionError

<br>

### Receiving Data
There are multiple ways to recceive data from a MQTT broker. The first line does not need to be called every time data should be sent.

#### RHINOpy.MQTTReceiver
```Python
rec = RHINOpy.MQTTReceiver(broker, topic)
rec.receive(timeout=timeout)
```
Receive data from a MQTT broker from a single topic. The first line does not need to be called every time data should be received.

**Parameters:**
  * broker (`string`): IP address/URL of the MQTT broker, e.g. `"192.168.2.52"`.
  * topic (`string`): Topic from which topic.
  * timeout (`float` | *optional*): Default None; Time [s] on how long to wait before the service disconnects from the broker if there is no new message.

**Returns:** string

**Raises:** TimeoutError or ConnectionError

<br>

#### RHINOpy.MQTTWrapperRP
```Python
rec = RHINOpy.MQTTWrapperRP(broker, generalStruct)
rec.start()
```
Receives data from a `RHINOpy` struct (e.g. `RHINOpy.LD90Joints`) from a MQTT broker. The default timeout time is 3 s. The first line does not need to be called every time data should be received.

**Parameters:**
  * broker (`string`): IP address/URL of the MQTT broker, e.g. `"192.168.2.52"`.
  * generalStruct(`RHINOpy.struct`): General struct (can be empty) of what should be received by this `rec`.

**Returns:** RHINOpy.struct

**Raises:** TimeoutError (after 3 s) or ConnectionError

<br>

### Passthrough

<br>

#### RHINOpy.MQTTPasstrough
```Python
RHINOpy.MQTTPasstrough(brokerFrom, brokerTo, topic)
```
Can receive data and send it to another broker.

**Parameters:**
  * brokerFrom (`string`): The target broker IP address or URL, e.g. `"192.168.2.52"`.
  * brokerTo (`string`): The target broker IP address or URL, e.g. `"192.168.2.52"`.
  * topic (`string`): Topic on which the data should be received and sent.

**Returns:** None

**Raises:** ConnectionError

<br>

### Digital Twin
To transfer live joint data to the digital twin of the VAL there could be a Python script on the Raspberry Pi. This script would request the joint data from the RHINO cobot and after that publish this data to the MQTT broker of the digital twin. The code would be:

```Python
# digital_twin_publish.py

import time
import RHINOpy as rp

FPS = 60

def connect():

  rhino = None

  while rhino == None:

    try:
      rhino = rp.RHINO()
      return rhino
    except:
      time.sleep(10) 


rhino = connect()
pub = MQTTWrapperPublish(rp.urlVAL, rp.RHINOJoints)

while True:

  joints = rhino.get_joints()
  pub.publish(joints)

  time.sleep(1/FPS)
```


<br><br>
## Image Recognition
When creating motion scripts with `RHINOpy` there is often times the scenario that the Omron LD90 moves to a defined destination and after that the Omron TM5 has to grab something. The problem thereby is that the Omron LD90 is not precise when moving. Often times it is possible that there are moving parts, which do not end up in the same place. Usually there is the need for the detection of objects. In `RHINOpy` there are some simple image recognition functionalities implemented.

Before using the following function there has to be an image recoginition object, like:
```Python
import RHINOpy

detect = RHINOpy.Detect(cameraNumber=cameraNumber)
```

**Parameters:**
  * cameraNumber (`int` | *optional*): Default 0; Specifies which camera of the computer should be used for image recoginition. First camera: 0, second camera: 1, ...

<br>

#### RHINOpy.Detect.rectangle
```Python
RHINOpy.Detect.rectangle()
```
Detects rectangular shapes in the camera view. Returns a `list` of all detected shapes and sizes. Per detected shape there will be the output of one sublist with the center point of the shape as a `RHINOpy.Pose` object (translation in [mm] and orientation in [°]) and another sublist with the width [mm] and the height [mm] of the object. The pose is given in the coordinate system of the camera (See `RHINOpy.transform`).

**Parameters:** None

**Returns:** [[RHINOpy.Pose, [width, height]], ..., [RHINOpy.Pose, [width, height]]]

**Raises:** None

<br>

#### RHINOpy.Detect.circle
```Python
RHINOpy.Detect.circle()
```
Detects circular shapes in the camera view. Returns a `list` of all detected shapes and sizes. Per detected shape there will be the output of a sublist with the center point of the shape as a `RHINOpy.Pose` object (translation in [mm]) and a variable containing the radius [mm] of the object. The pose is given in the coordinate system of the camera (See `RHINOpy.transform`).

**Parameters:** None

**Returns:** [[RHINOpy.Pose, radius], ..., [RHINOpy.Pose, radius]]

**Raises:** None

<br>

#### RHINOpy.Detect.human
```Python
RHINOpy.Detect.human()
```
Detects the pose of a human in the camera view. Returns a `RHINOpy.Pose` in the world coordinate system.

**Parameters:** None

**Returns:** RHINOpy.Pose

**Raises:** None
