import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import time
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QLineEdit, QProgressBar, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QFileDialog, QSplitter,
                             QGroupBox, QGridLayout, QFrame)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

class CrawlerThread(QThread):
    """
    크롤링 작업을 백그라운드에서 실행하는 스레드
    """
    progress_updated = pyqtSignal(str)
    data_updated = pyqtSignal(list)
    finished = pyqtSignal(pd.DataFrame)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, crawl_all=False):
        super().__init__()
        self.crawl_all = crawl_all
        self.stocks_data = []
        
    def run(self):
        try:
            if self.crawl_all:
                self.crawl_all_stocks()
            else:
                self.crawl_first_page()
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def crawl_first_page(self):
        """첫 페이지만 크롤링"""
        self.progress_updated.emit("첫 페이지 크롤링을 시작합니다...")
        
        url = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'euc-kr'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='type_1')
        
        if not table:
            self.error_occurred.emit("테이블을 찾을 수 없습니다.")
            return
        
        rows = table.find_all('tr')
        stock_data = []
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 7:
                row_data = self.extract_row_data(cells)
                if row_data and not any(keyword in row_data[0] for keyword in ['종목별', '현재가', '전일비', '등락률']):
                    stock_data.append(row_data)
        
        if stock_data:
            df = pd.DataFrame(stock_data)
            df.columns = ['종목명(코드)', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)']
            self.progress_updated.emit(f"첫 페이지 크롤링 완료! {len(df)}개 종목")
            self.finished.emit(df)
        else:
            self.error_occurred.emit("데이터를 찾을 수 없습니다.")
    
    def crawl_all_stocks(self):
        """모든 페이지 크롤링"""
        self.progress_updated.emit("전체 종목 크롤링을 시작합니다...")
        
        base_url = "https://finance.naver.com/sise/entryJongmok.naver"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_stocks_data = []
        page = 1
        total_stocks = 0
        
        while True:
            self.progress_updated.emit(f"페이지 {page} 크롤링 중... (누적: {total_stocks}개)")
            
            params = {'type': 'KPI200', 'page': page}
            
            try:
                response = requests.get(base_url, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                response.encoding = 'euc-kr'
                
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table', class_='type_1')
                
                if not table:
                    break
                
                rows = table.find_all('tr')
                page_data = []
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 7:
                        row_data = self.extract_row_data(cells)
                        if row_data and not any(keyword in row_data[0] for keyword in ['종목별', '현재가', '전일비', '등락률']):
                            page_data.append(row_data)
                
                if not page_data:
                    break
                
                all_stocks_data.extend(page_data)
                total_stocks += len(page_data)
                
                # 다음 페이지 확인
                next_page_link = soup.find('a', href=re.compile(r'page=' + str(page + 1)))
                if not next_page_link:
                    break
                
                page += 1
                time.sleep(1)  # 서버 부하 방지
                
            except Exception as e:
                self.error_occurred.emit(f"페이지 {page} 처리 중 오류: {str(e)}")
                break
        
        if all_stocks_data:
            df = pd.DataFrame(all_stocks_data)
            df.columns = ['종목명(코드)', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)']
            self.progress_updated.emit(f"전체 크롤링 완료! 총 {len(df)}개 종목")
            self.finished.emit(df)
        else:
            self.error_occurred.emit("크롤링할 데이터가 없습니다.")
    
    def extract_row_data(self, cells):
        """행 데이터 추출"""
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
        
        return row_data if any(row_data) else None

class Kospi200CrawlerGUI(QMainWindow):
    """
    코스피200 크롤러 GUI 메인 윈도우
    """
    def __init__(self):
        super().__init__()
        self.df = None
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('코스피200 편입종목 크롤러')
        self.setGeometry(100, 100, 1200, 800)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        
        # 상단 검색 영역
        self.create_search_area(main_layout)
        
        # 중앙 분할 영역
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 왼쪽 컨트롤 패널
        self.create_control_panel(splitter)
        
        # 오른쪽 데이터 표시 영역
        self.create_data_display_area(splitter)
        
        # 하단 로그 영역
        self.create_log_area(main_layout)
        
        # 상태바
        self.statusBar().showMessage('준비됨')
        
    def create_search_area(self, parent_layout):
        """검색 영역 생성"""
        search_group = QGroupBox("종목 검색")
        search_layout = QHBoxLayout(search_group)
        
        # 검색 입력창
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("종목명 또는 종목코드를 입력하세요...")
        self.search_input.returnPressed.connect(self.search_stocks)
        search_layout.addWidget(QLabel("검색:"))
        search_layout.addWidget(self.search_input)
        
        # 검색 버튼
        search_btn = QPushButton("검색")
        search_btn.clicked.connect(self.search_stocks)
        search_layout.addWidget(search_btn)
        
        # 검색 결과 라벨
        self.search_result_label = QLabel("")
        search_layout.addWidget(self.search_result_label)
        
        parent_layout.addWidget(search_group)
        
    def create_control_panel(self, splitter):
        """컨트롤 패널 생성"""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # 크롤링 버튼들
        btn_group = QGroupBox("크롤링 옵션")
        btn_layout = QVBoxLayout(btn_group)
        
        self.crawl_first_btn = QPushButton("첫 페이지 크롤링")
        self.crawl_first_btn.clicked.connect(lambda: self.start_crawling(False))
        btn_layout.addWidget(self.crawl_first_btn)
        
        self.crawl_all_btn = QPushButton("전체 종목 크롤링")
        self.crawl_all_btn.clicked.connect(lambda: self.start_crawling(True))
        btn_layout.addWidget(self.crawl_all_btn)
        
        # 진행률 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        btn_layout.addWidget(self.progress_bar)
        
        control_layout.addWidget(btn_group)
        
        # 저장 옵션
        save_group = QGroupBox("데이터 저장")
        save_layout = QVBoxLayout(save_group)
        
        self.save_csv_btn = QPushButton("CSV 파일로 저장")
        self.save_csv_btn.clicked.connect(self.save_to_csv)
        self.save_csv_btn.setEnabled(False)
        save_layout.addWidget(self.save_csv_btn)
        
        self.save_excel_btn = QPushButton("엑셀 파일로 저장")
        self.save_excel_btn.clicked.connect(self.save_to_excel)
        self.save_excel_btn.setEnabled(False)
        save_layout.addWidget(self.save_excel_btn)
        
        control_layout.addWidget(save_group)
        
        # 통계 정보
        stats_group = QGroupBox("통계 정보")
        self.stats_layout = QVBoxLayout(stats_group)
        self.update_statistics()
        control_layout.addWidget(stats_group)
        
        control_layout.addStretch()
        splitter.addWidget(control_widget)
        
    def create_data_display_area(self, splitter):
        """데이터 표시 영역 생성"""
        data_widget = QWidget()
        data_layout = QVBoxLayout(data_widget)
        
        # 테이블 위젯
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels([
            '종목명(코드)', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)'
        ])
        
        # 테이블 설정
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        
        data_layout.addWidget(self.table_widget)
        splitter.addWidget(data_widget)
        
    def create_log_area(self, parent_layout):
        """로그 영역 생성"""
        log_group = QGroupBox("크롤링 로그")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        parent_layout.addWidget(log_group)
        
    def start_crawling(self, crawl_all):
        """크롤링 시작"""
        self.crawler_thread = CrawlerThread(crawl_all)
        self.crawler_thread.progress_updated.connect(self.update_progress)
        self.crawler_thread.data_updated.connect(self.update_data)
        self.crawler_thread.finished.connect(self.crawling_finished)
        self.crawler_thread.error_occurred.connect(self.crawling_error)
        
        # UI 상태 변경
        self.crawl_first_btn.setEnabled(False)
        self.crawl_all_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 무한 진행률
        
        self.log_message("크롤링을 시작합니다...")
        self.crawler_thread.start()
        
    def update_progress(self, message):
        """진행률 업데이트"""
        self.log_message(message)
        self.statusBar().showMessage(message)
        
    def update_data(self, data):
        """데이터 업데이트"""
        pass
        
    def crawling_finished(self, df):
        """크롤링 완료"""
        self.df = df
        self.update_table(df)
        self.update_statistics()
        
        # UI 상태 복원
        self.crawl_first_btn.setEnabled(True)
        self.crawl_all_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.save_csv_btn.setEnabled(True)
        self.save_excel_btn.setEnabled(True)
        
        self.log_message(f"크롤링 완료! 총 {len(df)}개 종목")
        self.statusBar().showMessage(f"크롤링 완료 - {len(df)}개 종목")
        
    def crawling_error(self, error_message):
        """크롤링 오류"""
        self.log_message(f"오류: {error_message}")
        self.statusBar().showMessage("크롤링 실패")
        
        # UI 상태 복원
        self.crawl_first_btn.setEnabled(True)
        self.crawl_all_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.critical(self, "오류", f"크롤링 중 오류가 발생했습니다:\n{error_message}")
        
    def update_table(self, df):
        """테이블 업데이트"""
        self.table_widget.setRowCount(len(df))
        
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 읽기 전용
                self.table_widget.setItem(i, j, item)
                
    def search_stocks(self):
        """종목 검색"""
        if self.df is None:
            self.search_result_label.setText("먼저 데이터를 크롤링해주세요.")
            return
            
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            self.search_result_label.setText("검색어를 입력해주세요.")
            return
            
        # 검색 실행
        filtered_df = self.df[
            self.df['종목명(코드)'].str.lower().str.contains(search_term, na=False)
        ]
        
        if len(filtered_df) > 0:
            self.update_table(filtered_df)
            self.search_result_label.setText(f"검색 결과: {len(filtered_df)}개 종목")
            self.log_message(f"'{search_term}' 검색 결과: {len(filtered_df)}개 종목")
        else:
            self.search_result_label.setText("검색 결과가 없습니다.")
            self.log_message(f"'{search_term}' 검색 결과 없음")
            
    def save_to_csv(self):
        """CSV 파일로 저장"""
        if self.df is None:
            QMessageBox.warning(self, "경고", "저장할 데이터가 없습니다.")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"kospi200_stocks_{timestamp}.csv"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "CSV 파일 저장", default_filename, "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                self.df.to_csv(filename, index=False, encoding='utf-8-sig')
                self.log_message(f"CSV 파일 저장 완료: {filename}")
                QMessageBox.information(self, "완료", f"CSV 파일이 저장되었습니다:\n{filename}")
            except Exception as e:
                self.log_message(f"CSV 파일 저장 실패: {str(e)}")
                QMessageBox.critical(self, "오류", f"CSV 파일 저장 중 오류가 발생했습니다:\n{str(e)}")
                
    def save_to_excel(self):
        """엑셀 파일로 저장"""
        if self.df is None:
            QMessageBox.warning(self, "경고", "저장할 데이터가 없습니다.")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"kospi200_stocks_{timestamp}.xlsx"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "엑셀 파일 저장", default_filename, "Excel Files (*.xlsx)"
        )
        
        if filename:
            try:
                # 엑셀 파일로 저장
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    # 메인 데이터 시트
                    self.df.to_excel(writer, sheet_name='코스피200_편입종목', index=False)
                    
                    # 워크시트 가져오기
                    worksheet = writer.sheets['코스피200_편입종목']
                    
                    # 컬럼 너비 자동 조정
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)  # 최대 50자로 제한
                        worksheet.column_dimensions[column_letter].width = adjusted_width
                    
                    # 헤더 스타일링
                    from openpyxl.styles import Font, PatternFill, Alignment
                    header_font = Font(bold=True, color="FFFFFF")
                    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                    header_alignment = Alignment(horizontal="center", vertical="center")
                    
                    for cell in worksheet[1]:
                        cell.font = header_font
                        cell.fill = header_fill
                        cell.alignment = header_alignment
                    
                    # 통계 정보 시트 추가
                    stats_data = self.create_statistics_data()
                    stats_df = pd.DataFrame(stats_data)
                    stats_df.to_excel(writer, sheet_name='통계정보', index=False)
                    
                    # 통계 시트 스타일링
                    stats_worksheet = writer.sheets['통계정보']
                    for column in stats_worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 30)
                        stats_worksheet.column_dimensions[column_letter].width = adjusted_width
                    
                    # 통계 시트 헤더 스타일링
                    for cell in stats_worksheet[1]:
                        cell.font = header_font
                        cell.fill = header_fill
                        cell.alignment = header_alignment
                
                self.log_message(f"엑셀 파일 저장 완료: {filename}")
                QMessageBox.information(self, "완료", f"엑셀 파일이 저장되었습니다:\n{filename}\n\n- 코스피200_편입종목 시트: 전체 종목 데이터\n- 통계정보 시트: 상승/하락 통계")
                
            except ImportError:
                QMessageBox.critical(self, "오류", "openpyxl 라이브러리가 설치되지 않았습니다.\n다음 명령어로 설치해주세요:\npip install openpyxl")
            except Exception as e:
                self.log_message(f"엑셀 파일 저장 실패: {str(e)}")
                QMessageBox.critical(self, "오류", f"엑셀 파일 저장 중 오류가 발생했습니다:\n{str(e)}")
                
    def create_statistics_data(self):
        """통계 데이터 생성"""
        if self.df is None:
            return []
            
        stats_data = []
        
        # 기본 통계
        total_stocks = len(self.df)
        stats_data.append(["총 종목 수", f"{total_stocks}개"])
        
        # 등락률 분석
        try:
            df_copy = self.df.copy()
            df_copy['등락률_숫자'] = df_copy['등락률'].str.replace('%', '').str.replace('+', '').astype(float)
            상승종목 = len(df_copy[df_copy['등락률_숫자'] > 0])
            하락종목 = len(df_copy[df_copy['등락률_숫자'] < 0])
            보합종목 = len(df_copy[df_copy['등락률_숫자'] == 0])
            
            stats_data.append(["상승종목", f"{상승종목}개"])
            stats_data.append(["하락종목", f"{하락종목}개"])
            stats_data.append(["보합종목", f"{보합종목}개"])
            
            # 상승률 계산
            if total_stocks > 0:
                상승률 = (상승종목 / total_stocks) * 100
                하락률 = (하락종목 / total_stocks) * 100
                stats_data.append(["상승률", f"{상승률:.1f}%"])
                stats_data.append(["하락률", f"{하락률:.1f}%"])
                
        except Exception as e:
            stats_data.append(["등락률 분석", "분석 실패"])
            
        # 크롤링 정보
        stats_data.append(["크롤링 시간", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        stats_data.append(["데이터 출처", "네이버 금융"])
        
        return stats_data
                
    def update_statistics(self):
        """통계 정보 업데이트"""
        # 기존 위젯들 제거
        for i in reversed(range(self.stats_layout.count())):
            self.stats_layout.itemAt(i).widget().setParent(None)
            
        if self.df is None:
            self.stats_layout.addWidget(QLabel("데이터가 없습니다."))
            return
            
        # 통계 계산
        total_stocks = len(self.df)
        
        # 등락률 분석
        try:
            df['등락률_숫자'] = df['등락률'].str.replace('%', '').str.replace('+', '').astype(float)
            상승종목 = len(df[df['등락률_숫자'] > 0])
            하락종목 = len(df[df['등락률_숫자'] < 0])
            보합종목 = len(df[df['등락률_숫자'] == 0])
        except:
            상승종목 = 하락종목 = 보합종목 = 0
            
        # 통계 라벨들 추가
        self.stats_layout.addWidget(QLabel(f"총 종목 수: {total_stocks}개"))
        self.stats_layout.addWidget(QLabel(f"상승종목: {상승종목}개"))
        self.stats_layout.addWidget(QLabel(f"하락종목: {하락종목}개"))
        self.stats_layout.addWidget(QLabel(f"보합종목: {보합종목}개"))
        
    def log_message(self, message):
        """로그 메시지 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
    def closeEvent(self, event):
        """프로그램 종료 시 처리"""
        if hasattr(self, 'crawler_thread') and self.crawler_thread.isRunning():
            reply = QMessageBox.question(
                self, '확인', '크롤링이 진행 중입니다. 정말 종료하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.crawler_thread.terminate()
                self.crawler_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 애플리케이션 스타일 설정
    app.setStyle('Fusion')
    
    # 폰트 설정
    font = QFont("맑은 고딕", 9)
    app.setFont(font)
    
    # 메인 윈도우 생성 및 표시
    window = Kospi200CrawlerGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 