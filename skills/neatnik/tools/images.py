#!/usr/bin/env python3
"""images.py — measure the images a process produced, instead of looking at them.

Usage:
    python3 tools/images.py spec.json          the verdict, one JSON line
    python3 tools/images.py spec.json --human  the same, readable
    python3 tools/images.py --example          print a commented example spec
    python3 tools/images.py --selftest         exercise the tool on synthetic images

Exit code: **0** every measure passes · **1** at least one fails ·
           **2 when it could not look** — missing file, failed download, empty spec.
⚠️ The **2** is why this file exists: *"I could not look"* must never be able to resemble
*"I looked and it was fine"*.

⚠️ Why it is a tool and not an eye. A rule said *"measure it, don't eyeball it"* and nobody executed
it: a mark shipped **2 degrees crooked and off-centre** with the check reporting **zero errors**. An
eye that approves is an eye that did not measure.

⚠️ What it does NOT do, declared: **it does not say whether something looks good.** No heuristic
knows. Where a human eye is needed, this tool **saves the composed image and forces you to look at
it** — the judgement stays with whoever looks, but it can no longer be skipped by inattention.
"""
import io
import json
import os
import sys
import urllib.request

try:
    from PIL import Image
except ImportError:                                   # ⚠️ library missing is a 2, not an ok
    print(json.dumps({"error": "Pillow missing: pip install Pillow"}))
    sys.exit(2)

ATTEMPTS = 3
UA = {"User-Agent": "neatnik-images/1.0"}

EXAMPLE = """{
  "base": "https://example/images",          // or a local folder, or file://
  "background": "#101820",                   // the colour the image will be seen against
  "images": {
    "header": { "expected": [480, 150], "transparent_background": true },
    "icon":   { "expected": [512, 512], "min_margin_pct": 9 },
    "centre": { "expected": [1125, 432], "side_margin_pct": 8, "top_bottom_margin_pct": 4,
                "height_cap_pct": { "wide": 77, "square": 90 } }
  },
  "distinct": [["header", "centre"]],        // pairs that must NOT be the same file
  "covered_region": { "image": "centre", "active_if": 1, "tolerance_pct": 0.5 },
  "composite": "strip/2/strip.png",          // saved to disk, to be looked at by a human
  "out_dir": "."
}"""


def _read(base, name):
    """Returns (bytes, RGB image) or (None, reason). Local or remote, with retries."""
    import time
    if base.startswith(("http://", "https://")):
        url = "%s/%s" % (base.rstrip("/"), name)
        last = None
        for i in range(ATTEMPTS):
            try:
                raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read()
                return raw, Image.open(io.BytesIO(raw)).convert("RGB")
            except Exception as e:                     # noqa: BLE001
                last = str(e)
                if i + 1 < ATTEMPTS:
                    time.sleep(2 * (i + 1))
        return None, last
    p = os.path.join(base, name)
    try:
        raw = open(p, "rb").read()
        return raw, Image.open(io.BytesIO(raw)).convert("RGB")
    except OSError as e:
        return None, str(e)


def colour(s):
    s = str(s).lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) if len(s) == 6 else (255, 255, 255)


def margins(im, bg, threshold=36):
    """The drawing's margins: the pixels that are NOT background. None if it is a flat fill."""
    px = im.convert("RGB").load()
    xs, ys = [], []
    for y in range(0, im.height, 2):
        for x in range(0, im.width, 2):
            r, g, b = px[x, y]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > threshold:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), im.width - 1 - max(xs), im.height - 1 - max(ys)


def check(spec):
    """Returns (results, failures, not_looked_at). A not-looked-at is NOT a passing result."""
    base = spec.get("base", ".")
    bg = colour(spec.get("background", "#ffffff"))
    results, failures, not_looked = {}, [], {}
    raw, img = {}, {}

    for name in spec.get("images", {}):
        r, i = _read(base, name if name.endswith(".png") else name + ".png")
        if r is None:
            not_looked[name] = i                      # ⚠️ the error gets written down, not swallowed
        raw[name], img[name] = (r, i) if r is not None else (None, None)

    for name, rules in spec.get("images", {}).items():
        if img.get(name) is None:
            continue
        e = {}
        im = img[name]

        if "expected" in rules:
            e["size"] = {"found": list(im.size), "expected": list(rules["expected"]),
                         "ok": list(im.size) == list(rules["expected"])}

        # ⚠️ The background is read from the RAW BYTES, not from the RGB-converted image: the
        #    conversion throws the alpha away, so from there the corners come back ALWAYS opaque and
        #    the check would cry wolf on every image, every time. A check that is always wrong gets
        #    switched off.
        if rules.get("transparent_background"):
            rgba = Image.open(io.BytesIO(raw[name])).convert("RGBA")
            W, H = rgba.size
            al = rgba.getchannel("A")
            corners = [al.getpixel(p) for p in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)]]
            e["transparent_background"] = {"max_corner_alpha": max(corners), "ok": max(corners) <= 10}

        m = margins(im, bg)
        if m is None and ("min_margin_pct" in rules or "side_margin_pct" in rules):
            e["empty"] = True                          # flat fill: not a pass, a flag
        elif m:
            l, t, r, b = m
            W, H = im.size
            if "min_margin_pct" in rules:
                s = W * rules["min_margin_pct"] / 100.0
                e["margins"] = {"L": l, "T": t, "R": r, "B": b, "min": min(l, t, r, b),
                                "threshold": round(s), "ok": min(l, t, r, b) >= s}
            if "side_margin_pct" in rules:
                sl = W * rules["side_margin_pct"] / 100.0
                sv = H * rules.get("top_bottom_margin_pct", 0) / 100.0
                # ⚠️ The height cap DEPENDS on the shape, and that is not a detail: a wide drawing
                #    that fills the width must not also stretch vertically; a square one is bound by
                #    height alone, and holding it to the narrow cap makes it look tiny. One cap for
                #    two different shapes is wrong on one of them.
                caps = rules.get("height_cap_pct") or {}
                wide = (W - l - r) / float(W) > 0.45
                cap = (caps.get("wide") if wide else caps.get("square")) or 100
                height = (H - t - b) / float(H) * 100
                e["centre"] = {"L": l, "T": t, "R": r, "B": b,
                               "min_sides": min(l, r), "side_threshold": round(sl),
                               "height_pct": round(height), "height_cap_pct": cap,
                               "shape": "wide" if wide else "square",
                               "ok": min(l, r) >= sl - 2 and min(t, b) >= sv and height <= cap}
        results[name] = e

    for a, b in spec.get("distinct", []):
        if raw.get(a) and raw.get(b):
            results.setdefault("_pairs", {})["%s≠%s" % (a, b)] = {"identical": raw[a] == raw[b],
                                                                  "ok": raw[a] != raw[b]}

    # ⚠️ The covered region. When the process composes something ON TOP of an image, whatever sits
    #    underneath becomes unreadable and no check on the uploaded file notices: the file is clean,
    #    the composition is not. Measured: dozens of checks all green over a drawing that in the
    #    final result was covered entirely.
    cr = spec.get("covered_region")
    if cr and cr.get("active_if", 0) > 0 and raw.get(cr["image"]):
        rgba = Image.open(io.BytesIO(raw[cr["image"]])).convert("RGBA")
        px, W, H = rgba.load(), rgba.width, rgba.height
        n = 0
        for y in range(0, H, 2):
            for x in range(0, W, 2):
                r, g, b, al = px[x, y]
                # ⚠️ in RGBA, not RGB: a TRANSPARENT region (which is the correct one) converted to
                #    RGB turns BLACK, i.e. "drawn on" against every non-black background.
                if al > 10 and abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > 36:
                    n += 1
        tot = len(range(0, H, 2)) * len(range(0, W, 2))
        pct = n / float(tot) * 100
        results["covered_region"] = {"drawn_pct": round(pct, 2),
                                     "tolerance_pct": cr.get("tolerance_pct", 0.5),
                                     "ok": pct <= cr.get("tolerance_pct", 0.5)}

    if spec.get("composite"):
        dest = os.path.join(spec.get("out_dir", "."), "composite.png")
        r, _ = _read(base, spec["composite"])
        if r is None:
            not_looked["composite"] = "not downloaded"
        else:
            open(dest, "wb").write(r)
            results["composite"] = {"saved": dest,
                                    "ok": None,       # ⚠️ not judged: you are forced to look
                                    "note": "no heuristic knows whether it looks good: go look"}

    for name, e in results.items():
        for k, v in (e.items() if isinstance(e, dict) else []):
            if isinstance(v, dict) and v.get("ok") is False:
                failures.append("%s · %s" % (name, k))
            if isinstance(v, dict) and v.get("empty"):
                failures.append("%s · empty" % name)
    return results, failures, not_looked


def report(results, failures, not_looked, human=False):
    out = {"results": results, "failures": failures, "not_looked_at": not_looked}
    if not results and not not_looked:
        print(json.dumps({"error": "empty spec: no image to look at"}))
        return 2
    if human:
        for f in failures:
            print("  ✗ %s" % f)
        for n, m in not_looked.items():
            print("  ⚠️ NOT LOOKED AT: %s — %s" % (n, m))
        print("\n%d measures · %d failing · %d not looked at" % (len(results), len(failures), len(not_looked)))
    else:
        print(json.dumps(out, ensure_ascii=False))
    if not_looked:
        return 2                                    # ⚠️ before anything else: I could not look
    return 1 if failures else 0


def selftest():
    import tempfile
    d = tempfile.mkdtemp()

    def save(name, size, bg, box=None, corner_alpha=0):
        im = Image.new("RGBA", size, bg + (corner_alpha,))
        if box:
            for y in range(box[1], box[3]):
                for x in range(box[0], box[2]):
                    im.putpixel((x, y), (255, 0, 0, 255))
        im.save(os.path.join(d, name + ".png"))

    BG = (16, 24, 32)
    save("icon", (100, 100), BG, box=(20, 20, 80, 80))            # 20% margin → passes a 9% threshold
    save("narrow", (100, 100), BG, box=(2, 2, 98, 98))            # 2% margin → does not
    save("header", (40, 20), BG, corner_alpha=0)                  # transparent corners
    save("opaque", (40, 20), BG, corner_alpha=255)                # opaque corners

    spec = {"base": d, "background": "#101820",
            "images": {"icon": {"expected": [100, 100], "min_margin_pct": 9}}}
    r, f, n = check(spec)
    assert r["icon"]["size"]["ok"] is True, r
    assert r["icon"]["margins"]["ok"] is True, r
    assert f == [] and n == {}, (f, n)
    assert report(r, f, n) == 0

    spec["images"] = {"narrow": {"expected": [100, 100], "min_margin_pct": 9}}
    r, f, n = check(spec)
    assert r["narrow"]["margins"]["ok"] is False, r                # margin too tight
    assert report(r, f, n) == 1

    spec["images"] = {"icon": {"expected": [999, 999]}}
    r, f, n = check(spec)
    assert r["icon"]["size"]["ok"] is False, r                     # wrong size
    assert report(r, f, n) == 1

    # ⚠️ the background is measured from the real alpha: transparent passes, opaque does not
    spec["images"] = {"header": {"transparent_background": True}}
    r, _, _ = check(spec)
    assert r["header"]["transparent_background"]["ok"] is True, r
    spec["images"] = {"opaque": {"transparent_background": True}}
    r, f, n = check(spec)
    assert r["opaque"]["transparent_background"]["ok"] is False, r
    assert report(r, f, n) == 1

    # ⚠️ a file that is not there is NOT a pass: it is a 2, and it stays written down
    spec["images"] = {"never-existed": {"expected": [1, 1]}}
    r, f, n = check(spec)
    assert "never-existed" in n, n
    assert report(r, f, n) == 2

    # ⚠️ an empty spec is not "all clear"
    assert report(*check({"base": d, "images": {}})) == 2

    # two images identical where they must differ
    import shutil
    shutil.copy(os.path.join(d, "header.png"), os.path.join(d, "copy.png"))
    spec = {"base": d, "background": "#101820",
            "images": {"header": {}, "copy": {}}, "distinct": [["header", "copy"]]}
    r, f, n = check(spec)
    assert r["_pairs"]["header≠copy"]["ok"] is False, r
    print("selftest: 14 asserts, all passed")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--example" in sys.argv:
        print(EXAMPLE)
        sys.exit(0)
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        print("usage: images.py <spec.json> [--human]   ·   --example for a commented spec")
        sys.exit(2)
    spec = json.loads("\n".join(l for l in open(files[0], encoding="utf8") if not l.strip().startswith("//")))
    sys.exit(report(*check(spec), human="--human" in sys.argv))
