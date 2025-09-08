from bs4 import BeautifulSoup
import urllib.request

# 중고장터 게시판 URL
url = 'https://www.clien.net/service/board/sold'
print(url)
headers = {'User-Agent': 'Mozilla/5.0'}  # User-Agent 설정 필요

req = urllib.request.Request(url, headers=headers)
data = urllib.request.urlopen(req).read()
soup = BeautifulSoup(data, 'html.parser')

# 게시글 제목을 포함하는 태그들 찾기
list = soup.find_all('span', attrs={'data-role': 'list-title-text'})

# 제목 출력
for item in list:
    title = item.text.strip()
    print(title)


# <span class="subject_fixed" data-role="list-title-text" title="아이폰 15 프로맥스 512GB 화이트 애플케어+ 120만원">
# 		아이폰 15 프로맥스 512GB 화이트 애플케어+ 120만원
# </span>

