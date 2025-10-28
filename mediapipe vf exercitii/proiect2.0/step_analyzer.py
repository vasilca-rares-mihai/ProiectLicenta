import os
import cv2
from video_analyzer import VideoAnalyzer, mp_pose
from utils import distance_points

class StepAnalyzer(VideoAnalyzer):
    def __init__(self, video_path):
        super().__init__(video_path, window_name="Running Analysis")
        self.total_distance = 0.0
        self.speed = 0.0
        self.prev_distance_px = 0.0
        self.max_distance_px = 0.0
        self.in_pas = False
        self.scale = None
        self.athlete_height = 1.75
        self.athlete_height = float(input("The athlete has a height of (m): "))

    def extractLandmarks(self, landmarks):
        if self.cap.isOpened() and hasattr(self.cap, 'get'):
            h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        else:
            h, w = 1080, 1920

        left_heel = landmarks[mp_pose.PoseLandmark.LEFT_HEEL]
        right_heel = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL]
        ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
        nose = landmarks[mp_pose.PoseLandmark.NOSE]

        left_heel_coord = (int(left_heel.x * w), int(left_heel.y * h))
        right_heel_coord = (int(right_heel.x * w), int(right_heel.y * h))

        return left_heel_coord, right_heel_coord, ankle, nose, h, w

    def calculateScale(self, ankle, nose, h):
        if self.scale is None:
            capY = int(nose.y * h)
            footY = int(ankle.y * h)
            height_px = abs(footY - capY)
            if height_px > 0:
                self.scale = self.athlete_height / height_px
                print(f"Scale: {self.scale:.5f} m/px")

    def calcSpeed(self):
        frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps > 0 and frames > 0:
            duration_sec = frames / fps
            if duration_sec > 0:
                self.speed = self.total_distance / duration_sec
                return self.speed
        return 0.0

    def checkRep(self, landmarks_data):
        left_heel_coord, right_heel_coord, ankle, nose, h, w = landmarks_data

        self.calculateScale(ankle, nose, h)
        if self.scale is None:
            return

        distance_px = distance_points(left_heel_coord, right_heel_coord)

        if distance_px > self.max_distance_px:
            self.max_distance_px = distance_px

        if distance_px < self.prev_distance_px and self.in_pas:
            self.counter += 1
            distance_max_m = self.max_distance_px * self.scale
            self.total_distance += distance_max_m
            self.calcSpeed()

            print(
                f"Step {self.counter}: maximum distance {distance_max_m:.2f} m, "
                f"total = {self.total_distance:.2f} m, speed = {self.speed:.2f} m/s"
            )

            self.max_distance_px = 0.0
            self.in_pas = False

        elif distance_px > self.prev_distance_px:
            self.in_pas = True

        self.prev_distance_px = distance_px
        self.stage = "running"
