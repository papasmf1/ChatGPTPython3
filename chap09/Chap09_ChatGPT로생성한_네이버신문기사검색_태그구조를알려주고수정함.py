#Chap09_ChatGPT로생성한_네이버신문기사검색_태그구조를알려주고수정함.py 
import requests
from bs4 import BeautifulSoup

# 검색어에 해당하는 네이버 뉴스 검색 URL
url = 'https://search.naver.com/search.naver?query=%EB%B0%98%EB%8F%84%EC%B2%B4&where=news'

# 봇 차단 회피를 위한 헤더 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# 웹페이지 요청
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 기사 제목을 포함한 <a> 태그 찾기
title_links = soup.select('a.GUWgsNcVrWa67MoYor6N.o8ZxSqp8BlHYDNRhXpaz > span.sds-comps-text-type-headline1')

print("네이버 뉴스 기사 제목 목록:\n")
for i, title_span in enumerate(title_links, 1):
    print(f"{i}. {title_span.get_text(strip=True)}")
