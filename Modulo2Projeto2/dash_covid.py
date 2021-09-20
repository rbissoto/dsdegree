from re import T
from covid19dh import covid19
import datetime as dt
import pandas as pd
import numpy as np
import streamlit as st  # versão 0.87
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta # to add days or years

def choose_dataset():
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
    return list_y

def rename_columns(df1):
    df1.rename(columns={
                        'vaccines': 'Vaccines',
                        'tests': 'Tests',
                        'confirmed': 'Confirmed Cases',
                        'recovered': 'Recovered',
                        'deaths': 'Deaths',
                        'administrative_area_level_1': 'Country'
                        }, inplace=True
                    )
def handle_nan(df_h):
    for e in ['Vaccines','Tests','Confirmed Cases','Recovered','Deaths']:
        p = 0
        country = df_h.at[0,'Country']
        for i,b in enumerate(df_h[e].isna()):
            if df_h.at[i,'Country'] == country:
                if b:
                    df_h.at[i,e] = p
                else:
                    p = df_h.at[i,e]
            else:
                country = df_h.at[i,'Country']
                p = 0

def datetime_slider():
    format = 'MMM DD, YYYY'  # format output
    start_date = dt.date(year=2020,month=1,day=22)
    end_date = dt.datetime.now().date()
    slider = st.slider('Select date range', start_date, end_date, (start_date, end_date), format=format)
    #return slider[0].strftime('%Y-%m-%d'),slider[1].strftime('%Y-%m-%d')
    return pd.to_datetime(slider[0]),pd.to_datetime(slider[1])
    #return slider
def convert_to_percentage(df_p):
    df_p['vaccines'] = (df_p['vaccines'] / df_p['population'] / 2)
    df_p['tests'] = (df_p['tests'] / df_p['population'])
    df_p['deaths'] = (df_p['deaths'] / df_p['confirmed'])
    df_p['recovered'] = (df_p['recovered'] / df_p['confirmed'])
    df_p['confirmed'] = (df_p['confirmed'] / df_p['population'] )
    return df_p

# Inserindo texto
st.title('Covid 19 Dashboard')

option = st.selectbox("Which Dashboard?", ('','Single Country', 'Compare Countries', 'Historical Data Animation','World Map'))

df, src = covid19()
countries_list = df["administrative_area_level_1"].unique()
col1,col2 = st.columns(2)
if col1.button('Convert all values to %'):
    df = convert_to_percentage(df)
    percentage = True
else:  
    percentage = False
if col2.button('Convert back to absolute values'):
    df, src = covid19()
rename_columns(df)
if option == '':
    st.write('Instructions:')
    st.write('Single Countr:')
    st.write('Instructions:')
    st.write('Instructions:')
    st.write('Instructions:')
if option == 'Single Country':
    mask_dt = datetime_slider()
    country = st.sidebar.selectbox("Select a country", countries_list)
#    country2 = st.sidebar.text_input("Or type the country name here in English")
    list_y = choose_dataset()
    if not (country):
        st.warning('Please select a country')
        st.stop()
    handle_nan(df)
    if len(list_y) == 0:
        st.warning('Please select at least one data option to display on left between number of vaccines, covid tests, confirmed cases, recovered people and deaths')
        st.stop()
    df = df[(df['date'] >= mask_dt[0]) & (df['date'] <= mask_dt[1])]
 #   if country2:
 #       df, src = covid19(country2)
 #       if percentage:
  #          df = convert_to_percentage(df)
   #     rename_columns(df)
   #     df = df[(df['date'] >= mask_dt[0]) & (df['date'] <= mask_dt[1])]
   #     st.write(px.line(
   #         df,
   #         x='date',
   #         y=list_y,
   #         title=country2)) 
  #  else:
    df = df[df["Country"] == country]
    st.write(px.line(
            df,
            x='date',
            y=list_y,
            title=country))

if option == 'Historical Data Animation':
    countries = st.sidebar.multiselect('Select two or more countries to display animation:',countries_list)
    st.write(len(countries))
    list_x = choose_dataset()
    mask_dt = datetime_slider()
    if len(countries) < 2:
        st.warning('Please select one country to display on the left side')
        st.stop()
    if len(list_x) > 1:
        st.warning('Choosing more than one data element is not allowed, it will cause visualization problems due to difference in scale!')
        st.stop()
    df_ani = df[df['Country'].isin(countries)]
    handle_nan(df_ani)
    df_ani = df_ani[(df_ani['date'] >= mask_dt[0]) & (df_ani['date'] <= mask_dt[1])]
    df_ani['day'] = df_ani['date'].apply(lambda x: str(x.year)+'-'+str(x.month)+'-'+str(x.day))
    fig = px.bar(df_ani, 
            x = list_x[0], 
            y = 'Country',
            color ='Country',
            animation_frame ='day',
            #hover_name ='country',
            #range_x = [0, np.size(df_ani['id'].unique())],
            range_x = [0, df_ani[list_x[0]].max()])
 #   fig.update_layout(xaxis_range=(0, df_ani['Vaccines'].max())
    st.write(fig)

if option == 'Compare Countries':
    mask_dt = datetime_slider()
    countries = st.sidebar.multiselect('Select two or more countries to compare:',countries_list)
    list_y = choose_dataset()
    if len(countries) < 2:
        st.warning('Please select at least two country to display on the left side')
        st.stop()
    if len(list_y) == 0:
        st.warning('Please select at least one set of data to compare')
        st.stop()
    df_compare = df[df['Country'].isin(countries)]
    handle_nan(df_compare)
    df = df[(df['date'] >= mask_dt[0]) & (df['date'] <= mask_dt[1])]
    fig = go.Figure()
    for i in list_y:
        for j in countries:
            df_compare = df[df['Country'] == j]
            fig.add_trace(go.Scatter(
                    x=df_compare.date,
                    y=df_compare[i],
                    mode='lines',
                    name=j+' - '+i
                ))
    st.write(fig)

if option == 'World Map':
    d = choose_dataset()
    mask_dt = datetime_slider()
    if len(d) != 1:
        st.warning('Please select at least one set of data to compare')
        st.stop()
    handle_nan(df)
    df = df[(df['date'] >= mask_dt[0]) & (df['date'] <= mask_dt[1])]
    df['day'] = df['date'].apply(lambda x: str(x.year)+'-'+str(x.month)+'-'+str(x.day))
    fig = px.choropleth(df, locations="id", color=d[0], hover_name="Country", animation_frame="day")#, range_color=[20,80])
    st.write(fig)
    df

st.sidebar.write('Developed for Data Science Degree - Module 2')
st.sidebar.write('by Rafael Bissoto, Felipe Aliprandini, Fabricio Pavanin')
st.sidebar.write('Dataset from covid19dh by:')
st.sidebar.write('Guidotti, E., Ardia, D., (2020), "COVID-19 Data Hub", Journal of Open Source Software 5(51):2376, doi: 10.21105/joss.02376.')
st.stop()