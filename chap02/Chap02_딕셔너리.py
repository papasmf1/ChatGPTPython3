#Chap02_딕셔너리.py 
device = {"아이폰":5, "아이패드":10, "윈도우노트북":20}
print( device )
print( type(device) )
print( len(device) )

#검색
print( device["아이폰"] )
#입력
device["맥북"] = 15 
#수정
device["아이폰"] = 6 
#삭제
del device["아이패드"]
print( device )


