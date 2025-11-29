import pytest

from logic.evaluator import check_argument_validity, normalize_formula


def run(premises, conclusion):
    prem = [normalize_formula(p) for p in premises]
    concl = normalize_formula(conclusion)
    return check_argument_validity(prem, concl)


def test_single_p_implies_p():
    assert run(["p"], "p") == "Valid"


def test_single_p_not_imply_q():
    assert run(["p"], "q") == "Invalid"


def test_modus_ponens():
    assert run(["p -> q", "p"], "q") == "Valid"


def test_transitive_implication():
    assert run(["p -> q", "q -> r", "p"], "r") == "Valid"


def test_disjunction_elimination_simple():
    # p ∨ q, ¬p  ⊢ q
    assert run(["p || q", "!p"], "q") == "Valid"


def test_conjunction_projection():
    assert run(["p ∧ q"], "p") == "Valid"


def test_conclusion_tautology_with_no_premises():
    # With no premises, only tautologies are valid conclusions
    assert run([], "p || !p") == "Valid"


def test_malformed_formula_returns_error():
    res = run(["p &&"], "q")
    assert isinstance(res, str) and res.startswith("Error")
