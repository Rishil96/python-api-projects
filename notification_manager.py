import os
from twilio.rest import Client


class NotificationManager:

    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_from_phone = os.environ.get("TWILIO_PHONE_NUMBER")
        self.twilio_to_phone = os.environ.get("MY_PHONE_NUMBER")

    def send_notification(self, flight: dict, price_limit: float,  source: str, destination: str):
        """
        This method sends a notification to the user if any flight is available at a cheaper cost than previously
        decided
        """
        flight_price = flight.get("price", {}).get("grandTotal", 100000000)
        airline = flight.get("airline") if flight.get("airline") != "N/A" else flight.get("airlineCode")

        if flight_price <= price_limit:
            flight_details = f"""
            Low Price Alert!
            Only ₹{flight_price} to travel from {source} to {destination} via {airline}.
            Hurry up and book the tickets now!
            
            """
            print(flight_details)
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            message = client.messages.create(
                body=flight_details,
                from_=self.twilio_from_phone,
                to=self.twilio_to_phone,
            )
            print(message.status)
