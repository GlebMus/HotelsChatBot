import requests
from settings import *


class ApiUrl:
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": "moscow"}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': HEAD,
        "content-type": "application/json",
    }

    url2 = "https://hotels4.p.rapidapi.com/properties/v2/list"

    querystring2 = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {
            "regionId": "6054439"
        },
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 1
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 10,
        "sort": "PRICE_HIGH_TO_LOW"
    }

    @classmethod
    def return_results(self):
        try:
            response = requests.request("GET", self.url, headers=self.headers,
                                        params=self.querystring)
            self.querystring2["destination"]["regionId"] = f"{response.json()['sr'][0]['gaiaId']}"
            response2 = requests.post(self.url2, headers=self.headers, json=self.querystring2)
            response2result = response2.json()['data']['propertySearch']['properties']
            return response2result
        except Exception as exp:
            logger.debug(f'Ошибка в файле highpice.py!(Функция return_result) (debug) \nОшибка:\n{exp}')

