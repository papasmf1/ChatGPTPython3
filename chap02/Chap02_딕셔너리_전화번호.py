#Chap02_딕셔너리_전화번호.py 

phone = {"kim":"010-123-134","lee":"010-222-3333","park":"010-456-7890"}

print(phone)
#검색
print(phone["kim"])
#입력
phone["kang"] = "010-123-4567"
print(phone)
#수정
phone["kim"] = "010-111-2222"
print(phone)
#삭제
del phone["kim"]

#반복구문
for item in phone.items():
    print(item)

#2개의 반복변수 사용 
for k,v in phone.items():
    print(k,v)

#키만 받는 경우
for key in phone.keys():
    print(key)

#값만 받는 경우 
for value in phone.values():
    print(value)



