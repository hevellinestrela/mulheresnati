import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

# Função para carregar os dados
def load_data(filepath):
    data = pd.read_csv(filepath, sep=';', encoding='latin-1')
    return data

def load_and_clean_data(filepath):
    data = load_data(filepath)
    
    # Função para limpar valores de latitude e longitude
    def clean_coord(value):
        # Remove pontos e substitui por nada, convertendo em seguida para float
        try:
            cleaned_value = float(value.replace('.', '').replace(',', '.'))
        except ValueError:
            cleaned_value = None  # Retorna None para valores que não podem ser convertidos
        return cleaned_value
    
    # Aplica a função de limpeza para as colunas de latitude e longitude
    data['Latitude'] = data['Latitude'].astype(str).apply(clean_coord)
    data['Longitude'] = data['Longitude'].astype(str).apply(clean_coord)
    
    # Remover linhas onde latitude ou longitude são None (não puderam ser convertidos)
    data = data.dropna(subset=['Latitude', 'Longitude'])
    
    return data

# Função para gerar mapa com PyDeck (para detalhes geográficos, como cidades e estados)
def generate_map(data, lat_col, lon_col, tooltip_cols=[]):
    view_state = pdk.ViewState(latitude=data[lat_col].mean(), longitude=data[lon_col].mean(), zoom=4)
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

# Carregar dados
data_file = './dados.csv'  # Substitua pelo caminho real do seu arquivo
data = load_and_clean_data(data_file)

st.title('Mulheres na TI')

fig = px.histogram(data, x='Periodo', nbins=20, title='Programas por ano')
st.plotly_chart(fig)

state_counts = data['Estado'].value_counts().reset_index(name='count')
state_counts.rename(columns={'index': 'Estado'}, inplace=True)
fig = px.pie(state_counts, values='count', names='Estado', title='Distribuição de Programas por Estado')
st.plotly_chart(fig)

generate_map(data, 'Latitude', 'Longitude', ['Nome', 'Cidade', 'Estado'])

data
