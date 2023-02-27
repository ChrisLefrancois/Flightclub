from twilio.rest import Client
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

