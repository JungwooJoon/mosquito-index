import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from prophet import Prophet

def pred() :
    st.markdown("## 모기 예측 \n"
    "습도, 온도를 기반으로 주거지의 모기 지수를 예측합니다")
    st.write("---") 
    total_df = pd.read_csv('mortgages.csv')
    total_df['MOSQUITO_DATE'] = pd.to_datetime(total_df['MOSQUITO_DATE'], format='%Y-%m-%d')
    
    types = ['물가', '주거지', '공원']
    df_types = ['MOSQUITO_VALUE_WATER', 'MOSQUITO_VALUE_HOUSE', 'MOSQUITO_VALUE_PARK']
    
    periods = 30
    
    for i,j in enumerate(types):
        model = Prophet()
        
        summary_df = total_df[['MOSQUITO_DATE', df_types[i]]]
        summary_df = summary_df.rename(columns = {'MOSQUITO_DATE' : 'ds', df_types[i] : 'y'})
        
        model.fit(summary_df)
        
        future1 = model.make_future_dataframe(periods=periods)
        
        forcast1 = model.predict(future1)
        
        fig = model.plot(forcast1, uncertainty=True)
        st.markdown(f"#### {j}의 모기지수")
        st.pyplot(fig)
