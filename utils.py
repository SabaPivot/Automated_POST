import time
import glob

# 주소 파일 오류 확인
class NoAddressFileError(Exception):
    pass

class TooManyAddressFilesError(Exception):
    pass

def handle_dialog(dialog):
    dt = dialog.type
    alert_message = dialog.message
    print(f"{dt} message: \n{alert_message}")
    if alert_message == "결제카드를 재검증 해주시기 바랍니다.":
        exit()
    dialog.accept()
    time.sleep(1)


def login_and_cache(context, file):
    """
    Logs in manually and saves the authenticated session state to a file.
    """
    # 수동 로그인 20초
    time.sleep(20)
    # 20초 후 로그인 캐시 저장
    context.storage_state(path=file)
    print("Login state saved to cache.")


def find_file():
    xls_files = glob.glob("*.xls") + glob.glob("*.xlsx")
    if not xls_files:
        print("No .xls or .xlsx files found.")
        raise NoAddressFileError("No .xls or .xlsx files found.")

    if len(xls_files) > 1:
        print("More than 1 address file found.")
        raise TooManyAddressFilesError("More than two .xls or .xlsx files found.")

    file_to_upload = xls_files[0]
    return file_to_upload