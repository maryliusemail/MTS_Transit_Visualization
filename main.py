# main.py

import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.graph_objects as go
from shapely.geometry import Point

# Import functions you already wrote
from project import create_detailed_schedule, visualize_bus_network, \
find_neighbors, bfs, simulate_bus_arrivals, simulate_wait_times, visualize_wait_times


# === Load data ===
stops = pd.read_csv('data/stations.csv')
trips = pd.read_csv('data/routes.csv')
schedule = pd.read_csv('data/schedule.csv')

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

# === Helper function for histogram plots ===

def plot_histogram_with_mean_line(series, title="Distribution", xlabel="Value", nbins=30):
    """
    Plots a histogram with a vertical mean line.
    Input: series - a 1D pandas Series (e.g., arrival intervals or wait times)
    """
    mean_val = series.mean()

    # Generate histogram bins to find bar heights before plotting
    counts, bin_edges = np.histogram(series, bins=nbins)
    max_height = counts.max() * 1.1  # Extend line slightly beyond tallest bar

    fig = go.Figure()

    # Histogram bars
    fig.add_trace(go.Histogram(
        x=series,
        nbinsx=nbins,
        name="Data",
        marker_color="cornflowerblue",
        opacity=0.75
    ))

    # Vertical line at the mean
    fig.add_trace(go.Scatter(
        x=[mean_val, mean_val],
        y=[0, max_height],
        mode='lines',
        name='Mean Value',
        line=dict(color='red', width=2, dash='dash'),
    ))

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title="Count",
        template="plotly_white",
        barmode="overlay",
        legend_title_text="Legend",
        margin={"r": 30, "t": 50, "l": 30, "b": 50}
    )

    return fig







# Plot shortest path
fig2 = shortest_path_visualization(path_df)
fig2.show()

# === Step 5: Simulate Bus Arrivals (Fixed Function) ===
tau = 10  # Average interval in minutes
arrival_times_df = simulate_bus_arrivals(tau)

# (Optional) Print sample
print("\nSample bus arrivals:")
print(arrival_times_df.head())

# === Step 5b: Visualize Bus Interval Histogram  ===
fig_interval_hist = plot_histogram_with_mean_line(
    arrival_times_df['Interval'],
    title="Bus Arrival Interval Distribution",
    xlabel="Interval (minutes)"
)
fig_interval_hist.show()

# === Step 6: Simulate Passenger Wait Times ===
n_passengers = 100
wait_times_df = simulate_wait_times(arrival_times_df, n_passengers)

# === Step 7: Visualize Passenger Wait Times for One-Hour Block ===
# one_hour_start = pd.Timestamp("08:00:00")
# fig3 = visualize_wait_times(wait_times_df, one_hour_start)
# fig3.show()

wait_times_df = simulate_wait_times(simulate_bus_arrivals(10), 2000)
fig_q4 = visualize_wait_times(wait_times_df, pd.Timestamp('13:00:00'))
visualize_wait_times_fig = fig_q4.data
fig_q4.show()


# === Step 7b: Visualize Passenger Wait Time Histogram (NEW!) ===
fig_wait_hist = plot_histogram_with_mean_line(
    wait_times_df['Wait Time'],
    title="Passenger Wait Time Distribution",
    xlabel="Wait Time (minutes)"
)
fig_wait_hist.show()

# === End
print("✅ All graphs successfully displayed.")

# === End of Program ===
print("✅ All visualizations completed.")
