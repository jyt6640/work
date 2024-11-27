import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

key=st.secrets['key']

st.header('첫 홈페이지')
url='http://api.sexoffender.go.kr/openapi/SOCitysStats/'
params={
    'serviceKey':key,   
}
response=requests.get(url,params=params)
if response.status_code==200:
    root=ET.fromstring(response.content)
    data=[]
    for city in root.findall('.//City'):
        data.append({
            'city_name':city.find('city-name').text,
            'city_count':int(city.find('city-count').text),
        })
    df=pd.DataFrame(data)
    st.dataframe(df)
df['city_count']=df[['city_count']].astype(int)
df_sorted=df.sort_values(by='city_count',ascending=False).head(10)
mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['font.size'] = 11
mpl.rcParams['axes.unicode_minus'] = False

fig=plt.figure(figsize=(12,6))
sns.barplot(data=df_sorted,x='city_name',y='city_count')
plt.xticks(rotation=45)
plt.title('도시별 성범죄자 수')
st.pyplot(fig)

