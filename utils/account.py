import re
import os
import json

ALLOW_SITE_NAME_LIST = ["ondisk", "filenori", "filekuki", "wedisk"]
DEFAULT_ACCOUNT_VALUE = "$set_plz"

ACCOUNT_FILE_PATH = os.getcwd()
ACCOUNT_FILE_PATH = re.sub(r"automation_webhard/?.*", "automation_webhard/auth/account.json", ACCOUNT_FILE_PATH)

if not os.path.exists(ACCOUNT_FILE_PATH):
    default_account_file = {site_name: {
        "id": DEFAULT_ACCOUNT_VALUE,
        "pw": DEFAULT_ACCOUNT_VALUE
    }
        for site_name in ALLOW_SITE_NAME_LIST
    }

    f = open(ACCOUNT_FILE_PATH, "w")
    json.dump(default_account_file, f)
    f.close()

result_account_data = {}
with open(ACCOUNT_FILE_PATH, "r") as ac:
    current_account_data = json.load(ac)

for site_name, account_dict in current_account_data.items():
    if site_name not in ALLOW_SITE_NAME_LIST:
        continue
    if not account_dict:
        result_account_data[site_name] = {"id": DEFAULT_ACCOUNT_VALUE,
                                          "pw": DEFAULT_ACCOUNT_VALUE}
    if not account_dict['id'] or not account_dict['pw']:
        result_account_data["id"] = DEFAULT_ACCOUNT_VALUE
        result_account_data["pw"] = DEFAULT_ACCOUNT_VALUE

    result_account_data[site_name] = account_dict

for site_name in ALLOW_SITE_NAME_LIST:
    if site_name in result_account_data.keys():
        continue
    result_account_data[site_name] = {
        "id": DEFAULT_ACCOUNT_VALUE,
        "pw": DEFAULT_ACCOUNT_VALUE
    }

if current_account_data != result_account_data:
    with open(ACCOUNT_FILE_PATH, "w") as f:
        json.dump(result_account_data, f)
