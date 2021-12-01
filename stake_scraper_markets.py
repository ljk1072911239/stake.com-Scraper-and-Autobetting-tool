import pandas as pd
from stake_scraper import DataParser

class MoneyLine(DataParser):
    def __init__(self, sport, live):
        super().__init__(sport, live)
        self.__start_time = []
        self.__home_team = []
        self.__away_team = []
        self.__home_odds = []
        self.__away_odds = []
        self.__home_odds_ID = []
        self.__away_odds_ID = []
        self.__match_list = []

    def cleaner(self):
        self.__start_time.clear()
        self.__home_team.clear()
        self.__away_team.clear()
        self.__home_odds.clear()
        self.__away_odds.clear()
        self.__home_odds_ID.clear()
        self.__away_odds_ID.clear()
        self.__match_list.clear()
        self.dataframe = pd.DataFrame()

    def parse_data(self):

        fixture_list = self.get_fixture_list()

        for match in fixture_list:
            start_time = match['data']['startTime'][5:-4]  # Sat, 21 Aug 2021 15:00:00 GMT
            for market_groups in match['groups']:
                if market_groups['name'] == 'winner':  # The market of ML!
                    for templates in market_groups['templates']:
                        for markets in templates['markets']:
                            if markets['name'] == 'Winner':
                                if markets['status'] == 'active':

                                    try:
                                        home_player = markets['outcomes'][0]['name']
                                        home_odds = float(markets['outcomes'][0]['odds'])
                                        away_player = markets['outcomes'][1]['name']
                                        away_odds = float(markets['outcomes'][1]['odds'])
                                        home_odds_id = markets['outcomes'][0]['id']
                                        away_odds_id = markets['outcomes'][1]['id']

                                        self.__start_time.append(start_time)
                                        self.__home_team.append(home_player)
                                        self.__away_team.append(away_player)
                                        self.__home_odds.append(home_odds)
                                        self.__away_odds.append(away_odds)
                                        self.__home_odds_ID.append(home_odds_id)
                                        self.__away_odds_ID.append(away_odds_id)
                                    except Exception as e:
                                        print("Error while parsing! Skipping...")
                                        print(e)
                                        pass

    def build_dataframe(self):
        data = {
            "TIME": self.__start_time,
            "HOME": self.__home_team,
            "AWAY": self.__away_team,
            "HOME_ODDS": self.__home_odds,
            "AWAY_ODDS": self.__away_odds,
            "HOME_ODDS_ID": self.__home_odds_ID,
            "AWAY_ODDS_ID": self.__away_odds_ID,
        }

        self.dataframe = pd.DataFrame(data=data)

        self.dataframe = self.dataframe[
            (self.dataframe["HOME_ODDS"] > 1.00) & (self.dataframe["AWAY_ODDS"] > 1.00)]

        self.dataframe = self.dataframe.sort_values(by=["TIME"], ignore_index=True)

    def cycle(self):
        self.cleaner()
        self.parse_data()
        self.build_dataframe()
