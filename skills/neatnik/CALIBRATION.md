# Calibrating a judge

**An uncalibrated judge is not neutral. It errs in one direction and doesn't know it.**

| Question | Answer |
|---|---|
| **How many examples** | ⚠️ not a number of examples: a number of **distinct NEGATIVE examples**. **At least one for every tool the judge has in hand** |
| **When you calibrate** | per **rubric × tools** pair, not per project. And **again** at every change of tool **and every change of model** |
| **When it's calibrated** | it reproduces none of the known FALSE families · it misses none of the TRUE ones · where the set says **undecidable**, it doesn't decide |
| **Zero errors in calibration** | ⚠️ means **"the set is too easy"**, not "the judge is good" |
| **Who decides the label** | the **cited line** → a **refuter who reopens the file** → the owner **only on what's contested** |
| **How you notice it's drifted** | the **overturn rate**, with a measured baseline: **21%** (⚠️ over **eleven** cases: a start, not a proof). Above = severe; **at zero = silent**, and that's the worse case |
| **Who calculates that rate** | ⚠️ **the rhythm job** (`SKILL.md`, step 9), along with the rest: **overturns divided by verdicts**, on the window it covers. Not a count somebody does when they remember — if nobody calculates it, *"at zero it's silent"* never gets caught. ⚠️ **And that job calculates TWO rates, not one**: also the **historical FALSE rate per rubric line** (→ "How you prune"), which is the weight |
| **What does NOT calibrate** | ⚠️ **counting findings.** Measured: whoever finds the most also invents the most |

## The fact the whole thing rests on

⚠️ **Where no tool answered, there's nothing to contradict, and a judge doesn't learn scepticism.**
Measured: judgments produced **without** a checker having run carry **3 negative examples out of 39**;
those with a checker that had answered carry **36**.

Consequence: **chronological sampling is the wrong one.** Taking the first N cases yields few negative
examples; the curve that matters is the one of **rules actually invoked**, and it bends much earlier.

## Where new criteria come from

**They're collected from OUT-OF-RUBRIC findings rather than written**: judgments that fall outside
the rubric that produced them. Measured: **25.9% of findings**.

⚠️ **And the CLASSIFICATION calibrates on a different pile**: the corrections to the step-0 announcement
— artifact, `interactive|unattended`, `leaf|trunk`, the round's rung, whether it needs a human — which
pile up at the bottom of the four-section document and which `SKILL.md` §Step 0 assigns to this page and
to the rhythm job. You read them **when you calibrate classification**, and what you look at is **which
cell gets corrected most often**: that's the cell whose criterion is written badly, not the agent that
keeps getting it wrong.

⚠️ **Discovery looks at out-of-rubric findings, and it also asks a question no count produces:
*what could I have asked and didn't?*** Out-of-rubric findings are what the judge **already
saw** and the rubric couldn't accommodate; this question hunts for what **nobody looked at**, and
without it discovery only finds inside its own cone of light.

**How you ask it, or it stays a good intention**: take the artifact **and list what wasn't looked at**,
the field the judge fills on every verdict. The entries that keep coming back are the next
rubric line. ⚠️ **It's the only entrance this method has onto the capability overhang**: everything
else measures what we already know we should check.

⚠️ **Discovery fires at ≥2 out-of-rubric findings in a single judgment, and the judge runs it.** Tested
backwards: `≥1` fires almost every time (and something that always fires isn't a trigger), while `≥4`
would have waited sixteen cases. **It may only add criteria, never remove them.**

⚠️ **And the assumption that the judge is blind outside its own rubric is FALSE, measured**: the
out-of-rubric findings were produced **entirely by the judge**, and a good quarter had **no rule behind
them at all**. Of a separate agent on the same objects **there is no measurement**.

## Who may rewrite a rubric

⚠️ **The agent may too, but only on the owner's explicit instruction, and leaving written who changed
what.** The rule stays the owner's: what changes is who holds the pen.

The reason is measured: with exclusive rights, **nobody updates the rubrics**. A correction waiting on
one person is a correction that doesn't arrive.

⚠️ **Where you write it down, or the obligation isn't executable: on the LINE ITSELF**, next to its
text — **who · when · on whose instruction** — and **in the same act as the edit**, not in a separate
log nobody reopens later. It's the twin of the other signal: an overturn ends up "attached to the rubric
line that produced it" (`MECHANISM.md`, "The overturned rejection" → *Where it goes*). The `[OURS]` mark
doesn't cover this: it says **which source a line comes from**, not **who changed it and when**.

## How you prune

**A line goes when it rejects 0% or 100% of applicable cases on a real corpus.** Measured once: **47%
of the lines produced no information at all.**

⚠️ **Before the count, one question, or the zero isn't a proof: has this line ever had a chance to
fire?** A rule that's **never been wired up** rejects 0% **by construction**, and that zero says nothing
about its value: it isn't fat, it's **a project not yet built**, and you build it or drop it **by
decision, not by count** (`SKILL.md`, "The law that governs everything else"). The guard sits in the
law, and it's worth repeating **here**, because here is where pruning actually happens.

⚠️ **A criterion's weight is its historical FALSE rate, not a number**: that rate doesn't decide
whether a finding passes but **how much scepticism it takes to believe it**. A number attached to the
line can't express severity, because **severity belongs to the instance**: the same criterion yields a
cosmetic finding and a blocker.

⚠️ **And that rate has an owner, or it stays a definition**: it's calculated by **the rhythm job**
(`SKILL.md`, step 9), alongside the overturn rate and on the same window — **line by line, that line's
findings that turned out FALSE divided by the findings it produced.** Same sentence as its twin: it's
not a count somebody does when they remember. **A weight nobody calculates isn't a weight, it's an
adjective** — and until the count runs, a line enters service **with no weight, and says so**, never with
a number chosen by eye.

## Two warnings about calibration sources

⚠️ **A source that absorbs defects by customer name is not a yardstick.** If a document names one case
thirteen times and two others never, it's fine as a document and **unusable as a measure**: you
calibrate on cases the source **doesn't name**.

⚠️ **A calibration set has its own error rate, and it gets measured rather than assumed.** Measured:
**4-21%** depending on the subset. A judge calibrated on labels nobody ever attacked **inherits that
error without knowing**.

## On which case do you test

⚠️ **A case used to try out a new rubric or a new judge is chosen for MEASURABILITY, never for
convenience: either the answer is already known, or the outcome is falsifiable some other way — and
which of the two applies gets DECLARED.** On an arbitrary case the outcome is **plausible and
unfalsifiable** — and a method nobody can disprove looks like it always works. It's the criterion that
picks the cases, not the order they happen to arrive in: the same reason chronological sampling is the
wrong one.

## Which model judges

⚠️ **Not a question of tier, a question of round.** The higher tier finds ~1.5-1.7× what the lower one
finds, but among the findings **exclusive** to the higher tier: half hold, the rest are reduced or
**invented**. And a false-but-plausible finding **costs a human to demolish: it's worse than a missing
one**.

**You don't pick a judge by tier: you pair it**, and pairing matters **more** with the higher tier,
because that's the one that invents.
