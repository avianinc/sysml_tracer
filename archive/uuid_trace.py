import json

# Placeholder function to retrieve the details for an element by ID
def get_element_details_by_id(element_id, data):
    # You would typically search the JSON to find an element by its ID
    # and return its textual representation or other desired details.
    # For now, it returns a placeholder.
    return "ElementDetail"

# Load the JSON data from the file
with open('query_results.json', 'r') as file:
    data = json.load(file)

# Initialize an empty list to store constraint details
constraints_list = []

# Iterate through the data to find OperatorExpression elements
for element in data['elements']:
    if element.get('@type') == 'OperatorExpression':
        # Get the operator, assuming it can be found in the 'directedFeature' section
        # Here we need to know how operators are represented in the structure.
        # For now, let's use a placeholder.
        operator_placeholder = "[Operator]"
        
        # Extract arguments IDs
        arguments_ids = [arg['@id'] for arg in element.get('argument', [])]
        
        # Get the details of the arguments from their IDs
        arguments_details = [get_element_details_by_id(arg_id, data) for arg_id in arguments_ids]
        
        # Construct the constraint expression
        # This assumes binary expressions with a single operator.
        if len(arguments_details) == 2:
            constraint_expression = f"{arguments_details[0]} {operator_placeholder} {arguments_details[1]}"
            constraints_list.append(constraint_expression)

# Display the constraint equations
for constraint in constraints_list:
    print(constraint)