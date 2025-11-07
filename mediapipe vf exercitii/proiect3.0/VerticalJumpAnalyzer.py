import os
import cv2
from VideoAnalyzer import VideoAnalyzer, mp_pose
from Utils import distance_points

class VerticalJumpAnalyzer(VideoAnalyzer):
    def __init__(self, video_path):
        super().__init__(video_path, window_name='Vertical Jump Analysis')

    def calculateScale(self, ankle, nose, h):
        if self.scale is None:
            capY = int(nose[1] * h)
            footY = int(ankle[1] * h)
            height_px = abs(footY - capY)
            if height_px > 0:
                self.scale = self.athlete_height / height_px
                print(f"Scale: {self.scale:.5f} m/px")

    def extractLandmarks(self, landmarks):
        heelR = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
        heelL = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]

        return heelR, heelL, nose

    def displayInfo(self, landmarks_data, image):
        heelL, heelR, nose = landmarks_data
        drawLine(image, heelL, heelR)
        cv2.putText(image, self.stage, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)



    def checkRep(self, landmarks_data):
        ankle, nose = landmarks_data

        if(self.val == True):
            self.floor = ankle
            self.val = False

        distance_px = distance_points(self.floor, ankle)


        if(self.floor[1] - ankle[1] > 0):
            if (self.prev_distance_px > distance_px and self.prevCounter):
                self.prevCounter = False
                self.max_distance_px = distance_px
                print(f"{self.max_distance_px}")
                self.counter += 1
                print(self.counter)
        else:
            self.prevCounter = True


        if(self.floor[1] - ankle[1] > 0):
            print(f"+ :{self.floor[1]} / {ankle[1]} = {distance_px}")
        else:
            print(f"- :{self.floor[1]} / {ankle[1]} = {distance_px}")

        self.prev_distance_px = distance_px









