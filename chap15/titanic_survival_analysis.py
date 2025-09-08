import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
import platform
import matplotlib.font_manager as fm

# 한글 폰트 설정
def setup_korean_font():
    """운영체제에 따른 한글 폰트 설정"""
    system = platform.system()
    
    if system == "Windows":
        # Windows 한글 폰트 설정 - 강력한 방법
        try:
            # 사용 가능한 폰트 목록 가져오기
            font_list = [f.name for f in fm.fontManager.ttflist]
            print(f"사용 가능한 폰트 수: {len(font_list)}")
            
            # 한글 폰트 찾기 (더 많은 옵션 포함)
            korean_fonts = []
            for font in font_list:
                font_lower = font.lower()
                if any(korean in font_lower for korean in ['malgun', 'gulim', 'dotum', 'batang', 'nanum', 'noto']):
                    korean_fonts.append(font)
            
            print(f"발견된 한글 폰트: {korean_fonts}")
            
            if korean_fonts:
                # 맑은 고딕을 우선적으로 선택
                if 'Malgun Gothic' in korean_fonts:
                    selected_font = 'Malgun Gothic'
                elif '맑은 고딕' in korean_fonts:
                    selected_font = '맑은 고딕'
                else:
                    selected_font = korean_fonts[0]
                
                plt.rcParams['font.family'] = selected_font
                print(f"선택된 폰트: {selected_font}")
            else:
                # 한글 폰트가 없으면 기본 폰트 사용
                plt.rcParams['font.family'] = 'DejaVu Sans'
                print("한글 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
                
        except Exception as e:
            print(f"폰트 설정 중 오류 발생: {e}")
            plt.rcParams['font.family'] = 'DejaVu Sans'
            
    elif system == "Darwin":  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
        print("macOS: AppleGothic 폰트 사용")
        
    else:  # Linux
        plt.rcParams['font.family'] = 'DejaVu Sans'
        print("Linux: DejaVu Sans 폰트 사용")
    
    plt.rcParams['axes.unicode_minus'] = False

# 한글 폰트 설정 실행
setup_korean_font()

def download_titanic_data():
    """타이타닉 데이터셋을 인터넷에서 다운로드"""
    try:
        # Kaggle의 타이타닉 데이터셋 URL
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        
        print("타이타닉 데이터셋을 다운로드 중...")
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 체크
        
        # CSV 데이터를 DataFrame으로 변환
        df = pd.read_csv(io.StringIO(response.text))
        print(f"데이터 다운로드 완료! 총 {len(df)}개의 레코드")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"데이터 다운로드 중 오류 발생: {e}")
        return None

def analyze_survival_by_gender(df):
    """성별 생존율 분석"""
    if df is None:
        return None
    
    # 성별 생존율 계산
    survival_by_gender = df.groupby('Sex')['Survived'].agg(['count', 'sum']).reset_index()
    survival_by_gender['survival_rate'] = (survival_by_gender['sum'] / survival_by_gender['count'] * 100).round(2)
    
    # 성별을 한글로 변환
    gender_mapping = {'male': '남성', 'female': '여성'}
    survival_by_gender['Sex_Display'] = survival_by_gender['Sex'].map(gender_mapping)
    
    return survival_by_gender

def create_survival_chart(survival_data):
    """생존율 바차트 생성"""
    if survival_data is None:
        return
    
    # 그래프 스타일 설정
    try:
        plt.style.use('seaborn-v0_8')
    except:
        plt.style.use('default')
    
    # 폰트 재설정 (차트 생성 시점에서)
    setup_korean_font()
    
    # 한글 폰트 테스트
    try:
        test_text = "한글테스트"
        fig_test, ax_test = plt.subplots(figsize=(1, 1))
        ax_test.text(0.5, 0.5, test_text, fontsize=12)
        plt.close(fig_test)
        use_korean = True
        print("한글 폰트가 정상적으로 작동합니다.")
    except:
        use_korean = False
        print("한글 폰트에 문제가 있어 영어로 표시합니다.")
        plt.rcParams['font.family'] = 'DejaVu Sans'
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. 생존율 바차트
    colors = ['#FF6B6B', '#4ECDC4']
    bars = ax1.bar(survival_data['Sex_Display'], survival_data['survival_rate'], 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # 바 위에 퍼센트 표시
    for bar, rate in zip(bars, survival_data['survival_rate']):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # 조건부 제목 설정
    if use_korean:
        ax1.set_title('타이타닉호 성별 생존율', fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel('생존율 (%)', fontsize=12)
    else:
        ax1.set_title('Titanic Survival Rate by Gender', fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel('Survival Rate (%)', fontsize=12)
    
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. 생존자 수 바차트
    survival_counts = survival_data[['Sex_Display', 'sum', 'count']].copy()
    
    if use_korean:
        survival_counts['사망자'] = survival_counts['count'] - survival_counts['sum']
        survival_counts = survival_counts.rename(columns={'sum': '생존자'})
        
        # 스택 바차트
        x = range(len(survival_counts))
        ax2.bar(x, survival_counts['생존자'], label='생존자', color='#4ECDC4', alpha=0.8)
        ax2.bar(x, survival_counts['사망자'], bottom=survival_counts['생존자'], 
                label='사망자', color='#FF6B6B', alpha=0.8)
        
        # 바 위에 숫자 표시
        for i, (survived, died) in enumerate(zip(survival_counts['생존자'], survival_counts['사망자'])):
            ax2.text(i, survived/2, str(survived), ha='center', va='center', fontweight='bold')
            ax2.text(i, survived + died/2, str(died), ha='center', va='center', fontweight='bold')
        
        ax2.set_title('타이타닉호 성별 생존자/사망자 수', fontsize=16, fontweight='bold', pad=20)
        ax2.set_ylabel('인원 수', fontsize=12)
    else:
        survival_counts['Deceased'] = survival_counts['count'] - survival_counts['sum']
        survival_counts = survival_counts.rename(columns={'sum': 'Survived'})
        
        # 스택 바차트
        x = range(len(survival_counts))
        ax2.bar(x, survival_counts['Survived'], label='Survived', color='#4ECDC4', alpha=0.8)
        ax2.bar(x, survival_counts['Deceased'], bottom=survival_counts['Survived'], 
                label='Deceased', color='#FF6B6B', alpha=0.8)
        
        # 바 위에 숫자 표시
        for i, (survived, died) in enumerate(zip(survival_counts['Survived'], survival_counts['Deceased'])):
            ax2.text(i, survived/2, str(survived), ha='center', va='center', fontweight='bold')
            ax2.text(i, survived + died/2, str(died), ha='center', va='center', fontweight='bold')
        
        ax2.set_title('Titanic Survivors/Deceased by Gender', fontsize=16, fontweight='bold', pad=20)
        ax2.set_ylabel('Number of People', fontsize=12)
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(survival_counts['Sex_Display'])
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def print_statistics(survival_data):
    """통계 정보 출력"""
    if survival_data is None:
        return
    
    print("\n" + "="*50)
    print("타이타닉호 생존율 분석 결과")
    print("="*50)
    
    for _, row in survival_data.iterrows():
        print(f"{row['Sex_Display']}:")
        print(f"  - 총 승객 수: {row['count']}명")
        print(f"  - 생존자 수: {row['sum']}명")
        print(f"  - 생존율: {row['survival_rate']}%")
        print()
    
    # 전체 생존율 계산
    total_survived = survival_data['sum'].sum()
    total_passengers = survival_data['count'].sum()
    total_survival_rate = (total_survived / total_passengers * 100).round(2)
    
    print(f"전체 생존율: {total_survival_rate}% ({total_survived}/{total_passengers})")

def main():
    """메인 함수"""
    print("타이타닉호 생존율 분석을 시작합니다...")
    
    # 데이터 다운로드
    df = download_titanic_data()
    
    if df is not None:
        # 데이터 전처리
        print("\n데이터 전처리 중...")
        print(f"데이터 형태: {df.shape}")
        print(f"컬럼: {list(df.columns)}")
        
        # 결측치 확인
        print(f"\n결측치 확인:")
        print(df[['Sex', 'Survived']].isnull().sum())
        
        # 결측치 제거
        df_clean = df.dropna(subset=['Sex', 'Survived'])
        print(f"결측치 제거 후 데이터 수: {len(df_clean)}")
        
        # 성별 생존율 분석
        survival_data = analyze_survival_by_gender(df_clean)
        
        # 결과 출력
        print_statistics(survival_data)
        
        # 차트 생성
        create_survival_chart(survival_data)
        
        # 데이터 저장
        survival_data.to_csv('titanic_survival_analysis.csv', index=False, encoding='utf-8-sig')
        print("\n분석 결과가 'titanic_survival_analysis.csv' 파일로 저장되었습니다.")
        
    else:
        print("데이터를 가져올 수 없어 분석을 중단합니다.")

if __name__ == "__main__":
    main() 