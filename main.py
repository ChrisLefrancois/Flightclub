from data_manager import DataManager
from flight_search import FlightSearch
from datetime import *
import requests

data_manager = DataManager()
sheet_data = data_manager.get_data()
flight_search = FlightSearch()

if sheet_data[0]['iataCode'] == "":
    for cities in sheet_data:
        cities["iataCode"] = flight_search.get_code(cities["city"])

now = datetime.now() + timedelta(days=1)
three_month = datetime.now() + timedelta(days=(3 * 30))
flight_search.search_flight("YUL", "YYZ", now, three_month, 7, 28, )

data_manager.data = sheet_data
data_manager.update_codes()

