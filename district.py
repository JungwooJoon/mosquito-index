import pandas as pd
import streamlit as st
import requests
from datetime import datetime
import geopandas as gpd
import matplotlib.pyplot as plt

def area(temp_df) :
    st.markdown("#### 해당 구의 날씨를 확인할 수 있습니다.")

    seoul_gpd = gpd.read_file('seoul_sig.geojson')
    
    seoul_gpd = seoul_gpd.set_crs(epsg='5178', allow_override=True)
    seoul_gpd['center_point'] = seoul_gpd['geometry'].geometry.centroid
    seoul_gpd['geometry'] = seoul_gpd['geometry'].to_crs(epsg=4326)
    seoul_gpd['center_point'] = seoul_gpd['center_point'].to_crs(epsg=4326)
    seoul_gpd['경도'] = seoul_gpd['center_point'].map(lambda x: x.xy[0][0])
    seoul_gpd['위도'] = seoul_gpd['center_point'].map(lambda x: x.xy[1][0])

    month = st.selectbox("월", range(1,13))
    day = st.selectbox("일", range(1,32))
    if month and day == 1:
        st.markdown('\n ### 해당 연월일은 데이터가 없습니다.')
    else:
        summary_df = temp_df[temp_df['날짜']==f'2023-{month:02d}-{day:02d}']
        summary_df = summary_df.rename(columns={'자치구':'SIG_ENG_NM'})
        
        merge_df = seoul_gpd.merge(summary_df, on='SIG_ENG_NM')
        
        fig, ax = plt.subplots(ncols=2, sharey=True, figsize=(15, 10))
        
        merge_df.plot(ax=ax[0], column='온도 평균(℃)', cmap='OrRd', legend=False, alpha=0.9)
        merge_df.plot(ax=ax[1], column='습도 평균(%)', cmap='OrRd', legend=False, alpha=0.9)

        patch_col = ax[0].collections[0]
        cb = fig.colorbar(patch_col, ax=ax, shrink=0.5, location = 'left')
        
        patch_col = ax[1].collections[0]
        cb = fig.colorbar(patch_col, ax=ax, shrink=0.5)
        
        ax[0].set_title(f'2023-{month:02d}-{day:02d} Temperatures(℃)')
        ax[1].set_title(f'2023-{month:02d}-{day:02d} humidity(%)')  
        
        ax[0].set_axis_off()
        ax[1].set_axis_off()
        
        st.pyplot(fig)
