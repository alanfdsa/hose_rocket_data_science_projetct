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

def overview_data(data):

    st.title('Visão geral dos dados')

    st.write(data)

    return None

def portfolio_density(data,geofile):

    st.title('Visão da região')

    # f_attributes = st.multiselect('Selecione a classe do imóvel', data['dormitory_type'].unique())
    f_zipcode = st.multiselect('Escolha o zipcode', data['zipcode'].unique())


    if (f_zipcode != [] and (f_attributes) != []):
        data = data.loc[[data['zipcode'].isin(f_zipcode),pd.DataFrame(f_attributes)]]
    elif (f_zipcode != [] and (f_attributes) == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]
    elif (f_zipcode == [] and (f_attributes) != []):
        data = data.loc[:, data['dormitory_type'].isin(f_attributes)]
    else:
        data = data.copy()


    c1, c2 = st.columns((1, 1))
    df=data.copy()
    c1.header('Densidade de portfólio')

    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                             default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Price r${0}. Class: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms'.format(
                          row['preco_venda'],
                          row['dormitory_type'],
                          row['sqft_living'],
                          row['bedrooms'],
                          row['bathrooms']
                      )).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    c2.header('Densidade de preços')

    df = data[['preco_venda', 'zipcode']].groupby('zipcode').mean().reset_index()

    geofile = geofile[geofile['ZIP'].isin(df['zipcode'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(),
                                            data['long'].mean()],
                                  default_zoom_start=15)

    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['zipcode', 'preco_venda'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opaticy=0.7,
                                line_opacity=0.2,
                                legend_name='Average price')

    with c2:
        folium_static(region_price_map)
    return None

def commercial_at(data):
    st.sidebar.title('Opções para os histogramas')
    st.title('Histogramas')


    st.header('Distribuição de preços')
    st.sidebar.subheader('Selecione o preço máximo')

    min_price = int(data['preco_venda'].min())
    max_price = int(data['preco_venda'].max())
    avg_price = int(data['preco_venda'].mean())

    f_price = st.sidebar.slider('Preço', min_price, max_price, avg_price)
    df = data.loc[data['preco_venda'] <= f_price]

    fig = px.histogram(df, x='preco_venda', nbins=50)
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
    c1.header('Casas por número de quartos')
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
    path = 'dados_port.csv'
    data = get_data(path)
    geofile = gpd.read_file('Zip_Codes.geojson')

    # Transformação de dados

    overview_data(data)

    portfolio_density(data,geofile)

    commercial_at(data)

    attributes_dist(data)




