import pandas as pd
import streamlit as st
import numpy as np
import folium
import geopandas as gpd

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from datetime import datetime

import plotly.express as px

st.set_page_config(layout = 'wide')
##################################################

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data

def set_feature(data):
    data['preco_ft2'] = data['price'] / data['sqft_lot']
    return data

def overview_data(data):
    f_zipcode = st.sidebar.multiselect('Escolha o zipcode',data['zipcode'].unique())

    st.title('Visão geral')


    st.write(data)

    c1,c2 = st.columns((2,1))

    df1 = data[['id','zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price','zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living','zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['preco_ft2','zipcode']].groupby('zipcode').mean().reset_index()

    m1 = pd.merge(df1,df2,on='zipcode',how='inner')
    m2 = pd.merge(m1, df3, on='zipcode',how='inner')
    df = pd.merge(m2, df4, on ='zipcode',how='inner')

    df.columns=['zipcode','total_houses','price_mean','sqft_living_mean','preco_ft2_mean']

    c1.header('Valores médios por codigo postal')
    c1.write(df)

    data_copy = data.copy()

    num_attributes = data_copy.select_dtypes(include=['int64','float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))
    max = pd.DataFrame(num_attributes.apply(np.max))
    min = pd.DataFrame(num_attributes.apply(np.min))

    df_est = pd.concat([max,min,media,mediana,std],axis=1).reset_index()
    df_est.columns = ['attributes','max','min','mean','median','std']

    c2.header('Estatística descritiva')
    c2.write(df_est)

    return None

def portfolio_density(data,geofile):
    st.title('Visão da região')

    c1, c2 = st.columns((1, 1))
    df=data.copy()
    c1.header('Densidade de portfólio')

    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                             default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Price r${0} on : {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, {5} year built'.format(
                          row['price'],
                          row['date'],
                          row['sqft_living'],
                          row['bedrooms'],
                          row['bathrooms'],
                          row['yr_built']
                      )).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    c2.header('Densidade de preços')

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

    geofile = geofile[geofile['ZIP'].isin(df['zipcode'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(),
                                            data['long'].mean()],
                                  default_zoom_start=15)

    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['zipcode', 'price'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opaticy=0.7,
                                line_opacity=0.2,
                                legend_name='Average price')

    with c2:
        folium_static(region_price_map)
    return None

def commercial_at(data):
    st.sidebar.title('Opções comerciais')
    st.title('Atributos comerciais')

    min_yr_built = int(data['yr_built'].min())
    max_yr_built = int(data['yr_built'].max())

    st.sidebar.subheader('Selecione o ano máximo')
    f_yr_built = st.sidebar.slider('Ano construído', min_yr_built,
                                   max_yr_built,
                                   min_yr_built)

    st.header('Média de preço por ano de construção')

    df = data.loc[data['yr_built'] <= f_yr_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    fig = px.line(df, x='yr_built', y='price')

    st.plotly_chart(fig, use_container_width=True)

    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    st.header('Média dos preços por dia')
    st.sidebar.subheader('Selecione a data máxima')

    f_date = st.sidebar.slider('Date', min_date,
                               max_date,
                               min_date)

    data['date'] = pd.to_datetime(data['date'])
    df = data.loc[data['date'] <= f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    st.header('Distribuição de preços')
    st.sidebar.subheader('Selecione o preço máximo')

    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    avg_price = int(data['price'].mean())

    f_price = st.sidebar.slider('Preço', min_price, max_price, avg_price)
    df = data.loc[data['price'] <= f_price]

    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    return None

def attributes_dist(data):
    st.sidebar.title('Opções de atributos')
    st.title('Atributos das casas')

    f_bedrooms = st.sidebar.selectbox('Número máximo de quartos', sorted(set(data['bedrooms'].unique())))

    f_bathrooms = st.sidebar.selectbox('Número máximo de banheiros', sorted(set(data['bathrooms'].unique())))

    f_floors = st.sidebar.selectbox('Número máximo de andares', sorted(set(data['floors'].unique())))

    f_water_view = st.sidebar.checkbox('Selecione se a casa tem visão para água')

    c1, c2 = st.columns(2)

    # Casa por quarto
    c1.header('Casas por número de banheiros')
    df = data[data['bedrooms'] <= f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # Casa por banheiro
    c2.header('Casas por número de banheiros')
    df = data[data['bathrooms'] <= f_bathrooms]
    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    c1.header('Número de andares por casa')
    df = data[data['floors'] <= f_floors]
    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # Casa por visão d'água
    if f_water_view:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()

    c2.header('Visão do mar ')
    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)
    return None

#######################################################

if __name__ == "__main__":
    # ETL
    # Extração de dados
    path = 'dados_tratados.csv'
    data = get_data(path)
    geofile = gpd.read_file('Zip_Codes.geojson')

    # Transformação de dados
    data = set_feature(data)

    overview_data(data)

    portfolio_density(data,geofile)

    commercial_at(data)

    attributes_dist(data)




