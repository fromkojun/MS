import gurobipy as gp
from gurobipy import GRB

# Sets
I = [1, 2]         # sources
J = ['G', 'H']     # destinations

# Parameters
supply = {1: 5000, 2: 10000}
quality = {1: 10, 2: 5}
min_quality = {'G': 8, 'H': 6}
prices = {'G': 75, 'H': 60, 'leftover': {1: 50, 2: 55}}

# Create model
m = gp.Model("blending_full_revenue")

# Decision variables: x[i,j] = units sent from i to j
x = m.addVars(I, J, lb=0, name="x")

# Objective function: full revenue
m.setObjective(
    prices['G'] * (x[1, 'G'] + x[2, 'G']) +
    prices['H'] * (x[1, 'H'] + x[2, 'H']) +
    prices['leftover'][1] * (supply[1] - x[1, 'G'] - x[1, 'H']) +
    prices['leftover'][2] * (supply[2] - x[2, 'G'] - x[2, 'H']),
    GRB.MAXIMIZE
)

# Availability constraints
m.addConstr(x[1, 'G'] + x[1, 'H'] <= supply[1], "supply_1")
m.addConstr(x[2, 'G'] + x[2, 'H'] <= supply[2], "supply_2")

# Quality constraints
m.addConstr(quality[1]*x[1, 'G'] + quality[2]*x[2, 'G'] >= min_quality['G'] * (x[1, 'G'] + x[2, 'G']), "qual_G")
m.addConstr(quality[1]*x[1, 'H'] + quality[2]*x[2, 'H'] >= min_quality['H'] * (x[1, 'H'] + x[2, 'H']), "qual_H")

# Solve the model
m.optimize()

# Output the results
if m.status == GRB.OPTIMAL:
    xG = x[1, 'G'].X + x[2, 'G'].X
    xH = x[1, 'H'].X + x[2, 'H'].X
    leftover1 = supply[1] - x[1, 'G'].X - x[1, 'H'].X
    leftover2 = supply[2] - x[2, 'G'].X - x[2, 'H'].X
    revenue = m.ObjVal

    print("\n✅ Optimal Allocation:")
    print(f"  🚗 Gasoline (G): {xG:.2f} barrels")
    print(f"  🔥 Heating Oil (H): {xH:.2f} barrels")
    print(f"  🛢️ Leftover Crude 1: {leftover1:.2f} barrels")
    print(f"  🛢️ Leftover Crude 2: {leftover2:.2f} barrels")
    print(f"\n💰 Total Revenue: ${revenue:.2f}")
else:
    print("❌ No optimal solution found.")
