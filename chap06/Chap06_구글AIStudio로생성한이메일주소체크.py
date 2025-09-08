#Chap06_구글AIStudio로생성한이메일주소체크.py 
import re

def is_valid_email(email):
    """
    re.search()를 사용하여 이메일 주소 형식이 유효한지 검사합니다.
    
    Args:
        email (str): 검사할 이메일 주소 문자열
        
    Returns:
        bool: 형식이 유효하면 True, 그렇지 않으면 False를 반환합니다.
    """
    # 이메일 정규표현식 패턴
    # r''는 raw string으로, 백슬래시를 문자로 그대로 인식하게 해줍니다.
    # ^ : 문자열의 시작
    # [a-zA-Z0-9._%+-]+ : 이메일 사용자 이름 부분 (알파벳, 숫자, ., _, %, +, -가 1번 이상 반복)
    # @ : '@' 문자
    # [a-zA-Z0-9.-]+ : 도메인 이름 부분
    # \. : '.' 문자 (정규식에서 .은 모든 문자를 의미하므로 \를 붙여줌)
    # [a-zA-Z]{2,} : 최상위 도메인 (TLD) 부분 (알파벳이 2자 이상)
    # $ : 문자열의 끝
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # re.search()는 패턴과 일치하는 부분이 있으면 match 객체를, 없으면 None을 반환합니다.
    if re.search(email_pattern, email):
        return True
    else:
        return False

# --- 테스트 예제 ---

# 유효한 이메일 주소
valid_emails = [
    "test@example.com",
    "user.name@domain.co.kr",
    "user_name+tag@sub.domain.org",
    "12345@my-domain.net"
]

# 유효하지 않은 이메일 주소
invalid_emails = [
    "plainaddress",          # @가 없음
    "@missing-local.com",    # @ 앞부분이 없음
    "username@.com",         # 도메인 이름이 없음
    "username@domain..com",  # .. 연속 사용
    "username@domain.c",     # 최상위 도메인이 너무 짧음
    "username@domain.com."   # .으로 끝남
]

print("--- 유효한 이메일 테스트 ---")
for email in valid_emails:
    result = "유효함" if is_valid_email(email) else "유효하지 않음"
    print(f"'{email}': {result}")

print("\n--- 유효하지 않은 이메일 테스트 ---")
for email in invalid_emails:
    result = "유효함" if is_valid_email(email) else "유효하지 않음"
    print(f"'{email}': {result}")