import requests
import json
from stake_auth import AuthClass


class AutoBet:

    def __init__(self, dataframe, stake, currency, auth_object):
        self.dataframe = dataframe
        self.stake = stake
        self.currency = currency
        self.auth_object = auth_object

    def send_bet_request(self, odds, odds_id):
        # DIRTY CODE AHEAD, COPIED AND PASTED API DATA AS IS...
        payload = json.dumps({"operationName": "SportBet",
                              "variables": {"multiplier": odds, "amount": self.stake, "currency": self.currency,
                                            "outcomeIds": [odds_id], "oddsChange": "none"},
                              "query": "mutation SportBet($amount: Float!, $currency: CurrencyEnum!, $outcomeIds: "
                                       "[String!]!, $oddsChange: SportOddsChangeEnum!, $identifier: String, $multiplier:"
                                       " Float = 1) {\n  sportBet(amount: $amount, currency: $currency, outcomeIds: "
                                       "$outcomeIds, oddsChange: $oddsChange, identifier: $identifier, multiplier: "
                                       "$multiplier) {\n    id\n    amount\n    currency\n    payoutMultiplier\n    "
                                       "potentialMultiplier\n    cashoutMultiplier\n    outcomes {\n      odds\n      "
                                       "outcome {\n        ...Outcome\n        market {\n          ...BetSlip\n         "
                                       " __typename\n        }\n        __typename\n      }\n      __typename\n    }\n  "
                                       "  __typename\n  }\n}\n\nfragment Outcome on SportMarketOutcome {\n  active\n  "
                                       "id\n  odds\n  name\n  __typename\n}\n\nfragment BetSlip on SportMarket {\n  "
                                       "...MarketFragment\n  fixture {\n    id\n    status\n    slug\n    tournament "
                                       "{\n      ...TournamentTree\n      __typename\n    }\n    data {\n      "
                                       "...FixtureDataMatch\n      ...FixtureDataOutright\n      __typename\n    }\n    "
                                       "__typename\n  }\n  __typename\n}\n\nfragment MarketFragment on SportMarket {\n  "
                                       "id\n  name\n  status\n  extId\n  specifiers\n  outcomes {\n    id\n    active\n "
                                       "   name\n    odds\n    __typename\n  }\n  __typename\n}\n\nfragment "
                                       "TournamentTree on SportTournament {\n  id\n  name\n  slug\n  category "
                                       "{\n    id\n    name\n    slug\n    contentNotes {\n      id\n      createdAt\n  "
                                       "    publishAt\n      expireAt\n      linkText\n      linkUrl\n      message\n   "
                                       "   publishAt\n      __typename\n    }\n    sport {\n      id\n      name\n      "
                                       "slug\n      contentNotes {\n        id\n        createdAt\n        publishAt\n  "
                                       "      expireAt\n        linkText\n        linkUrl\n        message\n        "
                                       "publishAt\n        __typename\n      }\n      __typename\n    }\n    "
                                       "__typename\n  }\n  contentNotes {\n    id\n    createdAt\n    publishAt\n    "
                                       "expireAt\n    linkText\n    linkUrl\n    message\n    publishAt\n    "
                                       "__typename\n  }\n  __typename\n}\n\nfragment FixtureDataMatch on "
                                       "SportFixtureDataMatch {\n  startTime\n  competitors {\n    "
                                       "...Competitor\n    __typename\n  }\n  __typename\n}\n\nfragment "
                                       "Competitor on SportFixtureCompetitor {\n  name\n  extId\n  "
                                       "countryCode\n  abbreviation\n  __typename\n}\n\nfragment FixtureDataOutright on "
                                       "SportFixtureDataOutright {\n  name\n  startTime\n  endTime\n  __typename\n}\n"})

        response = requests.post(AuthClass.API_URL, headers=self.auth_object.get_headers(self.auth_object.read_token()),
                                 data=payload)

        json_resp = json.loads(response.text)

        try:
            print(json_resp)
            if json_resp['data']['sportBet']['id'] != "":
                print("Successful bet on STAKE.COM!")
                return True
            else:
                print("Bet unsuccessful on STAKE.COM!")
                return False
        except Exception as e:
            print("Bet unsuccessful on STAKE.COM!")
            print(e)
            return False


class MoneyLineBet(AutoBet):

    def __init__(self, dataframe, stake, currency, auth_object):

        super().__init__(dataframe, stake, currency, auth_object)

    def home(self, start_time, home_player, away_player):
        for data in self.dataframe.itertuples():
            if start_time == data.TIME:
                if home_player == data.HOME and away_player == data.AWAY:
                    return self.send_bet_request(data.HOME_ODDS, data.HOME_ODDS_ID)

        return False  # In case of the data was not found in the df

    def away(self, start_time, home_player, away_player):
        for data in self.dataframe.itertuples():
            if start_time == data.TIME:
                if home_player == data.HOME and away_player == data.AWAY:
                    return self.send_bet_request(data.AWAY_ODDS, data.AWAY_ODDS_ID)

        return False  # In case of the data was not found in the df
