#Chap07_ChatGPT로생성한_다운로드받은파일자동분류.py
import os
import shutil
import glob

# 기준 경로 설정
base_dir = r'C:\Users\student\Downloads'

# 분류할 대상 확장자와 폴더 매핑
categories = {
    'Images': ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG'],
    'PDFs': ['*.pdf'],
    'DataSets': ['*.csv', '*.tsv', '*.xlsx'],
    'Archives': ['*.zip']
}

# 각 폴더 생성 및 파일 이동
for folder, patterns in categories.items():
    target_dir = os.path.join(base_dir, folder)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for pattern in patterns:
        files = glob.glob(os.path.join(base_dir, pattern))
        for file in files:
            try:
                shutil.move(file, target_dir)
                print(f'Moved {os.path.basename(file)} → {folder}')
            except Exception as e:
                print(f'Error moving {file}: {e}')
