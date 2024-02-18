import cv2 as cv
import numpy as np
import os
import time
import math
import RHINOpy as rp

from .structs import Pose
from .helpers import get_datapath
from .cs import *
from scipy.spatial.transform import Rotation as R


class Detect:

    def __init__(self, cameraNumber=0):

        print(cameraNumber)
        self.cap = cv.VideoCapture(cameraNumber)
        self.cap.set(cv.CAP_PROP_FPS, 10)
        if not self.cap.isOpened():
            self.cap = cv.VideoCapture(cameraNumber)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        
        self.net = None


    def get_image(self):

        hasFrame, frame = self.cap.read()

        self.width = frame.shape[1]
        self.height = frame.shape[0]

        return hasFrame, frame


    def __detect_checker_board(self, image, grayImage, criteria, boardDimension):
        ret, corners = cv.findChessboardCorners(grayImage, boardDimension)
        if ret == True:
            corners1 = cv.cornerSubPix(grayImage, corners, (3, 3), (-1, -1), criteria)
            image = cv.drawChessboardCorners(image, boardDimension, corners1, ret)

        return image, ret
    

    def capture_calibration_images(self):

        CHESS_BOARD_DIM = (9, 6)

        n = 0  # image_counter

        # checking if images dir exists, if not then create images directory
        path = get_datapath()
        imageDirPath = path + "\\images"
        print(imageDirPath)

        CHECK_DIR = os.path.isdir(imageDirPath)
        # if directory does not exist create
        if not CHECK_DIR:
            os.makedirs(imageDirPath)
            print(f'"{imageDirPath}" Directory is created')
        else:
            print(f'"{imageDirPath}" Directory already Exists.')

        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        cap = cv.VideoCapture(0)

        while True:
            _, frame = cap.read()
            copyFrame = frame.copy()
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            image, board_detected = self.__detect_checker_board(frame, gray, criteria, CHESS_BOARD_DIM)
            # print(ret)
            cv.putText(
                frame,
                f"saved_img : {n}",
                (30, 40),
                cv.FONT_HERSHEY_PLAIN,
                1.4,
                (0, 255, 0),
                2,
                cv.LINE_AA,
            )

            cv.imshow("frame", frame)
            cv.imshow("copyFrame", copyFrame)

            key = cv.waitKey(1)

            if key == ord("q"):
                break
            if key == ord("s") and board_detected == True:
                # storing the checker board image
                cv.imwrite(f"{imageDirPath}/image{n}.png", copyFrame)

                print(f"saved image number {n}")
                n += 1  # incrementing the image counter
        cap.release()
        cv.destroyAllWindows()

        print("Total saved Images:", n)


    def camera_calibration(self):

        # Checker board size
        chessBoardDim = (9, 6)

        # The size of the square in the checker board
        squareSize = 20  # millimeters

        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        path = get_datapath()
        calibDataPath = path
        checkDir = os.path.isdir(calibDataPath)

        if not checkDir:
            os.makedirs(calibDataPath)
            print(f'"{calibDataPath}" Directory is created')

        else:
            print(f'"{calibDataPath}" Directory already Exists.')

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        obj3D = np.zeros((chessBoardDim[0] * chessBoardDim[1], 3), np.float32)

        obj3D[:, :2] = np.mgrid[0 : chessBoardDim[0], 0 : chessBoardDim[1]].T.reshape(
            -1, 2
        )
        obj3D *= squareSize
        print(obj3D)

        # Arrays to store object points and image points from all the images.
        objPoints3D = []  # 3d point in real world space
        imgPoints2D = []  # 2d points in image plane.

        # The images directory path
        imageDirPath = path + "\\images"

        files = os.listdir(imageDirPath)
        for file in files:
            print(file)
            imagePath = os.path.join(imageDirPath, file)
            # print(imagePath)

            image = cv.imread(imagePath)
            grayScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            ret, corners = cv.findChessboardCorners(image, chessBoardDim, None)
            if ret == True:
                objPoints3D.append(obj3D)
                corners2 = cv.cornerSubPix(grayScale, corners, (3, 3), (-1, -1), criteria)
                imgPoints2D.append(corners2)

                img = cv.drawChessboardCorners(image, chessBoardDim, corners2, ret)

        cv.destroyAllWindows()
        # h, w = image.shape[:2]
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
            objPoints3D, imgPoints2D, grayScale.shape[::-1], None, None
        )
        print("calibrated")

        print("dumping the data into one file using numpy ")
        np.savez(
            f"{calibDataPath}/MultiMatrix",
            camMatrix=mtx,
            distCoef=dist,
            rVector=rvecs,
            tVector=tvecs,
        )

        print("-------------------------------------------")

        print("loading data stored using numpy savez function\n \n \n")

        data = np.load(f"{calibDataPath}/MultiMatrix.npz")

        camMatrix = data["camMatrix"]
        distCof = data["distCoef"]
        rVector = data["rVector"]
        tVector = data["tVector"]

        print("loaded calibration data successfully")


    def __aruco_ratio(self, frame):

        path = get_datapath()
        calibPath = path + "\\MultiMatrix.npz"
        calibData = np.load(calibPath)

        camMatrix = calibData["camMatrix"]
        distCoef = calibData["distCoef"]
        rVectors = calibData["rVector"]
        tVectors = calibData["tVector"]

        self.markerSize = 100 # millimeters

        # Load Aruco detector
        arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_5X5_100)
        parameters = cv.aruco.DetectorParameters()

        # Save Aruco output
        arucoOutput = cv.aruco.detectMarkers(frame, arucoDict, parameters=parameters)
        corners, markerIDs, reject = arucoOutput

        # Check if Aruco marker is getting detected
        if not corners:
            markerDetected = None
            markerCorners = None
            rVec = None
            tVec = None
            ids = [None]
            print("No Aruco-marker detected!")

        # Get Aruco data
        else:
            markerDetected = 1
            print("Aruco-marker detected!")

            rVec, tVec, _ = cv.aruco.estimatePoseSingleMarkers(corners, self.markerSize, camMatrix, distCoef)
            totalMarkers = range(0, markerIDs.size)
    
            for ids, corner, i in zip(markerIDs, corners, totalMarkers):
                
                print(ids[0])
                corner = np.reshape(corner, (4, 2))
                corner = corner.astype(int)
                topRight = corner[0]
                bottomRight = corner[1]
                bottomLeft = corner[2]
                topLeft = corner[3]

                markerCorners = [topLeft, bottomLeft, topRight, bottomRight]

                distance = np.sqrt(tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2)
                
                # Draw the pose of the marker
                cv.drawFrameAxes(frame, camMatrix, distCoef, rVec[i], tVec[i], 20, 4)

                cv.putText(
                    frame,
                    f"id: {ids[0]} Dist: {round(distance, 2)}",
                    topRight,
                    cv.FONT_HERSHEY_PLAIN,
                    1.3,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(frame,
                    f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                    bottomRight,
                    cv.FONT_HERSHEY_PLAIN,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                # print(ids, "  ", corners)
            # Draw polygon around the marker
            intCorners = np.int0(corners)
            cv.polylines(frame, intCorners, True, (0, 255, 0), 5)

        return markerCorners, markerDetected, rVec, tVec, ids[0]


    def __detect_objects(self, frame):

        # Convert Image to grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Create a Mask with adaptive threshold
        mask = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 19, 5)

        # Find contours
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        #cv2.imshow("mask", mask)
        objects_contours = []

        for cnt in contours:
            area = cv.contourArea(cnt)

            if area > 2000:
                #cnt = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                objects_contours.append(cnt)

        return objects_contours
    

    def rectangle(self) -> list:
        
        # Ausblenden von schwarzen Bildbereichen
        # Entscheiden, welches Objekt übergeben werden soll
        # Eulerwinkel übergeben
        
        # If a marker gets detected, the method returns a value after 1s
        timeout = False
        
        # Set number of detected objects to 0
        nrOfObjects = 0

        # As long as you dont press a key
        while cv.waitKey(1) < 0:
            hasFrame, frame = self.get_image()
            
            if not hasFrame:
                cv.waitKey()
                break

            # Read Aruco
            arucoCorners, arucoDetected, rVector, tVector, arucoID = self.__aruco_ratio(frame)

            # Only run if marker is getting detected
            if arucoDetected == 1 and arucoID == 10:
                
                # Stop detection 1s after finding aruco
                if not timeout:
                    timeout = time.time() + 1
                if time.time() > timeout:
                    break

                # Apply Geometrical Transformation
                arucoPixelWidth = 100
                pixelMmRatio = arucoPixelWidth / self.markerSize
                
                points = np.float32([arucoCorners[0], arucoCorners[1], arucoCorners[2], arucoCorners[3]])
                pointsTransformed = np.float32([[0, 0], [0, arucoPixelWidth], [arucoPixelWidth, 0], [arucoPixelWidth, arucoPixelWidth]])

                # Transformation of image
                matrix = cv.getPerspectiveTransform(points, pointsTransformed)
                transformedFrame = cv.warpPerspective(frame, matrix, (self.width, self.height))

                # Detect Contours
                contours = self.__detect_objects(transformedFrame)
                
                poses = []

                for cnt in contours:
                    # Get rect
                    rect = cv.minAreaRect(cnt)
                    (x, y), (w, h), angle = rect

                    # Ignore the marker's contours
                    offsetToMarker = math.sqrt((x - 50) ** 2 + (y - 50) ** 2)
                    if offsetToMarker < arucoPixelWidth/2:
                        continue
                    
                    # Add 1 to number of Objects if any object (except marker) is detected
                    nrOfObjects =+ 1

                    # Get width and height of the objects by applying the ratio
                    objWidth = w / pixelMmRatio
                    objHeight = h / pixelMmRatio
                    objSize = [objWidth, objHeight]
                    
                    # Center
                    center = (int(x), int(y))
                    
                    cv.circle(transformedFrame, center, 5, (0, 0, 255), -1)

                    # Get position of objects in aruco coodinate system by applying the ratio
                    objXTrans = (y - arucoPixelWidth / 2) / pixelMmRatio
                    objYTrans = (x - arucoPixelWidth / 2) / pixelMmRatio
                    objZTrans = 0
                    objTrans = [objXTrans, objYTrans, objZTrans]
                                        
                    # Transform back to camera coordinate system                    
                    rotMat, _ = cv.Rodrigues(rVector)
                    
                    obj = rotMat.dot(objTrans) + tVector
                    print(f"Object detected at: {obj}")

                    # Draw box
                    box = cv.boxPoints(rect)
                    box = np.int0(box)
                    cv.polylines(transformedFrame, [box], True, (255, 0, 0), 2)
                    
                    cv.putText(transformedFrame, "Width {} mm".format(round(objWidth, 1)), (int(x - 100), int(y - 15)), cv.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
                    cv.putText(transformedFrame, "Height {} mm".format(round(objHeight, 1)), (int(x - 100), int(y + 20)), cv.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
                    cv.putText(transformedFrame, "Angle {} degrees".format(round(angle, 1)), (int(x - 100), int(y + 55)), cv.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
                    
                    # Convert pose and append data to list
                    pose = Pose(obj[0, 0, 0], obj[0, 0, 1], obj[0, 0, 2], 0, 0, 0)
                    objData = [pose, objSize]
                    poses.append(objData)
            else:
                transformedFrame = frame

            cv.imshow('Rectangle detection', frame)
            cv.imshow('Transformed Frame', transformedFrame)

        if nrOfObjects == 0:
            print("No objects have been found")
            poses = None
            objSize = None
        

        # Transform the objects camera coords to the TM5's base coords
        # trafPose = transform(pose, CS_CAMERA, CS_TM5_BASE)

        return poses


    def circle(self) -> list:
        
        # If a marker gets detected, the method returns a value after 1s
        timeout = False
        
        # Set number of detected objects to 0
        nrOfObjects = 0

        # As long as you dont press a key
        while cv.waitKey(1) < 0:
            hasFrame, frame = self.get_image()
            
            if not hasFrame:
                cv.waitKey()
                break

            # Read Aruco
            arucoCorners, arucoDetected, rVector, tVector, arucoID = self.__aruco_ratio(frame)

            # Only run if marker is getting detected
            if arucoDetected == 1 and arucoID == 10:
                
                # Stop detection 1s after finding aruco
                if not timeout:
                    timeout = time.time() + 1
                if time.time() > timeout:
                    break

                # Apply Geometrical Transformation
                arucoPixelWidth = 100
                pixelMmRatio = arucoPixelWidth / self.markerSize
                
                points = np.float32([arucoCorners[0], arucoCorners[1], arucoCorners[2], arucoCorners[3]])
                pointsTransformed = np.float32([[0, 0], [0, arucoPixelWidth], [arucoPixelWidth, 0], [arucoPixelWidth, arucoPixelWidth]])

                # Transformation of image
                matrix = cv.getPerspectiveTransform(points, pointsTransformed)
                transformedFrame = cv.warpPerspective(frame, matrix, (self.width, self.height))

                # Detect Contours
                contours = self.__detect_objects(transformedFrame)
                
                poses = []

                for cnt in contours:
                    # Get crcl
                    crcl = cv.minEnclosingCircle(cnt)
                    (x, y), radius = crcl

                    # Ignore the marker's contours
                    offsetToMarker = math.sqrt((x - 50) ** 2 + (y - 50) ** 2)
                    if offsetToMarker < arucoPixelWidth/2:
                        continue
                    
                    # Add 1 to number of Objects if any object (except marker) is detected
                    nrOfObjects =+ 1

                    # Get Radius of the objects by applying the ratio
                    objRadius = radius / pixelMmRatio

                    # center and radius
                    center = (int(x), int(y))
                    radius = int(radius)
                    cv.circle(frame, center, 5, (0, 0, 255), -1)
                    
                    # Get position of objects in aruco coodinate system by applying the ratio
                    objXTrans = (y - arucoPixelWidth / 2) / pixelMmRatio
                    objYTrans = (x - arucoPixelWidth / 2) / pixelMmRatio
                    objZTrans = 0
                    objTrans = [objXTrans, objYTrans, objZTrans]
                                        
                    # Transform back to camera coordinate system                    
                    rotMat, _ = cv.Rodrigues(rVector)
                    
                    obj = rotMat.dot(objTrans) + tVector
                    print(f"Object detected at: {obj}")

                    # Draw circle
                    cv.circle(frame, center, radius, (255, 0, 0), 2)
                    cv.putText(frame, "Radius {} mm".format(round(objRadius, 1)), (int(x - 100), int(y - 15)), cv.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
                    
                    # Convert pose and append data to list
                    pose = Pose(obj[0, 0, 0], obj[0, 0, 1], obj[0, 0, 2], 0, 0, 0)
                    objData = [pose, objRadius]
                    poses.append(objData)
            else:
                transformedFrame = frame

            cv.imshow('Circle detection', frame)
            cv.imshow('Transformed Frame', transformedFrame)

        if nrOfObjects == 0:
            print("No objects have been found")
            pose = None
            objRadius = None

        # Transform the objects camera coords to the TM5's base coords
        # trafPose = transform(pose, CS_CAMERA, CS_TM5_BASE)

        return poses


    def __import_net(self):
    
        path = get_datapath()
        datapath = path + "\\graph_opt.pb"
        self.net = cv.dnn.readNetFromTensorflow(datapath)


    def human(self) -> list:

        # folgen Wenn Aruco = Gassi Code
        # Aruco IDs für Menschen und Objekte

        # set timer
        timeout1 = time.time() + 200
        pose = False

        BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                       "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                       "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                       "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

        POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                       ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                       ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                       ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                       ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]
        
        inWidth = 368
        inHeight = 368
        thr = 0.2

        # Move TM5 facing forwards
        # standardPose = Pose(0, 0, 400, 0, 0, 0)
        # rp.TM5.ptp_pose(standardPose)

        # Import net if no net is imported yet
        if self.net == None:
            self.__import_net()

        # Loop
        while cv.waitKey(1) < 0:
            hasFrame, frame = self.get_image()

            if not hasFrame:
                cv.waitKey()
                break
            
            # Break after 20s
            if  time.time() > timeout1:
                break
            
            rightHand = 0
            leftHand = 0
            rightShoulder = 0
            leftShoulder = 0

            self.net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
            out = self.net.forward()
            out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

            assert(len(BODY_PARTS) == out.shape[1])

            points = []

            for i in range(len(BODY_PARTS)):
                # Slice heatmap of corresponging body's part.
                heatMap = out[0, i, :, :]

                # Originally, we try to find all the local maximums. To simplify a sample
                # we just find a global one. However only a single pose at the same time
                # could be detected this way.
                _, conf, _, point = cv.minMaxLoc(heatMap)
                x = (self.width * point[0]) / out.shape[3]
                y = (self.height * point[1]) / out.shape[2]
                # Add a point if it's confidence is higher than threshold.
                points.append((int(x), int(y)) if conf > thr else None)

            for pair in POSE_PAIRS:
                partFrom = pair[0]
                partTo = pair[1]
                assert(partFrom in BODY_PARTS)
                assert(partTo in BODY_PARTS)

                idFrom = BODY_PARTS[partFrom]  
                idTo = BODY_PARTS[partTo]

                if points[idFrom] and points[idTo]:
                    # cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                    # cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
                    # cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
                    # print(f"From {pair[0]}: {str(points[idFrom])} to {pair[1]}: {str(points[idTo])}")
                    pass

                if pair[1] == "RWrist" and points[idTo]:
                    rightHand = points[idTo]
                
                if pair[1] == "LWrist" and points[idTo]:
                    leftHand = points[idTo]

                if pair[1] == "RShoulder" and points[idTo]:
                    rightShoulder = points[idTo]
                
                if pair[1] == "LShoulder" and points[idTo]:
                    leftShoulder = points[idTo]

            t, _ = self.net.getPerfProfile()
            freq = cv.getTickFrequency() / 1000
            cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

            _, arucoDetected, _, tVector, arucoID = self.__aruco_ratio(frame)

            cv.imshow('OpenPose using OpenCV', frame)
            
            # Check if Aruco is detected
            if arucoDetected == 1 and arucoID == 20:

                # Clap-Detector
                if rightHand != 0 and leftHand != 0 and rightShoulder != 0 and leftShoulder != 0:

                    # Distance between hands
                    distHands = math.sqrt((rightHand[0] - leftHand[0]) ** 2 + (rightHand[1] - leftHand[1]) ** 2 )

                    # If hands are between shoulders and distance is between a certain threshold
                    if rightShoulder[0] < rightHand[0] and leftShoulder[0] > leftHand[0] and distHands < (self.width/10):
                        pose = Pose(tVector[0, 0, 0], 0, tVector[0, 0, 2], 0, 0, 0)
                        break
            
        # Return pose
        print("tvec", tVector[0, 0, 0], tVector[0, 0, 1], tVector[0, 0, 2])
        trafPose = transform(pose, CS_CAMERA, CS_WORLD)
        return trafPose

        # return [tVector[0, 0, 0], tVector[0, 0, 1], tVector[0, 0, 2]]

