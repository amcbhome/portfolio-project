# portfolio-project
# Prescriptive Analytics Engine: Operations & Resource Optimization

[![Streamlit App](https://static.streamlit.io/badge_svg.svg)](#) 
## 📌 Project Overview
This repository showcases an enterprise-grade optimization engine that upgrades traditional business modeling methodologies into modern analytical data applications.

Moving beyond static spreadsheet configurations, this system uses Python's `PuLP` library to build a linear programming framework capable of processing real-time operational limits, determining optimal product mixes, and providing interactive business intelligence visualizations via Streamlit.

## 🎯 Analytical & Business Objectives
* **Maximize Optimization Margins:** Automates product mix decisions to maximize overall contribution margins based on variable cost and resource factors.
* **Real-time Sensitivity Framework:** Replaces static calculations with an interactive dashboard, allowing users to run instant "what-if" operational scenarios.
* **Dynamic Bottleneck Detection:** Extracts model slack states to provide managers with immediate visibility into resource constraints.

## 📐 Mathematical Model Formulation
The underlying mathematical model runs the following linear programming structure:

* **Decision Variables:** $X_1$ (Product A Units), $X_2$ (Product B Units).
* **Objective Function:** Maximize $C = 30X_1 + 40X_2$ (Configurable)
* **Resource Constraints:**
    * Material Availability Boundary: $3X_1 + 5X_2 \le 15,000$ units
    * Labor Force Logistics Boundary: $4X_1 + 4X_2 \le 16,000$ hours

A complete breakdown of the formulation, along with the theoretical framework behind our resource slack calculations, is available in the formal document: [`documents/Prescriptive_Analytics_Formulation.pdf`](documents/Prescriptive_Analytics_Formulation.pdf).

## 🛠️ Technology Stack & Dependencies
* **Core Engine:** Python 3
* **Mathematical Solver:** `PuLP` (Linear Programming API)
* **BI Interface Layer:** `Streamlit` (Cloud Application Framework)
* **Typesetting Documentation:** `LaTeX`

## 🚀 Execution & Local Deployment Instructions

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/prescriptive-analytics-pulp.git](https://github.com/yourusername/prescriptive-analytics-pulp.git)
    cd prescriptive-analytics-pulp
    ```

2.  **Configure Local Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Required Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch the Interactive Web Application:**
    ```bash
    streamlit run app.py
    ```

## 💡 Analytical Insights & Strategic Impact
By checking resource slack directly via code ($s_i = \text{Capacity} - \text{Consumed}$), this system helps operations teams make clearer, data-driven decisions:
* **Zero-Slack Scenarios:** Highlight binding production constraints, indicating clear operational bottlenecks where expanding capacity could improve profitability.
* **Positive-Slack Scenarios:** Identify underutilized resources, alerting management to capacity that can be redirected to secondary operations without lowering core contribution margins.
