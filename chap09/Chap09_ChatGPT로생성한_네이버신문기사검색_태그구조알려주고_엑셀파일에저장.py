#Chap09_ChatGPT로생성한_네이버신문기사검색_태그구조를알려주고_엑셀에저장.py 
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import os

# 저장 경로 지정
save_path = r"c:\work"
file_name = "news_titles.xlsx"
full_path = os.path.join(save_path, file_name)

# URL 및 헤더 설정
url = 'https://search.naver.com/search.naver?query=%EB%B0%98%EB%8F%84%EC%B2%B4&where=news'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# 웹 페이지 요청 및 파싱
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 기사 제목 추출
title_elements = soup.select('a.GUWgsNcVrWa67MoYor6N.o8ZxSqp8BlHYDNRhXpaz > span.sds-comps-text-type-headline1')
titles = [title.get_text(strip=True) for title in title_elements]

# 엑셀 워크북 생성 및 시트 활성화
wb = Workbook()
ws = wb.active
ws.title = "뉴스기사제목"

# 헤더 작성
ws.append(["번호", "기사 제목"])

# 기사 제목들을 엑셀에 기록
for idx, title in enumerate(titles, 1):
    ws.append([idx, title])

# 디렉토리 없으면 생성
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 엑셀 파일 저장
wb.save(full_path)
print(f"✅ 엑셀 저장 완료: {full_path}")

