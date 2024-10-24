class ASTNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def to_dict(self):
        """Convert the ASTNode to a dictionary for JSON serialization."""
        return {
            'value': self.value,
            'children': [child.to_dict() for child in self.children]
        }

# Your other code (database setup, routes, etc.) goes here

def evaluate_rule(node, data):
    """
    Evaluate the AST node against the provided data.
    :param node: The AST node (should be an ASTNode object)
    :param data: A dictionary containing the data to evaluate against
    :return: Boolean result of the evaluation
    """
    if isinstance(node, dict):
        # If node is a dictionary, convert it back to an ASTNode
        node = ASTNode(node['value'], [ASTNode(child['value']) for child in node['children']])

    if not node.children:
        # Leaf node: it's a variable or a constant
        if isinstance(node.value, str) and node.value in data:
            return data[node.value]
        else:
            # If it's a literal value (like a number), return it
            return node.value

    # Non-leaf node: evaluate based on the operator
    operator = node.value

    if operator == "AND":
        return all(evaluate_rule(child, data) for child in node.children)
    elif operator == "OR":
        return any(evaluate_rule(child, data) for child in node.children)
    elif operator == "==":
        return evaluate_rule(node.children[0], data) == evaluate_rule(node.children[1], data)
    elif operator == ">":
        return evaluate_rule(node.children[0], data) > evaluate_rule(node.children[1], data)
    # Add more operators as needed...

    raise ValueError(f"Unknown operator: {operator}")