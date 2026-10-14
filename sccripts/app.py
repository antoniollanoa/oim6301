import bmi

result = bmi.compute_bmi(70, 1.75)
print(f"Computed BMI: {result:.2f}")

## Ctrl + i to create a list of dicts
people = [
    {"name": "Alice", "height": 1.75, "weight": 70},
    {"name": "Bob", "height": 1.80, "weight": 85},
    {"name": "Diana", "height": 1.70, "weight": 68},
    {"name": "Eve", "height": 1.65, "weight": 60},
    {"name": "Frank", "height": 1.72, "weight": 74},
    {"name": "Grace", "height": 1.69, "weight": 63},
    {"name": "Charlie", "height": 1.68, "weight": 62},
]

for person in people:
    #print(person)
    weight = person["weight"]
    height = person["height"]
    bmi_value = bmi.compute_bmi(weight, height)
    category = bmi.classify_bmi(bmi_value)
    print(f"{person['name']}' has a BMI of {bmi_value:.2f}. Which classifies as: {category}.")