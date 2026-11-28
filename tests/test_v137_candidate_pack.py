"""D-024/D-025 Phase A: proposals/v1.3.7/pack/ is v1.3.6 with only the logged corrections, amendments and stale-reference
fixes applied (v1.3.7 CANDIDATE, not audited). Checks the copy, not any implementation: it is rebuilt byte for byte
from the read-only baseline; only the expected files differ (renamed files compared under their v1.3.6 names); no
existing line moves and only the edited lines change; File 25's normative copy still equals the Protocol; checksums
and the fixture index agree; the corrected M27 reaches check (e). Not an F18 run and not evidence."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
HERE = REPO / "proposals/v1.3.7"
PACK = HERE / "pack"
BASE = REPO / "baseline/OpenVEF_Planning_v1_3_6"

try:  # D-030: only the M27 test needs the implementation; the document-audit bundle has the tests, not src/
    from openvef.stage_map import validate_vector  # noqa: E402
except ImportError:  # pragma: no cover - only outside the repository
    if (REPO / "src/openvef").exists():
        raise  # in the repository a failed import is an error, never a skip
    validate_vector = None

ADDED = {"CHANGELOG-v1.3.7-candidate.md", "CANDIDATE-LABEL.md", "SHA256SUMS-v1.3.7-candidate.txt"}
FX = "41_F18_Fixture_Inputs/"

# D-030 (D3-2): the three status parts as explicit labels, in this order (C19).
STATUS_LABELS = ("Development-run evidence", "Formal F18 status", "Approval")
QUOTES = "\"'`“”‘’"
# D-031 (D4-1): every quote kind in QUOTES, as (opening, closing). A straight mark opens and closes itself; a
# typographic pair opens with the first and closes with the second. The assertion keeps the two from drifting apart.
QUOTE_PAIRS = (('"', '"'), ("'", "'"), ("`", "`"), ("“", "”"), ("‘", "’"))
assert set(QUOTES) == {q for pair in QUOTE_PAIRS for q in pair}

# D-031 (D4-1): each clause's closed vocabulary, drawn from the 17 current status lines and the two fixture-index
# fields (C19; CORRECTIONS section 13), plus the forms D-031 names. A value must equal one of these as a whole (after
# "**" emphasis is removed); a prefix match is not enough. A new wording needs a new entry here, made on purpose.
# The only cross-reference: File 21's two table headers (L7, L40) point to the "## F18 result" section below them,
# whose lines L52 and L70 state the parts; test_current_status_lines_have_three_parts checks that the section exists.
XREF = 'see "F18 result" below'
# Development-run evidence: says the runs are not counted (not F18 acceptance), says none, or names runs.
DEV_EVIDENCE = (
    "development runs are not F18 acceptance",                                   # File 21 L26, File 36 L176, README L16
    "development runs only, not F18 acceptance",                                 # File 32 L33, README L46
    "runs of a project implementation are development runs, not F18 acceptance",  # Protocol L559
    "runs of a project implementation, recorded outside this pack, are development runs, not F1–F18 acceptance",
    # ^ Charter L177; v the other nine lines and both fixture-index fields
    "fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance",
    "none", "not counted",                                                       # D-031: "say none/not counted"
    XREF,                                                                        # File 21 L7, L40
)
RUN_ID = r"`?run(?:-[a-z0-9]+)?-\d{8}T\d{6}Z`?"
# D-031: "name a run": one or more run IDs (`run-…-YYYYMMDDTHHMMSSZ`), optionally said not to count.
DEV_NAMED_RUNS = rf"{RUN_ID}(?:(?:, | and ){RUN_ID})*(?:, not counted|, not F18 acceptance)?"
# Formal F18 status: the pack's formal-status terms as the 17 lines use them, and an optional closed qualifier.
FORMAL_TERMS = ("NOT RUN / NOT PASSED", "NOT RUN", "not run")
FORMAL_QUALIFIERS = ("", ", since no authorized F18 acceptance run exists",
                     ", since no authorized F1–F18 acceptance run exists", ", since there is no authorized F18 acceptance run",
                     ", as given in each row")
# Approval: an approval state. The clause ends at ";", "|", the end of its sentence ("." then a space or the end), or
# the ")" that closes a table header; File 36 L176 adds one fixed parenthesis.
APPROVAL_STATES = ("nothing is approved", "nothing is qualified or approved", "no implementation is qualified or approved",
                   "the implementation is not qualified or approved", XREF)
APPROVAL_TAIL = r"(?:\s*|\.(?:\s.*)?|\)\s*| \(see the status line at the top of this file\)\.(?:\s.*)?)"


def _inside_quotes(before: str) -> bool:
    """True when the text before a label leaves a quotation open, for every kind in QUOTE_PAIRS. A "'" or "’" between
    two word characters is an apostrophe ("descriptor's"), not a quotation mark."""
    import re
    text = re.sub(r"(?<=\w)['’](?=\w)", "", before)
    for opening, closing in QUOTE_PAIRS:
        if opening == closing:
            if text.count(opening) % 2:
                return True
        elif text.count(opening) > text.count(closing):
            return True
    return False


def _value_problem(i: int, value: str) -> str | None:
    """Why the value of clause i (0, 1, 2 in STATUS_LABELS order) is outside its closed vocabulary; None when inside."""
    import re
    plain = value.replace("**", "").strip()
    if not plain:
        return "empty value"
    if i == 0:
        if plain in DEV_EVIDENCE or re.fullmatch(DEV_NAMED_RUNS, plain):
            return None
        return f"value {plain[:60]!r} neither names a run nor says none/not counted"
    if i == 1:
        if any(plain == t + q for t in FORMAL_TERMS for q in FORMAL_QUALIFIERS):
            return None
        return f"value {plain[:60]!r} is not one of the formal-status terms {FORMAL_TERMS}"
    for state in APPROVAL_STATES:
        if plain.startswith(state) and re.fullmatch(APPROVAL_TAIL, plain[len(state):], re.S):
            return None
    return f"value {plain[:60]!r} does not state an approval state"


def labelled_status(line: str) -> list[str]:
    """Problems with a status line under C19; [] when it is well formed. Each label appears exactly once, as written
    (case included), not preceded by a quotation mark, a hyphen or a word character, not inside quotation marks of any
    kind in QUOTES (_inside_quotes), and directly followed by exactly ": " and a non-space character; the labels come in
    STATUS_LABELS order. Each value runs from its label to the next ";" or "|" (the last label's value; for the first
    two, it must end with "; " right before the next label) and must be in its clause's closed vocabulary
    (_value_problem, D-031). This is a lexical check: it rejects placeholders and unknown wordings, it cannot show that
    a value is true."""
    import re
    problems, at = [], []
    for label in STATUS_LABELS:
        hits = []
        for m in re.finditer(re.escape(label) + ":", line):
            before = line[:m.start()]
            if before and (before[-1].isalnum() or before[-1] in QUOTES + "-"):
                continue
            if _inside_quotes(before):
                continue
            if not re.match(r" \S", line[m.end():]):
                problems.append(f"{label!r}: not followed by exactly ': ' and a value")
                continue
            hits.append(m)
        if len(hits) != 1:
            problems.append(f"{label!r}: {len(hits)} unquoted occurrences, need exactly 1")
        else:
            at.append(hits[0])
    if problems:
        return problems
    if [m.start() for m in at] != sorted(m.start() for m in at):
        return ["labels out of order"]
    for i, m in enumerate(at):
        end = at[i + 1].start() if i + 1 < len(at) else len(line)
        value = line[m.end():end]
        if i + 1 < len(at):
            if not value.endswith("; "):
                problems.append(f"{STATUS_LABELS[i]!r}: value does not end with '; ' right before the next label")
            value = value.rstrip()[:-1] if value.rstrip().endswith(";") else value
        else:
            value = re.split(r"[;|]", value, maxsplit=1)[0]
        why = _value_problem(i, value)
        if why:
            problems.append(f"{STATUS_LABELS[i]!r}: {why}")
    return problems


def files(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def builder():
    spec = importlib.util.spec_from_file_location("build_candidate", HERE / "build_candidate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class LabelledStatusRuleTests(unittest.TestCase):
    """D-031 (D4-1): labelled_status on its own, without the pack. Each negative case must fail, and fail for the
    reason given (a substring of one problem), so that a vocabulary failure cannot hide a broken quote or separator
    check. The positive cases are lines the rule must keep accepting."""

    GOOD = "F18 status: Development-run evidence: none; Formal F18 status: NOT RUN; Approval: nothing is approved."

    BAD = {
        # Audit #4, D4-1, verbatim: the three labels inside one straight single-quoted block.
        "auditor: single-quoted labels": ("F18 NOT RUN; ' Development-run evidence: x; Formal F18 status: y; Approval: z'",
                                          "0 unquoted occurrences"),
        # The same, with in-vocabulary values and the quote not next to a label, so only the quote count rejects it.
        "single-quoted labels, valid values": ("F18 status: 'the line Development-run evidence: none; Formal F18 status: "
                                               "NOT RUN; Approval: nothing is approved'", "0 unquoted occurrences"),
        # Audit #4, D4-1, verbatim: placeholder values.
        "auditor: x/y/z placeholders": ("F18 NOT RUN; Development-run evidence: x; Formal F18 status: y; Approval: z.",
                                        "neither names a run"),
        # "label:" without the space, values otherwise valid.
        "no space after the colon": ("F18 status: Development-run evidence:none; Formal F18 status: NOT RUN; "
                                     "Approval: nothing is approved.", "not followed by exactly ': '"),
        # Claude's own (1): two spaces after the colon.
        "two spaces after the colon": ("F18 status: Development-run evidence: none; Formal F18 status:  NOT RUN; "
                                       "Approval: nothing is approved.", "not followed by exactly ': '"),
        # Claude's own (2): placeholder words, not one letter.
        "TBD/TODO/n/a placeholders": ("F18 status: Development-run evidence: TBD; Formal F18 status: TODO; Approval: n/a.",
                                      "neither names a run"),
        # Claude's own (3): a formal-status term with extra letters; a prefix match must not pass.
        "status term as a prefix": ("F18 status: Development-run evidence: none; Formal F18 status: NOT RUNNING; "
                                    "Approval: nothing is approved.", "is not one of the formal-status terms"),
        # Claude's own (4): an invented qualifier after a real term.
        "invented qualifier": ("F18 status: Development-run evidence: none; Formal F18 status: NOT RUN, y; "
                               "Approval: nothing is approved.", "is not one of the formal-status terms"),
        # Claude's own (5): an approval value that is not an approval state.
        "approval not a state": ("F18 status: Development-run evidence: none; Formal F18 status: NOT RUN; Approval: z.",
                                 "does not state an approval state"),
        # Claude's own (6): an approval state followed by words in the same sentence.
        "approval state plus words": ("F18 status: Development-run evidence: none; Formal F18 status: NOT RUN; "
                                      "Approval: nothing is approved by nobody yet.", "does not state an approval state"),
        # Claude's own (7): a cross-reference to some other section.
        "other cross-reference": ('F18 status: Development-run evidence: see "Glossary" below; Formal F18 status: NOT RUN; '
                                  "Approval: nothing is approved.", "neither names a run"),
        # Claude's own (8), a regression guard (the audited code already rejected it): typographic single quotes.
        "typographic single quotes": ("F18 status: ‘Development-run evidence: none; Formal F18 status: NOT RUN; "
                                      "Approval: nothing is approved’", "0 unquoted occurrences"),
        # Claude's own (9), a regression guard (the audited code already rejected it): a backtick code span.
        "backtick code span": ("F18 status: `Development-run evidence: none; Formal F18 status: NOT RUN; "
                               "Approval: nothing is approved`", "0 unquoted occurrences"),
        # Claude's own (10): no space between the first value's ";" and the next label.
        "no space after ';'": ("F18 status: Development-run evidence: none;Formal F18 status: NOT RUN; "
                               "Approval: nothing is approved.", "does not end with '; '"),
    }

    GOOD_TOO = {
        "the base form": GOOD,
        "an apostrophe before the labels": "The runner checks each descriptor's hash; F18 status: " + GOOD[12:],
        "a typographic apostrophe": "The runner checks each descriptor’s hash; F18 status: " + GOOD[12:],
        "a named run": ("F18 status: Development-run evidence: `run-v137c-20261127T163649Z`, not counted; "
                        "Formal F18 status: NOT RUN; Approval: nothing is approved."),
        "two named runs": ("F18 status: Development-run evidence: run-20261123T174358Z and run-v137c-20261127T163649Z; "
                           "Formal F18 status: NOT RUN / NOT PASSED; Approval: nothing is approved."),
        "emphasis and a qualifier": ("F18 status: Development-run evidence: not counted; Formal F18 status: **NOT RUN / "
                                     "NOT PASSED**, since no authorized F18 acceptance run exists; Approval: no "
                                     "implementation is qualified or approved. A further sentence."),
        "quoted text after the labels": GOOD + ' See "F18 result".',
    }

    def test_d4_1_negative_cases_fail_for_their_reason(self):
        import re
        for name, (line, reason) in self.BAD.items():
            with self.subTest(case=name):
                self.assertTrue("F18" in line and re.search(CandidatePackTests.STATUS_TERMS, line), name)
                problems = labelled_status(line)
                self.assertNotEqual(problems, [], name)
                self.assertTrue(any(reason in p for p in problems), f"{name}: {problems}")

    def test_well_formed_lines_still_pass(self):
        for name, line in self.GOOD_TOO.items():
            with self.subTest(case=name):
                self.assertEqual(labelled_status(line), [], name)

    def test_every_quote_kind_is_checked(self):
        """Each kind in QUOTES, opened before the labels and not closed, hides them."""
        for opening, _ in QUOTE_PAIRS:
            with self.subTest(quote=opening):
                self.assertNotEqual(labelled_status(f"F18 status: {opening}" + self.GOOD[12:]), [])


@unittest.skipUnless(PACK.exists(), "candidate pack not present (audit bundle)")
class CandidatePackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = mod = builder()
        cls.pack, cls.base = files(PACK), files(BASE)
        # Every (v1.3.6 file, line) an edit may touch, from the build's own tables.
        edited: dict[str, set[int]] = {}
        src, first, last, copy, shift = mod.MIRROR
        for rel, n in ([(e[3], e[4]) for e in mod.EDITS] + [(s[0], s[1]) for s in mod.STALE]
                       + [(e[3], e[4]) for e in mod.CYCLE2]  # D-027 cycle 2 edits lines in place too
                       + [(e[3], e[4]) for e in mod.CYCLE3]  # D-029 cycle 3 (C18) as well
                       + [(e[3], e[4]) for e in mod.CYCLE4]):  # D-030 cycle 4 (C19) as well
            edited.setdefault(rel, set()).add(n)
            if rel == src and first <= n <= last:
                edited.setdefault(copy, set()).add(n + shift)
        for rel, n in {**mod.VERSION_LINES, **mod.CYCLE2_VERSION_LINES}.items():
            edited.setdefault(rel, set()).add(n)
        old_hash = hashlib.sha256(cls.base[mod.P10]).hexdigest()
        edited[mod.P22] = {i + 1 for i, l in enumerate(cls.base[mod.P22].decode().split("\n")) if old_hash in l}
        cls.edited = edited
        cls.changed = (set(edited) | set(mod.WHOLE_FILES) | set(mod.CYCLE2_WHOLE)
                       | {e[3] for e in mod.CYCLE2_APPENDS} | {"27_SHA256SUMS.txt", FX + "fixture-index.json"})

    def name(self, rel: str) -> str:
        """v1.3.6 name -> candidate name."""
        return self.mod.RENAMES.get(rel, rel)

    def test_rebuild_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.mod.build(Path(tmp) / "pack")
            self.assertEqual(files(Path(tmp) / "pack"), self.pack)

    def test_only_the_expected_files_differ(self):
        self.assertEqual(set(self.pack), {self.name(f) for f in self.base} | ADDED)
        self.assertEqual({f for f in self.base if self.base[f] != self.pack[self.name(f)]}, self.changed)
        self.assertEqual(set(self.mod.RENAMES) - self.changed, set())  # every renamed file is also edited

    def test_no_line_moves_and_only_edited_lines_change(self):
        for rel in {e[3] for e in self.mod.CYCLE2_APPENDS} - set(self.edited):
            self.edited[rel] = set()
        for rel, lines in self.edited.items():
            old = self.base[rel].decode("utf-8").split("\n")
            new = self.pack[self.name(rel)].decode("utf-8").split("\n")
            with self.subTest(file=rel):
                if rel.endswith(".md") or rel == self.mod.P25:  # appended lines (C12-C16), then the trailer
                    extra = self.appended(rel)
                    tail = ("\n".join(extra) + "\n" if extra else "") + self.mod.TRAILER
                    self.assertEqual("\n".join(new[len(old) - 1:]), tail)
                else:
                    self.assertEqual(len(new), len(old))
                self.assertEqual({i + 1 for i in range(len(old) - 1) if old[i] != new[i]},
                                 {n for n in lines if n <= len(old) - 1})  # edits of appended lines: in the tail

    def appended(self, rel: str) -> list[str]:
        """The lines appended after rel's last v1.3.6 line: cycle 1's, with the cycle-2 edits of those lines applied,
        then cycle 2's (D-027)."""
        base_len = len(self.base[rel].decode("utf-8").split("\n")) - 1
        extra = list(self.mod.APPENDS.get(rel, []))
        for item, _, _, path, n, old, new in self.mod.CYCLE2:
            if path == rel and n > base_len:
                self.assertEqual(extra[n - base_len - 1].count(old), 1, (item, rel, n))
                extra[n - base_len - 1] = extra[n - base_len - 1].replace(old, new)
        return extra + [l for c in self.mod.CYCLE2_APPENDS if c[3] == rel for l in c[4]]

    def test_file_25_copy_still_equals_the_protocol(self):
        """A2: File 25 L32 "normative text below is identical to Protocol §3.4"."""
        src, first, last, copy, shift = self.mod.MIRROR
        p = self.pack[self.name(src)].decode("utf-8").split("\n")
        c = self.pack[copy].decode("utf-8").split("\n")
        self.assertEqual(p[first - 1:last], c[first - 1 + shift:last + shift])
        # Both model-visible bodies end before the copy starts (L32); those lines are byte-identical to v1.3.6.
        base = self.base[copy].decode("utf-8").split("\n")
        self.assertIn("--- END MODEL-VISIBLE REPAIR-MESSAGE BODY ---", "\n".join(base[:first - 1 + shift - 1]))
        self.assertEqual(c[:first - 1 + shift], base[:first - 1 + shift])

    def test_labels(self):
        for rel in self.changed - {"27_SHA256SUMS.txt"}:
            text = self.pack[self.name(rel)].decode("utf-8")
            with self.subTest(file=rel):
                self.assertTrue("v1.3.7 CANDIDATE, not audited" in text or "1.3.7-candidate, not audited" in text
                                or "v1.3.7-candidate" in text)
        label = self.pack["CANDIDATE-LABEL.md"].decode("utf-8")
        for rel in self.pack:
            self.assertIn(f"`{rel}`", label)

    def test_no_stale_name_or_hash(self):
        renamed = set(self.mod.RENAMES)
        old_hash = hashlib.sha256(self.base[self.mod.P10]).hexdigest()
        current = {self.name(r) for r in renamed} | {"README.md", self.mod.P25, self.mod.P22}
        for rel in current:
            text = self.pack[rel].decode("utf-8")
            with self.subTest(file=rel):
                self.assertFalse([r for r in renamed if r in text])
                self.assertNotIn(old_hash, text)

    def test_checksums_and_index(self):
        for sums in ("SHA256SUMS-v1.3.7-candidate.txt", "27_SHA256SUMS.txt"):
            for line in self.pack[sums].decode("utf-8").splitlines():
                digest, rel = line.split("  ", 1)
                if rel in self.pack:
                    with self.subTest(sums=sums, file=rel):
                        self.assertEqual(hashlib.sha256(self.pack[rel]).hexdigest(), digest)
        listed = {line.split("  ", 1)[1] for line in self.pack["SHA256SUMS-v1.3.7-candidate.txt"].decode().splitlines()}
        self.assertEqual(listed, set(self.pack) - {"SHA256SUMS-v1.3.7-candidate.txt"})
        in27 = {line.split("  ", 1)[1] for line in self.pack["27_SHA256SUMS.txt"].decode().splitlines()}
        self.assertLessEqual({self.name(r) for r in self.mod.RENAMES}, in27)
        index = json.loads(self.pack[FX + "fixture-index.json"])
        self.assertEqual(index["fixture_count"], 144)
        for f in index["fixtures"]:
            data = self.pack[f["path"]]
            self.assertEqual((hashlib.sha256(data).hexdigest(), len(data)), (f["sha256"], f["bytes"]), f["fixture_id"])
            self.assertEqual(json.loads(data)["expected"], f["expected"], f["fixture_id"])

    def test_expected_objects_unchanged(self):
        for rel in self.base:
            if rel.startswith(FX) and not rel.endswith("fixture-index.json"):
                with self.subTest(file=rel):
                    self.assertEqual(json.loads(self.pack[rel])["expected"], json.loads(self.base[rel])["expected"])

    def test_owner_specified_block(self):
        """D-026: OS-1-OS-3 are appended after the C12-C16 lines, labelled OWNER-SPECIFIED, logged as their own last
        CHANGELOG entry, and add no outcome code: every diagnostic, error class and stage they name is in the candidate
        Protocol."""
        import re
        label, pd, fixtures, block = self.mod.OS_BLOCK
        lines = self.pack[self.name(self.mod.P36)].decode("utf-8").split("\n")
        start = len(self.base[self.mod.P36].decode("utf-8").split("\n")) - 1 + self.mod.C12_C16_LINES
        block = self.appended(self.mod.P36)[self.mod.C12_C16_LINES:self.mod.C12_C16_LINES + len(block)]  # with cycle 2
        self.assertEqual(lines[start:start + len(block)], block)
        items = [l for l in block if l.startswith("- **")]
        self.assertEqual([re.search(r"\((OS-\d)", l).group(1) for l in items], ["OS-1", "OS-2", "OS-3"])
        self.assertIn("OWNER-SPECIFIED", block[1])
        self.assertIn("They add no outcome code.", "\n".join(block))
        protocol = self.pack[self.name(self.mod.P02)].decode("utf-8")
        text = "\n".join(block)
        inputs = set(re.findall(r"`[a-z_0-9]+` = `([A-Z][A-Z0-9_]*)`", text))  # input values, e.g. recovery_mode's
        self.assertEqual(inputs, {"OPERATIONAL_RECOVERY"})
        for token in set(re.findall(r"`([A-Z][A-Z0-9_]*(?:\|reason=[A-Z_]+)?)`", text)) - inputs:
            with self.subTest(token=token):
                self.assertIn(token, protocol)
        changelog = self.pack["CHANGELOG-v1.3.7-candidate.md"].decode("utf-8")
        entries = re.findall(r"^\| (E\d+) \| ([^|]+) \|", changelog, re.M)
        self.assertEqual(entries[157], ("E158", label))  # the last cycle-1 entry; cycle 2 (D-027) follows it

    def test_cycle2_follows_cycle1(self):
        """D-027: cycle-2 entries come after E158 and every cycle-1 entry keeps its number and correction."""
        import re
        changelog = self.pack["CHANGELOG-v1.3.7-candidate.md"].decode("utf-8")
        entries = re.findall(r"^\| (E\d+) \| ([^|]+) \|", changelog, re.M)
        cycle2 = {c[0] for c in self.mod.CYCLE2} | {c[0] for c in self.mod.CYCLE2_APPENDS} | {
            v[0] for v in self.mod.CYCLE2_WHOLE.values()}
        first2 = next((i for i, (_, c) in enumerate(entries) if c.strip().split(" ")[0] in cycle2
                       or c.strip().startswith("A2 (copy of OD") or c.strip().startswith("A2 (copy of A")), None)
        if cycle2:
            self.assertEqual(first2, 158)
        for item in cycle2:  # every OD rule is labelled in the pack text it adds
            if item.startswith("OD-"):
                self.assertTrue(any(f"OWNER-DECIDED {item}" in b.decode("utf-8", "replace") for b in self.pack.values()),
                                item)

    def test_cycle3_follows_cycle2(self):
        """D-029: cycle-3 (C18) entries come after E205, so every earlier entry keeps its number and correction."""
        import re
        changelog = self.pack["CHANGELOG-v1.3.7-candidate.md"].decode("utf-8")
        entries = re.findall(r"^\| (E\d+) \| ([^|]+) \|", changelog, re.M)
        c18 = [i for i, (_, c) in enumerate(entries) if c.strip() == "C18"]
        self.assertEqual(c18, list(range(205, 205 + len(self.mod.CYCLE3) + len(self.mod.INDEX_CYCLE3))))
        self.assertNotIn("C18", {c.strip() for _, c in entries[:205]})

    def test_cycle4_follows_cycle3(self):
        """D-030: cycle-4 (C19) entries come after E218, so every earlier entry keeps its number and correction."""
        import re
        changelog = self.pack["CHANGELOG-v1.3.7-candidate.md"].decode("utf-8")
        entries = re.findall(r"^\| (E\d+) \| ([^|]+) \|", changelog, re.M)
        c19 = [i for i, (_, c) in enumerate(entries) if c.strip() == "C19"]
        self.assertEqual(c19, list(range(218, 218 + len(self.mod.CYCLE4) + len(self.mod.INDEX_CYCLE4))))
        self.assertNotIn("C19", {c.strip() for _, c in entries[:218]})

    # D-029 item 1 (D2-1), D-030 item 2 (D3-2): the current documents of the candidate (section 6 of
    # CORRECTIONS-v1.3.7-candidate.md) and the fixture index. A line in them that states a status and mentions F18 must
    # give the three parts as explicit labels, in order, each with a value (labelled_status below).
    STATUS_TERMS = r"(?i)NOT RUN|NOT PASSED|PASSED|\bstatus\b"
    # Lines a current document keeps on purpose, with the reason (STATUS-SWEEP-D029.md). Matched by text, not number.
    STATUS_EXEMPT = {
        "01_OpenVEF_Project_Charter_v1.3.7-candidate.md": [
            ("> **Status note.** The v1.3, v1.3.1, v1.3.2 and v1.3.3 independent document audits",
             "history: what the v1.3.5 audit result reports (kept under C17)")],
        "32_v1.3.7-candidate_Status_and_Gates.md": [
            ("- The v1.3.4 independent document audit returned FAIL on N14;", "history: the v1.3.4 and v1.3.5 audits")],
        "36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md": [
            ("| P11b | parser | Syntactically truncated JSON without provider truncation status.",
             "not a status statement: P11b's input description")],
    }

    def test_current_status_lines_have_three_parts(self):
        """D-029 (D2-1), D-030 (D3-2): every current status line that mentions F18 states development-run evidence,
        formal F18 status and approval as explicit labels, in order, each with a value. Fails on a new or reworded line
        that drops, reorders, quotes or empties a part, and on a stale exemption."""
        import re
        current = sorted({self.name(r) for r in self.mod.RENAMES} | {"README.md"})
        used, checked = set(), 0
        for rel in current:
            for n, line in enumerate(self.pack[rel].decode("utf-8").split("\n"), 1):
                if "F18" not in line or not re.search(self.STATUS_TERMS, line):
                    continue
                exempt = [p for p, _ in self.STATUS_EXEMPT.get(rel, []) if line.startswith(p)]
                if exempt:
                    used.add((rel, exempt[0]))
                    continue
                checked += 1
                with self.subTest(file=rel, line=n):
                    self.assertEqual(labelled_status(line), [], line[:160])
                    if XREF in line:  # D-031: the cross-reference must point to a section below it in the same file
                        below = self.pack[rel].decode("utf-8").split("\n")[n:]
                        self.assertIn("## F18 result", below, f"{rel} L{n}: {XREF!r} has no section below it")
        self.assertEqual(used, {(f, p) for f, items in self.STATUS_EXEMPT.items() for p, _ in items})
        self.assertEqual(checked, 17)  # the 17 lines C19 labelled (CORRECTIONS section 13); a new one must be added there
        index = json.loads(self.pack[FX + "fixture-index.json"])
        for key in ("execution_status", "status"):
            with self.subTest(index_field=key):
                self.assertEqual(labelled_status(index[key]), [])

    def test_status_rule_rejects_unlabelled_quoted_reordered_and_empty(self):
        """D-030 (D3-2): the rule is lexical, but needs the labels, not the words. The v1.3.6 wording D2-1 named, the C18 wording (right words, no
        labels), audit #3's false-positive sentence, the labels in quotes, the labels out of order, a repeated label and
        an empty value all fail it; the C19 wording passes and keeps the A1-A11 and X14 status."""
        import re
        c19 = self.pack[self.name(self.mod.P21)].decode("utf-8").split("\n")[69]
        c18 = ("- Current release status: development-run evidence: fixture runs of a project implementation, recorded "
               "outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, "
               "since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved; "
               "A1–A11 **NOT ACCEPTED**; X14 **OWNER CHOICE REQUIRED**.")
        bad = {
            "v1.3.6 (D2-1)": "- Current release status: F18 **NOT RUN / NOT PASSED**; A1–A11 **NOT ACCEPTED**; X14 **OWNER "
                             "CHOICE REQUIRED**.",
            "C18 words without labels": c18,
            "audit #3 false positive": "F18 NOT RUN; “development-run” is a glossary term, “formal” describes the "
                                       "document style, and “approval” is a separate governance section.",
            "labels in curly quotes": "F18 NOT RUN; see “Development-run evidence: x; Formal F18 status: y; Approval: "
                                      "z” in the glossary.",
            "labels in straight quotes": 'F18 status: the phrase "Development-run evidence: x; Formal F18 status: y; '
                                         'Approval: z" is defined elsewhere.',
            "label words in quotes, no colon": 'F18 status: "Development-run evidence", "Formal F18 status" and '
                                               '"Approval" are glossary terms.',
            "out of order": "F18 status: Formal F18 status: NOT RUN; Development-run evidence: none; Approval: none.",
            "approval first": "F18 status: Approval: none; Development-run evidence: none; Formal F18 status: NOT RUN.",
            "repeated label": "F18 status: Development-run evidence: a; Formal F18 status: NOT RUN; Approval: none; "
                              "Approval: none.",
            "empty value": "F18 status: Development-run evidence: ; Formal F18 status: NOT RUN; Approval: none.",
            "punctuation-only value": "F18 status: Development-run evidence: x; Formal F18 status: **; Approval: none.",
            "missing part": "F18 status: Development-run evidence: x; Formal F18 status: NOT RUN.",
            "lower-case labels": "F18 status: development-run evidence: x; formal F18 status: NOT RUN; approval: none.",
        }
        for name, line in bad.items():
            with self.subTest(case=name):
                self.assertTrue("F18" in line and re.search(self.STATUS_TERMS, line), name)  # the test would check it
                self.assertNotEqual(labelled_status(line), [], name)
        self.assertEqual(labelled_status(c19), [])
        self.assertIn("A1–A11 **NOT ACCEPTED**; X14 **OWNER CHOICE REQUIRED**.", c19)  # D-029: kept
        for hdr in (self.mod._HDR4,):  # the File 21 column headers
            self.assertEqual(labelled_status(hdr), [])

    def test_od3_schema_covers_every_change_class_property(self):
        """OD-3 (D-027, D1-1/D1-2): Protocol §20 lists every property of the change-class and domain-validation expected
        objects, with the same value, and no property they lack. Values: `x` strings, `true`/`false`, integers,
        [`a`, `b`] arrays; `diagnostic` and the §20.3 rows per input value, the §20.2 rows for all."""
        import re
        protocol = self.pack[self.name(self.mod.P02)].decode("utf-8").split("\n")
        start = protocol.index("### 20.3 Further properties of each result")
        rows = [l for l in protocol[start:] if l.startswith("| `")]
        rows = rows[:next(i for i, l in enumerate(rows) if "File 36 L" in l)] if any("File 36 L" in l for l in rows) else rows

        def value(cell: str):
            cell = cell.strip()
            if cell.startswith("["):
                return re.findall(r"`([^`]*)`", cell)
            v = re.fullmatch(r"`([^`]*)`", cell).group(1)
            return {"true": True, "false": False}.get(v, int(v) if v.isdigit() else v)

        table: dict[str, dict] = {}
        for l in rows:
            cells = [c for c in l.strip("|").split(" | ")]
            table.setdefault(value(cells[0]), {})[value(cells[1])] = value(cells[3])
        l176 = protocol[175]
        for fid in ("M48", "M50", "M53", "M54", "M58"):
            d = json.loads(self.pack[FX + f"{fid}.json"])
            (key, cls), = d["input"].items()
            with self.subTest(fixture=fid):
                self.assertEqual(key, "domain_validation" if fid == "M54" else "change_class")
                expected = dict(d["expected"])
                common = {"disposition": "CONTROL_EXPECTATION", "stage_id": "DESIGN_HALT",
                          "error_class": expected["diagnostic"].split("|")[0]}
                action = re.search(rf"`{cls}` = `([^`]*)`", l176).group(1)
                got = {**common, **table[cls]}
                got["required_action"] = action  # §20.2: every result has the L176 literal
                self.assertEqual(got, expected)

    @unittest.skipIf(validate_vector is None, "openvef not importable (document-audit bundle)")
    def test_corrected_m27_reaches_check_e(self):
        m27 = json.loads(self.pack[FX + "M27.json"])
        inp = m27["input"]
        ns: dict = {}
        exec(inp["legal_input_predicate"]["source"], ns)  # pack text, not model output
        legal = ns[inp["legal_input_predicate"]["function"]]
        widths = inp["input_port_widths"]
        check = lambda v: validate_vector(v, widths, widths, lambda x: legal(x, inp["sampled_outputs"]))
        self.assertEqual(check(inp["driver_return"]).diagnostic, m27["expected"]["diagnostic"])
        self.assertIsNone(check({"wr_en": "0"}))  # legal at full
        self.assertIsNone(validate_vector(inp["driver_return"], widths, widths, lambda x: legal(x, {"full": "0"})))
        self.assertNotIn("FIFO", inp["legal_input_predicate"]["source"])  # A1: no design specification needed
        pred = inp["legal_input_predicate"]  # OD-2 (D-027): the frozen predicate carries its hash
        self.assertEqual(pred["source_sha256"], hashlib.sha256(pred["source"].encode("utf-8")).hexdigest())


if __name__ == "__main__":
    unittest.main()
