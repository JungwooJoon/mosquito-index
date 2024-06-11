import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from pingouin import ttest
from utils import load_TempData
from utils import load_MosquitoData

from district import area
from mosquito import mosq_pred
def weather(mosquit_df, temp_df):
    st.markdown('#### 날씨와 모기지수간에 차이검정')
    month = st.selectbox("확인하고자 하는 월", [5,6,7,8,9,10])
    
    temp_df['날짜'] = pd.to_datetime(temp_df['날짜'], format='%Y-%m-%d', errors='coerce')
    temp_df['month'] = temp_df['날짜'].dt.month
    mosquit_df['MOSQUITO_DATE'] = pd.to_datetime(mosquit_df['MOSQUITO_DATE'], format='%Y-%m-%d', errors='coerce')
    mosquit_df['month'] = mosquit_df['MOSQUITO_DATE'].dt.month
    
    temp_month = temp_df[temp_df['month'] == month]
    mosquit_month = mosquit_df[mosquit_df['month'] == month]
    
    mosquit_month['MOSQUITO_VALUE_HOUSE'] = pd.to_numeric(mosquit_month['MOSQUITO_VALUE_HOUSE'], errors='coerce')
    
    st.markdown(f'2023 {month}월의 온도와 모기지수의 차이검정')
    st.dataframe(ttest(mosquit_month['MOSQUITO_VALUE_HOUSE'], temp_month['온도 평균(℃)'], paired=False))
    
    st.markdown(f'2023 {month}월의 습도와 모기지수의 차이검정')
    st.dataframe(ttest(mosquit_month['MOSQUITO_VALUE_HOUSE'], temp_month['습도 평균(%)'], paired=False))
    
def weather_home():
    
    mosquit_df = load_MosquitoData()
    temp_df = load_TempData()
    
    st.markdown("## 날씨 확인 \n"
    "2023 데이터의 온도 및 습도를 확인할 수 있습니다.")
    
    selected = option_menu(None, ['모기와 날씨', '자치구', '모기지수'],
                          icons=['cloud', 'pin-map', 'bug'],
                          menu_icon='cast', default_index=0, orientation='horizontal',
                          styles={
                              'container' : {
                                  'padding' : '0',
                                  'backgroung-color' : '#808080'
                              },
                              'icon' : {
                                  'color' : 'red',
                                  'font-size' : '25px'
                              },
                              'nav-link':{
                                  'font-size' : '15px',
                                  'text-align' : 'left',
                                  'margin' : '0px',
                                  '--hover-color' : '#eee'
                              },
                              'nav-link-selected' : {
                                  'background-color' : '#555',
                                  'color' : 'white'
                              }
                          })
    
    if selected == '모기와 날씨' :
        weather(mosquit_df, temp_df)
    elif selected == '자치구' :
        area(temp_df)
    elif selected == '모기지수' :
        mosq_pred(mosquit_df, temp_df)
    else:
        st.warning('오류')