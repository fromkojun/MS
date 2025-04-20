import numpy as np
import gurobipy as gp
from gurobipy import GRB

# Load data
c = np.loadtxt("c_GE.csv", delimiter=",")          # (n,)
A = np.loadtxt("A_GE.csv", delimiter=",")              # (m,n)
b = np.loadtxt("b_GE.csv")                             # (m,)
food_names = [line.strip() for line in open("food_names.csv")]

n = len(c)

# Model
model = gp.Model("diet_GE_only")
x = model.addMVar(shape=n, lb=0.0, name="x")
model.setObjective(c @ x, GRB.MINIMIZE)

# Single GE constraint matrix
model.addConstr(A @ x >= b, name="GE_constraints")

# Solve
model.optimize()

# Output
if model.status == GRB.OPTIMAL:
    print("✅ Optimal solution:")
    for i, val in enumerate(x.X):
        if val > 1e-6:
            print(f"  {food_names[i]:<10} = {val:.2f}")
    print(f"\n💰 Total cost: ${model.ObjVal:.2f}")
else:
    print("❌ No optimal solution found.")