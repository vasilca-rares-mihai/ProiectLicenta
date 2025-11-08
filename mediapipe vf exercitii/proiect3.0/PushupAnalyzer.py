import cv2
from VideoAnalyzer import VideoAnalyzer, mp_pose
from Utils import calculate_angle, drawLine

class PushupAnalyzer(VideoAnalyzer):
    def __init__(self, video_path):
        super().__init__(video_path, window_name="Push-up Analysis")

    # function that extracts the coordinates of key points from the image and returns them
    def extractLandmarks(self, landmarks):
        sholderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        sholderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        heelL = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        return sholderR, sholderL, elbowR, elbowL, wristR, wristL, heelL, kneeL, hipL

    #function I used to draw some information, for exemple: body position for pushups
    def displayInfo(self, landmarks_data, image):
        sholderR, sholderL, elbowR, elbowL, wristR, wristL, heelL, kneeL, hipL = landmarks_data

        drawLine(image, heelL, kneeL)
        drawLine(image, kneeL, hipL)
        drawLine(image, hipL, sholderL)

        cv2.putText(image, self.stage, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 192, 203), 2)
        h, w, _ = image.shape
        kneeL_coords = (int(kneeL[0] * w), int(kneeL[1] * h))
        cv2.putText(image, str(int(calculate_angle(heelL, kneeL, hipL))), kneeL_coords, cv2.FONT_HERSHEY_DUPLEX , 0.5, (255, 192, 203), 2 )
        hipL_coords = (int(hipL[0] * w), int(hipL[1] * h))
        cv2.putText(image, str(int(calculate_angle(kneeL, hipL, sholderL))), hipL_coords, cv2.FONT_HERSHEY_DUPLEX , 0.5, (255, 192, 203), 2 )
        elbowL_coords = (int(elbowL[0] * w), int(elbowL[1] * h))
        cv2.putText(image, str(int(calculate_angle(sholderL, elbowL, wristL))), elbowL_coords, cv2.FONT_HERSHEY_DUPLEX , 0.5, (255, 192, 203), 2)

    def checkRep(self, landmarks_data):
        sholderR, sholderL, elbowR, elbowL, wristR, wristL, heelL, kneeL, hipL = landmarks_data

        if(calculate_angle(heelL, kneeL, hipL) > 145 and calculate_angle(kneeL, hipL, sholderL) > 145):
            elbow_angle = calculate_angle(sholderL, elbowL, wristL)
            if elbow_angle < 90:
                self.stage = "down"
            if elbow_angle > 160 and self.stage == "down":
                self.stage = "up"
                self.counter += 1
        else:
            print("INCORRECT BODY POSITION!!!")

        #print only when the counter has changed the value
        if self.prevCounter != self.counter:
            print(f"Push-ups: {self.counter}")
            self.prevCounter = self.counter