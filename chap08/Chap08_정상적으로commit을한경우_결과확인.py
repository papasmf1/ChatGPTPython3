#Chap08_정상적으로commit을한경우_결과확인.py
import sqlite3

#연결객체 생성(이번에는 데이터베이스 파일로 저장)
con = sqlite3.connect("c:\\work\\sample.db")
cur = con.cursor()
cur.execute("select * from PhoneBook;")
print(cur.fetchall())
