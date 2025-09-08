import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
)

DB_NAME = 'products.db'
TABLE_NAME = 'Products'

class ProductDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    prodID INTEGER PRIMARY KEY AUTOINCREMENT,
                    prodName TEXT NOT NULL,
                    prodPrice INTEGER NOT NULL
                )
            ''')

    def insert(self, prodName, prodPrice):
        try:
            with self.conn:
                self.conn.execute(f"INSERT INTO {TABLE_NAME} (prodName, prodPrice) VALUES (?, ?)", (prodName, prodPrice))
            return True
        except Exception as e:
            print('DB Insert Error:', e)
            return False

    def update(self, prodID, prodName, prodPrice):
        try:
            with self.conn:
                self.conn.execute(f"UPDATE {TABLE_NAME} SET prodName=?, prodPrice=? WHERE prodID=?", (prodName, prodPrice, prodID))
            return True
        except Exception as e:
            print('DB Update Error:', e)
            return False

    def delete(self, prodID):
        try:
            with self.conn:
                self.conn.execute(f"DELETE FROM {TABLE_NAME} WHERE prodID=?", (prodID,))
            return True
        except Exception as e:
            print('DB Delete Error:', e)
            return False

    def search(self, prodID=None):
        try:
            cur = self.conn.cursor()
            if prodID:
                cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE prodID=?", (prodID,))
            else:
                cur.execute(f"SELECT * FROM {TABLE_NAME}")
            return cur.fetchall()
        except Exception as e:
            print('DB Search Error:', e)
            return []

class ProductApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = ProductDB()
        self.initUI()
        self.load_data()

    def initUI(self):
        self.setWindowTitle('전자제품 데이터 입출력')
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        # prodID 입력란 제거
        # self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.price_input = QLineEdit()
        # form_layout.addWidget(QLabel('ID'))
        # form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel('이름'))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel('가격'))
        form_layout.addWidget(self.price_input)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('입력')
        self.btn_update = QPushButton('수정')
        self.btn_delete = QPushButton('삭제')
        self.btn_search = QPushButton('검색')
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_search)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', '이름', '가격'])
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.btn_add.clicked.connect(self.add_product)
        self.btn_update.clicked.connect(self.update_product)
        self.btn_delete.clicked.connect(self.delete_product)
        self.btn_search.clicked.connect(self.search_product)
        self.table.cellClicked.connect(self.table_row_clicked)

        self.selected_id = None

    def load_data(self, rows=None):
        if rows is None:
            rows = self.db.search()
        self.table.setRowCount(0)
        for row in rows:
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            for col, item in enumerate(row):
                self.table.setItem(row_pos, col, QTableWidgetItem(str(item)))

    def add_product(self):
        try:
            prodName = self.name_input.text().strip()
            prodPrice = int(self.price_input.text())
            if not prodName:
                raise ValueError('이름을 입력하세요.')
            if self.db.insert(prodName, prodPrice):
                QMessageBox.information(self, '성공', '입력 완료')
                self.load_data()
                self.name_input.clear()
                self.price_input.clear()
                self.selected_id = None
            else:
                QMessageBox.warning(self, '오류', '입력 오류입니다.')
        except ValueError:
            QMessageBox.warning(self, '오류', '가격은 숫자, 이름은 공백이 아니어야 합니다.')
        except Exception as e:
            QMessageBox.warning(self, '오류', str(e))

    def update_product(self):
        try:
            if self.selected_id is None:
                QMessageBox.warning(self, '오류', '수정할 항목을 테이블에서 선택하세요.')
                return
            prodName = self.name_input.text().strip()
            prodPrice = int(self.price_input.text())
            if not prodName:
                raise ValueError('이름을 입력하세요.')
            self.db.update(self.selected_id, prodName, prodPrice)
            QMessageBox.information(self, '성공', '수정 완료')
            self.load_data()
            self.name_input.clear()
            self.price_input.clear()
            self.selected_id = None
        except Exception as e:
            QMessageBox.warning(self, '오류', str(e))

    def delete_product(self):
        try:
            if self.selected_id is None:
                QMessageBox.warning(self, '오류', '삭제할 항목을 테이블에서 선택하세요.')
                return
            self.db.delete(self.selected_id)
            QMessageBox.information(self, '성공', '삭제 완료')
            self.load_data()
            self.name_input.clear()
            self.price_input.clear()
            self.selected_id = None
        except Exception as e:
            QMessageBox.warning(self, '오류', str(e))

    def search_product(self):
        try:
            prodName = self.name_input.text().strip()
            if prodName:
                rows = [row for row in self.db.search() if prodName in row[1]]
            else:
                rows = self.db.search()
            self.load_data(rows)
        except Exception as e:
            QMessageBox.warning(self, '오류', str(e))

    def table_row_clicked(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.price_input.setText(self.table.item(row, 2).text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ProductApp()
    win.show()
    sys.exit(app.exec_())
