import sys
import time

print("=== 파이썬 List, Tuple, Dict 비교 데모 ===\n")

# 1. 생성 시간 비교
def measure_creation_time():
    start = time.time()
    lst = [i for i in range(1000000)]
    list_time = time.time() - start

    start = time.time()
    tpl = tuple(i for i in range(1000000))
    tuple_time = time.time() - start

    start = time.time()
    dct = {i: i for i in range(1000000)}
    dict_time = time.time() - start

    print(f"[생성 시간 비교 (100만 항목)]")
    print(f"List 생성 시간: {list_time:.6f}초")
    print(f"Tuple 생성 시간: {tuple_time:.6f}초")
    print(f"Dict 생성 시간: {dict_time:.6f}초\n")

# 2. 메모리 사용 비교
def measure_memory_usage():
    lst = [0] * 1000
    tpl = tuple(lst)
    dct = {i: 0 for i in range(1000)}

    print("[메모리 사용량 비교 (1000개 항목)]")
    print(f"List 메모리: {sys.getsizeof(lst)} bytes")
    print(f"Tuple 메모리: {sys.getsizeof(tpl)} bytes")
    print(f"Dict 메모리: {sys.getsizeof(dct)} bytes\n")

# 3. 변경 가능 여부
def mutability_demo():
    print("[변경 가능성(Mutability)]")
    lst = [1, 2, 3]
    tpl = (1, 2, 3)
    dct = {"a": 1, "b": 2}

    lst[0] = 99  # 가능
    print(f"List 변경: {lst}")

    try:
        tpl[0] = 99  # 오류 발생
    except TypeError as e:
        print(f"Tuple 변경 불가: {e}")

    dct["a"] = 99  # 가능
    print(f"Dict 변경: {dct}\n")

# 4. 탐색 속도 비교
def lookup_demo():
    print("[탐색 속도 비교]")
    lst = list(range(100000))
    dct = {i: i for i in range(100000)}

    start = time.time()
    _ = 99999 in lst
    list_lookup = time.time() - start

    start = time.time()
    _ = 99999 in dct
    dict_lookup = time.time() - start

    print(f"List에서 값 찾기: {list_lookup:.6f}초")
    print(f"Dict에서 키 찾기: {dict_lookup:.6f}초\n")

# 실행
measure_creation_time()
measure_memory_usage()
mutability_demo()
lookup_demo()
