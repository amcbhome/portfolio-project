import streamlit as st
import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value

# Page Configuration
st.set_page_config(page_title="Logistics Optimizer", page_icon="🚛", layout="wide")

st.title("🚛 Prescriptive Analytics: Supply Chain Optimization Engine")
st.markdown("""
**ACCA SBL Case Study Portfolio Project:** Adjust the operational variables in the sidebar and layout grid. 
Click the **Calculate Optimal Routing** button to execute the `PuLP` linear programming engine and refresh your business intelligence outputs.
""")

# --- Baseline Framework Configurations ---
depots = ["D1", "D2", "D3"]
stores = ["Store 1", "Store 2", "Store 3"]

default_distances = {
    "Store 1": [22, 27, 36],
    "Store 2": [33, 30, 20],
    "Store 3": [40, 22, 25]
}
default_df = pd.DataFrame(default_distances, index=depots)

# --- Session State Management for Reset Button ---
if "distance_matrix" not in st.session_state:
    st.session_state.distance_matrix = default_df.copy()

# --- SIDEBAR: Parameter & Matrix Customization Layer ---
st.sidebar.header("⚙️ Network Configurations")

# Reset Button Action
if st.sidebar.button("🔄 Reset Distances to ACCA Defaults"):
    st.session_state.distance_matrix = default_df.copy()
    st.rerun()

st.sidebar.subheader("📍 Route Distance Matrix (Miles)")
st.sidebar.caption("Double-click any cell below to edit the transit miles directly:")
# Interactive Data Editor in Sidebar
edited_df = st.sidebar.data_editor(
    st.session_state.distance_matrix,
    hide_index=False,
    use_container_width=True,
    key="matrix_editor"
)
# Keep session state updated with modifications
st.session_state.distance_matrix = edited_df

st.sidebar.divider()
st.sidebar.subheader("💰 Financial Parameter")
cost_per_mile = st.sidebar.number_input("Cost per Mile (£)", min_value=0.0, value=5.00, step=0.25)


# --- MAIN PANEL: Calculator Inputs ---
with st.form("optimization_calculator_form"):
    st.header("📋 Supply & Demand Capacities")
    
    config_col1, config_col2 = st.columns(2)
    
    with config_col1:
        st.subheader("📦 Depot Supply Inventory")
        supply_caps = {
            "D1": st.number_input("D1 Inventory Level", min_value=0, value=2500, step=50),
            "D2": st.number_input("D2 Inventory Level", min_value=0, value=3100, step=50),
            "D3": st.number_input("D3 Inventory Level", min_value=0, value=1250, step=50)
        }
        
    with config_col2:
        st.subheader("🏪 Store Delivery Requirements")
        demand_caps = {
            "Store 1": st.number_input("Store 1 Required Volume", min_value=0, value=2000, step=50),
            "Store 2": st.number_input("Store 2 Required Volume", min_value=0, value=3000, step=50),
            "Store 3": st.number_input("Store 3 Required Volume", min_value=0, value=2000, step=50)
        }

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="⚡ Calculate Optimal Routing", use_container_width=True)


# --- CALCULATOR EXECUTION & MAIN SCREEN OUTPUTS ---
if submit_button:
    st.divider()
    
    # Convert Edited DataFrame back into dictionary for PuLP ingestion
    distances = edited_df.to_dict(orient="index")
    
    # --- PuLP Optimization Processing Engine ---
    model = LpProblem(name="Logistics_Minimization_Engine", sense=LpMinimize)

    # Multi-Indexed Decision Variables Matrix
    routes = [(d, s) for d in depots for s in stores]
    ship_vars = LpVariable.dicts(name="Ship", indices=(depots, stores), lowBound=0, cat="Continuous")

    # Objective Function: Cost Matrix Formulation + Shortage Penalty
    total_shipping_cost = lpSum([ship_vars[d][s] * distances[d][s] * cost_per_mile for (d, s) in routes])
    total_unshipped_penalty = lpSum([(supply_caps[d] - lpSum([ship_vars[d][s] for s in stores])) * 100000 for d in depots])
    
    model += total_shipping_cost + total_unshipped_penalty, "Total_Objective"

    # Supply Constraints (Outbound <= Available)
    for d in depots:
        model += lpSum([ship_vars[d][s] for s in stores]) <= supply_caps[d], f"Supply_{d}"

    # Demand Constraints (Received <= Store Capacity)
    for s in stores:
        model += lpSum([ship_vars[d][s] for d in depots]) <= demand_caps[s], f"Demand_{s}"

    # Execute Solution Run
    model.solve()

    # --- Main Screen Calculator Output Presentation ---
    res_col1, res_col2 = st.columns([4, 3])

    with res_col1:
        st.subheader("📊 Calculated Shipping Manifest")
        if model.status == 1:
            matrix_rows = []
            for d in depots:
                row = {"Source Depot": d}
                for s in stores:
                    val = ship_vars[d][s].varValue
                    row[s] = int(val) if val else 0
                matrix_rows.append(row)
            
            df_result = pd.DataFrame(matrix_rows).set_index("Source Depot")
            st.dataframe(df_result, use_container_width=True)
            
            total_cost = value(total_shipping_cost)
            st.metric(label="Calculated Minimum Network Logistics Cost", value=f"£{total_cost:,.2f}")
        else:
            st.error("🚨 Infeasible Network State: Review parameters.")

    with res_col2:
        st.subheader("📉 Operational Capacity & Stock Slack")
        
        if model.status == 1:
            st.markdown("**Depot Capacity Utilization (Supply Side Slack)**")
            for d in depots:
                shipped = sum([ship_vars[d][s].varValue for s in stores])
                available = supply_caps[d]
                slack = available - shipped
                
                st.write(f"**{d}** (Dispatched: {shipped:,.0f} / Total Available: {available:,.0f})")
                st.progress(float(shipped / available) if available > 0 else 0.0)
                if slack == 0:
                    st.caption("🔒 *Binding Limit:* 100% capacity deployed. Zero safety stock remaining.")
                else:
                    st.caption(f"📦 *Non-Binding Slack:* {slack:,.0f} reserve units remaining in storage.")
                    
            st.markdown("<br>**Store Volume Shortfalls (Demand Side Slack)**", unsafe_allow_html=True)
            for s in stores:
                received = sum([ship_vars[d][s].varValue for d in depots])
                required = demand_caps[s]
                shortfall = required - received
                
                st.write(f"**{s}** (Received: {received:,.0f} / Target Required: {required:,.0f})")
                st.progress(float(received / required) if required > 0 else 0.0)
                if shortfall == 0:
                    st.caption("🎯 *Demand Met:* Core store requirements fully satisfied.")
                else:
                    st.caption(f"⚠️ *Under-allocated Slack:* Shortfall of {shortfall:,.0f} units due to supply limitations.")
else:
    st.info("💡 Adjust the numerical parameters or sidebar distance cells, then click 'Calculate Optimal Routing' to generate the distribution report.")
