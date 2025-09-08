import requests
from bs4 import BeautifulSoup

def debug_kospi200_page():
    """
    네이버 금융 코스피200 페이지의 구조를 분석하는 함수
    """
    url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("네이버 금융에서 코스피200 정보를 가져오는 중...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'euc-kr'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("=== 페이지 구조 분석 ===")
        
        # 1. h4 태그들 찾기
        h4_tags = soup.find_all('h4')
        print(f"\n1. h4 태그 개수: {len(h4_tags)}")
        for i, h4 in enumerate(h4_tags):
            print(f"   h4 {i+1}: {h4.get_text(strip=True)}")
            print(f"   클래스: {h4.get('class', [])}")
        
        # 2. box_type_m 클래스를 가진 div들 찾기
        box_divs = soup.find_all('div', class_='box_type_m')
        print(f"\n2. box_type_m 클래스 div 개수: {len(box_divs)}")
        for i, div in enumerate(box_divs):
            h4_in_div = div.find('h4')
            if h4_in_div:
                print(f"   div {i+1}의 h4: {h4_in_div.get_text(strip=True)}")
        
        # 3. type_1 클래스를 가진 테이블들 찾기
        type1_tables = soup.find_all('table', class_='type_1')
        print(f"\n3. type_1 클래스 테이블 개수: {len(type1_tables)}")
        
        # 4. 편입종목 관련 텍스트가 포함된 요소들 찾기
        print("\n4. '편입종목' 텍스트가 포함된 요소들:")
        elements_with_text = soup.find_all(text=lambda text: text and '편입종목' in text)
        for i, element in enumerate(elements_with_text):
            print(f"   요소 {i+1}: {element.strip()}")
            parent = element.parent
            if parent:
                print(f"   부모 태그: {parent.name}, 클래스: {parent.get('class', [])}")
        
        # 5. 모든 테이블 찾기
        all_tables = soup.find_all('table')
        print(f"\n5. 전체 테이블 개수: {len(all_tables)}")
        
        # 6. 첫 번째 테이블의 구조 확인
        if all_tables:
            first_table = all_tables[0]
            print(f"\n6. 첫 번째 테이블 구조:")
            print(f"   클래스: {first_table.get('class', [])}")
            rows = first_table.find_all('tr')
            print(f"   행 개수: {len(rows)}")
            
            if rows:
                first_row = rows[0]
                cells = first_row.find_all(['td', 'th'])
                print(f"   첫 번째 행의 셀 개수: {len(cells)}")
                for i, cell in enumerate(cells):
                    print(f"   셀 {i+1}: {cell.get_text(strip=True)}")
        
        # 7. 페이지 제목 확인
        title = soup.find('title')
        if title:
            print(f"\n7. 페이지 제목: {title.get_text()}")
        
        # 8. 메인 콘텐츠 영역 확인
        content_div = soup.find('div', id='content')
        if content_div:
            print(f"\n8. 메인 콘텐츠 영역을 찾았습니다.")
            content_tables = content_div.find_all('table')
            print(f"   콘텐츠 영역의 테이블 개수: {len(content_tables)}")
        
        # 9. HTML 일부 출력 (디버깅용)
        print(f"\n9. HTML 일부 (처음 1000자):")
        print(response.text[:1000])
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    debug_kospi200_page() 