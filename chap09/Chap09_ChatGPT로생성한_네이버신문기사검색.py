#Chap09_ChatGPT로생성한_네이버신문기사검색.py 
import requests
from bs4 import BeautifulSoup

# 검색어 URL (한글은 인코딩 필요 없음, 이미 인코딩되어 있음)
url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%B0%98%EB%8F%84%EC%B2%B4"

# User-Agent를 지정하여 봇이 아닌 것처럼 가장
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 뉴스 기사 영역의 제목 찾기 (2025년 기준 구조는 다를 수 있음)
titles = soup.select("a.news_tit")  # 뉴스 기사 제목에 해당하는 클래스

print("기사 제목 목록:")
for idx, title in enumerate(titles, 1):
    print(f"{idx}. {title.text}")
