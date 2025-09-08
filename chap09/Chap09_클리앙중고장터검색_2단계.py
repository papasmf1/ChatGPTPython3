from bs4 import BeautifulSoup
import urllib.request

for i in range(0,11):
    # 중고장터 게시판 URL
    url = 'https://www.clien.net/service/board/sold?&od=T31&category=0&po=' + str(i)
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
