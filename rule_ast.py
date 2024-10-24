import ast

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            'node_type': self.node_type,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
            'value': self.value
        }

    @staticmethod
    def from_dict(data):
        return Node(
            node_type=data['node_type'],
            left=Node.from_dict(data['left']) if data['left'] else None,
            right=Node.from_dict(data['right']) if data['right'] else None,
            value=data['value']
        )


def create_rule(rule_string):
    try:
       
        rule_string = rule_string.replace('AND', 'and').replace('OR', 'or')

        print(f"Parsing rule: {rule_string}")
        rule_ast = ast.parse(rule_string, mode='eval')

        print(f"Generated AST: {rule_ast}")
        return rule_ast
    except Exception as e:
        print(f"Error while parsing rule: {e}")
        return None


def convert_to_ast(expression):
    if isinstance(expression, ast.BoolOp):
        left = convert_to_ast(expression.values[0])
        right = convert_to_ast(expression.values[1])
        op = 'AND' if isinstance(expression.op, ast.And) else 'OR'
        return Node(node_type="operator", left=left, right=right, value=op)

    elif isinstance(expression, ast.Compare):
        left = expression.left.id
        
        op_map = {
            ast.Gt: '>', ast.Lt: '<', ast.GtE: '>=', ast.LtE: '<=', ast.Eq: '==', ast.NotEq: '!='
        }
        op = op_map[type(expression.ops[0])]
        right = expression.comparators[0].n
        return Node(node_type="operand", value=f"{left} {op} {right}")


def combine_rules(rules):
    """
    Combines multiple rule ASTs into a single AST.
    :param rules: List of rule ASTs.
    :return: Combined AST.
    """
    if len(rules) == 1:
        return rules[0]

    combined_ast = rules[0]
    for rule in rules[1:]:
        combined_ast = Node(node_type="operator", left=combined_ast, right=rule, value="AND")
    
    return combined_ast

def evaluate_rule(ast, data):
    if ast.node_type == "operand":
        
        field, operator, value = ast.value.split(' ')
        value = int(value) if value.isdigit() else value.strip("'")
        
        
        if operator == '>':
            return data[field] > value
        elif operator == '<':
            return data[field] < value
        elif operator == '>=':
            return data[field] >= value
        elif operator == '<=':
            return data[field] <= value
        elif operator == '==':
            return data[field] == value
        elif operator == '!=':
            return data[field] != value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    elif ast.node_type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unsupported operator: {ast.value}")