# Automated_POST

## 로그인
입력값:  
<t>  new_login?  
<t>    True:  
<t>      id:  
<t>      pw:  
<t>      새롭게 입력, 로그인, 메인페이지로 이동  
<t>    False:  
<t>      원래 로그인 정보 활용해서 로그인.  
  


## User Expereince
### 로그인
1. 로그인 기록이 있다면, 프로그램 즉시 실행
2. 로그인 기록이 없다면, 페이지 우측 상단의 로그인 버튼 클릭 -> 수동 로그인 -> 20초 후 프로그램 실행


# PyInstaller로 배포판 만들기
```
$env:PLAYWRIGHT_BROWSERS_PATH="0"
playwright install chromium
pyinstaller -F main.py
```

# TimeSleep 사용하지 말기
```aiignore
https://playwright.dev/python/docs/library
```