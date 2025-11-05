from VideoAnalyzer import VideoAnalyzer, mp_pose
from Utils import calculate_angle


class PushupAnalyzer(VideoAnalyzer):
    def __init__(self, video_path):
        super().__init__(video_path, window_name="Push-up Analysis")
        self.prevCounter = None

    def extractLandmarks(self, landmarks):
        sholder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        self.angle = calculate_angle(sholder, elbow, wrist)
        return self.angle

    def checkRep(self, angle):
        if angle < 90:
            self.stage = "down"
        if angle > 160 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
        if self.prevCounter != self.counter:
            print(f"Push-ups: {self.counter}")
            self.prevCounter = self.counter