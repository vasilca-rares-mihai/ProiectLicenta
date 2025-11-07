import cv2
import mediapipe as mp
from abc import ABC, abstractmethod

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class VideoAnalyzer(ABC):
    def __init__(self, video_path, window_name="Training Analysis"):
        self.video_path = video_path
        self.window_name = window_name
        self.cap = cv2.VideoCapture(video_path)

        self.prevCounter = None
        self.flag = True
        self.stage = "initial"
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        self.angle = 0
        self.counter = 0
        self.speed = 0
        self.distance = 0

        self.athleteAge = None
        self.athleteGender = None
        self.athleteHeight = None
        self.athleteWeight = None


        if not self.cap.isOpened():
            raise FileNotFoundError(f"Error: Could not open the video file: {video_path}")

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    @abstractmethod
    def extractLandmarks(self, landmarks):
        pass

    @abstractmethod
    def checkRep(self, landmarks_data):
        pass

    @abstractmethod
    def displayInfo(self, landmarks_data, image):
        pass


    def analyze(self, athlete):
        self.athleteAge = athlete.age
        self.athleteGender = athlete.gender
        self.athleteHeight = athlete.height
        self.athleteWeight = athlete.weight
        print(f"Type of analysis: {self.__class__.__name__}")
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark

                    landmarks_data = self.extractLandmarks(landmarks)
                    self.displayInfo(landmarks_data, image)
                    self.checkRep(landmarks_data)

                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)


                cv2.imshow(self.window_name, image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        print(f"Analysis completed. Total repetitions: {self.counter}")
        self.cap.release()
        cv2.destroyAllWindows()

