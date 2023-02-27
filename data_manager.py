import requests
import config


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.data = {}

    def get_data(self):
        response = requests.get(url=config.SHEETY_ENDPOINT, auth=(config.SHEETY_USERNAME, config.SHEETY_PASSWORD))
        data = response.json()
        self.data = data["prices"]
        return self.data

    def update_codes(self):
        for city in self.data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{config.SHEETY_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=(config.SHEETY_USERNAME, config.SHEETY_PASSWORD)
            )
            data = response.json()

    def get_emails(self):
        customers_endpoint = config.SHEETY_USERS_ENDPOINT
        response = requests.get(url=customers_endpoint, auth=(config.SHEETY_USERNAME, config.SHEETY_PASSWORD))
        self.data = response.json()["users"]
        return self.data
