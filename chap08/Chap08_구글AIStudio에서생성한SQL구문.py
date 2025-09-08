#Chap08_구글AIStudio에서생성한SQL구문.py 
import sqlite3

# 데이터베이스 연결 함수
def get_db_connection():
    """데이터베이스에 연결하고 커서를 반환합니다."""
    # 'products.db' 파일에 데이터베이스를 생성하거나 연결합니다.
    # with 구문을 사용하면 작업 후 자동으로 연결이 닫힙니다.
    conn = sqlite3.connect('products.db')
    # 결과를 딕셔너리 형태로 받기 위해 row_factory 설정
    conn.row_factory = sqlite3.Row 
    return conn

# 1. 테이블 생성 함수
def create_table(conn):
    """Products 테이블을 생성합니다."""
    cursor = conn.cursor()
    print("--- 1. 테이블 생성 ---")
    # IF NOT EXISTS: 테이블이 이미 존재하면 오류 없이 넘어갑니다.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            productID INTEGER PRIMARY KEY,
            productName TEXT NOT NULL,
            productPrice INTEGER NOT NULL
        )
    ''')
    # 변경사항을 데이터베이스에 반영합니다.
    conn.commit()
    print("'Products' 테이블이 성공적으로 생성되었거나 이미 존재합니다.\n")

# 2. 데이터 추가 함수 (INSERT)
def insert_product(conn, name, price):
    """새로운 제품을 추가합니다."""
    cursor = conn.cursor()
    sql = "INSERT INTO Products (productName, productPrice) VALUES (?, ?)"
    # SQL 인젝션 방지를 위해 플레이스홀더(?) 사용
    cursor.execute(sql, (name, price))
    conn.commit()
    print(f"제품 추가: '{name}' (가격: {price})")

# 3. 데이터 조회 함수 (SELECT)
def select_all_products(conn):
    """모든 제품 목록을 조회하고 출력합니다."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    
    # 모든 결과를 가져옵니다.
    products = cursor.fetchall()
    
    if not products:
        print("테이블에 제품이 없습니다.")
        return

    print("\n--- 전체 제품 목록 ---")
    for product in products:
        # conn.row_factory = sqlite3.Row 설정으로 컬럼 이름으로 접근 가능
        print(f"ID: {product['productID']}, 이름: {product['productName']}, 가격: {product['productPrice']}")
    print("-" * 20)

# 4. 데이터 수정 함수 (UPDATE)
def update_product_price(conn, product_id, new_price):
    """특정 제품의 가격을 수정합니다."""
    cursor = conn.cursor()
    sql = "UPDATE Products SET productPrice = ? WHERE productID = ?"
    cursor.execute(sql, (new_price, product_id))
    conn.commit()
    # rowcount: 마지막 실행으로 영향을 받은 행의 수
    if cursor.rowcount > 0:
        print(f"\n--- 제품 ID {product_id}의 가격을 {new_price}으로 수정했습니다. ---")
    else:
        print(f"\n--- 제품 ID {product_id}을(를) 찾을 수 없습니다. ---")

# 5. 데이터 삭제 함수 (DELETE)
def delete_product(conn, product_id):
    """특정 제품을 삭제합니다."""
    cursor = conn.cursor()
    sql = "DELETE FROM Products WHERE productID = ?"
    cursor.execute(sql, (product_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"\n--- 제품 ID {product_id}을(를) 삭제했습니다. ---")
    else:
        print(f"\n--- 제품 ID {product_id}을(를) 찾을 수 없습니다. ---")


# 메인 실행 로직
if __name__ == "__main__":
    # 데이터베이스 연결
    conn = get_db_connection()

    # 1. 테이블 생성
    create_table(conn)

    # 초기화를 위해 기존 데이터 모두 삭제 (테스트 시 유용)
    conn.execute("DELETE FROM Products")
    conn.commit()

    # 2. 데이터 추가 (INSERT)
    print("\n--- 2. 데이터 삽입 (INSERT) ---")
    insert_product(conn, '노트북', 1500000)
    insert_product(conn, '마우스', 50000)
    insert_product(conn, '키보드', 120000)
    
    # 3. 전체 데이터 조회 (SELECT)
    select_all_products(conn)

    # 4. 데이터 수정 (UPDATE) - ID가 2인 '마우스'의 가격을 60000으로 변경
    update_product_price(conn, 2, 60000)
    
    # 수정 후 전체 데이터 다시 조회
    select_all_products(conn)

    # 5. 데이터 삭제 (DELETE) - ID가 3인 '키보드' 삭제
    delete_product(conn, 3)

    # 삭제 후 최종 데이터 조회
    select_all_products(conn)

    # 데이터베이스 연결 종료
    conn.close()
    print("\n데이터베이스 연결이 종료되었습니다.")