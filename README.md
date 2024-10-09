# Middle East Cities Map

This project scrapes data about cities in the Middle East and visualizes them on an interactive map.

## Contents

- `middle_east_cities_scraper.py`: Scrapes city data from OpenStreetMap using the Overpass API.
- `visualize.py`: Creates an interactive map using Folium.
- `middle_east_cities_data.json`: Raw data output from the scraper.
- `middle_east_cities_map.html`: Interactive map output.

## Setup

1. Clone this repository:

   ``` bash
   git clone https://github.com/yourusername/middle-east-cities-map.git
   cd middle-east-cities-map
   ```

2. Create a virtual environment:

   ``` bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install requirements:

   ``` bash
   pip install requests folium
   ```

## How it works

1. The scraper collects data on cities in Middle Eastern countries.
2. It estimates city sizes based on population or geographical data.
3. The visualizer plots these cities on a map, with markers and area estimates.

## Usage

1. Run the scraper: `python middle_east_cities_scraper.py`
2. Run the visualizer: `python visualize.py`
3. Open `middle_east_cities_map.html` in a web browser to view the map.

## Note

This is a rough estimate and may not be 100% accurate. Use for general visualization purposes only.
