import json
import re

# Simple heuristics to craft short hints based on question text and options

def make_hint(q):
    text = q.get('question', '').lower()
    options = [o.lower() for o in q.get('options', [])]

    # Early simple heuristics
    if 'tautology' in text:
        return 'Think whether the statement is always true regardless of variable values.'
    if 'negation' in text or 'negate' in text or 'negating' in text or 'negation of' in text:
        return 'Try applying De Morgan\'s laws or push the negation inward.'
    if 'which connective' in text or 'which operator' in text or 'which symbol' in text or 'corresponds to exclusive or' in text:
        return 'Consider the truth condition: which option is true exactly when one operand is true.'
    if 'conditional' in text or 'when p is false' in text or 'implication' in text or 'p -> q' in text or 'material implication' in text:
        return 'Remember that p → q is false only when p is true and q is false.'
    if 'equivalent to' in text or 'which is equivalent' in text or 'which formula is' in text:
        return 'You can use truth tables or known equivalences to test equivalence.'
    if 'how many rows' in text or 'truth table with' in text or 'rows are in a truth table' in text:
        return 'Use 2^n where n is the number of distinct propositional variables.'
    if 'cnf' in text or 'dnf' in text:
        return 'Check whether the formula is an AND of ORs (CNF) or an OR of ANDs (DNF).'
    if 'satisfiable' in text or 'unsatisfiable' in text:
        return 'Try to find at least one assignment that makes the formula true (or show none exist).'
    if 'contradiction' in text:
        return 'A contradiction can never be true; look for a formula that is always false.'
    if 'biconditional' in text or '↔' in text or 'p ↔ q' in text:
        return 'A biconditional is true when both sides have the same truth value.'
    if 'exclusive or' in text or 'xor' in text or '⊕' in text:
        return 'XOR is true when exactly one of the operands is true, not both.'
    if 'dual of' in text:
        return 'Swap ∧ and ∨ while leaving literals intact to get the dual.'
    if 'predicate logic' in q.get('topic','').lower() or 'quantifier' in text or '∀' in text or '∃' in text:
        return 'Think about how quantifiers distribute and how negation moves between them.'
    if 'sets' in q.get('topic','').lower() or 'union' in text or 'intersection' in text:
        return 'Consider members of the sets and whether the element satisfies the conditions.'
    if 'which is a contingency' in text or 'contingency' in text:
        return 'A contingency is sometimes true and sometimes false depending on the variables.'
    if 'which is logically equivalent' in text or 'logically equivalent to' in text:
        return 'Test equivalence by comparing truth values for all possible assignments.'
    if 'rules of inference' in q.get('topic','').lower() or 'modus' in text or 'inference' in text:
        return 'Apply known rules of inference like modus ponens or modus tollens.'
    if 'sets' in q.get('topic','').lower():
        return 'Think about how the set operations affect membership.'
    if 'proof' in q.get('topic','').lower() or 'introduction to proofs' in q.get('topic','').lower():
        return 'Try using known techniques: direct proof, contradiction, or induction where appropriate.'

    # Generic hints based on content
    if 'not' in text or '¬' in text or '!' in ''.join(q.get('options','')):
        return 'Consider how negation affects each part of the statement.'
    if 'and' in text or '∧' in text or '&' in ''.join(q.get('options','')):
        return 'An AND statement is true only when every part is true.'
    if 'or ' in text or '∨' in text or '|' in ''.join(q.get('options','')):
        return 'An OR statement is true when at least one part is true.'

    # Fallback
    return 'Focus on the structure of the statement and apply a relevant rule or truth table.'


import os
if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), '..', 'logic_questions_200.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        # Ensure we do not overwrite an existing hint
        if 'hint' in item:
            continue
        hint = make_hint(item)
        item_keys = list(item.keys())
        # Insert hint before explanation by constructing a new ordered dict-like sequence
        new = {}
        placed = False
        for k, v in item.items():
            if not placed and k == 'explanation':
                new['hint'] = hint
                placed = True
            new[k] = v
        # Replace item in data
        item.clear()
        item.update(new)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print('Hints added successfully.')
