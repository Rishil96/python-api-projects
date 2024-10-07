import smtplib

EMAIL_ID = "your-email"
PASSWORD = "your-password"
TO_SEND = "recipient-email"

# connection = smtplib.SMTP("smtp.gmail.com")
# # Make the connection secure using Transport Layer Security
# connection.starttls()
#
# connection.login(user=EMAIL_ID, password=PASSWORD)
# connection.sendmail(from_addr=EMAIL_ID,
#                     to_addrs=TO_SEND,
#                     msg="Subject:Python Mail Test\n\nThis mail is sent for testing SMTP library in Python.")
# connection.close()

# Use context manager
with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=EMAIL_ID, password=PASSWORD)
    connection.sendmail(from_addr=EMAIL_ID,
                        to_addrs=TO_SEND,
                        msg="Subject:Python Mail Test\n\n"
                            "This mail is sent for testing SMTP library in Python.")
