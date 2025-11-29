import json
import os

MAPPING = {
    1: "Check which statement is always true regardless of truth values.",
    2: "Apply De Morgan’s law to negate a conjunction.",
    3: "Recall: any implication with a false antecedent is true.",
    4: "A biconditional is true only when both truth values match.",
    5: "Exclusive OR means exactly one input is true.",
    6: "Rewrite p → q as ¬p ∨ q before comparing.",
    7: "A contradiction is never true under any valuation.",
    8: "To negate p→q, convert to ¬(¬p∨q) and simplify.",
    9: "Contingency means sometimes true, sometimes false.",
    10: "Truth table rows = 2ⁿ for n variables.",
    11: "Convert (p∧q)→r by negating the antecedent.",
    12: "CNF must be an AND of OR clauses.",
    13: "Expand p ↔ q using two implications.",
    14: "DNF is ORs of ANDs.",
    15: "Unsatisfiable means always false (no satisfying valuation).",
    16: "Dual swaps ∧ and ∨ everywhere.",
    17: "Negate step-by-step using De Morgan’s laws.",
    18: "XOR is associative like addition modulo 2.",
    19: "Use the identity ¬p → X ≡ p ∨ X.",
    20: "Satisfiable means true for at least one assignment.",
    21: "Universal quantifier means 'for all'.",
    22: "Negation of ∀ becomes ∃ with negated predicate.",
    23: "Existential translates to 'there exists…'.",
    24: "Domain is the universe over which variables range.",
    25: "Existential conjunction needs one element satisfying both.",
    26: "Negation of ∃ becomes ∀ with negated expression.",
    27: "Translate 'everyone likes someone' using nested quantifiers.",
    28: "Universal conditional fails when antecedent is true and consequent is false.",
    29: "∃x∀y means one single x works for all y.",
    30: "Negation of 'exactly one' becomes none or more than one.",
    31: "Check whether universal distributes over AND.",
    32: "Swap quantifiers and negate the implication.",
    33: "Universal does NOT distribute over OR.",
    34: "Uniqueness uses implication from equal outputs to equal inputs.",
    35: "Pull out independent quantifiers when possible.",
    36: "Compare logical strength by checking vacuous truth cases.",
    37: "∃x∀y means one x relates universally.",
    38: "At least two means existence of two distinct elements.",
    39: "Unique existence is encoded with ∃!.",
    40: "Negation of biconditional yields exclusive OR.",
    41: "Cardinality simply counts elements.",
    42: "The empty set is subset of every set.",
    43: "Power set contains all possible subsets.",
    44: "Intersection contains only common elements.",
    45: "Complement lists elements outside the set.",
    46: "Disjoint sets add cardinalities directly.",
    47: "Use De Morgan for complement of union.",
    48: "A − B keeps elements of A not in B.",
    49: "A ⊆ B implies intersections behave predictably.",
    50: "Apply inclusion–exclusion formula.",
    51: "Symmetric difference removes intersections.",
    52: "Cartesian product forms ordered pairs.",
    53: "Recognize symmetric difference patterns.",
    54: "Proper subset means strictly smaller size.",
    55: "Apply De Morgan twice for complement of intersection.",
    56: "Absorption law simplifies A ∪ (A∩B) to A.",
    57: "If intersection equals A, then A ⊆ B.",
    58: "If union equals A, then B ⊆ A.",
    59: "Subsets count = 2ⁿ.",
    60: "Divide |A×B| by |A| to solve for |B|.",
    61: "AND gate corresponds to multiplication.",
    62: "Identity for OR is 0.",
    63: "Complement flips each bit.",
    64: "NOT gate outputs the opposite value.",
    65: "AND requires both inputs to be true.",
    66: "XOR is true when inputs differ.",
    67: "x + x' always equals 1.",
    68: "Factor expressions before simplifying.",
    69: "NAND is functionally complete.",
    70: "Apply De Morgan on AND expression.",
    71: "XNOR checks for equality.",
    72: "Distribute and simplify step-by-step.",
    73: "MUX selects an input based on selector bit.",
    74: "Combine like terms to simplify.",
    75: "Use K-map grouping for minimal SOP.",
    76: "De Morgan’s gives complements of sums.",
    77: "XOR cannot be implemented with a single 2-input gate.",
    78: "Complement an expression using De Morgan carefully.",
    79: "XOR = x'y + xy'.",
    80: "Minimal POS comes from zeros in truth table.",
    81: "Modus Ponens uses p→q and p to infer q.",
    82: "Conjunction combines two true statements.",
    83: "Addition rule forms p∨q from p.",
    84: "Simplification extracts components of conjunction.",
    85: "Chain rule links implications in sequence.",
    86: "Modus Tollens rejects antecedent via ¬q.",
    87: "Proof by cases uses OR information.",
    88: "Resolution eliminates opposing literals.",
    89: "Hypothetical syllogism chains implications.",
    90: "Use contrapositive for clarity.",
    91: "Begin direct proof by assuming antecedent.",
    92: "Existential proof requires an explicit witness.",
    93: "Contradiction assumes negation of conclusion.",
    94: "Even integer proof uses n=2k.",
    95: "Contrapositive flips and negates.",
    96: "Universal falsehood requires single counterexample.",
    97: "Contrapositive often easier than direct proof.",
    98: "Prove biconditional by proving two implications.",
    99: "Even numbers are multiples of 2.",
    100: "Exhaustive proof works only with finite cases.",
    101: "Universal quantifier means ‘for all’.",
    102: "Negate ∃ to obtain ∀ with negation.",
    103: "Unique existence means exactly one instance.",
    104: "Existential outer quantifier binds x to all y.",
    105: "Apply De Morgan carefully inside quantifiers.",
    106: "Translate text to quantifiers stepwise.",
    107: "Negation of existential becomes universal negation.",
    108: "Universal conditional fails when P holds and Q doesn't.",
    109: "Existential conjunction needs one element satisfying both.",
    110: "Universal distributes only over AND.",
    111: "Negate ∀∃ by swapping quantifiers.",
    112: "Uniqueness requires existence plus uniqueness.",
    113: "¬∃ is equivalent to ∀¬.",
    114: "State distinctness explicitly for 'at least three'.",
    115: "Interpret implication inside quantifiers carefully.",
    116: "Negation swaps quantifiers and negates inner predicate.",
    117: "Non-empty domain shown by existential tautology.",
    118: "At most one uses uniqueness implication.",
    119: "Each person must admire at least one person.",
    120: "Negate ∃∀ using De Morgan and quantifier rules.",
    121: "Use combination formula C(n,r).",
    122: "Factorial grows multiplicatively.",
    123: "Subsets count equals 2ⁿ.",
    124: "Permutation of n distinct items is n!.",
    125: "Count strings using choices per position.",
    126: "Permutations count arrangements.",
    127: "Apply formula for combinations.",
    128: "Combination counts choose subsets without order.",
    129: "Number of functions is codomain^domain.",
    130: "Account for repeated letters using n!/(counts!).",
    131: "Circular arrangements use (n−1)!.",
    132: "No repetition means permutation rules.",
    133: "Surjection count uses inclusion–exclusion.",
    134: "Stirling number counts partitions.",
    135: "Use C(10,4) directly.",
    136: "Bell number counts partitions of a set.",
    137: "Use permutations for no repeats.",
    138: "Injective functions count as permutations.",
    139: "Use stars and bars for distribution problems.",
    140: "Exactly one way to separate items into singletons.",
    141: "Reflexive means self-pairs exist.",
    142: "Function assigns exactly one output to each input.",
    143: "Domain equals input set.",
    144: "Injective means distinct inputs give distinct outputs.",
    145: "Surjective means codomain fully covered.",
    146: "Equivalence relation needs three properties.",
    147: "Antisymmetric forbids symmetric pairs unless equal.",
    148: "Bijection requires both injective and surjective.",
    149: "Only bijective functions have inverses.",
    150: "Count functions using codomain^domain.",
    151: "Relations count as subsets of A×A.",
    152: "Partial order needs reflexive, antisymmetric, transitive.",
    153: "Composition g∘f means apply f then g.",
    154: "Number of bijections equals n!.",
    155: "Add missing reflexive pairs for equivalence.",
    156: "Solve using |A×B| = |A| × |B|.",
    157: "Idempotent means f(f(x))=f(x).",
    158: "Irreflexive means no element relates to itself.",
    159: "Not injective means two inputs share one output.",
    160: "Equivalence relations correspond to partitions."
}


def insert_hints(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        id_ = item.get('id')
        if id_ in MAPPING:
            hint = MAPPING[id_]
            # Insert hint before explanation while preserving order
            new = {}
            placed = False
            for k, v in item.items():
                if not placed and k == 'explanation':
                    new['hint'] = hint
                    placed = True
                new[k] = v
            # If there is no 'explanation' field, append 'hint' at the end
            if not placed:
                new['hint'] = hint

            item.clear()
            item.update(new)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    p = os.path.join(os.path.dirname(__file__), '..', 'logic_questions_200.json')
    insert_hints(p)
    print('Inserted exact-user hints for IDs 1-160.')
