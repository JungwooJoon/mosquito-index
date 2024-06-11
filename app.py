import streamlit as st
from streamlit_option_menu import option_menu
from home import run_home
from weather import weather_home
from prediction import pred

def main() :
    with st.sidebar:
        selected = option_menu('메뉴', ['오늘의 모기지수', '날씨 확인', '모기분석 예측'],icons=['bug', 'thermometer-half', 'graph-up-arrow'], menu_icon='cast', default_index=0)
        
    if selected == '오늘의 모기지수':
        run_home()
    elif selected == '날씨 확인' :
        weather_home()
    elif selected == '모기분석 예측' :
        pred()
    else:
        print('error')

if __name__ == "__main__":
    main()