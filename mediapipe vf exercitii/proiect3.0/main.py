from SquatAnalyzer import SquatAnalyzer
from PushupAnalyzer import PushupAnalyzer
from StepAnalyzer import StepAnalyzer
from PullupAnalyzer import PullupAnalyzer
from VerticalJumpAnalyzer import VerticalJumpAnalyzer
import os
import tkinter as tk
from tkinter import filedialog
from enum import Enum


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

    def run_analysis(self, workout_type):

        workout_type = workout_type.lower()

        if workout_type not in self.analyzers:
            print(f"Error: The workout type '{workout_type}' is not supported.")
            return

        initial_path = os.path.join("video", workout_type)
        print(initial_path)

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        video_path = filedialog.askopenfilename(
            title="Alege un clip video",
            initialdir=initial_path,
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )


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
    print("\n--- Running Analysis ---")
    manager.run_analysis(workout)
    print("The program has closed.")

