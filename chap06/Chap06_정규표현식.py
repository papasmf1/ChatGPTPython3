#Chap06_정규표현식.py 
import re 

result = re.search("[0-9]*th", "35th")
print(result)
print(result.group())
result = re.match("[0-9]*th", "35th")
print(result)
print(result.group())

#함정이 추가된 경우
result = re.search("[0-9]*th", "  35th")
print(result)
print(result.group())
 
# result = re.match("[0-9]*th", "  35th")
# print(result)
# print(result.group())

