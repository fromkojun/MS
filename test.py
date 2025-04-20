import gurobipy as gp
from gurobipy import GRB

# Create a new model
m = gp.Model("mip1")

# Add variables
x = m.addVar(vtype=GRB.BINARY, name="x")
y = m.addVar(vtype=GRB.BINARY, name="y")
z = m.addVar(vtype=GRB.BINARY, name="z")

# Set objective
m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

# Add constraint
m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

# Optimize
m.optimize()

for v in m.getVars():
    print(f"{v.varName} = {v.x}")
print(f"Obj: {m.objVal}")


