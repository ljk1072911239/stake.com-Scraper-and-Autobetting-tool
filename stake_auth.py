import json
import requests
import pickle

import stake_anti_captcha


class AuthClass:
    API_URL = "https://api.stake.com/graphql"

    def __init__(self, username, password, anti_cpt_api_key):
        self.__username = username
        self.__password = password
        self.__recaptcha_code = ""
        self.__login_token = ""
        self.__final_token = ""
        self.__driver = None
        self.__captcha_object = stake_anti_captcha.AntiCaptcha(anti_cpt_api_key)
        self.__captcha_code = ""

    @staticmethod
    def get_headers(auth_token: str = "") -> dict:
        headers = {
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'accept': '*/*',
            'x-language': 'en',
            'x-lockdown-token': '',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          '/92.0.4515.159 Safari/537.36',
            'content-type': 'application/json',
            'Origin': 'https://stake.com',
            'Referer': 'https://stake.com/'}

        if auth_token:
            headers['x-access-token'] = auth_token

        return headers

    def solve_captcha(self):
        self.__captcha_code = self.__captcha_object.cycle()

    def read_token(self) -> str:
        # FROM EXTERNAL FILE!
        try:
            with open(f"{self.__username}_token.pkl", "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print("Error while trying to load 'token.pkl'")
            print(e)
            return ""

    def save_token(self):
        # FROM EXTERNAL FILE!
        try:
            with open(f"{self.__username}_token.pkl", "wb") as f:
                pickle.dump(self.__final_token, f)
        except Exception as e:
            print("Error while saving 'token.pkl'")
            print(e)

    def request_login_user(self):  # login phase #1
        payload = json.dumps({
            "operationName": "RequestLoginUser",
            "variables": {
                "name": self.__username,
                "password": self.__password,
                "captcha": self.__captcha_code,
            },
            "query": "mutation RequestLoginUser($name: String, $email: String, $password: String!, "
                     "$captcha: String) {\n  requestLoginUser(name: $name, email: $email, password: "
                     "$password, captcha: $captcha) {\n    loginToken\n    hasTfaEnabled\n    "
                     "requiresLoginCode\n    user {\n      id\n      name\n      __typename\n    }\n"
                     "    __typename\n  }\n}\n"
        })

        resp = json.loads(
            requests.post(AuthClass.API_URL, headers=AuthClass.get_headers(), data=payload).text)
        self.__login_token = resp['data']['requestLoginUser']['loginToken']

    def complete_login_user(self):  # login phase 2
        # This is only optimized for single logins, not for 2FA or email code verifications...
        # If your account has 2FA it will throw an error
        # You need to add other functions for getting external data from emails/2FA...
        # You also need to modify the payload
        # Email logincode payload:
        # variables-> loginCode: "logincode_received_in_email"

        payload = json.dumps({
            "operationName": "CompleteLoginUser",
            "variables": {
                "loginToken": self.__login_token,
                "sessionName": "Chrome (Unknown)",
                "blackbox": "blackbox"
            },
            "query": "mutation CompleteLoginUser($loginToken: String, $tfaToken: String, $sessionName: String!, "
                     "$blackbox: String, $loginCode: String) {\n  completeLoginUser(loginToken: $loginToken, "
                     "tfaToken: $tfaToken, sessionName: $sessionName, blackbox: $blackbox, loginCode: $loginCode) "
                     "{\n    ...UserAuthenticatedSession\n    __typename\n  }\n}\n\nfragment UserAuthenticatedSession "
                     "on UserAuthenticatedSession {\n  token\n  session {\n    ...UserSession\n    "
                     "user {\n      ...UserAuth\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
                     "\n\nfragment UserSession on UserSession {\n  id\n  sessionName\n  ip\n  "
                     "country\n  city\n  active\n  updatedAt\n  __typename\n}\n\nfragment UserAuth on "
                     "User {\n  id\n  name\n  email\n  hasPhoneNumberVerified\n  hasEmailVerified\n  "
                     "hasPassword\n  intercomHash\n  createdAt\n  hasTfaEnabled\n  mixpanelId\n  "
                     "hasOauth\n  isKycBasicRequired\n  isKycExtendedRequired\n  isKycFullRequired\n  "
                     "kycBasic {\n    id\n    status\n    __typename\n  }\n  kycExtended {\n    id\n    "
                     "status\n    __typename\n  }\n  kycFull {\n    id\n    status\n    __typename\n  }\n  "
                     "flags {\n    flag\n    __typename\n  }\n  roles {\n    name\n    __typename\n  }\n  "
                     "balances {\n    ...UserBalanceFragment\n    __typename\n  }\n  activeClientSeed {\n    id\n    "
                     "seed\n    __typename\n  }\n  previousServerSeed {\n    id\n    seed\n    __typename\n  }\n  "
                     "activeServerSeed {\n    id\n    seedHash\n    nextSeedHash\n    nonce\n    blocked\n    "
                     "__typename\n  }\n  __typename\n}\n\nfragment UserBalanceFragment on UserBalance {\n "
                     " available {\n    amount\n    currency\n    __typename\n  }\n  vault {\n    amount\n    "
                     "currency\n    __typename\n  }\n  __typename\n}\n"
        })

        resp = json.loads(
            requests.post(AuthClass.API_URL, headers=AuthClass.get_headers(), data=payload).text)
        self.__final_token = resp['data']['completeLoginUser']['token']

    def login_check(self) -> bool:
        if not self.read_token():
            print("Not logged in to Stake.com!")
            return False

        payload = json.dumps({"operationName": "UserVaultBalances", "variables": {},
                              "query": "query UserVaultBalances {\n  user {\n    id\n    "
                                       "balances {\n      available {\n        amount\n     "
                                       "   currency\n        __typename\n      }\n      "
                                       "vault {\n        amount\n        currency\n        __"
                                       "typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"})

        try:
            response = json.loads(
                requests.post(AuthClass.API_URL, headers=AuthClass.get_headers(self.read_token()), data=payload).text)
            if response['data']['user']['id']:
                print(f"Logged in as {self.__username} to stake.com!")
                return True
            else:
                print("Not logged in!")
                return False
        except Exception as e:
            # If the request fails, we just simply return False
            print("Not logged in!")
            print(e)
            return False

    def cycle(self):
        # Intended to use as a constant loop
        if self.login_check():
            return True
        else:
            self.solve_captcha()
            self.request_login_user()
            self.complete_login_user()
            self.save_token()
