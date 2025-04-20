import numpy as np
import gurobipy as gp
from gurobipy import GRB

# Load data from CSV files
with open("food_names.csv", "r") as f:
    foods = [line.strip() for line in f]
c = np.loadtxt("c_GE.csv", delimiter=",")  # Cost vector
A = np.loadtxt("A_GE.csv", delimiter=",")     # Constraint matrix
b = np.loadtxt("b_GE.csv")                    # Right-hand side vector

# Create model
m = gp.Model("diet_vectorized")

# Decision variables
n_foods = len(foods)
x = m.addVars(n_foods, lb=0, name="x")

# Objective: Minimize c^T x
m.setObjective(gp.quicksum(c[i] * x[i] for i in range(n_foods)), GRB.MINIMIZE)

# Main constraint: A x >= b
for i in range(len(b)):
    m.addConstr(gp.quicksum(A[i,j] * x[j] for j in range(n_foods)) >= b[i], name=f"constraint_{i}")

# Optimize
m.optimize()

# Results
if m.status == GRB.OPTIMAL:
    print("\nOptimal Diet Plan:")
    print("------------------")
    for i, food in enumerate(foods):
        if x[i].X > 1e-6:  # Only show non-zero quantities
            print(f"{food:10}: {x[i].X:.2f} units")
    
    # Calculate total nutrients (flip sign of fat back for display)
    total_nutrients = A @ np.array([x[i].X for i in range(n_foods)])
    total_nutrients[2] = -total_nutrients[2]  # Flip fat sign back for display
    print("\nNutritional Summary:")
    print("-------------------")
    print(f"Calories: {total_nutrients[0]:.1f} kcal")
    print(f"Protein:  {total_nutrients[1]:.1f} g")
    print(f"Fat:      {total_nutrients[2]:.1f} g")
    
    print(f"\nTotal Cost: ${m.objVal:.2f}")
else:
    print("No optimal solution found.") 