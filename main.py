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
club_input = st.text_area("동아리 이름과 모집 인원 입력 (형식: 동아리1-5, 동아리2-3, ...)", "동아리 1-5, 동아리 2-3, 동아리 3-4, 동아리 4-2, 동아리 5-6")
student_input = st.text_area("학생 이름 입력 (쉼표로 구분)", "학생 1, 학생 2, 학생 3, 학생 4, 학생 5, 학생 6, 학생 7, 학생 8, 학생 9, 학생 10")

# 동아리 및 모집 인원 파싱
club_info = [club.strip() for club in club_input.split(",") if club.strip()]
club_data = {}
for club in club_info:
    try:
        name, capacity = club.rsplit("-", 1)
        club_data[name.strip()] = int(capacity.strip())
    except ValueError:
        st.error("입력 형식이 올바르지 않습니다. 예: 동아리1-5, 동아리2-3")
        st.stop()

student_names = [student.strip() for student in student_input.split(",") if student.strip()]

a = len(club_data)
b = len(student_names)

assignments = pd.DataFrame(columns=["학생", "동아리"])
result_area = st.empty()
final_result_displayed = False

if st.button("랜덤 배정 시작"):
    if a == 0 or b == 0:
        st.error("동아리 또는 학생을 입력해주세요.")
    else:
        # 학생을 랜덤으로 섞기
        random.shuffle(student_names)
        
        process_area = st.empty()
        
        # 동아리별 배정 인원 관리
        club_assignments = {club: [] for club in club_data.keys()}
        
        for student in student_names:
            available_clubs = [club for club in club_data.keys() if len(club_assignments[club]) < club_data[club]]
            if not available_clubs:
                st.warning("모든 동아리가 정원이 초과되었습니다. 일부 학생은 배정되지 않을 수 있습니다.")
                break
            
            # 동아리명 애니메이션 효과
            for _ in range(10):  # 10번 랜덤하게 바꿈
                temp_club = random.choice(list(club_data.keys()))
                process_area.markdown(f"<h2 style='text-align: center;'>🎲 {student} → {temp_club}</h2>", unsafe_allow_html=True)
                time.sleep(0.1)
            
            # 최종 결정된 동아리
            club = random.choice(available_clubs)
            club_assignments[club].append(student)
            
            # 결과 표시 후 잠시 멈춤
            process_area.markdown(f"<h2 style='text-align: center; color: green;'>✅ {student} → {club}</h2>", unsafe_allow_html=True)
            time.sleep(0.5)
            
            # 데이터 저장
            assignments = pd.concat([assignments, pd.DataFrame([[student, club]], columns=["학생", "동아리"])], ignore_index=True)
            
            # 최종 배정 결과 업데이트 (누적 표시, 한 번만 헤더 출력)
            if not final_result_displayed:
                st.subheader("최종 배정 결과")
                final_result_displayed = True
            result_area.dataframe(assignments)
