import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

def crawl_kospi200_top_stocks():
    """
    네이버 금융에서 코스피200 편입종목상위 정보를 크롤링하는 함수
    """
    url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    
    # User-Agent 설정 (웹 브라우저로 인식되도록)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("네이버 금융에서 코스피200 정보를 가져오는 중...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 체크
        
        # 한글 인코딩 설정
        response.encoding = 'euc-kr'
        
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 코스피200 편입종목상위 테이블 찾기
        # 네이버 금융의 구조에 따라 테이블을 찾습니다
        tables = soup.find_all('table')
        
        top_stocks_data = []
        
        # 편입종목상위 테이블을 찾기 위해 여러 방법을 시도
        for table in tables:
            # 테이블의 제목이나 내용에서 "편입종목상위" 또는 관련 키워드 찾기
            table_text = table.get_text()
            if any(keyword in table_text for keyword in ['편입종목', '상위', '종목명', '현재가']):
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:  # 최소 3개 컬럼이 있는 행만 처리
                        row_data = [cell.get_text(strip=True) for cell in cells]
                        if row_data and any(row_data):  # 빈 행 제외
                            top_stocks_data.append(row_data)
        
        # 만약 위 방법으로 찾지 못했다면, 다른 방법 시도
        if not top_stocks_data:
            print("편입종목상위 테이블을 찾지 못했습니다. 다른 방법으로 시도합니다...")
            
            # 코스피200 관련 섹션 찾기
            kospi200_section = soup.find('div', {'class': 'type_1'})
            if kospi200_section:
                tables = kospi200_section.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            row_data = [cell.get_text(strip=True) for cell in cells]
                            if row_data and any(row_data):
                                top_stocks_data.append(row_data)
        
        if top_stocks_data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(top_stocks_data)
            
            # 컬럼명 설정 (첫 번째 행이 헤더인 경우)
            if len(df) > 0:
                df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]
            
            print(f"\n크롤링 완료! 총 {len(df)}개의 행을 가져왔습니다.")
            print("\n=== 코스피200 편입종목상위 정보 ===")
            print(df.to_string(index=False))
            
            # CSV 파일로 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kospi200_top_stocks_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n데이터가 '{filename}' 파일로 저장되었습니다.")
            
            return df
        else:
            print("편입종목상위 정보를 찾을 수 없습니다.")
            print("페이지 구조를 확인해보겠습니다...")
            
            # 페이지 구조 출력 (디버깅용)
            print("\n=== 페이지 구조 분석 ===")
            main_content = soup.find('div', {'id': 'content'})
            if main_content:
                print("메인 콘텐츠 영역을 찾았습니다.")
                tables_in_content = main_content.find_all('table')
                print(f"콘텐츠 영역에서 {len(tables_in_content)}개의 테이블을 찾았습니다.")
                
                for i, table in enumerate(tables_in_content[:3]):  # 처음 3개 테이블만 확인
                    print(f"\n테이블 {i+1}:")
                    print(table.get_text()[:200] + "..." if len(table.get_text()) > 200 else table.get_text())
            
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류: {e}")
        return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def main():
    """
    메인 함수
    """
    print("=" * 50)
    print("네이버 금융 코스피200 편입종목상위 크롤러")
    print("=" * 50)
    
    # 크롤링 실행
    result = crawl_kospi200_top_stocks()
    
    if result is not None:
        print("\n크롤링이 성공적으로 완료되었습니다!")
    else:
        print("\n크롤링에 실패했습니다. 네트워크 연결이나 웹사이트 구조를 확인해주세요.")

if __name__ == "__main__":
    main() 