import requests
import json


class Resource:
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    def handle_response(self, response):
        try:
            return json.loads(response.body)
        except ValueError:
            return response.body

    def get_url(self, subdirectory):
        return "{base_url}{subdirectory}".format(
            base_url=self.endpoint, subdirectory=subdirectory
        )

    def get(self, subdirectory):
        url = self.get_url(subdirectory)
        response = requests.get(url)
        return self.handle_response(response)
