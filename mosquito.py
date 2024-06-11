import pandas as pd
import streamlit as st
import requests
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def mosq_pred(mosquit_df, temp_df) :
    st.markdown("#### 온도, 습도를 기반으로 모기지수를 예측합니다.")
    
    temp = st.number_input("온도를 입력하세요.")
    humidity = st.number_input("습도를 입력하세요.")
    
    temp_df = temp_df.rename(columns={'날짜':'MOSQUITO_DATE'})
    new_df = mosquit_df.merge(temp_df, on='MOSQUITO_DATE')
    
    df = pd.DataFrame(new_df)
    
    X = new_df[['온도 평균(℃)','습도 평균(%)']]
    y = new_df['MOSQUITO_VALUE_HOUSE']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    if temp and humidity is '':
        st.write("데이터를 입력하세요")
    else:
        y_pred = model.predict([[temp, humidity]])
        result = int(y_pred)
        st.markdown(f'{result}')