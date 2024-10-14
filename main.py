# Workout Tracker
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
API_KEY = os.environ.get("NUTRITIONIX_API_KEY")

NUTRITIONIX_API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"


# Function to get exercise stats from Nutritionix API
def get_workout_stats(query: str, weight: float, height: float, age: int):
    """
    This function gets the exercise stats from natural language using nutritionix endpoint
    """
    headers = {
        "Content-Type": "application/json",
        "x-app-id": APP_ID,
        "x-app-key": API_KEY
    }

    query_data = {
        "query": query,
        "weight_kg": weight,
        "height_cm": height,
        "age": age
    }

    response = requests.post(url=NUTRITIONIX_API_ENDPOINT, json=query_data, headers=headers)
    response.raise_for_status()

    return response.json()


# Function to add an entry in Google Sheets
def add_row_in_sheet(exercise: str, duration: float, calories: float):
    """
    This function adds an exercise entry in Google Sheets
    """
    today = datetime.now()
    date = today.strftime("%d/%m/%Y")
    time = today.strftime("%H:%M:%S")

    new_row = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }

    headers = {
        "Authorization": f"Bearer {os.environ.get("SHEET_API_KEY")}"
    }

    response = requests.post(url=os.environ.get("SHEET_API_URL"), json=new_row, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Get details about the workout
    exercises = input("Tell me which exercises you did: ")
    weight_in_kg = float(input("What is your current weight in kg: "))
    height_in_cm = float(input("What is your current height in cm: "))
    user_age = int(input("What is your age: "))

    # API Call to get workout stats
    workout_data = get_workout_stats(query=exercises,
                                     weight=weight_in_kg,
                                     height=height_in_cm,
                                     age=user_age)

    # Add all workouts in sheets
    for workout in workout_data["exercises"]:
        entry = add_row_in_sheet(exercise=workout["user_input"],
                                 duration=workout["duration_min"],
                                 calories=workout["nf_calories"])
        print(f"New entry added:", entry)
