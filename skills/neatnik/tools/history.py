#!/usr/bin/env python3
"""history.py — one row per round of `tidy`, and the curve that comes out of it.

Usage:
    python3 tools/history.py --file tidy/history.tsv --append "level=max\tpasses=1\t..."
    python3 tools/history.py --file tidy/history.tsv --curve
    python3 tools/history.py --selftest

⚠️ Why it exists. The most useful thing about nine consecutive rounds was not any single round: it
was **the row of them**, which shows whether you are converging or merely writing. But that row lived
only in the memory of whoever was there that night. The curve **was already written into the method
as a thing to look at**, and no step wrote it down anywhere: the exact signature of the defect the
method calls *«the rule is written and no step executes it»*.

⚠️ How to read it, and it is counter-intuitive: **the defect rate can go back up while the object
gets better.** Once the big holes are closed, the attacker stops looking for *«missing»* and looks
for *«declared with no executor»*, which is harder. A rate that rises on an object that is improving
is an attacker who has raised the bar. What must go down is **the severity**.
"""
import os
import sys

FIELDS = ("level", "passes", "decisions", "full", "half", "empty", "reopened", "defective")


def read(path):
    if not os.path.exists(path):
        return []
    rows = []
    for L in open(path, encoding="utf8"):
        L = L.strip()
        if not L or L.startswith("#"):
            continue
        d = {}
        for piece in L.split("\t"):
            if "=" in piece:
                k, v = piece.split("=", 1)
                d[k.strip()] = v.strip()
        if d:
            rows.append(d)
    return rows


def append(path, row):
    fresh = not os.path.exists(path)
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "a", encoding="utf8") as f:
        if fresh:
            f.write("# one round per row · " + " ".join(FIELDS) + "\n")
        f.write(row.rstrip("\n") + "\n")
    return len(read(path))


def curve(rows):
    if not rows:
        print("⛔ history empty: no round on record.")
        print("   It is not «all clear»: it is a curve with no points, and it says nothing.")
        return 2
    print("%-3s %-7s %5s %5s %5s %5s   %s" % ("#", "lvl", "dec", "full", "half", "empt", "attack"))
    for i, r in enumerate(rows, 1):
        reop = int(r.get("reopened", 0) or 0)
        defe = int(r.get("defective", 0) or 0)
        att = "%d/%d = %d%%" % (defe, reop, round(100 * defe / reop)) if reop else "none"
        print("%-3d %-7s %5s %5s %5s %5s   %s" % (
            i, r.get("level", "?"), r.get("decisions", "?"), r.get("full", "?"),
            r.get("half", "?"), r.get("empty", "?"), att))
    last = rows[-1]
    below = int(last.get("half", 0) or 0) + int(last.get("empty", 0) or 0)
    print()
    if below:
        print("⚠️ %d decisions below 100%%: you do NOT say «ready»." % below)
        return 1
    if last.get("level") == "low":
        print("⚠️ zero below 100%, but the level is low: the attack was a sample.")
        print("   You may say «no hole found», NOT «complete».")
        return 1
    print("✅ no decision below 100%%, at level %s." % last.get("level"))
    return 0


def selftest():
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "h.tsv")
    assert read(p) == []                          # file that does not exist: no rows, no error
    assert curve([]) == 2                         # ⚠️ an empty history is not an ok
    assert append(p, "level=max\tpasses=1\tdecisions=10\tfull=8\thalf=2\tempty=0\treopened=8\tdefective=6") == 1
    assert append(p, "level=max\tpasses=2\tdecisions=10\tfull=10\thalf=0\tempty=0\treopened=8\tdefective=1") == 2
    r = read(p)
    assert len(r) == 2 and r[0]["level"] == "max" and r[1]["full"] == "10", r
    assert curve(r[:1]) == 1                      # two halves: you do not say ready
    assert curve(r) == 0                          # zero below 100% at level max
    low = [{"level": "low", "decisions": "10", "full": "10", "half": "0", "empty": "0",
            "reopened": "8", "defective": "0"}]
    assert curve(low) == 1                        # ⚠️ zero holes at level low is NOT «complete»
    # the header comment must not become a data row
    assert not any("#" in x.get("level", "") for x in r)
    print("selftest: 9 asserts, all passed")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--file" not in sys.argv:
        print("usage: history.py --file <history.tsv> [--append \"k=v\\tk=v\"] [--curve]")
        sys.exit(2)
    path = sys.argv[sys.argv.index("--file") + 1]
    if "--append" in sys.argv:
        text = sys.argv[sys.argv.index("--append") + 1].replace("\\t", "\t")
        print("%d rounds on record" % append(path, text))
    if "--curve" in sys.argv or "--append" not in sys.argv:
        sys.exit(curve(read(path)))
    sys.exit(0)
