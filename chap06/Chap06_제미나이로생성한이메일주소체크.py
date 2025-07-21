#Chap06_제미나이로생성한이메일주소체크.py 
import re

def is_email_valid(email):
  """
  이 함수는 주어진 문자열이 유효한 이메일 주소인지 확인합니다.

  Args:
    email: 확인할 이메일 주소 문자열입니다.

  Returns:
    주어진 문자열이 유효한 이메일 주소인지 여부를 나타내는 True 또는 False를 반환합니다.
  """
  email_regex = r"""^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"""
  return bool(re.search(email_regex, email))

# 예제 사용
email1 = "user@example.com"
email2 = "user_name@example.com"
email3 = "user@example.ac.kr"
email4 = "user@example"

print(f"{email1} 이 유효한 이메일 주소인가요? {is_email_valid(email1)}")
print(f"{email2} 이 유효한 이메일 주소인가요? {is_email_valid(email2)}")
print(f"{email3} 이 유효한 이메일 주소인가요? {is_email_valid(email3)}")
print(f"{email4} 이 유효한 이메일 주소인가요? {is_email_valid(email4)}")
