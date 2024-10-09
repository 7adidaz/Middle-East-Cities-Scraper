import json
import folium
from folium.plugins import MarkerCluster

# Load the JSON data
with open('middle_east_cities_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create a map centered on the Middle East
m = folium.Map(location=[29.2985, 42.5510], zoom_start=5)

# Create a MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

# Iterate through countries and cities
for country, cities in data.items():
    for city in cities:
        # Extract city information
        name = city['name']
        population = city['population']
        lat = city['center']['latitude']
        lon = city['center']['longitude']
        radius = city['estimated_radius_km']

        # Create a circle marker
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            popup=f"<strong>{name}</strong><br>Population: {population}<br>Estimated Radius: {radius:.2f} km",
            color='red',
            fill=True,
            fillColor='red'
        ).add_to(marker_cluster)

        # Create a circle to represent the city's estimated area
        folium.Circle(
            location=[lat, lon],
            radius=radius * 1000,  # Convert km to meters
            color='blue',
            fill=False,
            popup=f"{name} estimated area"
        ).add_to(m)

# Save the map
m.save("middle_east_cities_map.html")

print("Map has been saved as middle_east_cities_map.html")
