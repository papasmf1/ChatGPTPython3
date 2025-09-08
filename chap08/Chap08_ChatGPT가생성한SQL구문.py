#Chap08_ChatGPT가생성한SQL구문.py
import sqlite3

# 데이터베이스 연결 (없으면 새로 생성됨)
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        productID INTEGER PRIMARY KEY,
        productName TEXT NOT NULL,
        productPrice INTEGER NOT NULL
    )
''')
conn.commit()

# 데이터 삽입 함수
def insert_product(productID, productName, productPrice):
    cursor.execute('''
        INSERT INTO Products (productID, productName, productPrice)
        VALUES (?, ?, ?)
    ''', (productID, productName, productPrice))
    conn.commit()

# 데이터 수정 함수
def update_product(productID, newName, newPrice):
    cursor.execute('''
        UPDATE Products
        SET productName = ?, productPrice = ?
        WHERE productID = ?
    ''', (newName, newPrice, productID))
    conn.commit()

# 데이터 삭제 함수
def delete_product(productID):
    cursor.execute('''
        DELETE FROM Products
        WHERE productID = ?
    ''', (productID,))
    conn.commit()

# 데이터 조회 함수
def select_all_products():
    cursor.execute('SELECT * FROM Products')
    rows = cursor.fetchall()
    for row in rows:
        print(f'ID: {row[0]}, Name: {row[1]}, Price: {row[2]}')

# 테스트 실행 예시
if __name__ == '__main__':
    # 삽입
    insert_product(1, '노트북', 1200000)
    insert_product(2, '모니터', 300000)
    
    # 조회
    print('--- 삽입 후 조회 ---')
    select_all_products()
    
    # 수정
    update_product(2, '게이밍 모니터', 350000)
    print('--- 수정 후 조회 ---')
    select_all_products()

    # 삭제
    delete_product(1)
    print('--- 삭제 후 조회 ---')
    select_all_products()

    # 연결 종료
    conn.close()
