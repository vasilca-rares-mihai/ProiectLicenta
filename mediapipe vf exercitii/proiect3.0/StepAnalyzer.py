import os
import cv2
from VideoAnalyzer import VideoAnalyzer, mp_pose
from Utils import distance_points, drawLine


class StepAnalyzer(VideoAnalyzer):
    def __init__(self, video_path):
        super().__init__(video_path, window_name="Running Analysis")
        self.prev_distance_px = 0.0
        self.in_pas = False
        self.video_timer = 0.0

    #I created this function to calculate the distance and speed achieved by the athlete.
    def calculateDistanceAndSpeed(self):
        #I found in the specialized documentation a ratio between height and step distance
        #Females: Height in inches multiplied by 0.413 equals stride length
        #Males: Height in inches multiplied by 0.415 equals stride length
        if self.athleteGender == "M":
            self.distance = 0.415 * self.athleteHeight * self.counter
        elif self.athleteGender == "F":
            self.distance = 0.413 * self.athleteHeight * self.counter
        #I calculated the duration at which a frame is processed, to obtain the instantaneous speed
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_time = 1 / fps
        self.video_timer += frame_time
        #Speed
        self.speed = self.distance / self.video_timer


    #function that extracts the coordinates of key points from the image and returns them
    def extractLandmarks(self, landmarks):
        heelL = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        heelR = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]

        return heelL, heelR

    #function I used to draw some information, for exemple: the distance between athlete's 2 legs
    def displayInfo(self, landmarks_data, image):
        heelL, heelR = landmarks_data
        drawLine(image, heelL, heelR)
        cv2.putText(image, self.stage, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)


    def checkRep(self, landmarks_data):
        heelL, heelR = landmarks_data
        #I calculate distance between athlet's to legs
        distanceLegs_px = distance_points(heelL, heelR)
        #if the distance starts to decrease, the step has been taken and the counter will increase.
        if distanceLegs_px < self.prev_distance_px and self.in_pas:
            self.counter += 1
            self.in_pas = False
        #if the distance starts to increase, a new step will begin
        elif distanceLegs_px > self.prev_distance_px:
            self.in_pas = True

        self.prev_distance_px = distanceLegs_px
        self.stage = "running"
        self.calculateDistanceAndSpeed()

        if(self.prevCounter != self.counter):
            print(f"Step {self.counter}, Distance {self.distance}, Speed {self.speed}")
            self.prevCounter = self.counter
