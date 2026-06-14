import streamlit as st
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value

# Page Configuration
st.set_page_config(
    page_title="Supply Chain Network Optimizer", page_icon="🚛", layout="wide"
)

st.title("🚛 Prescriptive Analytics: Supply Chain Network Optimization Engine")
st.markdown(
    """
**ACCA SBL Case Study Upgrade:** This engine optimizes a logistics network by transitioning a 3x3 matrix distribution problem from Excel Solver to Python's `PuLP` framework. 
It calculates the most cost-effective routes from multiple supply depots to retail stores while monitoring capacity bottlenecks and distribution slack.
"""
)

# --- Data Initializations ---
depots = ["D1", "D2", "D3"]
stores = ["Store 1", "Store 2", "Store 3"]

# Distance Matrix (Excel Rows C7:E9)
default_distances = {
    "D1": {"Store 1": 22, "Store 2": 33, "Store 3": 40},
    "D2": {"Store 1": 27, "Store 2": 30, "Store 3": 22},
    "D3": {"Store 1": 36, "Store 2": 20, "Store 3": 25},
}

# --- Sidebar Parameter Customization Layer ---
st.sidebar.header("⚙️ Supply Chain Parameters")

cost_per_mile = st.sidebar.number_input(
    "Cost of TV Delivery per Mile (£)", min_value=0.0, value=5.0, step=0.50
)

st.sidebar.subheader("📦 Depot Supply Capacity")
supply_caps = {
    "D1": st.sidebar.number_input("D1 Capacity", value=2500),
    "D2": st.sidebar.number_input("D2 Capacity", value=3100),
    "D3": st.sidebar.number_input("D3 Capacity", value=1250),
}

st.sidebar.subheader("🏪 Store Demand Capacity")
demand_caps = {
    "Store 1": st.sidebar.number_input("Store 1 Capacity", value=2000),
    "Store 2": st.sidebar.number_input("Store 2 Capacity", value=3000),
    "Store 3": st.sidebar.number_input("Store 3 Capacity", value=2000),
}

# --- Dynamic Distance Matrix Input Matrix in Main Panel ---
st.subheader("📍 Route Distance Configuration (Miles)")
cols = st.columns(3)
distances = {}
for i, depot in enumerate(depots):
    distances[depot] = {}
    with cols[i]:
        st.markdown(f"**From Depot: {depot}**")
        for store in stores:
            distances[depot][store] = st.number_input(
                f"To {store}",
                min_value=0,
                value=default_distances[depot][store],
                key=f"dist_{depot}_{store}",
            )

# --- PuLP Optimization Execution ---
# Define Problem: Minimize Logistics Cost
model = LpProblem(name="Supply_Chain_Minimization", sense=LpMinimize)

# Decision Variables: Quantities shipped along each route index (i, j)
routes = [(d, s) for d in depots for s in stores]
ship_vars = LpVariable.dicts(
    name="Ship", indices=(depots, stores), lowBound=0, cat="Continuous"
)


# Objective Function: Sum of (Units Shipped * Distance * Cost per Mile)
model += (
    lpSum(
        [
            ship_vars[d][s] * distances[d][s] * cost_per_mile
            for (d, s) in routes
        ]
    ),
    "Total_Transportation_Cost",
)

# Constraints Group 1: Shipped totals cannot exceed Depot Supply Capacity
for d in depots:
    model += (
        lpSum([ship_vars[d][s] for s in stores]) <= supply_caps[d],
        f"Supply_Constraint_{d}",
    )

# Constraints Group 2: Total received units must match or meet Store Capacity limits
# Looking closely at the Excel screenshot, the Solver constraints read: Received <= Store Capacity
for s in stores:
    model += (
        lpSum([ship_vars[d][s] for d in depots]) <= demand_caps[s],
        f"Demand_Constraint_{s}",
    )

# Execute Solver Engine
model.solve()

# --- Business Intelligence UI Presentation Layer ---
st.separator()
res_col1, res_col2 = st.columns([3, 2])

with res_col1:
    st.subheader("📊 Optimal Shipping Matrix (TVs Transported)")
    if model.status == 1:
        # Create a display matrix summary
        display_data = []
        for d in depots:
            row = {"Depot": d}
            total_transported = 0
            for s in stores:
                val = ship_vars[d][s].varValue
                row[s] = f"{val:,.0f}" if val else "0"
                total_transported += val if val else 0
            row["Total Transported"] = f"{total_transported:,.0f}"
            row["Available Supply"] = f"{supply_caps[d]:,}"
            display_data.append(row)

        st.table(display_data)

        total_cost = value(model.objective)
        st.metric(
            label="Minimized Total Logistical Cost", value=f"£{total_cost:,.2f}"
        )
    else:
        st.error("Optimization failed. Check capacity configurations.")

with res_col2:
    st.subheader("📉 Network Capacity & Slack Diagnostics")

    st.markdown("**Store Allocation Slack (Capacity vs Received)**")
    for s in stores:
        received = sum([ship_vars[d][s].varValue for d in depots])
        capacity = demand_caps[s]
        slack = capacity - received

        st.write(f"*{s}*")
        st.progress(float(received / capacity if capacity > 0 else 0))
        if slack == 0:
            st.caption(
                f"🔒 Fully Binding Capacity reached: {received:,.0f} units."
            )
        else:
            st.caption(
                f"⚠️ Non-binding Slack: {slack:,.0f} units of remaining capacity."
            )

    st.markdown("<br>**Depot Inventory Utilization Slack**", unsafeDepth=2)
    for d in depots:
        shipped = sum([ship_vars[d][s].varValue for s in stores])
        available = supply_caps[d]
        inventory_slack = available - shipped

        st.write(f"*{d}*")
        st.progress(float(shipped / available if available > 0 else 0))
        if inventory_slack == 0:
            st.caption(
                f"🔒 Supply Exhausted: {shipped:,.0f} units dispatched."
            )
        else:
            st.caption(
                f"📦 Safety Stock Slack: {inventory_slack:,.0f} units remaining at depot."
            )
