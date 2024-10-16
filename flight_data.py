class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, flights_json: dict):
        self.flights_json = flights_json
        self.all_flights = self.process_flight_data()
        self.flight_carriers = self.flights_json.get("dictionaries", {}).get("carriers", {})

    def process_flight_data(self) -> list:
        """
        This method processes the flight data and returns a list of flights and its details
        """
        flights_list = self.flights_json.get("data", [])
        return flights_list

    def format_flight_data(self) -> list:
        """
        This method is to format and only keep relevant data and return it to the user
        """
        formatted_flight_list = []
        for flight in self.all_flights:
            airline_code = flight.get("validatingAirlineCodes", [])
            airline_code = airline_code[0] if len(airline_code) > 0 else "N/A"
            current_flight_info = {
                "ticketDate": flight.get("lastTicketingDate", "N/A"),
                "remainingSeats": flight.get("numberOfBookableSeats", 0),
                "price": flight.get("price", {}),
                "airlineCodes": airline_code,
                "airline": self.flight_carriers.get(airline_code, "N/A")

            }
            formatted_flight_list.append(current_flight_info)

        return formatted_flight_list

    def find_cheapest_flight(self) -> dict:
        """
        This method finds the cheapest flight from all the available flights
        """
        formatted_flight_list = self.format_flight_data()
        result_flight = formatted_flight_list[0]

        for flight in formatted_flight_list:
            cheapest_flight = float(result_flight.get("price").get("grandTotal"))
            current_flight = float(flight.get("price").get("grandTotal"))
            if cheapest_flight > current_flight:
                result_flight = flight

        return result_flight
