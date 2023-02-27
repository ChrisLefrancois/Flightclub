from data_manager import DataManager

data_manager = DataManager()
sheet_data = data_manager.get_data()

if sheet_data[0]['iataCode'] == "":
    from flight_search import FlightSearch
    flight_search = FlightSearch()
    for cities in sheet_data:
        cities["iataCode"] = flight_search.get_code()


data_manager.update_codes()
