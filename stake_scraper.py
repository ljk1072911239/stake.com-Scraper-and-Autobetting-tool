import json
import requests
import pickle
import pandas as pd
from abc import ABC, abstractmethod

from stake_auth import AuthClass
from stake_postgresql import get_table, set_table


class EventFiles(ABC):

    # Class for grouping event file related functions and variables

    def __init__(self, sport, live):
        self.sport = sport
        self.live = live

        if self.live:
            self.__event_file_name = sport + "_event_live.pkl"
        else:
            self.__event_file_name = sport + "_event.pkl"

        self.dataframe = pd.DataFrame()
        self.match_events = {}  # Must be used by EventScraper for storing event data

    def save_event_file(self):
        with open(self.__event_file_name, "wb") as f:
            pickle.dump(self.match_events, f)

    def get_event_file(self):
        with open(self.__event_file_name, "rb") as f:
            return pickle.load(f)


class EventScraper(EventFiles):

    def __init__(self, sport, live):
        super().__init__(sport, live)
        self.__actual_sport_id = self.__get_sport_id()

    def __get_sport_id(self):
        """ Reads the sport_id from the database and returns it!"""

        sport_id_dataframe = get_table("sport_ids")

        sport_id = sport_id_dataframe[sport_id_dataframe["SPORT"] == self.sport].iloc[0].SPORT_ID

        return sport_id

    def get_event_payload(self):

        # API QUERY REPLICATED AS IS, DIRTY CODE AHEAD....

        if self.live:
            payload = json.dumps({"operationName": "liveSportFixtureList", "variables":
                {"tournamentLimit": 50, "sportId": self.__actual_sport_id, "groups": "winner"},
                                  "query":
                                      "query liveSportFixtureList"
                                      "($sportId: String!, $groups: String!, $tournamentLimit: Int = 25) "
                                      "{\n  sport(sportId: $sportId) {\n    id\n    tournamentList(type: live, "
                                      "limit: $tournamentLimit) {\n      ...TournamentTreeFragment\n      "
                                      "fixtureList(type: live) {\n        ...FixturePreviewFragment\n        "
                                      "groups(groups: [$groups], status: [active, suspended, deactivated]) "
                                      "{\n          "
                                      "...GroupFixtureFragment\n          __typename\n        }\n        "
                                      "__typename\n   "
                                      "   }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment "
                                      "GroupFixtureFragment on SportGroup {\n  ...Group\n  templates {\n    "
                                      "...TemplateFragment\n    markets {\n      ...MarketFragment\n      "
                                      "__typename\n    }\n    __typename\n  }\n  "
                                      "__typename\n}\n\nfragment MarketFragment on "
                                      "SportMarket {\n  id\n  name\n  status\n  "
                                      "extId\n  specifiers\n  outcomes {\n    "
                                      "id\n    active\n    name\n    odds\n    "
                                      "__typename\n  }\n  __typename\n}\n\nfragment "
                                      "TemplateFragment on SportGroupTemplate {\n  "
                                      "extId\n  rank\n  __typename\n}\n\nfragment "
                                      "Group on SportGroup {\n  name\n  "
                                      "translation\n  rank\n  "
                                      "__typename\n}\n\nfragment "
                                      "FixturePreviewFragment "
                                      "on SportFixture {\n  id\n  extId\n  status\n  slug\n  "
                                      "marketCount(status: [active, suspended])\n  data "
                                      "{\n    ...FixtureDataMatchFragment\n    "
                                      "...FixtureDataOutrightFragment\n    __typename\n  }"
                                      "\n  eventStatus {\n    ...FixtureEventStatus\n    "
                                      "__typename\n  }\n  tournament {\n    "
                                      "...TournamentTreeFragment\n    "
                                      "__typename\n  }\n  ...LiveStreamExistsFragment\n  __typename\n}\n\nfragment "
                                      "FixtureDataMatchFragment on SportFixtureDataMatch {\n  startTime\n  competitors "
                                      "{\n    ...CompetitorFragment\n    __typename\n  }\n  __typename\n}\n\nfragment "
                                      "CompetitorFragment on SportFixtureCompetitor {\n  name\n  extId\n  "
                                      "countryCode\n  abbreviation\n  __typename\n}\n\nfragment "
                                      "FixtureDataOutrightFragment on SportFixtureDataOutright "
                                      "{\n  name\n  startTime\n  endTime\n  "
                                      "__typename\n}\n\nfragment FixtureEventStatus on SportFixtureEventStatus "
                                      "{\n  homeScore\n  awayScore\n  matchStatus\n  clock {\n    "
                                      "matchTime\n    remainingTime\n    __typename\n  }\n  periodScores "
                                      "{\n    homeScore\n    awayScore\n    matchStatus\n    __typename\n  }"
                                      "\n  currentServer {\n    extId\n    __typename\n  }\n  "
                                      "homeGameScore\n  awayGameScore\n  statistic {\n    "
                                      "yellowCards {\n      away\n      home\n      "
                                      "__typename\n    }\n    redCards {\n      away\n      "
                                      "home\n      __typename\n    }\n    corners {\n      "
                                      "home\n      away\n      __typename\n    }\n    "
                                      "__typename\n  }\n  __typename\n}\n\nfragment "
                                      "TournamentTreeFragment on SportTournament "
                                      "{\n  id\n  name\n  slug\n  category "
                                      "{\n    id\n    name\n    "
                                      "slug\n    sport {\n      id\n      name\n      slug\n      __typename\n    }"
                                      "\n    __typename\n  }\n  __typename\n}\n\nfragment LiveStreamExistsFragment on "
                                      "SportFixture {\n  abiosStream {\n    exists\n    __typename\n  }\n  "
                                      "betradarStream {\n    exists\n    __typename\n  }\n  diceStream {\n    "
                                      "exists\n    __typename\n  }\n  __typename\n}\n"})
        else:
            payload = json.dumps({"operationName": "SportFixtureList",
                                  "variables": {"type": "upcoming", "sportId": self.__actual_sport_id,
                                                "groups": "winner", "limit": 50, "offset": 0},
                                  "query": "query SportFixtureList($type: SportSearchEnum!, $sportId: String!, "
                                           "$groups: String!, $limit: Int!, $offset: Int!) {\n  sport(sportId: "
                                           "$sportId) {\n    id\n    name\n    fixtureCount(type: $type)\n    "
                                           "fixtureList(type: $type, limit: $limit, offset: $offset) {\n      "
                                           "...FixturePreview\n      groups(groups: [$groups], status: [active, "
                                           "suspended, deactivated]) {\n        ...GroupFixture\n        "
                                           "__typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\n"
                                           "fragment FixturePreview on SportFixture {\n  id\n  status\n  slug\n  "
                                           "betradarStream {\n    exists\n    __typename\n  }\n  marketCount(status: "
                                           "[active, suspended])\n  data {\n    ...FixtureDataMatch\n    "
                                           "...FixtureDataOutright\n    __typename\n  }\n  tournament {\n    "
                                           "...TournamentTree\n    __typename\n  }\n  eventStatus {\n    "
                                           "...FixtureEventStatus\n    __typename\n  }\n  __typename\n}\n\nfragment "
                                           "FixtureDataMatch on SportFixtureDataMatch {\n  startTime\n  "
                                           "competitors {\n    ...Competitor\n    __typename\n  }\n  "
                                           "__typename\n}\n\nfragment Competitor on "
                                           "SportFixtureCompetitor {\n  name\n  extId\n  countryCode\n  "
                                           "abbreviation\n  __typename\n}\n\nfragment FixtureDataOutright "
                                           "on SportFixtureDataOutright {\n  name\n  startTime\n  endTime\n  "
                                           "__typename\n}\n\nfragment TournamentTree on SportTournament "
                                           "{\n  id\n  name\n  slug\n  category {\n    id\n    name\n    "
                                           "slug\n    contentNotes {\n      id\n      createdAt\n      "
                                           "publishAt\n      expireAt\n      linkText\n      linkUrl\n      "
                                           "message\n      publishAt\n      __typename\n    }\n    "
                                           "sport {\n      id\n      name\n      slug\n      "
                                           "contentNotes {\n        id\n        createdAt\n        "
                                           "publishAt\n        expireAt\n        linkText\n        "
                                           "linkUrl\n        message\n        publishAt"
                                           "\n        __typename\n      }\n  "
                                           "    __typename\n    }\n    __typename\n  }\n  contentNotes {\n    id\n    "
                                           "createdAt\n    publishAt\n    expireAt\n    linkText\n    linkUrl\n    "
                                           "message\n    publishAt\n    __typename\n  }\n  __typename\n}\n\nfragment "
                                           "FixtureEventStatus on SportFixtureEventStatus {\n  homeScore\n  "
                                           "awayScore\n  matchStatus\n  clock {\n    matchTime\n    "
                                           "remainingTime\n    __typename\n  }\n  periodScores {\n    "
                                           "homeScore\n    awayScore\n    matchStatus\n    __typename\n  }\n  "
                                           "currentServer {\n    extId\n    __typename\n  }\n  homeGameScore\n  "
                                           "awayGameScore\n  statistic {\n    yellowCards {\n      away\n      "
                                           "home\n      __typename\n    }\n    redCards {\n      away\n      "
                                           "home\n      __typename\n    }\n    corners {\n      home\n      "
                                           "away\n      __typename\n    }\n    __typename\n  }\n  "
                                           "__typename\n}\n\nfragment GroupFixture on SportGroup {\n  ..."
                                           "Group\n  templates {\n    ...Template\n    markets {\n      "
                                           "...MarketFragment\n      __typename\n    }\n    __typename\n  }\n  "
                                           "__typename\n}\n\nfragment Group on SportGroup {\n  name\n  "
                                           "translation\n  rank\n  __typename\n}\n\nfragment Template on "
                                           "SportGroupTemplate {\n  extId\n  rank\n  __typename\n}\n\nfragment "
                                           "MarketFragment on SportMarket {\n  id\n  name\n  status\n  extId\n  "
                                           "specifiers\n  outcomes {\n    id\n    active\n    name\n    odds\n   "
                                           " __typename\n  }\n  __typename\n}\n"})
        return payload

    def scrape_events(self):
        resp = requests.post(AuthClass.API_URL, headers=AuthClass.get_headers(), data=self.get_event_payload(),
                             timeout=5)

        self.match_events = json.loads(resp.text)

    def cycle(self):
        """ Helper function for the extract process! """
        self.scrape_events()
        self.save_event_file()


class DataParser(EventFiles):

    def __init__(self, sport, live):
        super().__init__(sport, live)

        self.start_time = []  # List of scraped start times...
        self.home_team = []  # List of home players...
        self.away_team = []  # List of away players...

        self.table_name = ""  # Table name for the database. Must be filled in every subclass!

    def get_fixture_list(self):

        # Both live and pre parsing are based on fixture lists..
        # So it could be wise to extract the relevant fixture list and return it to avoid code duplication
        # The get_event_file returns the data from the external file!

        fixture_list = []
        match_data = self.get_event_file()
        if self.live:
            for tournament in match_data['data']['sport']['tournamentList']:
                for match in tournament['fixtureList']:
                    fixture_list.append(match)
        else:
            for match in match_data['data']['sport']['fixtureList']:
                fixture_list.append(match)

        return fixture_list

    def cleaner_base(self):
        # This function is to clean all common data lists
        self.start_time.clear()
        self.home_team.clear()
        self.away_team.clear()
        self.dataframe = pd.DataFrame()

    @abstractmethod
    def cleaner_individual(self):
        # This function is to scrape individual markets!
        # like self.market or etc...
        pass

    def cleaner(self):
        self.cleaner_base()
        self.cleaner_individual()

    @abstractmethod
    def parse_data(self):
        """ This function is to parse raw data from the fixture list! """
        pass

    @abstractmethod
    def build_dataframe(self):
        """ This function is to build the DataFrame which has the event and odds data """
        pass

    def load_dataframe(self):
        """ Upload the dataframe to the database! """

        set_table(self.dataframe, self.table_name)

    def cycle(self):
        """ Helper function to do the full ETL process """

        self.cleaner()
        self.parse_data()
        self.build_dataframe()
        self.load_dataframe()
