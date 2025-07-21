# generate_map.py
import requests, folium

lat, lon = 22.998925, 120.217366
relation_id = 12731746
url = "https://overpass-api.de/api/interpreter"
query = f"""
[out:json];
area({relation_id})->.searchArea;
(
  node["amenity"="toilets"](area.searchArea);
);
out center;
"""

r = requests.post(url, data=query)
data = r.json()

m = folium.Map(location=[lat, lon], zoom_start=17)

for el in data['elements']:
    if 'lat' in el and 'lon' in el:
        tags = el.get('tags', {})
        popup = f"<b>OSM ID:</b> {el['id']}<br>"
        popup += "<br>".join([f"<b>{k}:</b> {v}" for k, v in tags.items()])
        color = 'green' if tags.get('wheelchair') == 'yes' else 'blue'
        folium.Marker(
            location=[el['lat'], el['lon']],
            popup=folium.Popup(popup, max_width=300),
            icon=folium.Icon(color=color)
        ).add_to(m)

m.save("toilets_map.html")
