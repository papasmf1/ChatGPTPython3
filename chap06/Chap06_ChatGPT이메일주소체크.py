#Chap06_ChatGPT이메일주소체크.py 

import re

def check_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.search(pattern, email):
        return True
    else:
        return False

# 샘플 이메일 리스트
emails = [
    "john.doe@example.com",       # 유효
    "user_name123@domain.co",     # 유효
    "user+tag@sub.domain.org",    # 유효
    "invalid-email.com",          # '@' 없음
    "user@.com",                  # 도메인 없음
    "user@domain",                # TLD 없음
    "@nouser.com",                # 로컬 파트 없음
    "user@domain.c",              # 너무 짧은 TLD (허용 가능)
    "user@domain..com",           # 연속된 점
    "user@@domain.com"            # '@' 두 개
]

# 결과 출력
for email in emails:
    result = check_email(email)
    print(f"{email:30} -> {'✅ 유효함' if result else '❌ 유효하지 않음'}")
