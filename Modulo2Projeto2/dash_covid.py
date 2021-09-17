from re import T
import yfinance as yf
from covid19dh import covid19
import datetime as dt
import pandas as pd
import numpy as np
import streamlit as st  # versão 0.87
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Inserindo texto
st.title('Covid 19 Dashboard for Module 2')
st.subheader('by Rafael,Felipe,Fabricio')

option = st.sidebar.selectbox("Which Dashboard?", ('','Single Country', 'Compare Countries', 'Historical Data Animation'))
st.header(option)
#def rename_columns(df1):
#    df1.rename(columns= {
#                        'vaccines': 'Vaccines',
#                        'tests': 'Tests',
#                       'confirmed': 'Confirmed Cases',
 #                       'recovered': 'Recovered',
 #                       'deaths': 'Deaths'
 #                       }, inplace=True
 #                   )
 #   return df1

if option == 'Single Country':
    df, src = covid19()
    country = st.sidebar.selectbox("Select a country", (df["id"].unique()))
    country2 = st.sidebar.text_input("Or type the country name here in English")
    if not (country or country2):
        st.warning('Please select a country')
        st.stop()
    #list_y = ['Vaccines','Tests','Confirmed Cases','Recovered','Deaths']
    list_y = []
    if st.sidebar.checkbox('Vaccines'):
        list_y.append('Vaccines')   
    if st.sidebar.checkbox('Tests'):
        list_y.append('Tests') 
    if st.sidebar.checkbox('Confirmed Cases'):
        list_y.append('Confirmed Cases') 
    if st.sidebar.checkbox('Recovered'):
        list_y.append('Recovered') 
    if st.sidebar.checkbox('Deaths'):
        list_y.append('Deaths') 
    
        
    if len(list_y) == 0:
        st.warning('Please select at least one data option to display')
        st.stop()
    st.write(str(list_y))
    if country2:
        df, src = covid19(country2)
        df.rename(columns= {
                        'vaccines': 'Vaccines',
                        'tests': 'Tests',
                        'confirmed': 'Confirmed Cases',
                        'recovered': 'Recovered',
                        'deaths': 'Deaths'
                        }, inplace=True
                    )
        st.write(px.line(
            df,
            x='date',
            y=['Vaccines','Deaths'],
            title=country2))
        df
    else:
        df, src = covid19(country)
        df.rename(columns= {
                        'vaccines': 'Vaccines',
                        'tests': 'Tests',
                        'confirmed': 'Confirmed Cases',
                        'recovered': 'Recovered',
                        'deaths': 'Deaths'
                        }, inplace=True
                    )
        st.write(px.line(df,
        x='date',
        y=['Vaccines','Deaths'],
        title=country))
        df

st.sidebar.write('Data from covid19dh by:')
st.sidebar.write('Guidotti, E., Ardia, D., (2020), "COVID-19 Data Hub", Journal of Open Source Software 5(51):2376, doi: 10.21105/joss.02376.')

st.stop()
if option == 'Historical Data Animation':
    option2 = st.sidebar.selectbox("Which Dashboard?", ('vaccines', 'tests', 'confirmed', 'recovered', 'deaths'))


df, src = covid19("BRA")
fig = go.Figure()
fig.add_trace(go.Scatter(
                    x=df.date,
                    y=df.vaccines,
                    mode='lines',
                    name='Apple'
                ))
st.write(fig)

#st.line_chart(data=df["date","vaccines"])

# Inserindo markdown
st.markdown('Aqui é um texto **negrito** $y=ax+b$')

st.markdown('Texto Latex $y=ax+b$')

# Escrevendo objetos

st.write('1 + 1 = ', 2)

df = pd.DataFrame({'a': [1,2], 'b': [3,4]})

st.write('Acima dataframe', df, 'Abaixo DF')

df = pd.DataFrame(np.random.randn(10, 20))

# Destacando valor máximo de cada coluna
st.dataframe(df.style.highlight_max(axis=0))

# Metricas  -> Ou tile ou card
col1, col2, col3, col4, col5 = st.columns(5)
col2.metric('Temperatura', '34°C', '-20°C')
col3.metric('Dia da semana', 'Segunda')
col4.metric('Umidade', '80%', '+70%')

# checkbox
if_filter = st.checkbox('Filtrar valores positivo?')
st.write(if_filter)

st.text('Filtrou?')
if if_filter:
    df_filtered = df[df>0].copy()
else:
    df_filtered = df.copy()
st.write(df_filtered.fillna(-999))

# Radio button

filme = st.radio(
    'Qual seu filme favorito',
    ('Comedia', 'Terror', 'Romance')  # Opções
)

st.write(filme, type(filme))

if filme == 'Comedia':
    st.write('Você é uma pessoa feliz')
    
else:
    st.write('Você é uma pessoa triste')
    
# Select box

filme_box = st.selectbox(
    'Qual seu filme favorito',
    ('Comedia', 'Terror', 'Romance')  # Opções
)
if filme_box == 'Comedia':
    st.write('Você é uma pessoa feliz')
    
else:
    st.write('Você é uma pessoa triste')

# Sliders
idade = st.slider('Qual sua idade', 0, 100, 37)

st.write(idade)

# Input
nome = st.text_input('Qual seu nome?', 'Escreva seu nome aqui')

st.write(nome, type(nome))

# Date input, date picker

d = st.date_input(
    'Qual sua a data de nascimento')

st.write(d)



# Emoji
# https://raw.githubusercontent.com/MarcSkovMadsen/awesome-streamlit/master/gallery/emojis/emojis.py
st.markdown(':poop:')


# Multiselect
options = st.multiselect('Escolha a ação',
                        ['AMZN', 'GOOG', 'APPL'])

st.write(options, type(options))

# Color picker
color = st.color_picker('Escolha uma cor')

st.write(src)