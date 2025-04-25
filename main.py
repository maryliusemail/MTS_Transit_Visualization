# main.py

import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.graph_objects as go
from shapely.geometry import Point

# Import functions you already wrote
from project import create_detailed_schedule, visualize_bus_network, find_neighbors, bfs, simulate_bus_arrivals_uniform, simulate_wait_times, visualize_wait_times

# === Load data ===
stops = pd.read_csv('data/stops.csv')
trips = pd.read_csv('data/trips.csv')
schedule = pd.read_csv('data/stop_times.csv')

# === Set parameters ===
bus_lines = ['30', '41', '43', '44', '105', '120', '150', '201', '202', '235']

# === Step 1: Create Detailed Schedule ===
detailed_schedule = create_detailed_schedule(schedule, stops, trips, bus_lines)

# === Step 2: Visualize Bus Network ===
fig1 = visualize_bus_network(detailed_schedule)
fig1.show()

# === Step 3: Find Shortest Path Example ===
# Example: Find path from one stop to another
start_station = "Gilman Dr & Eucalyptus Grove Ln"
end_station = "UTC Transit Center"
path_df = bfs(start_station, end_station, detailed_schedule)

# === Step 4: Visualize Shortest Path ===
def shortest_path_visualization(route_points_sorted):
    # (cleaner version)
    stops_gdf = gpd.GeoDataFrame(
        route_points_sorted,
        geometry=[Point(xy) for xy in zip(route_points_sorted['stop_lon'], route_points_sorted['stop_lat'])],
        crs="EPSG:4326"
    )
    san_diego_boundary_path = 'data/data_city/data_city.shp'
    san_diego_city_bounds = gpd.read_file(san_diego_boundary_path).to_crs("EPSG:4326")
    center_lat = route_points_sorted['stop_lat'].mean()
    center_lon = route_points_sorted['stop_lon'].mean()

    fig = go.Figure()

    fig.add_trace(go.Choroplethmapbox(
        geojson=san_diego_city_bounds.__geo_interface__,
        locations=san_diego_city_bounds.index,
        z=[1] * len(san_diego_city_bounds),
        colorscale="Greys",
        showscale=False,
        marker_opacity=0.4,
        marker_line_width=1,
    ))

    fig.add_trace(go.Scattermapbox(
        lat=route_points_sorted['stop_lat'],
        lon=route_points_sorted['stop_lon'],
        mode='markers+lines',
        marker=dict(size=10, color='red', opacity=0.8),
        line=dict(width=3, color='red'),
        name="Shortest Path",
        text=route_points_sorted['stop_name'],
        hoverinfo='text'
    ))

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=13
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=True,
        legend_title_text='Route'
    )

    return fig

# Plot shortest path
fig2 = shortest_path_visualization(path_df)
fig2.show()

# === Step 5: Simulate Bus Arrivals ===
tau = 10  # average arrival interval (minutes)
arrival_times_df = simulate_bus_arrivals_uniform(tau)

# (Optional: print sample)
print(arrival_times_df.head())

# === Step 6: Simulate Passenger Wait Times ===
n_passengers = 100
wait_times_df = simulate_wait_times(arrival_times_df, n_passengers)

# === Step 7: Visualize Wait Times for a One-Hour Block ===
import pandas as pd
one_hour_start = pd.Timestamp("08:00:00")
fig3 = visualize_wait_times(wait_times_df, one_hour_start)
fig3.show()

# === End of Program ===
print("✅ All visualizations completed.")
