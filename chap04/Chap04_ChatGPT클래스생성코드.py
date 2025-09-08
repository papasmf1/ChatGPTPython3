#Chap04_ChatGPT클래스생성코드.py 
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")

class Manager(Person):
    def __init__(self, id, name, skill, title):
        super().__init__(id, name)
        self.skill = skill
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}, Title: {self.title}")

class Employee(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")

class Alba(Person):
    def __init__(self, id, name):
        super().__init__(id, name)

    def printInfo(self):
        super().printInfo()

# 인스턴스 생성 및 출력
instances = [
    Manager(1, "Alice Johnson", "Management", "General Manager"),
    Manager(2, "Bob Smith", "IT", "IT Manager"),
    Employee(3, "Charlie Brown", "Software Engineer"),
    Employee(4, "David Wilson", "Analyst"),
    Alba(5, "Eve Davis"),
    Alba(6, "Frank Miller"),
    Manager(7, "Grace Lee", "Marketing", "Marketing Manager"),
    Employee(8, "Hannah Martin", "HR Specialist"),
    Alba(9, "Ivy Thompson"),
    Employee(10, "Jack White", "Sales Representative")
]

for instance in instances:
    instance.printInfo()
    print()

# 앞서 정의한 클래스 코드를 포함한 상태라고 가정합니다

if __name__ == "__main__":
    # 10개의 인스턴스 생성
    people = [
        Manager("M01", "Alice", "Python", "Team Lead"),
        Manager("M02", "David", "Project Management", "Senior Manager"),
        Employee("E01", "Bob", "Developer"),
        Employee("E02", "Eve", "Designer"),
        Employee("E03", "Frank", "Tester"),
        Alba("A01", "Charlie"),
        Alba("A02", "Grace"),
        Alba("A03", "Hannah"),
        Manager("M03", "Ivy", "Cloud Architecture", "CTO"),
        Employee("E04", "Jake", "Support Engineer")
    ]

    # 각 인스턴스의 정보 출력
    for idx, person in enumerate(people, start=1):
        print(f"\n--- Person {idx} Info ---")
        person.printInfo()

        