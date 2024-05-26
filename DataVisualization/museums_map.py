import json
import folium
import requests

# we load museums json data
with open('DataVisualization/museums.json') as f:
    museums = json.load(f)

# we convert museums addres to coordinates by using  Nominatim API
def get_coordinates(address):
    url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers, timeout=10)  # Zaman aşımını 10 saniye olarak ayarla
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
    return None, None

# we create map
map = folium.Map(location=[0, 0], zoom_start=2)

# we add museums to map
for museum in museums:
    address = f"{museum['address']}, {museum['city']}, {museum['country']}"
    lat, lon = get_coordinates(address)
    if lat and lon:
        folium.Marker(
            location=[float(lat), float(lon)],
            popup=museum['museum_name'],
            tooltip=address
        ).add_to(map)

# we create html code and map
map.save('DataVisualization/museums_map.html')
