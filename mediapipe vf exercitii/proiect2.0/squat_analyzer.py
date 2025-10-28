# squat_analyzer.py
from video_analyzer import VideoAnalyzer, mp_pose
from utils import calculate_angle


class SquatAnalyzer(VideoAnalyzer):

    def __init__(self, video_path):
        super().__init__(video_path, window_name="Squat Analysis")
        self.prevCounter = None

    def extractLandmarks(self, landmarks):
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        self.angle = calculate_angle(hip, knee, ankle)
        return self.angle

    def checkRep(self, angle):
        #print(self.angle)
        if angle < 70:
            self.stage = "down"
        if angle > 150 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
        if self.prevCounter != self.counter:
            print(f"Push-ups: {self.counter}")
            self.prevCounter = self.counter