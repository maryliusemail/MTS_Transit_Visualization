# project.py


import pandas as pd
import numpy as np
from pathlib import Path

###
from collections import deque
from shapely.geometry import Point
###

import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
pd.options.plotting.backend = 'plotly'

import geopandas as gpd

import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def create_detailed_schedule(schedule, stops, trips, bus_lines):
    merged = schedule.merge(stops, on='stop_id', how='left')
    merged = merged.merge(
        trips[['trip_id', 'route_id', 'service_id', 'direction_name']],
        on='trip_id',
        how='left'
    )
    
    merged = merged[merged['route_id'].isin(bus_lines)]

    merged['stop_count'] = merged.groupby('trip_id')['stop_sequence'].\
    transform('max')


    merged['route_id'] = pd.Categorical(
        merged['route_id'], 
        categories=bus_lines, 
        ordered=True
    )

    merged = merged.sort_values(
        by=['route_id', 'stop_count', 'trip_id', 'stop_sequence']
    )


    merged = merged.drop(columns='stop_count').set_index('trip_id')

    return merged[['stop_id', 'stop_sequence', 'shape_dist_traveled',
                   'stop_name', 'stop_lat', 'stop_lon',
                   'route_id', 'service_id', 'direction_name']]


def visualize_bus_network(bus_df):
    # Load the shapefile for San Diego city boundary
    san_diego_boundary_path = 'data/data_city/data_city.shp'
    san_diego_city_bounds = gpd.read_file(san_diego_boundary_path)

    # Ensure the coordinate reference system is correct
    san_diego_city_bounds = san_diego_city_bounds.to_crs("EPSG:4326")
    san_diego_city_bounds['lon'] = \
    san_diego_city_bounds.geometry.apply(lambda x: x.centroid.x)
    san_diego_city_bounds['lat'] = \
    san_diego_city_bounds.geometry.apply(lambda x: x.centroid.y)

    fig = go.Figure()

    # Add city boundary
    fig.add_trace(go.Choroplethmapbox(
        geojson=san_diego_city_bounds.__geo_interface__,
        locations=san_diego_city_bounds.index,
        z=[1] * len(san_diego_city_bounds),
        colorscale="Greys",
        showscale=False,
        marker_opacity=0.5,
        marker_line_width=1,
    ))

    colors = px.colors.qualitative.Plotly
    bus_lines = bus_df['route_id'].cat.categories if hasattr(\
        bus_df['route_id'], 'cat') else bus_df['route_id'].unique()

    for i, route in enumerate(bus_lines[:10]):  
        route_df = bus_df[bus_df['route_id'] == route]

        fig.add_trace(go.Scattermapbox(
            lat=route_df['stop_lat'],
            lon=route_df['stop_lon'],
            mode='markers',
            marker=dict(size=6, color=colors[i % len(colors)], opacity=0.8),
            name=f"Bus Line {route}",
            text=[
                f"({lat:.6f}°, {lon:.6f}°)<br>{name}<br>Bus Line {route}"
                for name, lat, lon in zip(route_df['stop_name'], \
                    route_df['stop_lat'], route_df['stop_lon'])
            ],
            hoverinfo='text'
        ))


    # Update layout
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center={"lat": san_diego_city_bounds['lat'].mean(), \
            "lon": san_diego_city_bounds['lon'].mean()},
            zoom=10,
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    return fig




# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------

def find_neighbors(station_name, detailed_schedule):
    neighbors = set()
    matching_rows = detailed_schedule[detailed_schedule['stop_name'] == \
    station_name]
    for trip_id in matching_rows.index.unique():
        trip_data = detailed_schedule.loc[trip_id]
        trip_data = trip_data.sort_values('stop_sequence')

        if isinstance(trip_data, pd.Series):
            trip_data = trip_data.to_frame().T

        current_rows = trip_data[trip_data['stop_name'] == station_name]

        for index, row in current_rows.iterrows():
            next_stop_seq = row['stop_sequence'] + 1
            next_stop = trip_data[trip_data['stop_sequence'] == next_stop_seq]
            if not next_stop.empty:
                neighbors.add(next_stop.iloc[0]['stop_name'])

    return np.array(list(neighbors))



def bfs(start_station, end_station, detailed_schedule):
    all_stations = detailed_schedule['stop_name'].unique()
    if start_station not in all_stations:
        return f"Start station {start_station} not found."
    
    if end_station not in all_stations:
        return f"End station '{end_station}' not found."

    queue = deque()
    queue.append([start_station])  
    visited = set()

    while queue:
        path = queue.popleft()
        current_station = path[-1]

        if current_station == end_station:
            path_df = detailed_schedule[detailed_schedule['stop_name']\
            .isin(path)]
            path_df = path_df.drop_duplicates(subset='stop_name')
            path_df = path_df.set_index('stop_name').loc[path].reset_index()
            path_df = path_df[['stop_name', 'stop_lat', 'stop_lon']]
            path_df['stop_num'] = range(1, len(path_df) + 1)
            return path_df

        if current_station not in visited:
            visited.add(current_station)
            neighbors = find_neighbors(current_station, detailed_schedule)

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(path + [neighbor])

    return "No path found"


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def simulate_bus_arrivals(tau, seed=12):
    
    np.random.seed(seed) # Random seed -- do not change
    
    start_min = 360
    end_min = 1440
    time_range = end_min - start_min
    num_buses = int(time_range / tau)

    arrival_minutes = np.random.uniform(start_min, end_min, size=num_buses)
    arrival_minutes.sort()

    arrival_times_str = [
        f"{int(m // 60):02d}:{int(m % 60):02d}:{int((m - int(m)) * 60):02d}"
        for m in arrival_minutes
    ]

    intervals = np.diff(np.insert(arrival_minutes, 0, start_min))
    intervals = np.round(intervals, 2)

    return pd.DataFrame({
        'Arrival Time': arrival_times_str,
        'Interval': intervals
    })



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def simulate_wait_times(arrival_times_df, n_passengers):

    bus_minutes = arrival_times_df['Arrival Time'].apply(
        lambda t: int(t[:2]) * 60 + int(t[3:5]) + int(t[6:]) / 60
    ).values
    bus_minutes.sort()

    start_min = 360  
    end_min = max(bus_minutes)

    passenger_minutes =np.random.uniform(start_min, end_min, size=n_passengers)
    passenger_minutes.sort()

    results = []
    bus_idx = 0
    for p in passenger_minutes:
        while bus_idx < len(bus_minutes) and bus_minutes[bus_idx] < p:
            bus_idx += 1
        if bus_idx == len(bus_minutes):
            break

        wait = round(bus_minutes[bus_idx] - p, 2)

        p_str = f"{int(p // 60):02d}:{int(p % 60):02d}:{int((p - int(p)) * \
            60):02d}"
        b_str = f"{int(bus_minutes[bus_idx] // 60):02d}:{int(bus_minutes\
            [bus_idx] % 60):02d}:{int((bus_minutes[bus_idx] - int(bus_minutes\
                [bus_idx])) * 60):02d}"

        results.append({
            'Passenger Arrival Time': p_str,
            'Bus Arrival Time': b_str,
            'Bus Index': bus_idx,
            'Wait Time': wait
        })

    return pd.DataFrame(results)

def visualize_wait_times(wait_times_df, timestamp):
    wait_times_df = wait_times_df.copy()

    wait_times_df['Passenger Timestamp'] = \
    pd.to_datetime(wait_times_df['Passenger Arrival Time'])
    wait_times_df['Bus Timestamp'] = \
    pd.to_datetime(wait_times_df['Bus Arrival Time'])

    start = pd.to_datetime(timestamp)
    end = start + pd.Timedelta(hours=1)

    block = wait_times_df[
        (wait_times_df['Passenger Timestamp'] >= start) &
        (wait_times_df['Passenger Timestamp'] <= end)
    ]

    fig = go.Figure()


    fig.add_trace(go.Scatter(
        x=block['Bus Timestamp'],
        y=[0]*len(block),
        mode='markers',
        marker=dict(color='blue'),
        name='Bus Arrival'
    ))


    fig.add_trace(go.Scatter(
        x=block['Passenger Timestamp'],
        y=block['Wait Time'],
        mode='markers',
        marker=dict(color='red'),
        name='Passenger Wait Time'
    ))

 
    for _, row in block.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Passenger Timestamp'], row['Passenger Timestamp']],
            y=[0, row['Wait Time']],
            mode='lines',
            line=dict(color='red', width=1),
            showlegend=False
        ))

    fig.update_layout(
        title="Passenger Wait Times",
        xaxis_title="Time",
        yaxis_title="Wait Time (minutes)",
        template="plotly_white"
    )

    return fig
