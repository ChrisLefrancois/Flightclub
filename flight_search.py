from flight_data import FlightData
import requests
import config


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_code(self, city_search):
        headers = {"apikey": config.KIWI_API_KEY}
        params = {"term": city_search, "location_types": "city"}

        response = requests.get(url=f"{config.KIWI_API_ENDPOINT}/locations/query",  params=params, headers=headers)
        flight_data = response.json()["locations"][0]["code"]
        return flight_data

    def search_flight(self, fly_from_code, fly_to_code, date_from, date_to):
        headers = {"apikey": config.KIWI_API_KEY}

        params = {
            "fly_from": fly_from_code,
            "fly_to": fly_to_code,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 3,
            "curr": "cad"
        }

        response = requests.get(url=f'{config.KIWI_API_ENDPOINT}/v2/search', headers=headers, params=params)
        print(response.status_code)
        try:
            print(response.json())
            data = response.json()['data'][0]
        except IndexError:
            print("No flight found")
            return None
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["cityTo"],
                destination_airport=data["flyTo"],
                departure_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            return flight_data



