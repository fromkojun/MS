# Note: This code will NOT work in Google Colab unless you have a valid Gurobi license activated
import gurobipy as gp
from gurobipy import GRB

# Food data
foods = ["chicken", "beef", "rice", "broccoli"]
cost = {"chicken": 2.0, "beef": 3.0, "rice": 1.0, "broccoli": 0.5}
calories = {"chicken": 250, "beef": 300, "rice": 200, "broccoli": 50}
protein = {"chicken": 30, "beef": 20, "rice": 4, "broccoli": 4}
fat = {"chicken": 10, "beef": 20, "rice": 1, "broccoli": 0}

# Create model
m = gp.Model("diet")

# Decision variables
x = m.addVars(foods, name="x", lb=0)

# Objective: Minimize cost
m.setObjective(gp.quicksum(cost[i] * x[i] for i in foods), GRB.MINIMIZE)

# Constraints
m.addConstr(gp.quicksum(calories[i] * x[i] for i in foods) >= 500, "calories")
m.addConstr(gp.quicksum(protein[i] * x[i] for i in foods) >= 35, "protein")
m.addConstr(gp.quicksum(fat[i] * x[i] for i in foods) <= 25, "fat")

# Optimize 
# this is the line that runs the optimization
m.optimize()

# Results
if m.status == GRB.OPTIMAL:
    for f in foods:
        print(f"{f}: {x[f].X:.2f}")
    print(f"Total cost = ${m.objVal:.2f}")
else:
    print("No optimal solution found.")