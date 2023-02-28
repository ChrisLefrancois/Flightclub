from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import *

data_manager = DataManager()
notification_manager = NotificationManager()
flight_search = FlightSearch()

ORIGIN_CITY = "YUL"
#

sheet_data = data_manager.get_data()


if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    print(city_names)
    codes = flight_search.get_code(city_names)
    data_manager.update_codes()
    sheet_data = data_manager.get_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

tommorow = datetime.now() + timedelta(1)
nine_month_date = datetime.now() + timedelta(9 * 30)

for destination_code in destinations:
    flight = flight_search.search_flight(
        ORIGIN_CITY,
        destination_code,
        date_from=tommorow,
        date_to=nine_month_date
    )

    if flight is None:
        continue

    if flight.price < destinations[destination_code]["price"]:

        users = data_manager.get_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert! Only ${flight.price} to fly from " \
                  f"{flight.origin_city}-{flight.origin_airport} to " \
                  f"{flight.destination_city}-{flight.destination_airport}, from {flight.departure_date}" \
                  f" to {flight.return_date}."

        link = f"https://www.google.com/travel/flights?q=Flights%20to%20{flight.destination_airport}%20from%20{flight.origin_airport}%20on%20{flight.departure_date}%20through%20{flight.return_date}"
        notification_manager.send_emails(emails, message, link)
