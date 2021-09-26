import re
import os
import json

ALLOW_SITE_NAME_LIST = ["ondisk", "filenori, filekuki", "wedisk"]
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
