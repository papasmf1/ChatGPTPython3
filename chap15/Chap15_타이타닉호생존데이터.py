import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows: Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 타이타닉 데이터셋 다운로드
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# 2. 데이터 클렌징 (결측치 처리 등)
# Age 결측치는 평균값으로 대체, Embarked 결측치는 최빈값으로 대체
df['Age'].fillna(df['Age'].mean(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
df['Sex'] = df['Sex'].map({'male': '남성', 'female': '여성'})

# 3. 남성과 여성의 생존율 계산
survival_rate = df.groupby('Sex')['Survived'].mean() * 100

# 4. 바 차트로 시각화
plt.bar(survival_rate.index, survival_rate.values, color=['blue', 'pink'])
plt.title('성별 생존율(%)')
plt.ylabel('생존율(%)')
plt.xlabel('성별')
plt.ylim(0, 100)
plt.show()