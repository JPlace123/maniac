# The `audit` mode

**`neatnik audit <project>` delivers a verdict. ⚠️ IT REWRITES NOTHING**: not a comment, not a typo.
If that rule falls, *"the audit doesn't rewrite"* dies on day one and the audit becomes a rebuild.

⚠️ **Verdicts live on a map of their own, separate from the project's, and the two say different
things**: the project map says **how a thing should be**, the audit map says **what needs fixing in
what already runs**. Keeping them together collapses them into the second, because work-to-do shouts
louder than design. A separate map also means the verdict **survives whoever didn't want to hear it**.

**Where it ends**: at the **verdicts** (one per objective), plus the remediation plan and the tickets.
**Executing the remedies is separate work.**

## The order

**First the channel through which everyone else's failures reach the owner**, because it's both the
cheapest and the highest-leverage point. Then **by descending harm**.

⚠️ **An objective that already has a verdict isn't redone: it's ratified.**

## The gate, and the window for what already runs

⚠️ **The step-7 gate applies here too, and here is where it really bites.** Anything that can't answer
**what triggers it · what context it has · how you steer it** doesn't start, but what **already runs**
doesn't get switched off: **you declare a window with a date** by which it answers, and **a window with
no date is an extension**. The place that date gets written is this mode's verdict: it's the only
document the owner rereads when the date arrives. ⚠️ **The rule lives in this mode too, not only in step 7**: the mode that designs
**new** things never meets a thing that already runs, so a window written only there is a rule nobody
is ever in a position to apply.

## The stopping criterion

⚠️ **It applies to adapting, not to auditing: you look at all of them.** And **"not worth adapting" is
a written verdict**, with its reason, not a skip. A skipped objective is indistinguishable from a
forgotten one.

## The shape of a verdict

| If the object is | Shape |
|---|---|
| **trunk** (things rest on it, even if only to notice) | **four full sections, plus the judge** |
| **leaf** | **short card, ≤20 lines** |

**The four sections** are `b` **verifiability** · `c` **what the owner has to understand** · `d`
**loud failure** · `e` **unblocking**. ⚠️ **`a` isn't the fifth: it isn't prose, it's the judge
installed** (a separate evaluator + a negotiated contract), which is why the row above says "four full
sections, PLUS the judge." Listing it alongside the others would make five items under a four, which is
the mistake this row used to make.

**What a verdict contains**: which rubrics apply · the two axes · the verdict (`conformant` /
`needs adapting` / `not worth adapting`) · findings with `file:line` and **binary severity on the
instance** · the remediation plan, each item with the `file:line` that motivates it · **one single
line** for the owner, or `none`.

## What to look at — the failure modes already measured

- **does it produce and publish in the same step?** — if so, there's nowhere to put a gate
- **is the contract parseable, or prose in a log?** — a human reads prose, a machine doesn't
- **does the exit code separate *it worked* from *it broke*?** — and ⚠️ **a process that always exits 0
  cannot fail by construction**: its crash is indistinguishable from *all fine*
- ⚠️ **does the outward effect fire before or after the mark on disk?**
- **what happens if it fires twice?**
- **is there an executable check, and does it exercise the real path or a stub?** ⚠️ Stubs that don't
  exercise the real path **invent failures** as well as hiding them
- ⚠️ **does a mode that calls itself "a dry run" have real effects?** It's the worst of the family,
  because **whoever uses it feels safe**: a dry run that writes anyway, a demo mode that really sends,
  a preview that saves. **You prove it the only way that counts**: run it and look at **what changed
  outside**, not at what the log says
- ⚠️ **a green self-test proves nothing on its own**: break the rule **on purpose** and the check must
  shout. If it doesn't shout, it wasn't there
- ⚠️ **how does the code that runs here arrive, and in which direction?** — **manual push, automatic
  pull**: if the outbound side is automatic too there are **two writers on the same branch with no
  lock**, and the defect only shows up the day the two overwrite each other (see "How code reaches
  another machine" below)

## What you prove, and what you judge

⚠️ **You prove the PROCESS that executes; you judge the OBJECTIVE.** An objective has no mouth: the
process does, and one process can cover four objectives. **The verdict stays per objective, the
silence proof is done per process.**

## How you touch a live object

**Stop it, change it, restart it.** ⚠️ But *"stop"* doesn't mean the same thing everywhere: if the work
is shared across machines, stopping it here **doesn't stop it**: it moves to the other one, which runs
**its own copy**. Before changing anything, establish **what "stopped" means** for that object.

## The re-check after an adaptation

- the **self-test proves the piece**;
- ⚠️ **the boundary contract proves the boundary**: the *"I assume"* section is, line by line, the
  regression suite;
- ⚠️ **you touch a shared resource → re-run the checks in EVERYONE else's contracts.** Not yours.

## How code reaches another machine

⚠️ **Manual push, automatic pull. Never bidirectional**: automatic outbound means two writers on the
same branch with no lock.

⚠️ **And the notice that something changed reaches the owner by their own channel, not a shared one**:
a shared channel is read by whoever happens to pass. **Silence = nothing changed.**
