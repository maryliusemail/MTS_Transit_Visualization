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

## Deliverables
- A complete visualization of San Diego's bus system using shapefiles and stop data.
- A Python script (`project.py`) containing all functional code.
- A validation script (`project-validation.py`) to confirm correctness and readiness for submission.

---

## San Diego City Boundary

**Description**:  
Utilized a shapefile to plot the geographic outline of San Diego, establishing a foundational map for subsequent transit data visualizations.

![San Diego City Boundary](![ScreenRecording2025-04-25at12 03 51PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/8ed508ed-60e1-4651-8e69-e71860dd4da0)
)

---

## MTS Bus Stops Distribution

**Description**:  
Plotted all MTS bus stops within San Diego, revealing the distribution and density of stops across various neighborhoods.

![MTS Bus Stops](insert_image_path_here)

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
