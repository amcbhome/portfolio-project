# Save this block as app.py
import streamlit as st
from pulp import LpMaximize, LpProblem, LpVariable, value

# Page Configuration for BI Presentation
st.set_page_config(
    page_title="Prescriptive Analytics Engine", page_icon="📊", layout="wide"
)

st.title("📊 Prescriptive Analytics: Operations Optimization Engine")
st.markdown(
    """
This decision-support system transitions traditional financial linear programming from manual models to an interactive software layer. 
By utilizing the **PuLP** optimization library, the application identifies the optimal product mix to maximize contribution margin while reporting real-time resource utilization and slack capacity.
"""
)

# Sidebar - Parameter Customization Layer
st.sidebar.header("🔧 Interactive Parameters & Constraints")

st.sidebar.subheader("Objective Function Coefficients")
c_prod_a = st.sidebar.number_input(
    "Product A Unit Contribution (£)", min_value=0.0, value=30.0, step=1.0
)
c_prod_b = st.sidebar.number_input(
    "Product B Unit Contribution (£)", min_value=0.0, value=40.0, step=1.0
)

st.sidebar.subheader("Resource Availability Limits")
max_material = st.sidebar.number_input(
    "Material Capacity Limit", min_value=0.0, value=15000.0, step=500.0
)
max_labor = st.sidebar.number_input(
    "Labor/Logistics Hours Limit", min_value=0.0, value=16000.0, step=500.0
)

st.sidebar.subheader("Resource Utilization per Unit")
mat_a = st.sidebar.slider("Product A Material Usage", 1.0, 10.0, 3.0, 0.5)
mat_b = st.sidebar.slider("Product B Material Usage", 1.0, 10.0, 5.0, 0.5)
lab_a = st.sidebar.slider("Product A Labor Allocation", 1.0, 10.0, 4.0, 0.5)
lab_b = st.sidebar.slider("Product B Labor Allocation", 1.0, 10.0, 4.0, 0.5)

# --- PuLP Optimization Engine Core Execution ---
# Instantiate Optimization Problem
model = LpProblem(name="Product_Mix_Optimization", sense=LpMaximize)

# Define Continuous Decision Variables bounded by Non-Negativity
x1 = LpVariable(name="Product_A_Qty", lowBound=0, cat="Continuous")
x2 = LpVariable(name="Product_B_Qty", lowBound=0, cat="Continuous")

# Register Objective Function
model += c_prod_a * x1 + c_prod_b * x2, "Total_Contribution"

# Register Structural Constraints
model += mat_a * x1 + mat_b * x2 <= max_material, "Material_Constraint"
model += lab_a * x1 + lab_b * x2 <= max_labor, "Labor_Constraint"

# Run Solver Engine
model.solve()

# --- Business Intelligence Presentation Layer ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Optimization Results")
    if model.status == 1:
        opt_a = x1.varValue
        opt_b = x2.varValue
        total_revenue = value(model.objective)

        st.success(f"**Optimal Solution Found**: Status = Successful")
        metrics_col1, metrics_col2 = st.columns(2)
        metrics_col1.metric(label="Product A Optimal Units", value=f"{opt_a:,.2f}")
        metrics_col2.metric(label="Product B Optimal Units", value=f"{opt_b:,.2f}")

        st.metric(
            label="Maximized Total Contribution", value=f"£{total_revenue:,.2f}"
        )
    else:
        st.error("The current optimization parameters yield an infeasible solution.")

with col2:
    st.subheader("📉 Resource Slack & Constraint Diagnostic")

    # Extracting Slack and calculating consumption figures
    mat_slack = model.constraints["Material_Constraint"].slack
    lab_slack = model.constraints["Labor_Constraint"].slack

    mat_consumed = max_material - mat_slack
    lab_consumed = max_labor - lab_slack

    # UI Visual Reporting
    st.write("**Material Resource Breakdown**")
    st.progress(min(max(mat_consumed / max_material, 0.0), 1.0))
    st.caption(
        f"Consumed: {mat_consumed:,.2f} / Total: {max_material:,.2f} units"
    )

    st.write("**Labor/Logistics Capacity Breakdown**")
    st.progress(min(max(lab_consumed / max_labor, 0.0), 1.0))
    st.caption(f"Consumed: {lab_consumed:,.2f} / Total: {max_labor:,.2f} hours")

# --- Prescriptive Analytics & Slack Capacity Discussion ---
st.subheader("💡 Managerial Insights & Analytical Diagnostics")
insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("#### Material Constraints")
    if mat_slack == 0:
        st.warning(
            "⚠️ **Material Capacity is BINDING.** Every unit of this resource is completely exhausted. "
            "To scale operational throughput and increase profitability, supply chain managers should procure additional "
            "materials or look into alternative suppliers with higher availability."
        )
    else:
        st.info(
            f"ℹ️ **Material Capacity is NON-BINDING (Slack Available: {mat_slack:,.2f} units).** "
            "There is excess material remaining in stock. Sourcing more of this raw item will not boost financial performance. "
            "Instead, investigate opportunities to redirect capital away from holding costs for this excess safety stock."
        )

with insight_col2:
    st.markdown("#### Labor/Logistics Capacity")
    if lab_slack == 0:
        st.warning(
            "⚠️ **Labor/Logistics Capacity is BINDING.** Workforce scheduling or logistics throughput is at absolute capacity. "
            "Operational improvements should target bottleneck reduction, such as scheduling overtime or expanding logistics "
            "fleet availability, to unlock further volume."
        )
    else:
        st.info(
            f"ℹ️ **Labor/Logistics Capacity is NON-BINDING (Slack Available: {lab_slack:,.2f} hours).** "
            "The workforce has idle capacity under this configuration. Management can reallocate these specific labor hours "
            "to maintenance, strategic training, or alternative product lines without impacting the optimized contribution margin."
        )
