import os
import requests
from pprint import pprint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SHEET_PRICES_ENDPOINT = "https://api.sheety.co/d1d6eaca05258647c2e89ceecab654ce/flightDeals/prices"


class DataManager:

    def __init__(self):
        self._authorization_header = {
            "Authorization": f"Bearer {os.environ.get("FLIGHT_SHEET_API_KEY")}"
        }
        self.destination_data = {}

    def get_destination_data(self):
        # Use the Google Sheets API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEET_PRICES_ENDPOINT, headers=self._authorization_header)
        data = response.json()
        self.destination_data = data["prices"]
        # Try importing pretty print and printing the data out again using pprint() to see it formatted.
        pprint(data)
        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self) -> None:
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEET_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=self._authorization_header
            )
            print(response.text)
