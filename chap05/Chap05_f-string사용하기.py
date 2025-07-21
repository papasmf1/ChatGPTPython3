#Chap05_f-string사용하기.py

value = 12345
# 기본적인 오른쪽 정렬 (기본은 공백으로 채움)
formatted_str = f"{value:>10}"
print(formatted_str)  # 출력: '     12345'

# 오른쪽 정렬 + 빈자리 0으로 채우기
formatted_str = f"{value:0>10}"
print(formatted_str)  # 출력: '0000012345'

# 왼쪽 정렬 + 빈자리 *로 채우기
formatted_str = f"{value:*<10}"
print(formatted_str)  # 출력: '12345*****'

value = 1234567890

# 3자리마다 콤마 추가
formatted_str = f"{value:,}"
print(formatted_str)  # 출력: '1,234,567,890'

value = 1234567

# 20자리 오른쪽 정렬 + 빈자리 *로 채우기 + 3자리마다 콤마 추가
formatted_str = f"{value:*>20,}"
print(formatted_str)  # 출력: '**********1,234,567'
