#Chap10_ChatGPT_ProductList_리팩토링.py 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3
import os.path

class DatabaseHandler:
    def __init__(self, db_name="ProductList.db"):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        self.initialize_db()

    def initialize_db(self):
        # 데이터베이스 파일이 없으면 테이블 생성
        if not os.path.exists(self.db_name):
            self.cur.execute(
                "create table Products (id integer primary key autoincrement, Name text, Price integer);"
            )

    def add_product(self, name, price):
        # 제품 추가
        self.cur.execute("insert into Products (Name, Price) values(?,?);", (name, price))
        self.con.commit()

    def update_product(self, prod_id, name, price):
        # 제품 업데이트
        self.cur.execute("update Products set name=?, price=? where id=?;", (name, price, prod_id))
        self.con.commit()

    def remove_product(self, prod_id):
        # 제품 삭제
        self.cur.execute("delete from Products where id=?;", (prod_id,))
        self.con.commit()

    def get_products(self):
        # 모든 제품 가져오기
        self.cur.execute("select * from Products;")
        return self.cur.fetchall()



# 디자인 파일을 로딩
form_class = uic.loadUiType("Chap10_ProductList.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self, db_handler):
        super().__init__()
        self.setupUi(self)
        
        self.db_handler = db_handler
        
        # 초기값 셋팅
        self.id = 0 
        self.name = ""
        self.price = 0 

        # QTableWidget의 행의 갯수와 컬럼의 갯수 지정하기 
        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(3)
        # QTableWidget의 컬럼폭 셋팅하기 
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        # QTableWidget의 헤더 셋팅하기
        self.tableWidget.setHorizontalHeaderLabels(["제품ID", "제품명", "가격"])
        # QTableWidget의 컬럼 정렬하기 
        # self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignRight)
        # self.tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
        # 탭키로 네비게이션 금지 
        self.tableWidget.setTabKeyNavigation(False)
        # 엔터키를 클릭하면 다음 컨트롤로 이동하는 경우 
        self.prodID.returnPressed.connect(lambda: self.focusNextChild())
        self.prodName.returnPressed.connect(lambda: self.focusNextChild())
        self.prodPrice.returnPressed.connect(lambda: self.focusNextChild())
        # 더블클릭 시그널 처리
        self.tableWidget.doubleClicked.connect(self.doubleClick)
        
        # 초기 데이터 로드
        self.getProduct()

    def addProduct(self):
        # 입력 파라메터 처리 
        self.name = self.prodName.text()
        self.price = self.prodPrice.text()
        self.db_handler.add_product(self.name, self.price)
        # 리프레시
        self.getProduct() 

    def updateProduct(self):
        # 업데이트 작업시 파라메터 처리 
        self.id  = self.prodID.text()
        self.name = self.prodName.text()
        self.price = self.prodPrice.text()
        self.db_handler.update_product(self.id, self.name, self.price)
        # 리프레시
        self.getProduct() 

    def removeProduct(self):
        # 삭제 파라메터 처리 
        self.id  = self.prodID.text() 
        self.db_handler.remove_product(self.id)
        # 리프레시
        self.getProduct() 

    def getProduct(self):
        # 검색 결과를 보여주기전에 기존 컨텐트를 삭제(헤더는 제외)
        self.tableWidget.clearContents()

        products = self.db_handler.get_products()
        # 행숫자 카운트 
        row = 0 
        for item in products:
            int_as_strID = "{:10}".format(item[0])
            int_as_strPrice = "{:10}".format(item[2])
            
            # 각 열을 Item으로 생성해서 숫자를 오른쪽으로 정렬해서 출력한다. 
            itemID = QTableWidgetItem(int_as_strID) 
            itemID.setTextAlignment(Qt.AlignRight) 
            self.tableWidget.setItem(row, 0, itemID)
            
            # 제품명은 그대로 출력한다. 
            self.tableWidget.setItem(row, 1, QTableWidgetItem(item[1]))
            
            # 각 열을 Item으로 생성해서 숫자를 오른쪽으로 정렬해서 출력한다. 
            itemPrice = QTableWidgetItem(int_as_strPrice) 
            itemPrice.setTextAlignment(Qt.AlignRight) 
            self.tableWidget.setItem(row, 2, itemPrice)
            
            row += 1

    def doubleClick(self):
        # 더블클릭 시 선택된 아이템의 정보를 입력 폼에 설정
        self.prodID.setText(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
        self.prodName.setText(self.tableWidget.item(self.tableWidget.currentRow(), 1).text())
        self.prodPrice.setText(self.tableWidget.item(self.tableWidget.currentRow(), 2).text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_handler = DatabaseHandler()
    demoForm = DemoForm(db_handler)
    demoForm.show()
    app.exec_()
