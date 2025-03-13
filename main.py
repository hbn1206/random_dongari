import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import matplotlib.pyplot as plt
from matplotlib import rc
import platform

# 한글 폰트 설정 (MacOS, Windows 대응)
if platform.system() == "Darwin":
    rc('font', family='AppleGothic')
elif platform.system() == "Windows":
    rc('font', family='Malgun Gothic')

# 스트림릿 UI 설정
st.title("동아리 랜덤 배정 프로그램")

# 사용자 입력 받기
a = st.number_input("동아리 개수 입력", min_value=1, value=5)
b = st.number_input("학생 수 입력", min_value=1, value=20)

# 동아리 이름 입력
default_club_names = [f"동아리 {i+1}" for i in range(a)]
club_names = []
for i in range(a):
    club_names.append(st.text_input(f"동아리 {i+1} 이름", value=default_club_names[i]))

# 학생 이름 입력
default_student_names = [f"학생 {i+1}" for i in range(b)]
student_names = []
for i in range(b):
    student_names.append(st.text_input(f"학생 {i+1} 이름", value=default_student_names[i]))

if st.button("배정 시작"):
    # 학생을 랜덤으로 섞기
    random.shuffle(student_names)
    
    # 배정 결과를 저장할 데이터프레임
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
        time.sleep(0.5)  # 애니메이션 효과
        
        # 데이터 저장
        assignments = pd.concat([assignments, pd.DataFrame([[student, club]], columns=["학생", "동아리"])], ignore_index=True)
    
    # 최종 배정 결과 출력
    st.subheader("최종 배정 결과")
    st.dataframe(assignments)
    
    # 시각화: 동아리별 학생 수 그래프
    st.subheader("동아리별 학생 수 시각화")
    club_counts = {club: len(members) for club, members in club_assignments.items()}
    
    fig, ax = plt.subplots()
    ax.bar(club_counts.keys(), club_counts.values(), color='skyblue')
    ax.set_xlabel("동아리")
    ax.set_ylabel("학생 수")
    ax.set_title("동아리별 학생 수 분포")
    ax.set_xticklabels(club_counts.keys(), rotation=45)
    
    st.pyplot(fig)
