import pandas as pd

def load_TempData():
    df = pd.read_csv('weather.csv', encoding='cp949')
    return df

def load_MosquitoData():
    df = pd.read_csv('mortgages.csv')
    return df