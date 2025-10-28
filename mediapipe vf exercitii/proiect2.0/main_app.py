from squat_analyzer import SquatAnalyzer
from pushup_analyzer import PushupAnalyzer
from step_analyzer import StepAnalyzer
from pullup_analyzer import PullupAnalyzer
from verticalJump_analyzer import VerticalJumpAnalyzer
import os


class WorkoutManager:

    def __init__(self):
        self.analyzers = {
            'pushups': PushupAnalyzer,
            'squats': SquatAnalyzer,
            'running': StepAnalyzer,
            'pullups': PullupAnalyzer,
            'vjump': VerticalJumpAnalyzer,
        }

    def display_menu(self):
        print("\n\t\t\tVideo Training Analysis Menu")
        print("Available options:")
        for key in self.analyzers:
            print(f" - {key.capitalize()}")
        print("\n")

    def run_analysis(self, workout_type, video_path):

        workout_type = workout_type.lower()

        if workout_type not in self.analyzers:
            print(f"Error: The workout type '{workout_type}' is not supported.")
            return

        if not os.path.exists(video_path):
            print(f"Error: The video file '{video_path}' was not found.")
            return

        AnalyzerClass = self.analyzers[workout_type]

        try:
            analyzer = AnalyzerClass(video_path)
            analyzer.analyze()

        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"An error occurred during the analysis: {e}")


if __name__ == "__main__":
    manager = WorkoutManager()

    manager.display_menu()

    workout = input("Choose the type of analysis (pushups/squats/running/pullups/vjump): ")
    video = input("Enter the path to the video (e.g., video0.mp4): ")

    print("\n--- Running Analysis ---")
    manager.run_analysis(workout, video)
    print("The program has closed.")

