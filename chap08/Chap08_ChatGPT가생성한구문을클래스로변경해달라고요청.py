#Chap08_ChatGPT가생성한구문을클래스로변경해달라고요청.py
import sqlite3

class Products:
    def __init__(self, db_name='products.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                productID INTEGER PRIMARY KEY,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def insert(self, productID, productName, productPrice):
        self.cursor.execute('''
            INSERT INTO Products (productID, productName, productPrice)
            VALUES (?, ?, ?)
        ''', (productID, productName, productPrice))
        self.conn.commit()

    def update(self, productID, newName, newPrice):
        self.cursor.execute('''
            UPDATE Products
            SET productName = ?, productPrice = ?
            WHERE productID = ?
        ''', (newName, newPrice, productID))
        self.conn.commit()

    def delete(self, productID):
        self.cursor.execute('''
            DELETE FROM Products
            WHERE productID = ?
        ''', (productID,))
        self.conn.commit()

    def select_all(self):
        self.cursor.execute('SELECT * FROM Products')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


# 테스트 코드
if __name__ == '__main__':
    db = Products()

    # 10개의 데이터 삽입
    sample_products = [
        (1, '노트북', 1200000),
        (2, '모니터', 300000),
        (3, '키보드', 50000),
        (4, '마우스', 25000),
        (5, '스피커', 70000),
        (6, '프린터', 150000),
        (7, '웹캠', 40000),
        (8, 'USB 허브', 20000),
        (9, 'SSD 1TB', 130000),
        (10, '헤드셋', 90000)
    ]

    for pid, name, price in sample_products:
        db.insert(pid, name, price)

    # 전체 데이터 출력
    print('--- 전체 제품 목록 ---')
    for row in db.select_all():
        print(f'ID: {row[0]}, Name: {row[1]}, Price: {row[2]}')

    # 제품 수정
    db.update(3, '기계식 키보드', 75000)
    print('\n--- 수정 후 목록 ---')
    for row in db.select_all():
        print(f'ID: {row[0]}, Name: {row[1]}, Price: {row[2]}')

    # 제품 삭제
    db.delete(5)
    print('\n--- 삭제 후 목록 ---')
    for row in db.select_all():
        print(f'ID: {row[0]}, Name: {row[1]}, Price: {row[2]}')

    db.close()
