#Chap08_제미나이에서생성한SQL구문.py 
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# 테이블 생성 (없으면 생성, 있으면 건너뛸 수 있도록 `IF NOT EXISTS` 사용)
cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
    productID INTEGER PRIMARY KEY,
    productName TEXT,
    productPrice TEXT
)''')

# 제품 데이터 삽입
data = [
    (1, 'iPhone 13 Pro Max', '1,299,000'),
    (2, 'Galaxy S22 Ultra', '1,199,000'),
    (3, 'Macbook Pro 14', '2,499,000'),
    (4, 'Surface Laptop Studio', '1,999,000'),
    (5, 'Google Pixel 6 Pro', '999,000')
]
cursor.executemany('INSERT INTO Products VALUES (?, ?, ?)', data)

# 데이터베이스 커밋 (변경 내용 저장)
conn.commit()

# 제품 정보 업데이트
cursor.execute('UPDATE Products SET productName = ?, productPrice = ? WHERE productID = ?',
                ('iPhone 14 Pro Max', '1,499,000', 1))

# 특정 제품 삭제
cursor.execute('DELETE FROM Products WHERE productID = ?', (3,))

# 모든 제품 조회
cursor.execute('SELECT * FROM Products')
products = cursor.fetchall()
for product in products:
    print(f"제품 ID: {product[0]}, 제품 이름: {product[1]}, 가격: {product[2]}")

# 데이터베이스 연결 종료
conn.close()
