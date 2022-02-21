import json
import requests
import pandas as pd

from stake_auth import AuthClass
from stake_postgresql import set_table, get_table


class SportIdUpdater:
    """
        Bookmakers can create dynamically changing sport IDs in order to make scraping harder
        This script has been created to make sure the sport IDs are always up to date!
    """

    SPORT_DICT = {
        'table_tennis': 'table-tennis',  # Sport names to be used in API | Created for myself because of pref.
        'football': 'soccer',
        'tennis': 'tennis',
        'basketball': 'basketball',
    }

    SPORT_ID_TABLE = "sport_ids"



    def __init__(self):
        self.__sport_id_dict = {
            "soccer": None,
            "table-tennis": None,
            "tennis": None,
            "basketball": None}

        self.sport_id_dataframe = pd.DataFrame()

    @staticmethod
    def get_sport_id(sport):
        """ Return the ID of the given sport """

        payload = json.dumps({"operationName": "AllSportGroups", "variables": {"sport": sport},
                              "query": "query AllSportGroups($sport: String!) {\n  slugSport(sport: $sport) "
                                       "{\n    id\n    allGroups {\n     "
                                       " name\n      translation\n      rank\n      id\n      __typename\n    }"
                                       "\n    __typename\n  }\n}\n"})

        resp = json.loads(
            requests.post(AuthClass.API_URL, headers=AuthClass.get_headers(), data=payload).text)

        return resp['data']['slugSport']['id']

    @staticmethod
    def get_sport_id_table():
        """ Return the sport IDs dataframe from the database """
        return get_table(f"public.{SportIdUpdater.SPORT_ID_TABLE}")


    def get_all_sport_ids(self):
        """ Iterate through sports and save their IDs """

        for a in self.__sport_id_dict:
            self.__sport_id_dict[a] = SportIdUpdater.get_sport_id(a)

    def build_dataframe(self):
        """ Build the sport ID dataframe, it will be uploaded to PostgreSQL! """
        data = {
            "SPORT": [s for s in SportIdUpdater.SPORT_DICT],
            "SPORT_API": [SportIdUpdater.SPORT_DICT[s] for s in SportIdUpdater.SPORT_DICT],
            "SPORT_ID": [self.__sport_id_dict[SportIdUpdater.SPORT_DICT[s]] for s in SportIdUpdater.SPORT_DICT]
        }

        return pd.DataFrame(data=data)

    def cycle(self):
        """ Helper function to do the full ETL process! """
        self.get_all_sport_ids()
        sport_id_df = self.build_dataframe()
        set_table(sport_id_df, SportIdUpdater.SPORT_ID_TABLE)


sport_ids = SportIdUpdater()
sport_ids.cycle()