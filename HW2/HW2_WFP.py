import gurobipy as gp
from gurobipy import GRB

# ---------------------
# Data Preparation
# ---------------------

# List of food items
foods = [
    "Breastmilk", "Maize, dried, raw", "Cowpeas, whole dried", "Cowpeas, fresh", "Lemon", "Coconut, ground",
    "Leaf, cowpea", "Leaf, amaranth, wild", "Beef, liver", "Fish, sardines, canned in oil", "Sweet potato, white",
    "Yogurt", "Vinegar", "Cassava, dried, flour", "Cassava, raw", "Sugar, brown", "Vegetable oil",
    "Fish, small, dried, freshwater"
]

# Food cost per 1000g
costs = {
    "Breastmilk": 0.00, "Maize, dried, raw": 18.24, "Cowpeas, whole dried": 27.62, "Cowpeas, fresh": 10.50,
    "Lemon": 7.62, "Coconut, ground": 11.71, "Leaf, cowpea": 7.35, "Leaf, amaranth, wild": 12.06,
    "Beef, liver": 90.08, "Fish, sardines, canned in oil": 172.88, "Sweet potato, white": 12.19,
    "Yogurt": 96.93, "Vinegar": 30.48, "Cassava, dried, flour": 21.08, "Cassava, raw": 8.10,
    "Sugar, brown": 26.91, "Vegetable oil": 106.93, "Fish, small, dried, freshwater": 58.70
}

# Nutrient list
nutrients = [
    "Energy", "Protein", "Fat", "VitA", "VitC", "VitB1", "VitB2", "VitB6", "FolicAcid", "VitB12", "Calcium", "Magnesium", "Zinc"
]

# Nutrition content per 1000g of each food
# Format: nutrients[food][nutrient] = value
food_nutrients = {
    # energy, protein, fat, VitA, VitC, VitB1, VitB2, VitB6, Folic, B12, Ca, Mg, Zn
    "Breastmilk":     [650.11, 10.50, 38.99, 500.00, 40.01, 0.21, 0.35, 0.08, 84.99, 0.97, 89.61, 34.99, 1.21],
    "Maize, dried, raw": [3625.41, 81.11, 36.16, 0.00, 0.00, 3.91, 1.95, 2.93, 250.49, 0.00, 14.98, 1271.99, 17.92],
    "Cowpeas, whole dried": [3060.32, 202.86, 13.02, 25.08, 0.00, 5.40, 1.59, 2.54, 5490.16, 0.00, 157.46, 1400.00, 33.97],
    "Cowpeas, fresh": [3060.16, 203.01, 13.00, 25.00, 0.00, 5.31, 1.60, 2.61, 5490.19, 0.00, 157.50, 1400.05, 34.00],
    "Lemon":          [285.71, 11.43, 2.86, 15.24, 530.48, 0.00, 0.00, 0.95, 110.48, 0.00, 117.14, 80.00, 0.95],
    "Coconut, ground": [2120.35, 20.02, 201.04, 0.00, 20.02, 0.38, 0.11, 0.27, 160.01, 0.00, 36.00, 190.04, 7.00],
    "Leaf, cowpea":   [369.63, 36.96, 2.01, 2594.08, 329.89, 0.86, 1.91, 5.44, 1039.64, 0.00, 105.44, 619.77, 4.01],
    "Leaf, amaranth, wild": [371.43, 37.14, 1.90, 2594.92, 330.16, 0.95, 1.90, 5.40, 1040.00, 0.00, 105.40, 620.00, 4.13],
    "Beef, liver":    [1610.69, 243.89, 48.85, 203545.42, 150.00, 1.91, 35.88, 5.34, 2899.62, 1100.00, 22.52, 200.00, 61.07],
    "Fish, sardines, canned in oil": [3406.78, 245.76, 266.10, 671.19, 0.00, 0.00, 3.39, 5.08, 79.66, 89.83, 1762.71, 520.34, 30.51],
    "Sweet potato, white": [1120.00, 24.00, 0.95, 0.00, 140.00, 1.14, 0.38, 2.67, 180.00, 0.00, 22.48, 300.00, 6.10],
    "Yogurt":         [1168.58, 69.73, 64.75, 489.27, 29.89, 0.77, 3.07, 0.77, 139.85, 8.05, 856.70, 259.77, 11.88],
    "Vinegar":        [285.71, 11.43, 2.86, 15.24, 530.48, 0.00, 0.00, 0.95, 110.48, 0.00, 82.86, 80.00, 0.95],
    "Cassava, dried, flour": [3139.66, 25.99, 6.98, 70.00, 719.87, 3.10, 0.52, 6.98, 359.96, 0.00, 115.00, 239.96, 6.98],
    "Cassava, raw":   [1309.92, 11.00, 3.01, 30.00, 299.98, 1.30, 0.20, 2.90, 149.99, 0.00, 47.50, 100.00, 3.01],
    "Sugar, brown":   [3760.94, 0.00, 0.00, 0.00, 0.00, 0.11, 0.11, 0.27, 10.01, 0.00, 272.05, 290.04, 2.02],
    "Vegetable oil":  [8622.09, 0.00, 1000.21, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    "Fish, small, dried, freshwater": [3349.63, 585.91, 93.99, 0.00, 0.00, 1.00, 2.70, 4.08, 279.96, 119.97, 5439.31, 1399.81, 51.98],
}

# Nutrition requirements per person (index = 0 to 4)
persons = ["Child_12_23mo", "Child_3_4yr", "Child_7_8yr", "Man_30_59yr", "Woman_30_59yr"]
requirements = {
    "Child_12_23mo": [6258.0, 76.3, 208.6, 2800.0, 210.0, 3.5, 3.5, 3.5, 1050.0, 6.3, 1050.0, 420, 28.7],
    "Child_3_4yr": [8400.0, 122.5, 280.0, 2800.0, 210.0, 3.5, 3.5, 3.5, 1050.0, 6.3, 1050.0, 420, 28.7],
    "Child_7_8yr": [11375.0, 189.0, 379.2, 3500.0, 245.0, 6.3, 6.3, 7.0, 2100.0, 12.6, 1470.0, 700, 39.2],
    "Man_30_59yr": [24150.0, 315.0, 805.0, 4200.0, 315.0, 8.4, 9.1, 9.1, 2800.0, 16.8, 2100.0, 1820.0, 49.0],
    "Woman_30_59yr": [22972.5, 385.0, 762.4, 5950.0, 490.0, 10.5, 11.2, 11.2, 3500.0, 19.6, 2100.0, 1890.0, 59.5]
}

# ---------------------
# Optimization Model
# ---------------------

m = gp.Model("diet_plan")

# Decision variables: food intake in grams (per person per food)
x = m.addVars(persons, foods, name="food_intake", lb=0, ub=5000)

# Objective: minimize total cost
m.setObjective(gp.quicksum((costs[f] / 1000.0) * x[p, f] for p in persons for f in foods), GRB.MINIMIZE)

# Nutrition constraints for each person and nutrient
for p in persons:
    for i, n in enumerate(nutrients):
        m.addConstr(
            gp.quicksum((food_nutrients[f][i] / 1000.0) * x[p, f] for f in foods) >= requirements[p][i],
            name=f"{p}_{n}"
        )

# Constraint: No breastmilk for person 3, 4, 5
for p in persons[2:]:
    m.addConstr(x[p, "Breastmilk"] == 0, name=f"no_breastmilk_{p}")

# Solve
m.optimize()

# ---------------------
# Output Results
# ---------------------

if m.status == GRB.OPTIMAL:
    print("\nOptimal diet plan (in grams per week):")
    for p in persons:
        print(f"\n{p}:")
        for f in foods:
            amount = x[p, f].X
            if amount > 1e-3:
                print(f"  {f}: {amount:.2f} g")
    print(f"\nTotal Cost: {m.objVal:.2f} MZM")
else:
    print("No feasible solution found.")
