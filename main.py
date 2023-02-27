from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import *

data_manager = DataManager()
notification_manager = NotificationManager()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "YUL"
#

sheet_data = data_manager.get_data()


if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    print(city_names)
    codes = flight_search.get_code(city_names)
    data_manager.update_codes()
    sheet_data = data_manager.get_data()

today = datetime.now() + timedelta(1)
six_month_from_today = datetime.now() + timedelta(6 * 30)

for destination in sheet_data:
    print(destination)
    flight = flight_search.search_flight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        date_from=today,
        date_to=six_month_from_today
    )

    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.departure_date} to {flight.return_date}."
        )

