import cv2
from VideoAnalyzer import VideoAnalyzer, mp_pose
from Utils import calculate_angle, drawLine

class SquatAnalyzer(VideoAnalyzer):

    def __init__(self, video_path):
        super().__init__(video_path, window_name="Squat Analysis")

    #function that extracts the coordinates of key points from the image and returns them
    def extractLandmarks(self, landmarks):
        hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        hipR = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        kneeR = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        ankleL = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        ankleR = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        return hipL, hipR, kneeL, kneeR, ankleL, ankleR

    #function I used to draw some information, for exemple: legs position for squats
    def displayInfo(self, landmarks_data, image):
        hipL, hipR, kneeL, kneeR, ankleL, ankleR = landmarks_data

        drawLine(image, hipL, kneeL)
        drawLine(image, kneeL, ankleL)

        cv2.putText(image, self.stage, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 192, 203), 2)
        h, w, _ = image.shape
        kneeL_coords = (int(kneeL[0] * w), int(kneeL[1] * h))
        cv2.putText(image, str(int(calculate_angle(hipL, kneeL, ankleL))), kneeL_coords, cv2.FONT_HERSHEY_DUPLEX , 0.5, (255, 192, 203), 2 )


    def checkRep(self, landmarks_data):
        hipL, hipR, kneeL, kneeR, ankleL, ankleR = landmarks_data

        knee_angle = calculate_angle(hipL, kneeL, ankleL)

        if knee_angle < 70:
            self.stage = "down"
        if knee_angle > 150 and self.stage == "down":
            self.stage = "up"
            self.counter += 1

        # print only when the counter has changed the value
        if self.prevCounter != self.counter:
            print(f"Squats: {self.counter}")
            self.prevCounter = self.counter