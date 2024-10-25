from function import execute_drive
from utils import (
    card_isvalid,
    card_month_year,
    card_password,
    birthdate,
    load_card_info,
    save_card_info,
)

# 카드 정보 저장할 파일
CARD_INFO_FILE = "card_info.json"

if __name__ == "__main__":
    # 카드 정보 불러오기
    saved_card_info = load_card_info(CARD_INFO_FILE)
    # 만약 카드 정보가 있다면 기존 카드 정보 사용할지 확인
    if saved_card_info:
        user_choice = (
            input("저장된 카드 정보를 사용하여 진행하시겠습니까? (Y/N): ")
            .strip()
            .upper()
        )
    # 카드 정보가 없다면 카드 정보 입력
    else:
        user_choice = "N"

    # Y를 입력하면 기존 카드 정보 사용
    if user_choice == "Y":
        card_info = saved_card_info
    else:
        # N을 입력하면 새로 카드 정보 입력
        card_info = dict()
        (
            card_info["card1"],
            card_info["card2"],
            card_info["card3"],
            card_info["card4"],
        ) = card_isvalid()
        card_info["month"], card_info["year"] = card_month_year()
        card_info["pass1"], card_info["pass2"] = card_password()
        card_info["credit_birth"] = birthdate()

        # 카드 정보 json 파일로 저장
        save_card_info(CARD_INFO_FILE, card_info)

    # 자동화 스크립트 실행
    execute_drive(card_info=card_info)
