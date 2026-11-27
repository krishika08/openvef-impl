"""D-024 Phase B: the candidate-only adapters (runner/adapters_v137.py) meet the same D-013/D-017/D-022 conditions as
the v1.3.6 adapters, checked with the same functions (tests/test_dispatch_shapes.py) against the v1.3.7 CANDIDATE
pack (proposals/v1.3.7/pack; not audited). Also: v1.3.6 keeps its table, every v1.3.6 contract is still verbatim
in the candidate, and every value the candidate ledger produces is in the candidate line it cites.

One stated difference from the v1.3.6 boundary check: an in-domain edge may be a fixture input for a property in
EDGE_MAY_BE_A_FIXTURE_INPUT, and only if every value of that property's closed domain is a fixture input (D-024
Phase B; owner review pending).
"""
from __future__ import annotations

import ast
import json
import sys
import unittest
import unittest.mock
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
for p in (HERE, REPO / "src", REPO / "runner"):
    sys.path.insert(0, str(p))

import adapters_v137  # noqa: E402
import run_f18  # noqa: E402
import test_dispatch_shapes as v136  # noqa: E402
from adapter_contracts import CONTRACTS as CONTRACTS_136, DOMAINS as DOMAINS_136  # noqa: E402
from adapter_contracts_v137 import CONTRACTS, DOMAINS, VALUE_SUPPORT  # noqa: E402
from adapter_vectors_v137 import (BLOCKED, BOUNDARIES, EDGE_MAY_BE_A_FIXTURE_INPUT, JUDGED_BY_RULE,  # noqa: E402
                                  OUT_OF_DOMAIN, VECTORS)
from openvef.ledger import CANDIDATE_TOKENS, LIFECYCLE_CASES, lifecycle_expectation_candidate  # noqa: E402

CAND = REPO / "proposals/v1.3.7/pack"
TABLE = run_f18.PACKS["v1.3.7-candidate"]["adapters"]
REPLACED = {fn.__name__: adapters_v137.REPLACEMENTS[fn.__name__] for *_, fn in run_f18.ADAPTERS
            if fn.__name__ in adapters_v137.REPLACEMENTS}
ROWS = adapters_v137.ROWS
SOURCES = [REPO / "runner/adapters_v137.py", REPO / "runner/adapter_contracts_v137.py"]
# Fixtures C1-C10 do not cover (proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md section 1). M42 and M47 have an
# adapter but stop at PD-26.
# D-026: M41 and M37 have OWNER-SPECIFIED rows (OS-1, OS-2); P17's shape is OS-3, left unspecified (CORRECTIONS section 10).
OUT_OF_SCOPE = {"P17"}


def descriptors() -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text("utf-8")) for p in (CAND / "41_F18_Fixture_Inputs").glob("*.json")
            if p.name != "fixture-index.json"}


def line(tag: str, n: int) -> str:
    return next(CAND.glob(f"{tag}_*")).read_text("utf-8").splitlines()[n - 1]


def run(inp):
    validator = run_f18.load_schema_validator(CAND)
    with unittest.mock.patch.object(run_f18, "ADAPTER_TABLE", TABLE), \
            unittest.mock.patch.object(adapters_v137, "PACK_VERIFIED", True):  # as main() sets it after verifying
        rows = run_f18.find_adapters(inp)
        return [r[2].__name__ for r in rows], run_f18.execute({"input": inp, "manifest_clause_ids": ["UART-001"]}, validator)


def check(case, expected, outcome):
    status, actual, note = outcome
    if isinstance(expected, str):
        case.assertEqual(status, "NOT_IMPLEMENTED", actual)
        case.assertIn(expected[len(BLOCKED):], note)
    else:
        case.assertEqual((status, actual), ("EXECUTED", expected))


@unittest.skipUnless(CAND.exists(), "candidate pack not present (audit bundle)")
class CandidateDispatchTests(unittest.TestCase):
    def setUp(self):
        self.descs = descriptors()
        self.assertEqual(len(self.descs), 144)

    # --- the two tables
    def test_v136_table_is_unchanged_and_candidate_extends_it(self):
        self.assertEqual(run_f18.PACKS["v1.3.6"]["adapters"], run_f18.ADAPTERS)
        self.assertIs(run_f18.ADAPTER_TABLE, run_f18.ADAPTERS)
        self.assertEqual(TABLE, tuple((r, o, adapters_v137.REPLACEMENTS.get(fn.__name__, fn)) for r, o, fn in run_f18.ADAPTERS)
                         + ROWS)
        self.assertEqual(set(REPLACED), {"adapt_halt_recurrence"})  # the only v1.3.6 row the candidate replaces
        self.assertFalse({fn for *_, fn in ROWS} & {fn for *_, fn in run_f18.ADAPTERS})

    def test_v136_contracts_still_verbatim_in_the_candidate(self):
        with unittest.mock.patch.object(v136, "PACK", CAND):
            self.assertEqual(v136.contract_problems(run_f18.ADAPTERS, CONTRACTS_136), [])
        for adapter, props in DOMAINS_136.items():
            for prop, d in props.items():
                text = "\n".join(line(t, n) for t, n in d["lines"])
                for term in d["terms"]:
                    self.assertIn(term, text, (adapter, prop))

    # --- (a) contracts, domains, values
    def test_every_candidate_adapter_has_a_cited_contract(self):
        new = ROWS + tuple((r, o, REPLACED[fn.__name__]) for r, o, fn in run_f18.ADAPTERS if fn.__name__ in REPLACED)
        with unittest.mock.patch.object(v136, "PACK", CAND):
            self.assertEqual(v136.contract_problems(new, CONTRACTS), [])
        self.assertEqual(set(CONTRACTS), {fn.__name__ for *_, fn in new})

    def test_cited_text_covers_every_property_domain(self):
        self.assertEqual({a: set(c["inputs"]) for a, c in CONTRACTS.items()}, {a: set(d) for a, d in DOMAINS.items()})
        for adapter, props in DOMAINS.items():
            for prop, d in props.items():
                text = "\n".join(line(t, n) for t, n in d["lines"])
                for term in d["terms"]:
                    with self.subTest(adapter=adapter, prop=prop, term=term):
                        self.assertIn(term, text)

    def test_selecting_values_cited_within_a_domain_and_supported(self):
        for adapter, c in CONTRACTS.items():
            lines = {l for d in DOMAINS[adapter].values() for l in d["lines"]}
            for value, (tag, n, _) in c["values"].items():
                self.assertIn((tag, n), lines, (adapter, value))
        self.assertEqual(v136.value_support_problems(CONTRACTS, VALUE_SUPPORT), [])
        self.assertEqual(set(CONTRACTS["adapt_change_class"]["values"]), set(adapters_v137.CHANGE_CLASSES))
        self.assertEqual(set(CONTRACTS["adapt_domain_validation"]["values"]), set(adapters_v137.DOMAIN_VALIDATIONS))
        self.assertFalse(set(adapters_v137.CHANGE_CLASSES) & set(adapters_v137.DOMAIN_VALIDATIONS))  # OD-3
        self.assertEqual(set(CONTRACTS["adapt_parser_unit_vector"]["values"]), set(adapters_v137.SOURCE_FILES))

    def test_compared_strings_are_cited(self):
        tree = ast.parse(SOURCES[0].read_text("utf-8"))
        for fn in (n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("adapt_")):
            with self.subTest(adapter=fn.name):
                self.assertEqual(v136.uncited_values(fn.name, [fn], CONTRACTS), set())

    def test_every_property_is_checked_against_its_domain(self):
        self.assertEqual({a: set(d) for a, d in OUT_OF_DOMAIN.items()}, {a: set(d) for a, d in DOMAINS.items()})
        for adapter, props in OUT_OF_DOMAIN.items():
            for prop, inp in props.items():
                with self.subTest(adapter=adapter, prop=prop):
                    names, (status, actual, note) = run(inp)
                    self.assertEqual(names, [adapter])
                    if (adapter, prop) in JUDGED_BY_RULE:
                        self.assertEqual((status, actual["disposition"]), ("EXECUTED", "REPAIR"))
                    else:
                        self.assertEqual(status, "NOT_IMPLEMENTED", (actual, note))

    # --- (b) vectors
    def test_every_candidate_adapter_has_synthetic_vectors(self):
        new = ROWS + tuple((r, o, REPLACED[fn.__name__]) for r, o, fn in run_f18.ADAPTERS if fn.__name__ in REPLACED)
        self.assertEqual(v136.vector_problems(new, VECTORS, self.descs), [])

    def test_vectors_give_the_expected_outcome(self):
        for name, vectors in VECTORS.items():
            for inp, expected in vectors:
                with self.subTest(adapter=name, inp=str(inp)[:120]):
                    names, outcome = run(inp)
                    self.assertEqual(names, [name])
                    check(self, expected, outcome)

    # --- (c) boundaries (D-017)
    def test_every_property_has_boundary_pairs(self):
        problems = v136.boundary_problems(DOMAINS, BOUNDARIES, self.descs)
        allowed = {f"{a}.{p} ({term}): a fixture input" for a, pairs in BOUNDARIES.items()
                   for term, p, edge, _, outside, _ in pairs
                   if (a, p) in EDGE_MAY_BE_A_FIXTURE_INPUT and outside not in [d["input"] for d in self.descs.values()]}
        self.assertEqual([p for p in problems if p not in allowed], [])
        self.assertEqual(set(BOUNDARIES), {fn.__name__ for *_, fn in ROWS} | {f.__name__ for f in REPLACED.values()})

    def test_edge_exception_holds_only_for_a_fully_used_closed_domain(self):
        self.assertEqual(EDGE_MAY_BE_A_FIXTURE_INPUT, {("adapt_change_class", "change_class"),
                                                       ("adapt_domain_validation", "domain_validation")})
        used = {d["input"].get("change_class") for d in self.descs.values()}
        self.assertLessEqual(set(adapters_v137.CHANGE_CLASSES), used)
        used = {d["input"].get("domain_validation") for d in self.descs.values()}
        self.assertLessEqual(set(adapters_v137.DOMAIN_VALIDATIONS), used)

    def test_boundary_pairs_give_the_expected_outcomes(self):
        for adapter, pairs in BOUNDARIES.items():
            for term, prop, edge, edge_exp, outside, outside_exp in pairs:
                for inp, expected in ((edge, edge_exp), (outside, outside_exp)):
                    with self.subTest(adapter=adapter, prop=prop, term=term, inp=ascii(inp[prop])[:100]):
                        names, outcome = run(inp)
                        self.assertEqual(names, [adapter])
                        check(self, expected, outcome)

    # --- structure
    def test_no_ambiguous_shape_and_shapes_left_out(self):
        with unittest.mock.patch.object(run_f18, "ADAPTER_TABLE", TABLE):
            for fid, d in self.descs.items():
                self.assertLessEqual(len(run_f18.find_adapters(d["input"])), 1, fid)
            self.assertEqual({f for f, d in self.descs.items() if not run_f18.find_adapters(d["input"])}, OUT_OF_SCOPE)

    def test_no_shape_branch_and_no_fixture_id(self):
        # Allowed (approved by Krishika, D-026 item 1): the two primitive adapters check their cited `test_scope` property
        # against the one value candidate File 36 L196/L197 fixes, and refuse any other; this selects no code path.
        allowed = {"adapt_truncation_primitive: inp['test_scope'] == TRUNCATION_SCOPE",
                   "adapt_json_primitive: inp['test_scope'] == JSON_SCOPE"}
        found = v136.shape_branches(ast.parse(SOURCES[0].read_text("utf-8")))
        self.assertEqual([f for f in found if f not in allowed], [])
        for path in [*SOURCES, REPO / "src/openvef/ledger.py"]:
            for node in ast.walk(ast.parse(path.read_text("utf-8"))):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    self.assertNotIn(node.value, self.descs, path.name)

    # --- D-026: OWNER-SPECIFIED rows are labelled, counted apart, and cite only the OWNER-SPECIFIED lines
    def test_owner_specified_rows_and_open_shapes(self):
        names = {fn.__name__ for *_, fn in ROWS}
        self.assertEqual(adapters_v137.OWNER_SPECIFIED, {"adapt_operational_recovery": "OS-1",
                                                         "adapt_paired_run_outcome": "OS-2"})
        self.assertLessEqual(set(adapters_v137.OWNER_SPECIFIED), names)
        self.assertEqual([o[2] for o in adapters_v137.OPEN_SHAPES], ["OS-3"])
        info = run_f18.PACKS["v1.3.7-candidate"]
        self.assertIs(info["owner_specified"], adapters_v137.OWNER_SPECIFIED)
        self.assertNotIn("owner_specified", run_f18.PACKS["v1.3.6"])  # v1.3.6 records carry no category
        for name, os_id in adapters_v137.OWNER_SPECIFIED.items():
            cited = [c for c in CONTRACTS[name]["inputs"].values()]
            self.assertTrue(all((t, n) == ("36", {"OS-1": 205, "OS-2": 206}[os_id]) for t, n, _ in cited), name)
            self.assertIn(f"({os_id}", line("36", 205 if os_id == "OS-1" else 206))
        self.assertIn("(OS-3)", line("36", 207))
        self.assertIn("OWNER-SPECIFIED", line("36", 201))

    def test_owner_specified_labels_reach_the_record_reason(self):
        validator = run_f18.load_schema_validator(CAND)
        with unittest.mock.patch.object(run_f18, "ADAPTER_TABLE", TABLE), \
                unittest.mock.patch.object(run_f18, "OWNER_SPECIFIED_ROWS", adapters_v137.OWNER_SPECIFIED), \
                unittest.mock.patch.object(run_f18, "OPEN_SHAPES", adapters_v137.OPEN_SHAPES):
            for fid, d in self.descs.items():
                run_f18.OWNER_SPEC = None
                status, _, note = run_f18.execute(d, validator)
                with self.subTest(fixture=fid):
                    if fid in OUT_OF_SCOPE:
                        self.assertEqual((status, run_f18.OWNER_SPEC), ("NOT_IMPLEMENTED", "OS-3"))
                        self.assertIn("OS-3 (OWNER-SPECIFIED, D-026)", note)
                    names = [r[2].__name__ for r in run_f18.find_adapters(d["input"])]
                    expected = adapters_v137.OWNER_SPECIFIED.get(names[0]) if names else "OS-3"
                    self.assertEqual(run_f18.OWNER_SPEC, expected)
            run_f18.OWNER_SPEC = None

    def test_owner_decided_rows(self):
        """D-027: every OD rule an adapter rests on is labelled in a candidate line that adapter's contract cites."""
        names = {fn.__name__ for *_, fn in ROWS} | {f.__name__ for f in REPLACED.values()}
        self.assertLessEqual(set(adapters_v137.OWNER_DECIDED), names)
        self.assertIs(run_f18.PACKS["v1.3.7-candidate"]["owner_decided"], adapters_v137.OWNER_DECIDED)
        self.assertNotIn("owner_decided", run_f18.PACKS["v1.3.6"])
        for name, items in adapters_v137.OWNER_DECIDED.items():
            c = CONTRACTS[name]
            cited = "\n".join(line(t, n) for t, n, _ in [*c["inputs"].values(), *c["outcome"]])
            for item in items:
                with self.subTest(adapter=name, item=item):
                    self.assertIn(f"OWNER-DECIDED {item}", cited)

    def test_paired_run_outcome_runs_no_artifact_code(self):
        """OS-2 runs steps (1)-(6) only: no sandbox and no factory check is reached (D-015, D-026 option (a))."""
        from adapter_vectors_v137 import paired
        with unittest.mock.patch.object(run_f18, "factory_checks", side_effect=AssertionError("step (7) reached")), \
                unittest.mock.patch.object(run_f18, "SANDBOX", None):
            names, (status, actual, _) = run(paired())
        self.assertEqual((names, status, actual["error_class"]),
                         (["adapt_paired_run_outcome"], "EXECUTED", "DRIVER_NONDETERMINISM"))

    # --- the candidate ledger: every produced value is in the candidate line that states it
    def test_candidate_lifecycle_values_are_in_their_candidate_lines(self):
        l175, l176, l185 = line("02", 175), line("02", 176), line("02", 185)
        self.assertEqual(set(LIFECYCLE_CASES), set(adapters_v137.CHANGE_CLASSES) | set(adapters_v137.DOMAIN_VALIDATIONS))
        for change_class, case in LIFECYCLE_CASES.items():
            record, missing = lifecycle_expectation_candidate(change_class)
            self.assertEqual(missing, {}, change_class)
            self.assertIn(f"`{change_class}`", l176)
            self.assertIn(f"`{change_class}`", line("02", 571 if change_class in adapters_v137.CHANGE_CLASSES else 572))
            self.assertIn(f"`{record['error_class']}`", l175)
            self.assertIn(f"`{record['diagnostic']}`", l175)
            if "required_action" in record:
                self.assertIn(f"`{change_class}` = `{record['required_action']}`", l176)
            for name, (value, _) in CANDIDATE_TOKENS.get(change_class, {}).items():
                self.assertIn(f"`{name}` = `{value}`", l176 + l185, (change_class, name))
                self.assertEqual(record[name], value)
        with self.assertRaises(ValueError):
            lifecycle_expectation_candidate("SOMETHING_ELSE")


if __name__ == "__main__":
    unittest.main()
