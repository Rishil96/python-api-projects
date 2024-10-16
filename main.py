# Flight Deal Finder
from dotenv import load_dotenv
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
from pprint import pprint

# Load env variables
load_dotenv()

# Initialize objects
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Get Sheets data for flights
city_list = data_manager.get_city_table()
print("List of Destinations to travel")
pprint(city_list)

# Get the source city from the user
source_city = input("Please enter your source city from where you would like to take the flight: ")
source_city_iata = flight_search.get_airport_code(city_name=source_city)
source_city_iata = source_city_iata["data"][0]["iataCode"]
print(f"IATA Code for {source_city} is {source_city_iata}.")

# Loop through destinations list and check for flight prices
for dest_city in city_list:
    destination_city = dest_city["city"]
    print(f"Searching flights for {destination_city}...")
    # Search for flights
    flights = flight_search.get_flights(origin_city_iata_code=source_city_iata,
                                        destination_city_iata_code=dest_city["iataCode"],
                                        time_range_in_days=180,
                                        adults=1,
                                        currency_code="INR")

    # Find the cheapest flight using object
    flight_data = FlightData(flights_json=flights)
    cheapest_flight = flight_data.find_cheapest_flight()

    print(f"Cheapest flight from {source_city} to {destination_city} is displayed below:-")
    print(cheapest_flight)

    # Send notification to the user if the flight price fits the budget
    notify = NotificationManager()
    notify.send_notification(flight=cheapest_flight,
                             price_limit=dest_city["lowestPrice"],
                             source=source_city,
                             destination=destination_city)

print("Script run successful!")
