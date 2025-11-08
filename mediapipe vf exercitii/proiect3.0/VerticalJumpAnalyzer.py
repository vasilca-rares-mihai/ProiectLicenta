import cv2
from VideoAnalyzer import VideoAnalyzer, mp_pose
from Utils import distance_points, drawLine, pxToM

class VerticalJumpAnalyzer(VideoAnalyzer):
    def __init__(self, video_path):
        super().__init__(video_path, window_name='Vertical Jump Analysis')
        self.line = None
        self.prevCoord = 1
        self.flag2 = True
        self.flag3 = True
        self.listOfJumps = [0]
        self.jumpHeight_px = 0
        self.athleteHeight_px = None
        self.legsOnFirstFrame = None

    def initializeVariablesForHeight(self, landmarks_data):
        if self.flag3:
            heelR, heelL, kneeR, kneeL, eyeR, eyeL = landmarks_data
            self.flag3 = False
            self.flag3 = False
            legs = ((heelR[0] + heelL[0]) / 2, (heelR[1] + heelL[1]) / 2)
            head = ((eyeR[0] + eyeL[0]) /2, (eyeR[1] + eyeL[1]) /2)
            self.athleteHeight_px = distance_points(legs, head)
            self.legsOnFirstFrame = legs



    #function that extracts the coordinates of key points from the image and returns them
    def extractLandmarks(self, landmarks):
        heelR = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
        heelL = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        kneeR = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        eyeR = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y]
        eyeL = [landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y]
        return heelR, heelL, kneeR, kneeL, eyeR, eyeL

    #function I used to draw some information, for exemple: the line that shows, when crossed by the athlete's legs, a jump is performed
    def displayInfo(self, landmarks_data, image):
        heelR, heelL, kneeR, kneeL, eyeR, eyeL = landmarks_data
        if self.flag:
            self.line = ((heelR[1] + heelL[1]) / 2 + (kneeR[1] + kneeR[1]) / 2) / 2
            self.flag = False
        drawLine(image, (0,self.line), (300,self.line))
        cv2.putText(image, self.stage, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)



    def checkRep(self, landmarks_data):
        heelR, heelL, kneeR, kneeL, eyeR, eyeL = landmarks_data
        #the function call that helps me calculate the height in meters of the jump. an initialization of the variables
        self.initializeVariablesForHeight(landmarks_data)
        # when yJump decrease, the athlete jumps off the ground. when yJump increase, the athlete lands on the ground
        yJump = (heelR[1] + heelL[1]) / 2
        if yJump > self.line:
            self.stage = "down"
            self.flag2 = True
        elif yJump < self.line and self.stage == "down":
            self.stage = "up"
        #after the line that I consider the jump has been crossed, I start calculating the maximum height jumped and convert it into meters
        if self.prevCoord < (heelR[1] + heelL[1]) / 2 and self.stage == "up" and self.flag2:
            self.flag2 = False
            self.counter += 1
            self.jumpHeight_px = self.legsOnFirstFrame[1] - self.prevCoord
            self.listOfJumps.append(pxToM(self.athleteHeight, self.jumpHeight_px, self.athleteHeight_px))


        self.prevCoord = (heelR[1] + heelL[1]) / 2

        if self.prevCounter != self.counter:
            print(f"Jump: {self.counter}; jump height: {self.listOfJumps[self.counter]} m")
            self.prevCounter = self.counter
















