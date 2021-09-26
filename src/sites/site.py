import json

from utils.account import ACCOUNT_FILE_PATH, DEFAULT_ACCOUNT_VALUE


class Site:
    def __init__(self, site_name):
        self.site_name = site_name
        self.load_account_info()

    def load_account_info(self):
        with open(ACCOUNT_FILE_PATH, "r") as f:
            account_info = json.load(f)
            account_id = account_info[self.site_name]['id']
            account_pw = account_info[self.site_name]['pw']

            if account_id == DEFAULT_ACCOUNT_VALUE or account_pw == DEFAULT_ACCOUNT_VALUE:
                # TODO: must need to change logging module
                raise
