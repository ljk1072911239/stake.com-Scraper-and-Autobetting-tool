import json
import time
import requests


class AntiCaptcha:
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    CREATE_TASK_URL = "https://api.anti-captcha.com/createTask"
    GET_TASK_RESULT_URL = "https://api.anti-captcha.com/getTaskResult"

    STAKE_LOGIN_URL = "https://stake.com/?action=login&modal=auth"
    STAKE_SITE_KEY = "7830874c-13ad-4cfe-98d7-e8b019dc1742"  # SHOULD BE DYNAMIC...

    def __init__(self, api_key):
        self.__api_key = api_key

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key):
        self.__api_key = api_key

    def post_request(self, json_payload):
        # Custom post request method for AntiCaptcha
        try:
            return json.loads(
                requests.post(AntiCaptcha.CREATE_TASK_URL, headers=AntiCaptcha.HEADERS, data=json_payload).text)
        except Exception as e:
            print("Error while sending request to the AntiCaptcha API!")
            print(e)

    def create_task(self):
        # Creates the task returns the task id for checking...
        payload = json.dumps({
            "clientKey": self.__api_key,
            "task":
                {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": AntiCaptcha.STAKE_LOGIN_URL,
                    "websiteKey": AntiCaptcha.STAKE_SITE_KEY
                }
        })

        resp = requests.post(AntiCaptcha.CREATE_TASK_URL, headers=AntiCaptcha.HEADERS, data=payload)
        return json.loads(resp.text)['taskId']

    def get_task_result(self, taskid):
        payload = json.dumps({"clientKey": self.__api_key,
                              "taskId": str(taskid)})

        resp = requests.post(AntiCaptcha.GET_TASK_RESULT_URL, headers=AntiCaptcha.HEADERS, data=payload)
        return json.loads(resp.text)

    def wait_for_captcha_response(self, taskid, wait_seconds=240):

        now = time.time()
        while time.time() - now <= wait_seconds:
            time.sleep(0.1)
            try:
                result = self.get_task_result(taskid)
                if result['status'] == "processing":
                    print("The captcha is still being processed...")
                    print("Waiting for 3 seconds before checking again...")
                    time.sleep(3)
                elif result['status'] == "ready":
                    if result['errorId'] == 0:
                        print("Captcha has been processed, returning the response!")
                        return result['solution']['gRecaptchaResponse']
                    else:
                        return False
            except Exception as e:
                print("Exception while waiting for captcha response!")
                print(e)
                print("Trying again to get task result in 3 seconds...")
                time.sleep(3)
        return False

    def cycle(self):
        # Aggregator function to get the solved captcha code required for login...
        task_id = self.create_task()
        # print(task_id)
        return self.wait_for_captcha_response(task_id)