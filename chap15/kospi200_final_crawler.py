import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

def crawl_kospi200_entry_stocks():
    """
    네이버 금융에서 코스피200 편입종목 정보를 크롤링하는 함수
    """
    # 편입종목 전용 페이지 URL
    url = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("네이버 금융에서 코스피200 편입종목 정보를 가져오는 중...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'euc-kr'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 편입종목 테이블 찾기
        table = soup.find('table', class_='type_1')
        if not table:
            print("편입종목 테이블을 찾을 수 없습니다.")
            return None
        
        print("편입종목 테이블을 찾았습니다!")
        
        # 테이블 데이터 추출
        rows = table.find_all('tr')
        stock_data = []
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 7:  # 헤더와 데이터 행 모두 처리
                row_data = []
                
                for i, cell in enumerate(cells):
                    # 종목명 (첫 번째 컬럼)
                    if i == 0:
                        # a 태그에서 종목명 추출
                        link = cell.find('a')
                        if link:
                            stock_name = link.get_text(strip=True)
                            stock_code = link.get('href', '').split('code=')[-1] if 'code=' in link.get('href', '') else ''
                            row_data.append(f"{stock_name} ({stock_code})")
                        else:
                            row_data.append(cell.get_text(strip=True))
                    
                    # 현재가 (두 번째 컬럼)
                    elif i == 1:
                        price = cell.get_text(strip=True)
                        row_data.append(price)
                    
                    # 전일비 (세 번째 컬럼)
                    elif i == 2:
                        # 상승/하락 아이콘과 값 추출
                        change_icon = cell.find('em', class_='bu_p')
                        change_value = cell.find('span', class_='tah')
                        
                        if change_icon and change_value:
                            # 상승/하락 판단
                            if 'bu_pup' in change_icon.get('class', []):
                                direction = "▲"
                            elif 'bu_pdn' in change_icon.get('class', []):
                                direction = "▼"
                            else:
                                direction = ""
                            
                            value = change_value.get_text(strip=True)
                            row_data.append(f"{direction} {value}")
                        else:
                            row_data.append(cell.get_text(strip=True))
                    
                    # 등락률 (네 번째 컬럼)
                    elif i == 3:
                        rate_span = cell.find('span', class_='tah')
                        if rate_span:
                            rate = rate_span.get_text(strip=True)
                            row_data.append(rate)
                        else:
                            row_data.append(cell.get_text(strip=True))
                    
                    # 거래량 (다섯 번째 컬럼)
                    elif i == 4:
                        volume = cell.get_text(strip=True)
                        row_data.append(volume)
                    
                    # 거래대금 (여섯 번째 컬럼)
                    elif i == 5:
                        amount = cell.get_text(strip=True)
                        row_data.append(amount)
                    
                    # 시가총액 (일곱 번째 컬럼)
                    elif i == 6:
                        market_cap = cell.get_text(strip=True)
                        row_data.append(market_cap)
                    
                    else:
                        row_data.append(cell.get_text(strip=True))
                
                if row_data and any(row_data):
                    stock_data.append(row_data)
        
        if stock_data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(stock_data)
            
            # 컬럼명 설정
            if len(df) > 0:
                df.columns = ['종목명(코드)', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)']
            
            print(f"\n크롤링 완료! 총 {len(df)}개의 종목 정보를 가져왔습니다.")
            print("\n=== 코스피200 편입종목 정보 (첫 10개) ===")
            print(df.head(10).to_string(index=False))
            
            # CSV 파일로 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kospi200_entry_stocks_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n데이터가 '{filename}' 파일로 저장되었습니다.")
            
            return df
        else:
            print("편입종목 데이터를 추출할 수 없습니다.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류: {e}")
        return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def crawl_kospi200_all_pages():
    """
    코스피200 편입종목의 모든 페이지를 크롤링하는 함수
    """
    base_url = "https://finance.naver.com/sise/entryJongmok.naver"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_stocks_data = []
    
    try:
        # 첫 번째 페이지부터 시작해서 모든 페이지 크롤링
        page = 1
        while True:
            print(f"페이지 {page} 크롤링 중...")
            
            params = {
                'type': 'KPI200',
                'page': page
            }
            
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            response.encoding = 'euc-kr'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 편입종목 테이블 찾기
            table = soup.find('table', class_='type_1')
            if not table:
                print(f"페이지 {page}에서 테이블을 찾을 수 없습니다.")
                break
            
            # 테이블 데이터 추출
            rows = table.find_all('tr')
            page_data = []
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 7:
                    row_data = []
                    
                    for i, cell in enumerate(cells):
                        if i == 0:  # 종목명
                            link = cell.find('a')
                            if link:
                                stock_name = link.get_text(strip=True)
                                stock_code = link.get('href', '').split('code=')[-1] if 'code=' in link.get('href', '') else ''
                                row_data.append(f"{stock_name} ({stock_code})")
                            else:
                                row_data.append(cell.get_text(strip=True))
                        elif i == 1:  # 현재가
                            row_data.append(cell.get_text(strip=True))
                        elif i == 2:  # 전일비
                            change_icon = cell.find('em', class_='bu_p')
                            change_value = cell.find('span', class_='tah')
                            
                            if change_icon and change_value:
                                if 'bu_pup' in change_icon.get('class', []):
                                    direction = "▲"
                                elif 'bu_pdn' in change_icon.get('class', []):
                                    direction = "▼"
                                else:
                                    direction = ""
                                
                                value = change_value.get_text(strip=True)
                                row_data.append(f"{direction} {value}")
                            else:
                                row_data.append(cell.get_text(strip=True))
                        elif i == 3:  # 등락률
                            rate_span = cell.find('span', class_='tah')
                            if rate_span:
                                row_data.append(rate_span.get_text(strip=True))
                            else:
                                row_data.append(cell.get_text(strip=True))
                        elif i == 4:  # 거래량
                            row_data.append(cell.get_text(strip=True))
                        elif i == 5:  # 거래대금
                            row_data.append(cell.get_text(strip=True))
                        elif i == 6:  # 시가총액
                            row_data.append(cell.get_text(strip=True))
                        else:
                            row_data.append(cell.get_text(strip=True))
                    
                    if row_data and any(row_data):
                        page_data.append(row_data)
            
            if not page_data:
                print(f"페이지 {page}에서 데이터를 찾을 수 없습니다.")
                break
            
            all_stocks_data.extend(page_data)
            print(f"페이지 {page}에서 {len(page_data)}개 종목 정보를 가져왔습니다.")
            
            # 다음 페이지가 있는지 확인
            next_page = soup.find('a', href=re.compile(r'page=' + str(page + 1)))
            if not next_page:
                print("더 이상 페이지가 없습니다.")
                break
            
            page += 1
        
        if all_stocks_data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(all_stocks_data)
            df.columns = ['종목명(코드)', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)']
            
            print(f"\n전체 크롤링 완료! 총 {len(df)}개의 종목 정보를 가져왔습니다.")
            
            # CSV 파일로 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kospi200_all_stocks_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"전체 데이터가 '{filename}' 파일로 저장되었습니다.")
            
            return df
        else:
            print("크롤링할 데이터가 없습니다.")
            return None
            
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def main():
    """
    메인 함수
    """
    print("=" * 60)
    print("네이버 금융 코스피200 편입종목 크롤러 (최종版)")
    print("=" * 60)
    
    print("\n1. 첫 페이지 편입종목 정보만 크롤링")
    print("2. 모든 페이지의 편입종목 정보 크롤링")
    
    choice = input("\n선택하세요 (1 또는 2): ").strip()
    
    if choice == "1":
        print("\n첫 페이지 편입종목 정보를 크롤링합니다...")
        result = crawl_kospi200_entry_stocks()
    elif choice == "2":
        print("\n모든 페이지의 편입종목 정보를 크롤링합니다...")
        result = crawl_kospi200_all_pages()
    else:
        print("잘못된 선택입니다. 첫 페이지 정보만 크롤링합니다.")
        result = crawl_kospi200_entry_stocks()
    
    if result is not None:
        print("\n크롤링이 성공적으로 완료되었습니다!")
    else:
        print("\n크롤링에 실패했습니다. 네트워크 연결이나 웹사이트 구조를 확인해주세요.")

if __name__ == "__main__":
    main() 