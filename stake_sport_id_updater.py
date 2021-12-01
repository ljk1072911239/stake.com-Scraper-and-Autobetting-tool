import json
import pickle
import requests

from stake_auth import AuthClass

class SportIdUpdater:

    SPORT_DICT = {
        'table_tennis': 'table-tennis',  # Sport names to be used in API
        'football': 'soccer',
        'tennis': 'tennis'
    }

    def __init__(self):
        self.__sport_id_dict = {
            "soccer": None,
            "table-tennis": None,
            "tennis": None}

    @staticmethod
    def get_sport_id(sport):
        payload = json.dumps({"operationName": "AllSportGroups", "variables": {"sport": sport},
                              "query": "query AllSportGroups($sport: String!) {\n  slugSport(sport: $sport) "
                                       "{\n    id\n    allGroups {\n     "
                                       " name\n      translation\n      rank\n      id\n      __typename\n    }"
                                       "\n    __typename\n  }\n}\n"})

        resp = json.loads(
            requests.post(AuthClass.API_URL, headers=AuthClass.get_headers(), data=payload).text)

        return resp['data']['slugSport']['id']

    def get_all_sport_ids(self):
        for a in self.__sport_id_dict:
            self.__sport_id_dict[a] = SportIdUpdater.get_sport_id(a)

    def save_sport_ids(self):
        with open("sport_ids.pkl", "wb") as f:
            pickle.dump(self.__sport_id_dict, f)

    def cycle(self):
        self.get_all_sport_ids()
        self.save_sport_ids()
