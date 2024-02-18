import os
from resources.accounts import Accounts

default_endpoint = os.environ["ONVO_API_ENDPOINT"]
default_api_key = os.environ["ONVO_API_KEY"]


class Onvo:
    def __init__(self, endpoint=default_endpoint, api_key=default_api_key):
        self.endpoint = endpoint
        self.api_key = api_key

        params = [endpoint, api_key]

        self.accounts = Accounts.new(*params)
        # self.teams = Teams.new(*params)
        # self.embed_users = EmbedUsers.new(*params)
        # self.datasources = Datasources.new(*params)
        # self.automations = Automations.new(*params)
        # self.dashboards = Dashboards.new(*params)
