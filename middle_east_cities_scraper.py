import requests
import json
from math import radians, sin, cos, sqrt, atan2
import re


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def estimate_radius(bbox):
    center_lat = (bbox["min_lat"] + bbox["max_lat"]) / 2
    center_lon = (bbox["min_lon"] + bbox["max_lon"]) / 2

    distances = [
        haversine_distance(center_lat, center_lon, bbox["min_lat"], bbox["min_lon"]),
        haversine_distance(center_lat, center_lon, bbox["min_lat"], bbox["max_lon"]),
        haversine_distance(center_lat, center_lon, bbox["max_lat"], bbox["min_lon"]),
        haversine_distance(center_lat, center_lon, bbox["max_lat"], bbox["max_lon"]),
    ]

    return max(distances)  # Use the maximum distance as the radius


def population_to_radius(population):
    # This is a simplified model and can be adjusted based on real-world data
    if population < 10000:
        return 2  # Small town
    elif population < 100000:
        return 5  # Medium-sized city
    elif population < 1000000:
        return 10  # Large city
    else:
        return 20  # Metropolis


def approximate_bbox(lat, lon, radius_km):
    # Approximate 1 degree of latitude and longitude in kilometers
    lat_km = 111.32  # Approximately true for all latitudes
    lon_km = 111.32 * cos(radians(lat))  # Varies with latitude

    lat_delta = radius_km / lat_km
    lon_delta = radius_km / lon_km

    return {
        "min_lat": lat - lat_delta,
        "max_lat": lat + lat_delta,
        "min_lon": lon - lon_delta,
        "max_lon": lon + lon_delta,
    }


def parse_population(population_str):
    if not population_str:
        return 0

    # Remove any non-digit characters except for commas and periods
    cleaned_str = re.sub(r"[^\d,.]", "", population_str)

    # Replace comma with period if it's used as a decimal separator
    if "," in cleaned_str and "." not in cleaned_str:
        cleaned_str = cleaned_str.replace(",", ".")
    else:
        # Remove commas if they're used as thousand separators
        cleaned_str = cleaned_str.replace(",", "")

    try:
        return int(float(cleaned_str))
    except ValueError:
        print(f"Warning: Could not parse population value: {population_str}")
        return 0


def get_middle_east_cities(country_code):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    area["ISO3166-1"="{country_code}"]->.searchArea;
    (
      node["place"="city"](area.searchArea);
      way["place"="city"](area.searchArea);
      relation["place"="city"](area.searchArea);
    );
    out geom;
    """

    response = requests.get(overpass_url, params={"data": overpass_query})
    data = response.json()

    cities = []
    for element in data["elements"]:
        name = element["tags"].get("name:en", element["tags"].get("name", "Unknown"))
        population_str = element["tags"].get("population", "0")
        population = parse_population(population_str)

        if element["type"] == "node":
            lat, lon = element["lat"], element["lon"]
            radius = population_to_radius(population) if population > 0 else 5
            bbox = approximate_bbox(lat, lon, radius)
        elif element["type"] == "way":
            lats = [node["lat"] for node in element["geometry"]]
            lons = [node["lon"] for node in element["geometry"]]
            bbox = {
                "min_lat": min(lats),
                "max_lat": max(lats),
                "min_lon": min(lons),
                "max_lon": max(lons),
            }
        elif element["type"] == "relation":
            lats = []
            lons = []
            for member in element["members"]:
                if "geometry" in member:
                    lats.extend([node["lat"] for node in member["geometry"]])
                    lons.extend([node["lon"] for node in member["geometry"]])
            bbox = {
                "min_lat": min(lats),
                "max_lat": max(lats),
                "min_lon": min(lons),
                "max_lon": max(lons),
            }

        estimated_radius = estimate_radius(bbox)

        cities.append(
            {
                "name": name,
                "population": population,
                "center": {
                    "latitude": (bbox["min_lat"] + bbox["max_lat"]) / 2,
                    "longitude": (bbox["min_lon"] + bbox["max_lon"]) / 2,
                },
                "bounding_box": bbox,
                "estimated_radius_km": estimated_radius,
            }
        )

    return cities


# List of Middle Eastern country codes (ISO 3166-1 alpha-2)
middle_east_countries = [
    "DZ",
    "BH",
    "KM",
    "EG",
    "IQ",
    "JO",
    "KW",
    "LB",
    "LY",
    "MR",
    "MA",
    "OM",
    "PS",
    "QA",
    "SA",
    "SO",
    "SD",
    "SY",
    "TN",
    "AE",
    "YE",
]

all_cities = {}

for country_code in middle_east_countries:
    print(f"Fetching cities for country code: {country_code}")
    cities = get_middle_east_cities(country_code)
    all_cities[country_code] = cities
    print(f"Found {len(cities)} cities in {country_code}")

# Save the results to a JSON file
with open("middle_east_cities_data.json", "w", encoding="utf-8") as f:
    json.dump(all_cities, f, ensure_ascii=False, indent=2)

print("Data saved to middle_east_cities_data.json")
