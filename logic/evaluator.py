
from logic.parser import parse_expression, evaluate, extract_variables
import itertools

# ----------------------------------------
# 1. TRUTH TABLE GENERATOR
# ----------------------------------------
def generate_truth_table(expr):
    try:
        ast = parse_expression(expr)
        vars = sorted(list(extract_variables(ast)))
        rows = list(itertools.product([False, True], repeat=len(vars)))

        table_rows = []
        for row in rows:
            val_map = dict(zip(vars, row))
            result = evaluate(ast, val_map)
            bools = ["T" if b else "F" for b in row]
            table_rows.append(bools + [("T" if result else "F")])

        return {
            "headers": vars + [expr],   # LAST COLUMN = formula
            "rows": table_rows
        }

    except Exception as e:
        return {
            "error": str(e),
            "headers": [],
            "rows": []
        }



# ----------------------------------------
# 2. FORMULA CLASSIFIER
# ----------------------------------------

def classify_formula(expr):
    try:
        ast = parse_expression(expr)
        vars = extract_variables(ast)
        for combo in itertools.product([False, True], repeat=len(vars)):
            val_map = dict(zip(sorted(vars), combo))
            result = evaluate(ast, val_map)
            if result is False:
                for combo2 in itertools.product([False, True], repeat=len(vars)):
                    val_map2 = dict(zip(sorted(vars), combo2))
                    if evaluate(ast, val_map2) is True:
                        return "Contingent"
                return "Contradiction"
        return "Tautology"
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------------------
# 3. EQUIVALENCE CHECKER
# ----------------------------------------

def check_equivalence(expr1, expr2):
    try:
        ast1 = parse_expression(expr1)
        ast2 = parse_expression(expr2)
        vars = sorted(list(extract_variables(ast1) | extract_variables(ast2)))
        for combo in itertools.product([False, True], repeat=len(vars)):
            val_map = dict(zip(vars, combo))
            if evaluate(ast1, val_map) != evaluate(ast2, val_map):
                return False
        return True
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------------------
# 4. ARGUMENT VALIDITY CHECKER
# ----------------------------------------

def check_argument_validity(premises, conclusion):
    try:
        premise_asts = [parse_expression(p.strip()) for p in premises]
        conclusion_ast = parse_expression(conclusion)
        vars = set()
        for p in premise_asts:
            vars |= extract_variables(p)
        vars |= extract_variables(conclusion_ast)
        vars = sorted(list(vars))

        for combo in itertools.product([False, True], repeat=len(vars)):
            val_map = dict(zip(vars, combo))
            all_true = all(evaluate(p, val_map) for p in premise_asts)
            if all_true and not evaluate(conclusion_ast, val_map):
                return "Invalid"
        return "Valid"
    except Exception as e:
        return f"Error: {str(e)}"
def normalize_formula(expr: str) -> str:
    """Convert ASCII programmer operators INTO real logic symbols."""
    if not expr:
        return ""

    replacements = {
        "&&": "∧",
        "&": "∧",
        "||": "∨",
        "|": "∨",
        "!": "¬",
        "~": "¬",
        "not ": "¬",
        "->": "→",
        "=>": "→",
        "<->": "↔",
        "<=>": "↔",
    }

    for old, new in replacements.items():
        expr = expr.replace(old, new)

    return expr
