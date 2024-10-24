class ASTNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def to_dict(self):
        return {
            "value": self.value,
            "children": [child.to_dict() for child in self.children]
        }

def tokenize(rule_string):
    return rule_string.replace('(', ' ( ').replace(')', ' ) ').split()

def parse_rule_string_to_ast(rule_string):
    tokens = tokenize(rule_string)
    stack = []

    for token in tokens:
        if token == "AND" or token == "OR":
            right = stack.pop()
            left = stack.pop()
            stack.append(ASTNode(token, [left, right]))
        elif token.startswith('(') or token.endswith(')'):
            continue
        else:
            stack.append(ASTNode(token))

    return stack[0] if stack else None
