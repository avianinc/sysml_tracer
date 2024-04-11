import json

# Load JSON data from a file
with open('data.json', 'r') as file:
    sysml_model = json.load(file)

# A dictionary to hold the mappings of IDs to fully qualified names
id_to_fqn = {}

# Function to find all elements and map their IDs to their fully qualified names
def map_ids_to_fqns(model):
    for element in model:
        el_id = element.get('@id')
        el_fqn = element.get('qualifiedName')  # Assuming 'qualifiedName' exists
        if el_id and el_fqn:
            id_to_fqn[el_id] = el_fqn

# Call the function to populate the id_to_fqn dictionary
map_ids_to_fqns(sysml_model)

# Function to extract and recreate the equations
def extract_equations(model):
    equations = []
    for element in model:
        if element.get('@type') == 'ConstraintUsage':
            left_operand = right_operand = operator = None
            for feature in element.get('ownedFeature', []):
                if feature.get('@type') == 'OperatorExpression':
                    operator = feature.get('operator')
                    operands = feature.get('operand', []) if isinstance(feature.get('operand'), list) else []
                    if len(operands) > 1:
                        left_operand = id_to_fqn.get(operands[0].get('@id'))
                        right_operand = id_to_fqn.get(operands[1].get('@id'))
            if left_operand and right_operand and operator:
                equation = f"{left_operand} {operator} {right_operand}"
                equations.append(equation)
    return equations

# Extract equations from the model
equations = extract_equations(sysml_model)

# Output the equations in a table-like format
print("{:<30} {:<15} {:<30}".format('Left Operand', 'Operator', 'Right Operand'))
for eq in equations:
    left_operand, operator, right_operand = eq.split()
    print("{:<30} {:<15} {:<30}".format(left_operand, operator, right_operand))

# Now, you could build a function to evaluate these equations with given inputs
# such as `measuredRange` and `uav_range` by the user or returned from an analysis