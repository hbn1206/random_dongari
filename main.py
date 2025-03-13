import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import platform

# 한글 폰트 설정 (MacOS, Windows 대응)
import matplotlib.pyplot as plt
from matplotlib import rc

if platform.system() == "Darwin":
    rc('font', family='AppleGothic')
elif platform.system() == "Windows":
    rc('font', family='Malgun Gothic')
elif platform.system() == "Linux":
    rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False  # 한글 폰트 적용 시 마이너스 기호 깨짐 방지

# 스트림릿 UI 설정
st.title("동아리 랜덤 배정 프로그램")

# 동아리 및 학생 입력
club_input = st.text_input("동아리 이름 입력 (쉼표로 구분)", "동아리 1, 동아리 2, 동아리 3, 동아리 4, 동아리 5")
student_input = st.text_input("학생 이름 입력 (쉼표로 구분)", "학생 1, 학생 2, 학생 3, 학생 4, 학생 5, 학생 6, 학생 7, 학생 8, 학생 9, 학생 10")

# 입력값을 리스트로 변환
club_names = [club.strip() for club in club_input.split(",") if club.strip()]
student_names = [student.strip() for student in student_input.split(",") if student.strip()]

a = len(club_names)
b = len(student_names)

if st.button("랜덤 배정 시작"):
    if a == 0 or b == 0:
        st.error("동아리 또는 학생을 입력해주세요.")
    else:
        # 학생을 랜덤으로 섞기
        random.shuffle(student_names)
        
        # 배정 결과 저장
        assignments = pd.DataFrame(columns=["학생", "동아리"])
        
        st.subheader("배정 과정")
        process_area = st.empty()
        
        # 랜덤 배정 (균등 분배)
        club_assignments = {club: [] for club in club_names}
        
        for i, student in enumerate(student_names):
            club = club_names[i % a]  # 균등 배정을 위한 모듈러 연산
            club_assignments[club].append(student)
            
            # 실시간 업데이트 (추첨하듯이 보이도록)
            process_area.write(f"🎲 {student} → {club}")
            time.sleep(0.5)
            
            # 데이터 저장
            assignments = pd.concat([assignments, pd.DataFrame([[student, club]], columns=["학생", "동아리"])], ignore_index=True)
        
        # 최종 배정 결과 출력
        st.subheader("최종 배정 결과")
        st.dataframe(assignments)
