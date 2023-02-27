from twilio.rest import Client
import smtplib
import config

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self,):
        self.client = Client(config.TWILIO_SID, config.TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=config.TWILIO_VIRTUAL_NUMBER,
            to=config.TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=config.MY_EMAIL, password=config.MY_EMAIL_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=config.MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )

