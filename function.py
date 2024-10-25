from playwright.sync_api import sync_playwright
import time
import os
from utils import handle_dialog, login_and_cache, find_file

# 카드 정보 오류 확인
class PaymentVerificationError(Exception):
    pass

AUTH_FILE = "auth_state.json"  # Path to save the cached authentication state

def execute_drive(card_info):
    with sync_playwright() as p:
        # 브라우저 열기
        browser = p.chromium.launch(headless=False)

        # 캐시 파일이 존재하면 로그인
        if os.path.exists(AUTH_FILE):
            print("이전 로그인 정보로 로그인을 시도합니다.")
            context = browser.new_context(storage_state=AUTH_FILE)
        # 캐시 파일이 존재하지 않으면 수동으로 로그인
        else:
            print("이전 로그인 정보를 찾지 못했습니다. 수동으로 로그인해주세요. 20초 후에 자동화 프로그램이 시작됩니다.")
            context = browser.new_context()

        page = context.new_page()

        # 캐시로 웹사이트 접속하기
        try:
            page.goto("https://service.epost.go.kr/front.commonpostplus.RetrieveAcceptPlus.postal?gubun=1")
            # 로그인 성공했는지 확인
            member_info_visible = page.is_visible('div.memberInfo')
            if not member_info_visible:
                raise Exception("로그인이 필요합니다.")

        except Exception as e:
            print(f"로그인이 실패했습니다. 수동으로 로그인해주세요. 20초 후에 자동화 프로그램이 시작됩니다.: {str(e)}")
            login_and_cache(context, page, AUTH_FILE)

        page.goto("https://service.epost.go.kr/front.commonpostplus.RetrieveAcceptPlus.postal?gubun=1")

        # 보내는분 정보 수정 (이름 입력)
        page.fill('#tSndNm', '')
        page.fill('#tSndNm', '블랙독')

        # 배송 정보 수신 (SMS)
        page.click('#recevYn4')

        # 팝업 창 popup_info로 받아주기
        with page.expect_popup() as popup_info:
            page.click('#tSpecialDivCd4')  # '준등기' 버튼 클릭하기

        # 팝업창 핸들링 (닫기)
        popup = popup_info.value
        popup.close()

        # 우체통 접수 서비스
        # 팝업 창 popup_info로 받아주기
        with page.expect_popup() as popup_info:
            page.click("#mBoxThwrY2")

        # 팝업창 핸들링 (닫기)
        popup = popup_info.value
        popup.close()

        # 내용물 코드 '510' 선택
        page.select_option('#semiCode', '510')


        # 업로드할 주소 파일 찾기 (1개만!)
        file_to_upload = find_file()

        # 주소(파일)이용하기
        with page.expect_popup() as popup_info:
            page.click('#btnUseAddrFile')
            popup = popup_info.value
            popup.set_input_files('#uploadFile', file_to_upload)

        # 카드 번호 입력
        card1 = card_info["card1"]
        card2 = card_info["card2"]
        card3 = card_info["card3"]
        card4 = card_info["card4"]
        month = card_info["month"]
        year = card_info["year"]
        pass1 = card_info["pass1"]
        pass2 = card_info["pass2"]
        credit_birth = card_info["credit_birth"]

        # 카드 정보 입력
        credit_no_input1 = page.locator('#creditNo1')
        credit_no_input1.scroll_into_view_if_needed()
        credit_no_input1.fill(card1)

        credit_no_input1 = page.locator('#creditNo2')
        credit_no_input1.scroll_into_view_if_needed()
        credit_no_input1.fill(card2)

        credit_no_input1 = page.locator('#creditNo3')
        credit_no_input1.scroll_into_view_if_needed()
        credit_no_input1.fill(card3)

        credit_no_input1 = page.locator('#creditNo4')
        credit_no_input1.scroll_into_view_if_needed()
        credit_no_input1.fill(card4)

        creditExp1 = page.locator('#creditExp1')
        creditExp2 = page.locator('#creditExp2')
        creditExp1.fill(month)
        creditExp2.fill(year)

        creditPwd1 = page.locator('#creditPwd1')
        creditPwd2 = page.locator('#creditPwd2')
        creditPwd1.fill(pass1)
        creditPwd2.fill(pass2)

        creditBirth = page.locator('#creditBirth1')
        creditBirth.fill(credit_birth)

        # 결제카드검증
        page.wait_for_selector('#certCreditInfo')  # Wait for the button to appear
        time.sleep(1)
        page.click('#certCreditInfo')
        time.sleep(1)
        page.click('#certCreditInfo')

        error_locator1 = page.locator('li#mag4.red_b')
        error_locator2 = page.locator('li#mag5.red_b')
        error_locator3 = page.locator('li#mag6.red_b')

        if error_locator1.is_visible():
            raise PaymentVerificationError("Error: 결제카드 검증에 실패했습니다. 결제카드정보를 확인해주세요.")

        if error_locator2.is_visible():
            raise PaymentVerificationError("Error: 현재 검증서비스를 이용할 수 없습니다.")

        if error_locator3.is_visible():
            raise PaymentVerificationError("Error: 결제카드 검증에 실패했습니다. 네트워크 상태를 확인해주세요.")

        # 개인정보 수집 동의
        # 스크롤 끝까지 내리고 '동의합니다' 체크
        page.wait_for_selector('#agreeBox')  # Wait until the element is available
        page.evaluate("""() => {
            var element = document.getElementById('agreeBox');
            element.scrollIntoView();  // Scroll the box into view
            element.scrollTop = element.scrollHeight;  // Scroll inside the box to the bottom
        }""")
        page.click("#applyAgree_Priv")

        # 접수 신청
        page.on("dialog", handle_dialog)
        page.click("#btnReqClick")
        # 주소 검증 팝업 (자동 처리)

        # 다시 접수 신청
        page.click('#btnReqClick')
        page.click('#btnReqClick')
        # Wait for the notification to appear
        page.wait_for_selector('#notiContentDiv.show')

        # Wait for the close button to be visible
        confirm_button = page.wait_for_selector('a.btn_m.bg_red#confirmBtn', state='visible')

        # Click the close button
        confirm_button.click()

        if page.url == "https://service.epost.go.kr/front.commonpostplus.RetrieveRegiPostPlus.postal":
            print("간편사전접수 신청이 완료되었습니다.")

        time.sleep(50000)

        # page.close()
        # browser.close()