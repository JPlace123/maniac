#!/usr/bin/env python3
"""citations.py — the first rung, made executable: does every `file:line` you cited actually exist?

Usage:
    python3 tools/citations.py VERDICT.md [more.md ...]
    python3 tools/citations.py --root . --root ~/the/sources VERDICT.md
    python3 tools/citations.py --selftest

Exit code: **1 if even one citation is dead.** 0 only when they all hold.
           **2 if it found no citations to check at all** — a document with no citations isn't a
           clean document, it's a document that proves nothing.

⚠️ Why it exists. The first of the five rungs is *"back to the line on every citation, always, on
everything"*, and it was the one step of the method **with no tool that executed it**: it stayed a
thing you did by hand, which is a thing that at some point stops being done. And the defect it catches
is real and measured: more than once a verdict cited a line **as proof of a rule that line doesn't
contain**, and the citation looked solid precisely because the file and the line both existed.

⚠️ What it does NOT do, declared: it checks the line **exists**, not that it **says** what you
attribute to it. That stays a judgement. With `--phrase` it also checks a keyword appears nearby,
which is less than reading and more than nothing.
"""
import os
import re
import sys

# `file.md:12` · `file.md:12-15` · `path/to/file.py:340` · in quotes or backticks
CITATION = re.compile(r"`?([\w./~-]+\.(?:md|py|js|mjs|cjs|ts|json|sh|txt|tsv)):(\d+)(?:-(\d+))?`?")


def find(text):
    out = []
    for m in CITATION.finditer(text):
        a = int(m.group(2))
        b = int(m.group(3)) if m.group(3) else a
        out.append((m.group(1), a, b))
    return out


def check(citations, roots=".", phrase=None):
    """Returns (alive, dead). A citation is dead if the file is missing or the line doesn't exist.

    ⚠️ `roots` can be more than one, and it needs to be: a document cites **its own project** and
    **its sources**, which live elsewhere. With a single root every citation to a source came back
    dead — a false alarm that would have got the tool switched off on first use.
    """
    if isinstance(roots, str):
        roots = [roots]
    alive, dead = [], []
    cache = {}

    def open_at(path):
        """⚠️ ALL the copies that exist, one per root — not just the first.

        This used to stop at the first root where the name existed, and the same name sits under
        two roots more often than it looks (`CONTRACT.md` lives both in the repo and in the skill).
        A citation valid in the second copy came back **dead**, with the line count of the first: a
        false alarm, the one defect that gets a tool switched off.
        """
        out = []
        for r in roots:
            p = path if os.path.isabs(path) else os.path.join(r, path)
            p = os.path.expanduser(p)
            if p not in cache:
                try:
                    cache[p] = open(p, encoding="utf8", errors="replace").read().split("\n")
                except OSError:
                    cache[p] = None
            if cache[p] is not None:
                out.append(cache[p])
        return out

    def holds(lines, a, b):
        if a < 1 or b > len(lines):
            return False
        return not phrase or phrase.lower() in " ".join(lines[a - 1:b]).lower()

    for path, a, b in citations:
        copies = open_at(path)
        if not copies:
            dead.append((path, a, b, "no such file under any root"))
            continue
        if any(holds(lines, a, b) for lines in copies):
            alive.append((path, a, b))
            continue
        # no copy holds: give the reason using the one that comes closest (the longest)
        lines = max(copies, key=len)
        if a < 1 or b > len(lines):
            dead.append((path, a, b, "the file has %d lines" % len(lines)))
        else:
            dead.append((path, a, b, "the line does not contain «%s»" % phrase))
    return alive, dead


def report(alive, dead):
    if not alive and not dead:
        print("⛔ no citations found.")
        print("   That isn't \"all clear\": it's a document that points at nothing,")
        print("   and the first rung asks for a return to the line on EVERY citation.")
        return 2
    for path, a, b, why in dead:
        where = "%s:%d" % (path, a) if a == b else "%s:%d-%d" % (path, a, b)
        print("  ✗ %-52s %s" % (where, why))
    print("\n%d citations · %d hold · %d dead" % (len(alive) + len(dead), len(alive), len(dead)))
    if dead:
        print("\n⚠️ A dead citation isn't a typo: it's a proof that isn't there.")
    return 1 if dead else 0


def selftest():
    import shutil
    import tempfile
    d = tempfile.mkdtemp()
    open(os.path.join(d, "real.md"), "w", encoding="utf8").write("one\ntwo\nthree\n")
    doc = ("see `real.md:2` and `real.md:1-3`, then a dead one `real.md:99` "
           "and an invented one `never-existed.md:1`\n")
    c = find(doc)
    assert len(c) == 4, c
    assert c[0] == ("real.md", 2, 2), c[0]
    assert c[1] == ("real.md", 1, 3), c[1]           # a range reads as a range
    alive, dead = check(c, roots=d)
    assert len(alive) == 2, alive
    assert dead[0][3] == "the file has 4 lines", dead[0]
    assert dead[1][3] == "no such file under any root", dead[1]
    assert report(alive, dead) == 1                   # one dead, exit 1
    assert report(alive, []) == 0                     # all alive, exit 0
    # ⚠️ zero citations is not an ok: it's the false ok this tool exists to refuse
    assert report([], []) == 2
    # --phrase: the line exists but doesn't say what you attribute to it
    _, m2 = check([("real.md", 1, 1)], roots=d, phrase="four")
    assert len(m2) == 1 and "does not contain" in m2[0][3], m2
    _, m3 = check([("real.md", 1, 1)], roots=d, phrase="one")
    assert m3 == [], m3
    # ⚠️ two roots: the source lives elsewhere and must not come back dead
    d2 = tempfile.mkdtemp()
    open(os.path.join(d2, "source.md"), "w", encoding="utf8").write("a\nb\nc\nd\n")
    a4, m4 = check([("real.md", 1, 1), ("source.md", 3, 3)], roots=[d, d2])
    assert len(a4) == 2 and m4 == [], (a4, m4)
    # ⚠️ the SAME NAME under two roots: the citation must hold on the longer copy, not come back dead
    open(os.path.join(d2, "real.md"), "w", encoding="utf8").write("one\ntwo\nthree\nfour\nfive\n")
    a5, m5 = check([("real.md", 5, 5)], roots=[d, d2])       # d has 3+1, d2 has 5+1
    assert a5 == [("real.md", 5, 5)] and m5 == [], (a5, m5)
    a6, m6 = check([("real.md", 99, 99)], roots=[d, d2])     # dead in both, stays dead
    assert a6 == [] and "the file has 6 lines" == m6[0][3], m6
    shutil.rmtree(d2)
    print("selftest: 15 assertions, all passed")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    roots = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--root"] or ["."]
    phrase = None
    if "--phrase" in sys.argv:
        phrase = sys.argv[sys.argv.index("--phrase") + 1]
    skip = set(roots) | {"--root", "--phrase", phrase}
    files = [a for a in sys.argv[1:] if not a.startswith("--") and a not in skip]
    if not files:
        print("usage: citations.py <document.md>... [--root DIR]... [--phrase WORD]")
        sys.exit(2)
    every = []
    for f in files:
        every += find(open(f, encoding="utf8", errors="replace").read())
    sys.exit(report(*check(every, roots, phrase)))
