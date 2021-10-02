import traceback
import argparse
from src.sites.ondisk import Ondisk
from utils.account import update_account_info, DEFAULT_ACCOUNT_VALUE
from logger import logger

sites = {
    "ondisk": Ondisk()
}


def config_argument():
    parser = argparse.ArgumentParser(description="웹하드 자동 출석기 명령행 인자")
    parser.add_argument("--site_name", help="웹하드 사이트 이름", type=str)
    parser.add_argument("--id", help="account id", default=DEFAULT_ACCOUNT_VALUE, type=str)
    parser.add_argument("--pw", help="account password", default=DEFAULT_ACCOUNT_VALUE, type=str)

    parse_arg = parser.parse_args()
    if "site_name" not in parse_arg:
        logger.error("사이트 이름이 입력되지 않았습니다.")
    if "id" not in parse_arg and "pw" not in parse_arg:
        logger.error("계정정보가 입력되지 않았습니다.")

    return parse_arg


if __name__ == '__main__':
    argument = config_argument()

    site_name = argument.site_name
    account_id = argument.id
    account_pw = argument.pw

    # 계정정보 입력
    update_account_info(site_name, account_id, account_pw)

    # 실행
    if site_name not in sites:
        logger.error(f"{site_name}의 로직이 존재하지 않습니다.")
    else:
        sites[site_name].run()

