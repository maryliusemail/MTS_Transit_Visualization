# Project 1 – MTS Transit: Navigating San Diego's Bus Network 🚌

## Project Overview
This project explores the structure and behavior of San Diego’s MTS bus network through data visualization and statistical analysis. By mapping the bus system and evaluating arrival intervals, the project highlights patterns in public transit service and examines assumptions often made in modeling passenger wait times.

## Objective
Visualize San Diego's bus lines and stops, using shapefiles and schedule data to reveal spatial patterns in the city’s transit network. Assess statistical properties of bus arrivals and analyze how they differ from theoretical models.

## Key Insight: The Waiting Time Paradox
Although real-world bus arrivals do not follow a Poisson process, average passenger wait times (6 minutes) are still close to average bus intervals (7 minutes). This reflects the Waiting Time Paradox, where passengers often experience longer-than-expected waits due to uneven intervals between buses.

## Real-World Implications
Bus schedules are optimized for regularity and reliability, not randomness. This project emphasizes the need to validate assumptions in data analysis—real-world systems often defy clean theoretical models.

## Lessons Learned
- Be cautious when applying mathematical models to practical scenarios.
- Real transit systems may resemble theoretical processes only loosely.
- Data-driven visualizations can reveal hidden inefficiencies or unexpected insights.

## Tools Used
- **Python**: Core programming language for data analysis and visualization.
- **Pandas**: Data manipulation and analysis.
- **GeoPandas**: Handling and visualizing geospatial data.
- **Plotly**: Creating interactive visualizations.
- **Shapely**: Geometric operations on spatial data.
- **Matplotlib**: Plotting static graphs and maps.
- **NumPy**: Numerical computations.
- **Jupyter Notebook**: Interactive coding and documentation.
- **project-validation.py**: Script to validate project code against test cases.

---

## San Diego City Boundary Visualization

**Description**:  
Build a clean, organized bus schedule and map visualization for selected San Diego routes:
  - **`create_detailed_schedule`:** Combine schedule, stop, and trip data into a structured DataFrame showing the full stop sequence for each trip. Ensure routes are sorted properly and grouped by bus line.
  - **`visualize_bus_network`:** Plot the bus routes on an interactive map using Plotly, assigning each line a distinct color and enabling hover labels for bus stop names.


![ScreenRecording2025-04-25at12 03 51PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/8ed508ed-60e1-4651-8e69-e71860dd4da0)


---

## MTS Bus Stops Distribution

**Description**:   
Build a system to find the shortest bus route between two stops using a graph traversal approach:
  - **`find_neighbors`:** Identify all immediate next stops from a given station by looking across multiple bus trips and routes in the dataset.
  - **`bfs`:** Implement Breadth-First Search (BFS) to find the shortest path (fewest stops) between a start and end station, returning an ordered list of stops with their coordinates.

![ScreenRecording2025-04-25at12 16 04PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/d7a7238b-9da5-4b16-9130-3253ca304f97)


---

## Bus Arrival Interval Analysis

**Description**:  
Examined the intervals between bus arrivals to assess their alignment with a Poisson process, uncovering insights into scheduling regularity and passenger wait times.

![Bus Arrival Intervals](insert_image_path_here)

---

## Waiting Time Paradox Visualization

**Description**:  
Explored the discrepancy between average bus intervals and passenger wait times, illustrating the Waiting Time Paradox in the context of San Diego's transit system.

![Waiting Time Analysis](insert_image_path_here)

---
