# solver.py
from pulp import LpMinimize, LpProblem, LpVariable, lpSum


def optimize_supply_chain(depots, stores, distances, supply_caps, demand_caps, cost_per_mile):
    """
    Executes a multi-indexed linear programming transportation model using PuLP.
    
    Parameters:
        depots (list): Identifiers for source warehouses (e.g., ['D1', 'D2', 'D3'])
        stores (list): Identifiers for retail outlets (e.g., ['Store 1', 'Store 2', 'Store 3'])
        distances (dict): Nested dictionary of miles between depots and stores
        supply_caps (dict): Max stock available per depot
        demand_caps (dict): Target requirements per store
        cost_per_mile (float): Financial scaling parameter per transit mile
        
    Returns:
        tuple: (status_code, objective_cost, shipping_matrix)
    """
    # Instantiate Optimization Problem Engine
    model = LpProblem(name="Logistics_Minimization_Engine", sense=LpMinimize)

    # Multi-Indexed Decision Variables Matrix (Routes)
    routes = [(d, s) for d in depots for s in stores]
    ship_vars = LpVariable.dicts(name="Ship", indices=(depots, stores), lowBound=0, cat="Continuous")

    # Objective Function: Base Cost Formulation + Shortage Penalty to match Excel logic
    total_shipping_cost = lpSum([ship_vars[d][s] * distances[d][s] * cost_per_mile for (d, s) in routes])
    total_unshipped_penalty = lpSum([(supply_caps[d] - lpSum([ship_vars[d][s] for s in stores])) * 100000 for d in depots])
    
    model += total_shipping_cost + total_unshipped_penalty, "Total_Objective"

    # Supply Constraints (Outbound <= Available Inventory)
    for d in depots:
        model += lpSum([ship_vars[d][s] for s in stores]) <= supply_caps[d], f"Supply_{d}"

    # Demand Constraints (Received <= Target Capacity)
    for s in stores:
        model += lpSum([ship_vars[d][s] for d in depots]) <= demand_caps[s], f"Demand_{s}"

    # Execute Solution Run
    model.solve()
    
    # Parse results safely if an optimal solution exists
    status_code = model.status
    objective_cost = 0.0
    shipping_matrix = {d: {s: 0 for s in stores} for d in depots}
    
    if status_code == 1:
        objective_cost = sum(ship_vars[d][s].varValue * distances[d][s] * cost_per_mile for (d, s) in routes)
        for d in depots:
            for s in stores:
                val = ship_vars[d][s].varValue
                shipping_matrix[d][s] = int(val) if val else 0
                
    return status_code, objective_cost, shipping_matrix
