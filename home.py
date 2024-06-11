import pandas as pd
import streamlit as st
import requests
from datetime import datetime

def run_home() :
    st.markdown("## 모기지수 \n"
    "서울지역의 모기 발생 현황을 알기 쉽게 발생 단계별로 나누어\
    시민 행동요령을 알려주는 일일 모기 발생 예보 서비스입니다.")

    tab1, tab2 = st.tabs(["오늘 날짜 보기", "다른 날짜 보기"])
    
    with tab1:
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        mosquit_list = get_mosquit(today)
        
        area_list = ['수변부', '주거지', '공원']
        
        st.subheader(f'오늘({mosquit_list[0]})의 모기지수')
        for i,j in enumerate(area_list):
            st.markdown(f'{j}의 모기지수: {mosquit_list[i+1]}')
    with tab2:
        year = st.selectbox("년도", [2024, 2023, 2022])
        month = st.selectbox("월", [5,6,7,8,9,10])
        day = st.selectbox("일", range(1,32))
        date = f'{year}-{month:02d}-{day:02d}'
        st.subheader(f'{date}의 모기지수')
        
        
        if type(get_mosquit(date)) is str:
            st.markdown(get_mosquit(date))
        else:
            mosquit_list = get_mosquit(date)
            area_list = ['수변부', '주거지', '공원']
            
            for i,j in enumerate(area_list):
                st.markdown(f'{j}의 모기지수: {mosquit_list[i+1]}')
            


def get_mosquit(date):
    key = '584f516242776a6439344e7370484c'

    url = f'http://openapi.seoul.go.kr:8088/{key}/json/MosquitoStatus/1/1/{date}'
    response = requests.get(url)

    data = response.json()
    
    if 'MosquitoStatus' in data:
        result = data['MosquitoStatus'].get('RESULT', {})
    else:
        result = data.get('RESULT', {})
    if result['CODE'] == 'INFO-000':
        df = pd.DataFrame(data['MosquitoStatus']['row'])
        return df.iloc[0].tolist()
    if result['CODE'] == 'INFO-200':
        return '해당 연월일은 존재하지 않습니다.'
    else:
        return '오류가 발생하였습니다.'


    
