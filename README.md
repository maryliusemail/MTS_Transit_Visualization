# MTS Transit: Navigating San Diego's Bus Network 🚌

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

