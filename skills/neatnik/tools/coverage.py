#!/usr/bin/env python3
"""coverage.py — how many decisions from the map are really inside the skill, and which are not.

Usage:
    python3 tools/coverage.py              the count, and the list of what is missing
    python3 tools/coverage.py --absent     only the ABSENT ones
    python3 tools/coverage.py --partial    only the PARTIAL ones
    python3 tools/coverage.py --id D1-12   a single decision
    python3 tools/coverage.py --selftest   test the check

Exit code: **1 if even one in-scope decision is not IMPLEMENTED.** 0 only at zero.

⚠️ Why it exists. A skill was published that implemented half of what had been decided, and the first
hole was found by the reader it was handed to. The defect was not carelessness: it was that
**nothing could fail when a decision stayed on paper**. The skill itself prescribes that every
assumption comes with the check that proves it; this is that check, applied to the skill.

⚠️ Declared ceiling: the boxes come from `coverage.tsv`, which is an inventory produced by agents and
**has a measured error rate**: 16 IMPLEMENTED boxes reopened, **11 defective (69%)**. So `IMPLEMENTED`
here means *declared implemented*, not *verified*. A `--verify` that reopens every row against the
source does not exist yet: that is the next rung, and until it exists it has to be said out loud.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TSV = os.environ.get("TIDY_TSV", os.path.join(os.getcwd(), "coverage.tsv"))
STATES = ("IMPLEMENTED", "PARTIAL", "ABSENT", "OUT-OF-SCOPE")

# below this threshold the inventory is not «clean», it is empty: exit 2, never 0.
EMPTY_THRESHOLD = 50


def load(path=TSV):
    with open(path, encoding="utf8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def count(rows):
    c = {s: 0 for s in STATES}
    for r in rows:
        c[r["state"]] = c.get(r["state"], 0) + 1
    return c


def missing(rows):
    return [r for r in rows if r["state"] in ("ABSENT", "PARTIAL")]


def report(rows, only=None, one=None, threshold=EMPTY_THRESHOLD):
    if one:
        for r in rows:
            if r["id"] == one:
                print("%s  [%s]\n  %s\n  → %s" % (r["id"], r["state"], r["decision"], r["where"]))
                return 0
        print("id not found: %s" % one)
        return 1

    c = count(rows)
    in_scope = len(rows) - c["OUT-OF-SCOPE"]
    holes = missing(rows)

    # ⚠️ A check that has read nothing does NOT say ok. It is the defect the skill itself names:
    #    a process that cannot fail by construction. Success on zero data is the worst false ok.
    if in_scope < threshold:
        print("⛔ inventory too small: %d in-scope decisions (threshold %d)." % (in_scope, threshold))
        print("   It is not a «no hole»: it is a check that has read nothing.")
        print("   Redo `inventory.py` on the files of the round, and look at how many rows it extracts.")
        return 2

    for state in ("ABSENT", "PARTIAL"):
        if only and only != state:
            continue
        listed = [r for r in holes if r["state"] == state]
        if not listed:
            continue
        print("%s (%d)" % (state, len(listed)))
        for r in listed:
            print("  %-8s %s" % (r["id"], r["decision"][:110]))
        print()

    print("%d decisions · %d in scope · %d out" % (len(rows), in_scope, c["OUT-OF-SCOPE"]))
    print("  IMPLEMENTED (declared)  %3d   %4.1f%%" % (c["IMPLEMENTED"], 100 * c["IMPLEMENTED"] / max(in_scope, 1)))
    print("  PARTIAL                 %3d" % c["PARTIAL"])
    print("  ABSENT                  %3d" % c["ABSENT"])
    if holes:
        print("\n⚠️ %d decisions are not in the skill. The work is not finished." % len(holes))
    else:
        print("\n✅ no declared hole. ⚠️ «implemented» here means DECLARED, not verified: "
              "the inventory has a measured error rate of 69% on the boxes that were reopened.")
    return 1 if holes else 0


def selftest():
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "c.tsv")
    with open(p, "w", encoding="utf8") as f:
        f.write("id\tstate\tdecision\twhere\n")
        f.write("A-1\tIMPLEMENTED\tone\tSKILL.md:1\n")
        f.write("A-2\tABSENT\ttwo\t-\n")
        f.write("A-3\tPARTIAL\tthree\tSKILL.md:9\n")
        f.write("A-4\tOUT-OF-SCOPE\tfour\t-\n")
    r = load(p)
    assert len(r) == 4
    c = count(r)
    assert c["IMPLEMENTED"] == 1 and c["ABSENT"] == 1 and c["PARTIAL"] == 1 and c["OUT-OF-SCOPE"] == 1
    # the holes are ABSENT + PARTIAL, and OUT-OF-SCOPE is not a hole
    assert [x["id"] for x in missing(r)] == ["A-2", "A-3"]
    # with a single hole, the exit is 1
    assert report(r, threshold=1) == 1
    # holes removed, the exit goes back to 0
    clean = [x for x in r if x["state"] in ("IMPLEMENTED", "OUT-OF-SCOPE")]
    assert missing(clean) == []
    assert report(clean, threshold=1) == 0
    # a non-existent id does not pass in silence
    assert report(r, one="Z-9") == 1
    # ⚠️ an empty inventory exits 2, not 0: the false ok is the defect this check exists to avoid
    assert report([]) == 2                    # zero rows: never an ok
    assert report(r, threshold=99) == 2       # inventory below threshold: never an ok
    assert report(r, threshold=1) == 1        # and above threshold it judges again
    print("selftest: 10 asserts, all passed")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    rows = load()
    only = "ABSENT" if "--absent" in sys.argv else ("PARTIAL" if "--partial" in sys.argv else None)
    one = None
    if "--id" in sys.argv:
        one = sys.argv[sys.argv.index("--id") + 1]
    sys.exit(report(rows, only, one))
