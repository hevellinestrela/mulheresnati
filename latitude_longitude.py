from geopy.geocoders import Nominatim
import pandas as pd
import time

# Suponha que `df` é o seu DataFrame que contém as colunas 'Cidade' e 'Estado'
df = pd.read_csv('./data/data_clean.csv', sep=';', encoding='latin-1') # Descomente e altere para o caminho do seu arquivo

geolocator = Nominatim(user_agent="geoapiExercises")

def get_lat_lon(city, state):
    try:
        dados = f"{city}, {state}, Brasil"
        print(dados)
        location = geolocator.geocode(dados)
        print(location)
        return (location.latitude, location.longitude)
    except Exception as e: 
        print(e)
        return (None, None)

# Adicione colunas de latitude e longitude ao DataFrame
df['Latitude'], df['Longitude'] = zip(*df.apply(lambda row: get_lat_lon(row['Cidade'], row['Estado']), axis=1))

# Aguarda um segundo entre as chamadas para evitar o bloqueio do IP por fazer muitas requisições em um curto período de tempo
time.sleep(2)

df.to_csv('./data/data_final.csv', sep=';')
