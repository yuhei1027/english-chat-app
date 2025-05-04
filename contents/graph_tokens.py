import pandas as pd
import streamlit as st
import os

st.title('トークン利用状況')
df=pd.read_csv('./log/log.csv')
df['日付']=df['datetime'].apply(lambda x:x.split(' ')[0])
df['日付']=df['日付'].apply(lambda x:x.split('-')[0]+'/'+x.split('-')[1]+'/'+x.split('-')[2])
df=df.groupby(['日付','model'])['total_tokens'].sum().reset_index()
df=df.pivot(index='日付',columns='model',values='total_tokens')
cols=df.columns.tolist()
df=df.reset_index()
st.bar_chart(
   df, x='日付', y=cols
)