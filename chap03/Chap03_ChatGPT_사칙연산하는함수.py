#Chap03_ChatGPT_사칙연산하는함수.py

# 덧셈 함수
def add(a, b):
    return a + b

# 뺄셈 함수
def subtract(a, b):
    return a - b

# 곱셈 함수
def multiply(a, b):
    return a * b

# 나눗셈 함수
def divide(a, b):
    if b == 0:
        return "0으로 나눌 수 없습니다."
    return a / b

# 테스트
x = 10
y = 5

print("덧셈:", add(x, y))       # 15
print("뺄셈:", subtract(x, y))  # 5
print("곱셈:", multiply(x, y))  # 50
print("나눗셈:", divide(x, y))  # 2.0

