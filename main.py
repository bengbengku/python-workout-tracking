import requests
import os
from dotenv import find_dotenv, load_dotenv
from datetime import datetime

load_dotenv(find_dotenv())


APP_ID = os.getenv("ID")
API_KEY = os.getenv("KEY")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.getenv("SHT_END")

exercise_text = input("Tell me which exercise you did: ")

AUTH_SHEETY_BEARER = os.getenv("BEARER")

nutrients_params = {
    "query": exercise_text,
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0"
}

res = requests.post(url=exercise_endpoint, json=nutrients_params, headers=headers)
result = res.json()["exercises"]

today_date = datetime.now().strftime("%d/%m/%Y")
today_time = datetime.now().strftime("%X")



for exercise in result:
    sheet_input = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": round(exercise["nf_calories"])
        }
    }

    sheet_headers = {
        "Authorization": AUTH_SHEETY_BEARER
    }

    res_sheet = requests.post(url=sheety_endpoint, json=sheet_input, headers=sheet_headers)

