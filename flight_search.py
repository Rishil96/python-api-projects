import os
import requests
from datetime import datetime, timedelta


class FlightSearch:

    TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
    AIRPORT_CITY_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations"
    FLIGHT_OFFERS_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ.get("AMADEUS_API_KEY")
        self._api_secret = os.environ.get("AMADEUS_API_SECRET")
        self._token = self._get_new_token()
        self.headers = {
            "Authorization": f"Bearer {self._token["access_token"]}"
        }

    def get_airport_code(self, city_name) -> str:
        """
        This method returns an IATA code for a given input city
        """
        parameters = {
            "subType": "CITY",
            "keyword": city_name
        }

        response = requests.get(url=self.AIRPORT_CITY_ENDPOINT, params=parameters, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _get_new_token(self) -> dict:
        """
        This method is used to get a token to interact with the Amadeus API
        """
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=self.TOKEN_ENDPOINT, headers=header, data=body)
        response.raise_for_status()
        return response.json()

    def get_flights(self, origin_city_iata_code: str, destination_city_iata_code: str, time_range_in_days: int,
                    adults: int) -> dict:
        """
        This method returns the list of flights available between the next 6 months from origin to destination
        """

        from_date = datetime.now() + timedelta(days=1)
        to_date = from_date + timedelta(days=time_range_in_days)

        # Convert both dates into usable format
        from_date = from_date.strftime("%Y-%m-%d")
        to_date = to_date.strftime("%Y-%m-%d")

        parameters = {
            "originLocationCode": origin_city_iata_code,
            "destinationLocationCode": destination_city_iata_code,
            "departureDate": from_date,
            "returnDate": to_date,
            "adults": adults
        }

        response = requests.get(url=self.FLIGHT_OFFERS_ENDPOINT, params=parameters, headers=self.headers)
        response.raise_for_status()
        return response.json()
