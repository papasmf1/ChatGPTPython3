import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import time

def crawl_kospi200_all_stocks():
    """
    코스피200의 모든 편입종목을 페이징 처리하여 크롤링하는 함수
    """
    base_url = "https://finance.naver.com/sise/entryJongmok.naver"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_stocks_data = []
    page = 1
    total_stocks = 0
    
    try:
        print("코스피200 모든 편입종목 크롤링을 시작합니다...")
        print("=" * 60)
        
        while True:
            print(f"페이지 {page} 크롤링 중...")
            
            params = {
                'type': 'KPI200',
                'page': page
            }
            
            try:
                response = requests.get(base_url, params=params, headers=headers, timeout=10)
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
                            # 헤더 행 제외 (종목별, 현재가 등의 텍스트가 포함된 행)
                            if not any(keyword in row_data[0] for keyword in ['종목별', '현재가', '전일비', '등락률']):
                                page_data.append(row_data)
                
                if not page_data:
                    print(f"페이지 {page}에서 종목 데이터를 찾을 수 없습니다.")
                    break
                
                all_stocks_data.extend(page_data)
                total_stocks += len(page_data)
                print(f"페이지 {page}에서 {len(page_data)}개 종목 정보를 가져왔습니다. (누적: {total_stocks}개)")
                
                # 다음 페이지가 있는지 확인
                next_page_link = soup.find('a', href=re.compile(r'page=' + str(page + 1)))
                if not next_page_link:
                    print("더 이상 페이지가 없습니다.")
                    break
                
                page += 1
                
                # 서버 부하 방지를 위한 딜레이
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                print(f"페이지 {page} 요청 중 오류 발생: {e}")
                break
            except Exception as e:
                print(f"페이지 {page} 처리 중 오류 발생: {e}")
                break
        
        if all_stocks_data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(all_stocks_data)
            df.columns = ['종목명(코드)', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)']
            
            print("\n" + "=" * 60)
            print(f"전체 크롤링 완료!")
            print(f"총 {len(df)}개의 종목 정보를 가져왔습니다.")
            print(f"총 {page-1}페이지를 크롤링했습니다.")
            print("=" * 60)
            
            # CSV 파일로 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kospi200_all_200_stocks_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n전체 데이터가 '{filename}' 파일로 저장되었습니다.")
            
            # 상위 10개 종목 미리보기
            print("\n=== 상위 10개 종목 미리보기 ===")
            print(df.head(10).to_string(index=False))
            
            # 통계 정보 출력
            print("\n=== 크롤링 통계 ===")
            print(f"총 종목 수: {len(df)}개")
            print(f"총 페이지 수: {page-1}페이지")
            
            # 등락률 분석
            df['등락률_숫자'] = df['등락률'].str.replace('%', '').str.replace('+', '').astype(float)
            상승종목 = len(df[df['등락률_숫자'] > 0])
            하락종목 = len(df[df['등락률_숫자'] < 0])
            보합종목 = len(df[df['등락률_숫자'] == 0])
            
            print(f"상승종목: {상승종목}개")
            print(f"하락종목: {하락종목}개")
            print(f"보합종목: {보합종목}개")
            
            return df
        else:
            print("크롤링할 데이터가 없습니다.")
            return None
            
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return None

def crawl_kospi200_with_progress():
    """
    진행률을 표시하며 코스피200 모든 종목을 크롤링하는 함수
    """
    print("=" * 60)
    print("코스피200 전체 편입종목 크롤러 (페이징 처리)")
    print("=" * 60)
    
    print("\n크롤링을 시작합니다...")
    print("예상 소요 시간: 약 2-3분")
    print("서버 부하 방지를 위해 페이지당 1초 딜레이를 적용합니다.")
    
    start_time = datetime.now()
    result = crawl_kospi200_all_stocks()
    end_time = datetime.now()
    
    if result is not None:
        elapsed_time = (end_time - start_time).total_seconds()
        print(f"\n크롤링 완료!")
        print(f"소요 시간: {elapsed_time:.1f}초")
        print(f"평균 처리 속도: {len(result)/elapsed_time:.1f}종목/초")
    else:
        print("\n크롤링에 실패했습니다.")

def main():
    """
    메인 함수
    """
    print("코스피200 전체 편입종목 크롤러")
    print("이 프로그램은 코스피200의 모든 편입종목(약 200개)을 크롤링합니다.")
    
    confirm = input("\n크롤링을 시작하시겠습니까? (y/n): ").strip().lower()
    
    if confirm in ['y', 'yes', '예', '네']:
        crawl_kospi200_with_progress()
    else:
        print("크롤링이 취소되었습니다.")

if __name__ == "__main__":
    main() 