#!/usr/bin/env python3
"""inventory.py — rebuilds `coverage.tsv` from the files of one checking round.

Usage:
    python3 tools/inventory.py tidy/tidy-*-p1.md        # TIDY_TSV=... to choose the destination
    python3 tools/inventory.py --selftest

It reads the markdown tables the coverage agents produce and extracts one row per decision:
`id · state · decision · where`. Then `coverage.py` reads on top of it and exits 1 if something is
missing.

⚠️ Why this is a script and not a copy-and-paste. The round is redone every time the skill changes,
and an inventory rebuilt by hand every time is an inventory that at some point **stops being
rebuilt**. The cost of redoing it has to be one command.

⚠️ Declared ceiling: the agents' tables have their columns in a different order from one round to the
next, so the box is found **by content** and not by position. If an agent writes the box inside a
sentence instead of in a cell of its own, this line still catches it; if they write it in a brand new
form, **it does not catch it**, and it ends up among the UNATTRIBUTED rows, which get counted, printed
and make the run exit **1**.
"""
import glob
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("TIDY_TSV", os.path.join(os.getcwd(), "coverage.tsv"))


def box(cells):
    """The box is looked for by content: the column order changes from one round to the next."""
    for i, c in enumerate(cells):
        u = c.upper()
        if "OUT OF SCOPE" in u or "OUT-OF-SCOPE" in u:
            return "OUT-OF-SCOPE", i
        if "IMPLEMENTED" in u:
            return "IMPLEMENTED", i
        if "PARTIAL" in u:
            return "PARTIAL", i
        if re.search(r"\bABSENT\b", u):
            return "ABSENT", i
    return None, None


# ⚠️ The agents write in FOUR different forms, and they change from one round to the next: markdown
#    table · `**N. text** — **BOX**` · `**N. text** (pointer) — **BOX**` · a heading followed by
#    `→ **BOX**` on the next line. Chasing the forms is a race you lose: here we look for **the box**,
#    and attribute it to the LAST numbered heading seen. A new form keeps working as long as there is
#    a number before and a box after.
# ⚠️ **A fifth form seen in the field**: `**D01 · title** (map.md:1937) — **IMPLEMENTED**`.
#    The id is no longer a bare number but a tag, and the separator is not a dot but a `·`.
#    That is why the id here is **a tag or a number**, and the separator **any one of `.`, `)`, `·`, `-`**:
#    chasing the exact form is the race you lose, and it has already been lost four times.
# ⚠️ **A sixth and a seventh form**: `**CP-01 · title**` and `**CP-p8-01a · title**`. The id has the
#    **hyphen before the digits**, and the earlier line (`[A-Za-z]{0,4}[0-9]+`) didn't catch it: on a
#    file with 211 decisions it counted **1** and exited **0**. So the id here is **a token with at
#    least one digit somewhere in it**, in pieces joined by `-` or `_` — not an exact shape.
HEADING = re.compile(
    r"^\**\s*((?=[^\s]*[0-9])[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+){0,3}|[a-z])\s*[.)·—-]\s*\**\s*(.{3,})", re.I)
VERDICT = re.compile(r"\b(IMPLEMENTED|PARTIAL|ABSENT|OUT[ -]OF[ -]SCOPE)\b")
# lines that name the boxes without judging anything (legends, table headers, prefaces)
NOISE = re.compile(r"legend|direction:|check command|^\s*\|?\s*-{3,}|box\s*\|", re.I)

# ⚠️ Verdict lines SEEN but not ATTRIBUTED to any decision. Without this list the total stays
#    plausible while the content has quietly left: that's exactly how 210 out of 211 verdicts went
#    missing without a single number changing shape. Filled by `extract`, read by `__main__`.
LOST = []


def extract(paths):
    """You look for the BOX and attribute it to the last numbered heading."""
    rows = []
    del LOST[:]
    for f in sorted(paths):
        if "rebuttal" in os.path.basename(f):
            continue
        slice_ = re.sub(r"\.md$", "", os.path.basename(f)).split("-")[-1]
        current = None       # (id, text)
        decided = set()
        for n, L in enumerate(open(f, encoding="utf8"), 1):
            t = L.strip()
            if not t:
                continue
            # a table row carrying the box settles itself
            if t.startswith("|") and not NOISE.search(t):
                cells = [x.strip() for x in t.strip("|").split("|")]
                if len(cells) >= 3 and re.match(r"^\**\d+\**$", cells[0]):
                    st, k = box(cells)
                    if st:
                        idr = f"{slice_}-{cells[0].strip('*')}"
                        if idr not in decided:
                            decided.add(idr)
                            rows.append((idr, st, " ".join(cells[1:k])[:300].replace("\t", " "),
                                         " ".join(cells[k + 1:])[:300].replace("\t", " ")))
                        continue
            m = HEADING.match(t)
            v = VERDICT.search(t)
            # ⚠️ the noise filter must NOT eat a line that has an id AND a box: that's a decision,
            #    not a legend. On a real file the word "direction:" inside the title of `CP-120`
            #    made the whole line disappear.
            if NOISE.search(t) and not (m and v):
                continue
            if m:
                current = (f"{slice_}-{m.group(1)}", m.group(2)[:300].replace("\t", " "))
            if v:
                if current and current[0] not in decided:
                    decided.add(current[0])
                    rows.append((current[0], v.group(1).upper().replace(" ", "-"),
                                 current[1], t[:300].replace("\t", " ")))
                else:
                    LOST.append((os.path.basename(f), n, t[:120]))
    return rows


def write(rows, out=OUT):
    with open(out, "w", encoding="utf8") as o:
        o.write("id\tstate\tdecision\twhere\n")
        for r in rows:
            o.write("\t".join(r) + "\n")


def selftest():
    import tempfile
    d = tempfile.mkdtemp()
    # the four forms seen in the field, plus the noise that must not get in
    open(os.path.join(d, "c-TB.md"), "w", encoding="utf8").write(
        "| # | Decision | Box | Where |\n|---|---|---|---|\n"
        "| 1 | one thing | IMPLEMENTED | SKILL.md:10 |\n"
        "| 2 | another | **ABSENT** | - |\n")
    open(os.path.join(d, "c-PR.md"), "w", encoding="utf8").write(
        "Legend: IMPLEMENTED · PARTIAL · ABSENT\n"
        "**1. First** — **IMPLEMENTED**. `SKILL.md:12`\n"
        "**2. Second** (map.md:2032) — **PARTIAL**.\n")
    open(os.path.join(d, "c-TWO.md"), "w", encoding="utf8").write(
        "**a. The companion does not exist.**\n"
        "→ **IMPLEMENTED** · `SKILL.md:21`\n"
        "**b. Another thing.**\n"
        "→ **ABSENT** · grep = 0\n")
    # the fifth form: tag + `·` + verdict on the same line (round 8)
    open(os.path.join(d, "c-TG.md"), "w", encoding="utf8").write(
        "**D01 · A decision** (`map.md:1937`) — **IMPLEMENTED** · `SKILL.md:221`\n"
        "**D02 · Another one** (`map.md:1938`) — **OUT OF SCOPE** (does not enter the skill)\n")
    # the sixth and seventh: the hyphen BEFORE the digits (round 10). These were the 210 lost verdicts.
    open(os.path.join(d, "c-CP.md"), "w", encoding="utf8").write(
        "**CP-01 · A decision** (map.md:216) — **IMPLEMENTED** · `SKILL.md:251`\n"
        "**CP-p8-01a · With the slice inside the id** (map.md:217) — **PARTIAL** · `SKILL.md:260`\n"
        "**CP-120 · The direction: start from the source** (map.md:1160) — **IMPLEMENTED** · `SKILL.md:58`\n")
    open(os.path.join(d, "c-rebuttal.md"), "w", encoding="utf8").write(
        "| 1 | must not get in | IMPLEMENTED | x |\n")
    r = extract(glob.glob(os.path.join(d, "c-*.md")))
    ids = sorted(x[0] for x in r)
    assert ids == ["CP-CP-01", "CP-CP-120", "CP-CP-p8-01a", "PR-1", "PR-2", "TB-1", "TB-2",
                   "TG-D01", "TG-D02", "TWO-a", "TWO-b"], ids   # rebuttal excluded
    c = Counter(x[1] for x in r)
    assert c["IMPLEMENTED"] == 6, c      # table + prose + two lines + tag + the two with a hyphen
    assert c["ABSENT"] == 2, c
    assert c["PARTIAL"] == 2, c
    # the legend names the boxes and must NOT produce a row
    assert not any(x[0] == "PR-0" for x in r)
    # the box on the line AFTER the heading is attributed to the heading
    assert [x for x in r if x[0] == "TWO-a"][0][1] == "IMPLEMENTED"
    # and a decision is not counted twice
    assert len(ids) == len(set(ids))
    # the fifth form must not get lost
    assert [x for x in r if x[0] == "TG-D01"][0][1] == "IMPLEMENTED"
    assert [x for x in r if x[0] == "TG-D02"][0][1] == "OUT-OF-SCOPE"
    # ⚠️ round-10 defect: `CP-120` has "direction:" in its title, which the noise filter used to eat
    assert [x for x in r if x[0] == "CP-CP-120"][0][1] == "IMPLEMENTED"
    # on well-formed files, nothing is lost: verdict lines seen are verdict lines attributed
    assert LOST == [], LOST
    # ⚠️ and a box with no heading before it does NOT vanish: it counts, and it exits 1
    open(os.path.join(d, "orphan.md"), "w", encoding="utf8").write(
        "some random line — **ABSENT**, with no id before it\n")
    assert extract([os.path.join(d, "orphan.md")]) == []
    assert len(LOST) == 1, LOST
    print("selftest: 15 asserts, all passed")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not paths:
        print("usage: inventory.py <check file>...")
        sys.exit(2)
    rows = extract(paths)
    write(rows)
    c = Counter(r[1] for r in rows)
    print("%d decisions → %s" % (len(rows), OUT))
    for k, v in c.most_common():
        print("  %-16s %d" % (k, v))
    # ⚠️ The count that makes the loss visible: verdict lines SEEN against ATTRIBUTED. Without it,
    #    "1 decision" on a 211-line file exited **0** and looked like a plausible total.
    if LOST:
        print("\n⛔ boxes seen %d · attributed %d · NOT attributed %d"
              % (len(rows) + len(LOST), len(rows), len(LOST)))
        for name, n, t in LOST[:10]:
            print("   %s:%d  %s" % (name, n, t))
        if len(LOST) > 10:
            print("   … and %d more." % (len(LOST) - 10))
        print("   An unattributed box is a verdict that is NOT in the tsv: either the heading has a")
        print("   shape the regex doesn't catch, or it's a repetition in prose. Look at them before trusting the count.")
        sys.exit(1)
    sys.exit(0)
