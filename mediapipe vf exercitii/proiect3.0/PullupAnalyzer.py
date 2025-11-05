import cv2
from VideoAnalyzer import VideoAnalyzer, mp_pose
from Utils import calculate_angle, drawLine

class PullupAnalyzer(VideoAnalyzer):
    def __init__(self, video_path):
        super().__init__(video_path, window_name="Pull-up Analysis")
        self.prevCounter = None

    #function that extracts the coordinates of key points from the image and returns them
    def extractLandmarks(self, landmarks):
        sholderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        sholderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y]

        return sholderL, sholderR, elbowL, elbowR, wristL, wristR, mouth

    #function I used to draw some information, for exemple: bar for pullups
    def displayInfo(self, landmarks_data, image):
        sholderL, sholderR, elbowL, elbowR, wristL, wristR, mouth = landmarks_data

        drawLine(image, wristL, wristR)

        cv2.putText(image, self.stage, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        h, w, _ = image.shape
        leftArm_coords = (int(elbowL[0] * w), int(elbowL[1] * h))
        cv2.putText(image, str(int(calculate_angle(sholderL, elbowL, wristL))), leftArm_coords, cv2.FONT_HERSHEY_DUPLEX , 0.5,(255, 192, 203), 2)
        rightArm_coords = (int(elbowR[0] * w), int(elbowR[1] * h))
        cv2.putText(image, str(int(calculate_angle(sholderR, elbowR, wristR))), rightArm_coords, cv2.FONT_HERSHEY_DUPLEX , 0.5,(255, 192, 203), 2)

    def checkRep(self, landmarks_data):
        sholderL, sholderR, elbowL, elbowR, wristL, wristR, mouth = landmarks_data

        #variables that help me count exercise repetitions
        #bar - y coord. whrn bar < chin.y => one correct rep
        bar = (wristR[1] + wristL[1]) / 2
        #angleL and angleR. angle because a correct rep is when the angles > 160
        angleL = calculate_angle(sholderL, elbowL, wristL)
        angleR = calculate_angle(sholderR, elbowR, wristR)
        #I approximated the chin level (between shoulder and mouth, on the y coordinate
        chin = ((sholderL[1]+sholderR[1]) /2 + mouth[1])/2

        if angleL > 160 and angleR > 160:
            self.stage = "down"
        if angleL < 90 and angleR < 90 and self.stage == "down" and chin < bar:
            self.stage = "up"
            self.counter += 1

        #print only when the counter has changed the value
        if(self.prevCounter != self.counter):
            print(f"Pull-ups: {self.counter}")
            self.prevCounter = self.counter