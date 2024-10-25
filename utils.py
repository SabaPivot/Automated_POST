import time
import glob
import os
import json

# 주소 파일 오류 확인
class NoAddressFileError(Exception):
    pass

class TooManyAddressFilesError(Exception):
    pass

def handle_dialog(dialog):
    dt = dialog.type
    alert_message = dialog.message
    if alert_message == "결제카드를 재검증 해주시기 바랍니다.":
        pass
    else:
        print(f"{dt} message: \n{alert_message}")
    dialog.accept()
    time.sleep(1)


def login_and_cache(context, page, file):
    """
    Logs in manually and saves the authenticated session state to a file.
    """
    page.click("#loginSURL")
    # 수동 로그인 20초
    time.sleep(20)
    # 20초 후 로그인 캐시 저장
    context.storage_state(path=file)
    print("로그인 정보가 저장되었습니다.")


def find_file():
    xls_files = glob.glob("*.xls") + glob.glob("*.xlsx")
    if not xls_files:
        print(".xls 또는 .xlsx 형식의 파일을 찾지 못했습니다.")
        time.sleep(99999)

    if len(xls_files) > 1:
        print(".xls 또는 .xlsx 파일이 하나 이상 존재합니다.")
        time.sleep(99999)

    file_to_upload = xls_files[0]
    return file_to_upload

def card_isvalid():
    card_number = input("카드 번호를 입력하세요: ").strip()
    if len(card_number) != 16:
        print("입력하신 카드 번호가 16자리가 아닙니다. \n")
        return card_isvalid()
    else:
        return card_number[:4], card_number[4:8], card_number[8:12], card_number[12:16]


def card_month_year():
    card_month = input("카드 유효 기간을 입력하세요 ex) 08/27: ").strip()
    if len(card_month) != 5:
        print("카드 유효 기간을 잘못 입력하였습니다. 다시 입력해주세요. \n")
        return card_month_year()
    else:
        month, year = card_month.split("/")
        return month, year

def card_password():
    pwd = input("카드 비밀번호 앞 두 자리를 입력하세요: ").strip()
    if len(pwd) != 2:
        print("카드 비밀번호 앞 두 자리를 잘못 입력하였습니다. 다시 입력해주세요. \n")
        return card_password()
    else:
        return pwd[0], pwd[1]

def birthdate():
    bd = input("카드 소유자 생년월일을 입력하세요 ex) 890403: ")
    if len(bd) != 6:
        print("카드 소유자 생년월일을 잘못 입력하였습니다. 다시 입력해주세요. \n")
        return birthdate()
    else:
        return bd


def load_card_info(card_info_file):
    """Load card information from a JSON file."""
    if os.path.exists(card_info_file):
        with open(card_info_file, 'r') as file:
            saved_card = json.load(file)
        print("현재 사용 중인 카드 정보: ")
        keys = ['card1', 'card2', 'card3', 'card4']
        card_number, expire_date = "", ""
        for key in keys:
            card_number += saved_card[key]
        expire_date = f"{saved_card['month']}/{saved_card['year']}"
        print(f"저장된 카드 번호: {card_number}")
        print(f"저장된 카드 유효기간: {expire_date}")
        return saved_card
    else:
        return None


def save_card_info(card_info_file, card_info):
    """Save card information to a JSON file."""
    with open(card_info_file, 'w') as file:
        json.dump(card_info, file)
