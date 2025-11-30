import re

# ----------------------------------------
# TOKENS AND PRECEDENCE
# ----------------------------------------

OPERATORS = {
    '¬': 3,
    '∧': 2,
    '∨': 2,
    '→': 1,
    '↔': 1
}

def tokenize(expr):
    expr = expr.replace(" ", "")
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c in '¬∧∨→↔()':
            tokens.append(c)
            i += 1
        elif c.isalpha():
            var = ''
            while i < len(expr) and expr[i].isalnum():
                var += expr[i]
                i += 1
            tokens.append(var)
        else:
            raise ValueError(f"Unknown character: {c}")
    return tokens

# ----------------------------------------
# PARSER (Shunting Yard + AST Builder)
# ----------------------------------------

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value  # operator or variable
        self.left = left
        self.right = right

def build_ast(tokens):
    def precedence(op):
        return OPERATORS.get(op, 0)

    def is_operator(token):
        return token in OPERATORS

    output = []
    ops = []

    for token in tokens:
        if token.isalnum():
            output.append(Node(token))
        elif token == '¬':
            ops.append(token)
        elif is_operator(token):
            while ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(token):
                op = ops.pop()
                if op == '¬':
                    node = output.pop()
                    output.append(Node(op, right=node))
                else:
                    right = output.pop()
                    left = output.pop()
                    output.append(Node(op, left, right))
            ops.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                op = ops.pop()
                if op == '¬':
                    node = output.pop()
                    output.append(Node(op, right=node))
                else:
                    right = output.pop()
                    left = output.pop()
                    output.append(Node(op, left, right))
            if not ops:
                raise ValueError("Mismatched parentheses")
            ops.pop()  # pop '('

    while ops:
        op = ops.pop()
        if op == '¬':
            node = output.pop()
            output.append(Node(op, right=node))
        else:
            right = output.pop()
            left = output.pop()
            output.append(Node(op, left, right))

    if len(output) != 1:
        raise ValueError("Invalid formula")
    return output[0]

# ----------------------------------------
# EVALUATOR
# ----------------------------------------

def evaluate(ast, values):
    if ast.value in OPERATORS:
        if ast.value == '¬':
            return not evaluate(ast.right, values)
        elif ast.value == '∧':
            return evaluate(ast.left, values) and evaluate(ast.right, values)
        elif ast.value == '∨':
            return evaluate(ast.left, values) or evaluate(ast.right, values)
        elif ast.value == '→':
            return (not evaluate(ast.left, values)) or evaluate(ast.right, values)
        elif ast.value == '↔':
            return evaluate(ast.left, values) == evaluate(ast.right, values)
    else:
        return values.get(ast.value, False)

# ----------------------------------------
# HELPERS
# ----------------------------------------

def extract_variables(ast):
    if ast is None:
        return set()
    if ast.value in OPERATORS:
        return extract_variables(ast.left) | extract_variables(ast.right)
    return {ast.value}

# ----------------------------------------
# EXPORTABLE FUNCTIONS
# ----------------------------------------

def parse_expression(expr):
    tokens = tokenize(expr)
    ast = build_ast(tokens)
    return ast
