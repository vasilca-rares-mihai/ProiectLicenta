from VideoAnalyzer import VideoAnalyzer, mp_pose
from Utils import calculate_angle, drawLine

class PullupAnalyzer(VideoAnalyzer):
    def __init__(self, video_path):
        super().__init__(video_path, window_name="Pull-up Analysis")
        self.prevCounter = None

    def extractLandmarks(self, landmarks):
        sholderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        sholderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y]

        angle = calculate_angle(sholderL, elbowL, wristL)
        sholder = (sholderR[1] + sholderL[1]) / 2
        chin = (sholder + mouth[1])/2
        return angle, wristL, wristR, chin


    def checkRep(self, landmarks_data, image):
        angle, wristL, wristR, chin = landmarks_data

        bar = (wristR[1] + wristL[1]) / 2
        drawLine(image, wristL[0], wristL[1], wristR[0], wristR[1])

        if angle > 160:
            self.stage = "down"
        if angle < 90 and self.stage == "down" and chin < bar:
            self.stage = "up"
            self.counter += 1
        if(self.prevCounter != self.counter):
            print(f"Pull-ups: {self.counter}")
            self.prevCounter = self.counter