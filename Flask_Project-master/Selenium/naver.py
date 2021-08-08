# 네이버 지도 데이터 수집하기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time

# set option 
options = webdriver.ChromeOptions()
## 사람처럼 보이게 하는 옵션들
options.add_argument('--headless')
options.add_argument("disable-gpu") # 가속 사용x
options.add_argument("lang=ko_KR") # 가짜 플러그인 탑재
driver = webdriver.Chrome('chromedriver.exe') # 드라이버 생성


# 검색할 회사목록 리스트화
df_companys = pd.read_csv('company2.csv')
list_companys = df_companys['회사명'].tolist()[0:100]



# 구버전 네이버 지도 접속
driver.get("https://v4.map.naver.com")

# 네이버 지도 업데이트 안내 메시지 끄기
driver.find_elements_by_css_selector('button.btn_close')[1].click()

# 검색창에 검색어 입력하기 // 검색창: input#search-input

result = [] 
for company in list_companys :
	try:
		time.sleep(3)
		search_box = driver.find_element_by_css_selector("input#search-input")
		search_box.clear()
		search_box.send_keys(company)
		# 검색버튼 누르기 // 검색버튼: button.spm
		search_button = driver.find_element_by_css_selector('button.spm')
		search_button.click()

		# 컨테이너(가게 정보 ) 수
		stores = driver.find_element_by_css_selector("div.lsnx").text
		result.append(stores)
		print(result)
	except :
		result.append(None)

df_result= pd.DataFrame(data = result, columns='주소명')
df_result.to_csv(path_or_buf='result.csv', encoding='cp949')

		

driver.close()