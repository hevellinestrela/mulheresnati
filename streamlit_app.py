import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

def load_data(filepath):
    data = pd.read_csv(filepath, sep=';')
    return data

def load_and_clean_data(filepath):
    data = load_data(filepath)
    data = data.dropna(subset=['Latitude', 'Longitude'])
    
    return data

def generate_map(data, lat_col, lon_col, tooltip_cols=[]):
    view_state = pdk.ViewState(latitude=data[lat_col].mean(), longitude=data[lon_col].mean(), zoom=3)
    layer = pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position=[lon_col, lat_col],
        get_color="[200, 30, 0, 160]",
        get_radius=20000,
        pickable=True
    )
    tool_tip = {"html": "<b>" + "</b><br><b>".join(tooltip_cols) + "</b>", "style": {"backgroundColor": "steelblue", "color": "white"}}
    map = pdk.Deck(map_style="mapbox://styles/mapbox/light-v9", initial_view_state=view_state, layers=[layer], tooltip=tool_tip)
    st.pydeck_chart(map)

data_file = './dados_final.csv'
data = load_and_clean_data(data_file)

st.title('Mulheres na TI')

fig = px.histogram(data, x='Periodo', nbins=20, title='Programas por ano')
fig.update_layout(bargap=0.2)
st.plotly_chart(fig)

state_counts = data['Estado'].value_counts().reset_index(name='count')
state_counts.rename(columns={'index': 'Estado'}, inplace=True)
fig = px.pie(state_counts, values='count', names='Estado', title='Distribuição de Programas por Estado')
st.plotly_chart(fig)

tipo_count = data['Tipo'].value_counts().reset_index(name='count')
tipo_count.rename(columns={'index': 'Tipo'}, inplace=True)
fig = px.pie(tipo_count, values='count', names='Tipo', title='Distribuição de Programas por Tipo de Instituição')
st.plotly_chart(fig)

fig = px.sunburst(
    data,
    path=['Estado', 'Região'],
    title='Distribuição de Programas por Estado e Região',
)
st.plotly_chart(fig)

generate_map(data, 'Latitude', 'Longitude', ['Nome', 'Cidade', 'Estado'])

data
