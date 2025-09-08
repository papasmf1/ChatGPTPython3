# 리스트 (List)
print("=== 리스트 (List) ===")
my_list = [1, 2, 3, 4, 5]

# 리스트의 요소 추가
my_list.append(6)
print("리스트에 6 추가:", my_list)

# 리스트의 요소 삭제
my_list.remove(3)
print("리스트에서 3 제거:", my_list)

# 리스트의 요소 접근
print("리스트의 두 번째 요소:", my_list[1])

# 리스트의 길이
print("리스트의 길이:", len(my_list))

# 리스트는 가변적 (mutable)입니다.
my_list[0] = 10
print("리스트의 첫 번째 요소를 10으로 변경:", my_list)

# 리스트는 순서가 있는 자료구조입니다.
print("리스트의 모든 요소 출력:")
for item in my_list:
    print(item)

print("\n")

# 튜플 (Tuple)
print("=== 튜플 (Tuple) ===")
my_tuple = (1, 2, 3, 4, 5)

# 튜플의 요소 접근
print("튜플의 두 번째 요소:", my_tuple[1])

# 튜플의 길이
print("튜플의 길이:", len(my_tuple))

# 튜플은 불변적 (immutable)입니다.
# my_tuple[0] = 10  # 오류 발생

# 튜플은 순서가 있는 자료구조입니다.
print("튜플의 모든 요소 출력:")
for item in my_tuple:
    print(item)

print("\n")

# 딕셔너리 (Dict)
print("=== 딕셔너리 (Dict) ===")
my_dict = {"a": 1, "b": 2, "c": 3}

# 딕셔너리의 요소 추가
my_dict["d"] = 4
print("딕셔너리에 'd': 4 추가:", my_dict)

# 딕셔너리의 요소 삭제
del my_dict["b"]
print("딕셔너리에서 'b' 삭제:", my_dict)

# 딕셔너리의 값 접근
print("딕셔너리에서 'a'의 값:", my_dict["a"])

# 딕셔너리의 길이
print("딕셔너리의 길이:", len(my_dict))

# 딕셔너리는 키-값 쌍으로 이루어져 있습니다.
print("딕셔너리의 모든 키와 값 출력:")
for key, value in my_dict.items():
    print(f"키: {key}, 값: {value}")

print("\n")

