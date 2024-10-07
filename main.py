import os
import random
import datetime as dt
import smtplib

import pandas as pd

# Declare constants
EMAIL = "your-email"
PASSWORD = "your-password"

# Step 1: Load birthday csv data
birthdays = pd.read_csv("birthdays.csv")

# Step 2: Load all letter templates
letters = []

for letter_path in os.listdir("letter_templates"):
    with open(f"letter_templates/{letter_path}", "r") as file:
        letters.append(file.read())


# Step 3: Go through the list of birthdays
def send_birthday_mail(person_name: str, person_email: str) -> None:
    """
    Sends an email to the person wishing him/her a happy birthday
    """
    # Choose a template randomly and update name in it
    letter = random.choice(letters)
    letter = letter.replace("[NAME]", person_name)

    # Establish a connection to send email
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL,
                            to_addrs=person_email,
                            msg=f"Subject:Happy Birthday\n\n{letter}")
        print(f"Email sent to {person_name} successfully")


# Step 4: Go through the list of birthdays
for index, row in birthdays.iterrows():
    name = row["name"]
    to_send = row["email"]
    # Get birth month and day
    birth_month = row["month"]
    birth_day = row["day"]
    # Get today's month and day
    today_month = dt.datetime.now().month
    today_day = dt.datetime.now().day

    # Send birthday email if today is the person's birthday
    if birth_month == today_month and birth_day == today_day:
        send_birthday_mail(name, to_send)
