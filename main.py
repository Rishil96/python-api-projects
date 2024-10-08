# ISS Overhead Tracker
import requests
from datetime import datetime
import smtplib
import time

# Constants
# Latitude and Longitude of current location
LATITUDE = 19.104521
LONGITUDE = 72.921860
# Email details
EMAIL = "your-email"
PASSWORD = "your-password"


# Check if ISS is close to our location
def is_iss_overhead() -> bool:
    """
    Returns true if ISS is near our current latitude and longitude
    """
    # Get ISS API response
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    iss_data = iss_response.json()
    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    print(f"ISS Current Location: ({iss_latitude}, {iss_longitude})")

    return LATITUDE - 5 <= iss_latitude <= LATITUDE + 5 and LONGITUDE - 5 <= iss_longitude <= LONGITUDE + 5


# Check if its night time
def is_night() -> bool:
    # Get today's sunrise and sunset timings to spot ISS during night
    parameters = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0
    }

    sun_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()

    sun_data = sun_response.json()
    print(sun_data)

    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

    print(f"Sunrise Hour: {sunrise}")
    print(f"Sunset Hour: {sunset}")

    time_now = datetime.now().hour

    return time_now >= sunset or time_now <= sunrise


while True:

    print("Running ISS Script...")
    # Send email if it's nighttime and ISS is overhead
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=EMAIL,
                                msg="Subject:Look up\n\nThe ISS is above you in the sky!")
    time.sleep(60)
