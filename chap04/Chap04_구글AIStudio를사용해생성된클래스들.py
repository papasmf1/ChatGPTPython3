# 1. 부모 클래스 정의
class Person:
    """
    모든 구성원의 기본이 되는 부모 클래스
    """
    def __init__(self, id, name):
        """
        생성자: id와 name을 초기화합니다.
        """
        self.id = id
        self.name = name

    def printInfo(self):
        """
        id와 name 정보를 출력하는 인스턴스 메서드
        """
        print(f"ID: {self.id}")
        print(f"이름: {self.name}")


# 2. 자식 클래스 정의
class Manager(Person):
    """
    Person 클래스를 상속받는 Manager 클래스
    """
    def __init__(self, id, name, skill, title):
        """
        생성자: 부모 클래스의 __init__을 호출하여 id, name을 초기화하고,
               추가 멤버변수인 skill과 title을 초기화합니다.
        """
        super().__init__(id, name)  # 부모 클래스의 생성자 호출
        self.skill = skill
        self.title = title

    def printInfo(self):
        """
        메서드 오버라이딩: 부모의 printInfo()를 호출하여 기본 정보를 출력하고,
                        Manager의 추가 정보를 출력합니다.
        """
        super().printInfo()  # 부모 클래스의 printInfo() 메서드 호출
        print(f"보유기술: {self.skill}")
        print(f"직책: {self.title}")


class Employee(Person):
    """
    Person 클래스를 상속받는 Employee 클래스
    """
    def __init__(self, id, name, title):
        """
        생성자: 부모 클래스의 __init__을 호출하여 id, name을 초기화하고,
               추가 멤버변수인 title을 초기화합니다.
        """
        super().__init__(id, name) # 부모 클래스의 생성자 호출
        self.title = title

    def printInfo(self):
        """
        메서드 오버라이딩: 부모의 printInfo()를 호출하여 기본 정보를 출력하고,
                        Employee의 추가 정보를 출력합니다.
        """
        super().printInfo() # 부모 클래스의 printInfo() 메서드 호출
        print(f"직책: {self.title}")


class Alba(Person):
    """
    Person 클래스를 상속받는 Alba 클래스
    """
    # Alba 클래스는 추가적인 멤버변수가 없으므로,
    # __init__ 메서드를 별도로 정의(오버라이딩)할 필요가 없습니다.
    # 인스턴스 생성 시 부모인 Person의 __init__이 자동으로 호출됩니다.
    # printInfo 메서드 또한 부모의 것을 그대로 사용합니다.
    pass


# 3. 클래스 사용 예제
print("--- 매니저 정보 ---")
manager = Manager("M001", "김관리", "프로젝트 관리", "팀장")
manager.printInfo()

print("\n--- 직원 정보 ---")
employee = Employee("E001", "이직원", "대리")
employee.printInfo()

print("\n--- 아르바이트 정보 ---")
alba = Alba("A001", "박알바")
alba.printInfo()