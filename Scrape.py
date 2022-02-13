from urllib import response
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)                 


def get_requests():
    result = requests.get("https://www.ilimiz.net/il-plaka-kodlari.html")
    return result


def get_data(response):
    soup = BeautifulSoup(response.content, "lxml")
    data = soup.find_all("span", {"class": "sehir op"})
    return data


def data_preprocessing(data):
    dataframe = pd.DataFrame(data, columns=["city_name", "empty", "plate_code"])
    
    dataframe['plate_code'] = dataframe['plate_code'].str.replace('Nerenin Plakası', '').str.strip()
    dataframe = dataframe.drop(columns=['empty'])
    dataframe['city_name'] = dataframe['city_name'].astype(str).str.replace('<strong>', '').str.replace("</strong>", "")

    return dataframe

def df_to_db(dataframe : pd.DataFrame):
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    dataframe.to_sql("CityPlateCode", conn, if_exists='replace', index=False)
    

def convert_df_to_csv(df):
    return df.to_csv(index=False)


    
    
    
    
    