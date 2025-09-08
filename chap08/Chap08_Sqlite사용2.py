#Chap08_Sqlite2.py

import sqlite3

#연결객체 생성(이번에는 데이터베이스 파일로 저장)
con = sqlite3.connect(":memory:")
#SQL구문을 실행할 커서 객체 리턴
cur = con.cursor()
cur.execute(
    "create table if not exists PhoneBook " + 
    "(id integer primary key autoincrement, name text, phoneNum text);")
#1건 입력
cur.execute("insert into PhoneBook (name, phoneNum) values ('홍길동','010-111-1234');")
#파라메터로 입력 처리 
name = "이순신"
phoneNumber = "010-222-1234"
cur.execute("insert into PhoneBook (name, phoneNum) values (?, ?);", (name, phoneNumber))

#다중의 데이터를 입력
datalist = (("전우치","010-123-1234"), ("박문수","010-123-5678"))
cur.executemany("insert into PhoneBook (name, phoneNum) values (?, ?);", datalist)

#수정 작업
cur.execute("update PhoneBook set name='김길동', phoneNum='010-333-5555' where id=1;")

#삭제 작업 
cur.execute("delete from PhoneBook where id=2;")

#결과 확인 
cur.execute("select * from PhoneBook;")
print(cur.fetchall())

#각각의 메서드로 결과를 다시 확인
cur.execute("select * from PhoneBook;")
print("===fetchone()===")
print(cur.fetchone())
print("===fetchmany(2)===")
print(cur.fetchmany(2))
print("===fetchall()===")
cur.execute("select * from PhoneBook;")
print(cur.fetchall())


