# The rubrics — the judge gets them ALL AT ONCE

⚠️ **All at once, not one at a time.** Loading a single rubric per judgment is chunking, and the
most recent guidance prescribes the opposite: you no longer need to split the window the way you
once did. Where two sources disagree, the more recent one wins, and you tell which is more recent by the
models it names.

**How to read a rubric.** An artifact is classified by **what can go wrong**, never by format or
recipient. **Severity is binary and lives on the instance** (`blocking` / `non-blocking`, a required
field), and it is **not a property of the criterion**: the same criterion produces a cosmetic finding
and a blocker. A rule's **weight** is its **historical FALSE rate**, not a number: that rate doesn't
decide whether a finding passes but **how much scepticism it takes to believe it**.

⚠️ **The eight are not ranked, and that's a declared deviation.** The original form distinguished **two
primary wounds** (what reaches a customer, and silent failure) from a third of a different kind: wrong
numbers, serious but internal, which touch a decision rather than an output. Here that ranking is
**deliberately absent**: severity belongs to **the instance, not the criterion**, and an order among the
rubrics would produce exactly the invented weight the metric refuses. **What remains, and it's worth
more**: *outward harm* versus *harm to a decision* (irreversible versus correctable), and that governs
the *make it impossible* step, not the order of the rubrics.

⚠️ **A rubric with no corpus enters service UNCALIBRATED, and says so.**

---

## The eight

⚠️ **The irreversible ones are `R-01` · `R-03` · `R-05` · `R-07` · `R-08`**, the ones whose damage
goes out and doesn't come back: a design already installed, a message already sent, an action already
taken on the platform, **code already in production**, a page already public. **On these there is no
sampling, no after-the-fact authorisation, no threshold.** The other three (`R-02` `R-04` `R-06`) can
be loosened **after** measuring a base rate. ⚠️ **`R-07` belongs here and moving it out is not an option**: it is the class the
obligation of the three end-to-end tests rests on, and loosening it there removes the net exactly
where it is most needed. ⚠️ **And a rule that says *"no discount on the irreversible ones"* without
naming which ones they are is not a rule**: whoever applies it redoes by eye a classification that
was already settled.

| id | Artifact | Judges | Irreversible? |
|---|---|---|---|
| **R-01** | **Anything carrying a brand outward** | assets used whole, never cropped · colours taken from the live product, not from one asset · text legible against its background · **only public-facing identifiers** (numbers, handles) ever go on it · ⚠️ **an artifact already delivered is not the same object as a draft**: check what re-issuing it does to the copies already out there, before you re-issue · ⚠️ **and anything that READS AS GENERATED is a defect, not a taste call**: the rubric also says what's forbidden because it's recognisable — default gradients, choices nobody actually made | **yes** |
| **R-02** | **Numeric report** | reconciles with the source · **every figure from a rerunnable script**, never reused from a previous document · facts kept separate from hypotheses | no |
| **R-03** | **Outgoing message** | **draft approved before it leaves**, no exceptions · a format the destination actually renders · **no dangling references**: every sentence says what it refers to and what to do | **yes** |
| **R-04** | **Data synchronisation** | you write **only to the system of record**, never to a derived view · the join key declared · one write path, with its guard | no |
| **R-05** | **Action on a platform** | **idempotence · reversibility · "what if it fires twice?"** · ⚠️ **a mode that calls itself "a dry run" and acts for real**: the most dangerous defect in this rubric, because whoever uses it feels safe · ⚠️ **ordering**: does the outward effect fire **before or after** the mark on disk? | **yes** |
| **R-06** | **Interface** | view only · parity with the primary interface · no silent divergence from the underlying data | no |
| **R-07** | **Code** | ⚠️ **a versioned copy of what runs exists**, which isn't a given: the real case isn't *the copy has drifted*, it's **there is no copy**, production code whose only history is a disk's revisions · no version-control operation can change what production runs · loud failure · **three end-to-end tests** (happy path + two error cases) | **yes** |
| **R-08** | **Publishing to anyone** (public repo, site, shared page) | ⚠️ **Searching for words is not enough, and this is measured**: a `grep` for the proper nouns found **zero** traces where three attackers found **dozens**. The **indirect fingerprints** are what identifies you, not the name: rules that only one domain has, exact counts, writing conventions, calques from the author's first language · **the check is an identification test**: play a stranger and answer *who wrote this, what sector, what product, how many of them, which tools* — if any answer comes out, the trace is there · ⚠️ **and traces don't live only in the text**: commit author and email, **timezone**, `reflog`, licence, example URLs. The remedy has to be in place **before the first commit**, because a `git init` done afterwards already carries them | **yes** |

⚠️ **`R-01` has its own executable check, and it ships**: `tools/images.py`. It measures sizes,
transparent background, per-side margins and the **region covered** by whatever the process composes
on top, the defect no check on the uploaded file can see, because **the file is clean and the
composition is not**. ⚠️ **It does not say whether something looks good**, and it says so: where a
human eye is needed it **saves the composed image and forces you to look at it**, so the judgement
stays with whoever looks but can no longer be skipped by inattention. ⚠️ And **could not look** exits
**2**, never 0: the only defence against a *"zero errors"* nobody measured.

⚠️ **Rubric 5 isn't verified by a judge on every run**: a read-only judge cannot judge an action — on
one real corpus, across 21 reports, **rubric 5 never produced a single finding** — and no amount of
examples calibrates a judge on what it can't see. It
lives in the **boundary contract** that declares the assumption, plus an **executable check** that
proves it, **in the job's own code**. ⚠️ Putting it inside the artifact's judge would make whoever
judges **the product** judge **the machine** instead — the mix-up the two axes exist to prevent.

⚠️ **An artifact that drags another one along with it is not two rubrics: it's one rubric with an
appendix.**

⚠️ **[OURS]** — **The three tests in rubric 7 are mandatory on everything**, not advice: a small error leads to
wrong data and code that doesn't work. **The endurance proof isn't theirs**: it belongs to the judge
that opens the product and uses it over time. ⚠️ **The `[OURS]` mark isn't decoration**: that
obligation is **an addition of ours, not a source prescription**, and it's the heaviest one we've
added. Without the mark it was indistinguishable from a source rule, that is, **unprunable**, because
the law says prescriptions don't get removed and our own additions do.

---

## The two cross-cutting requirements

Not rubrics: **every rubric carries them.**

### A — Failure must be loud

**Six questions, one answer each, the same for every process.** There is no per-process knob.

| Question | Answer |
|---|---|
| **How many noises** | **two, declared**: *I rejected something* = **outcome**, goes straight to whoever decides · *I didn't run* = **fault**, goes where faults go |
| **Who classifies** | **whoever writes**, with a `type` field. ⚠️ Never the reader guessing from a prefix: that gets it wrong **in both directions** |
| **Who watches for "it didn't run"** | ⚠️ **somebody OUTSIDE the thing that breaks.** A dead process cannot declare itself dead |
| **Within how long** | **the damage decides**: high → immediately; low → **self-cancelling**, one alert a day that switches itself off |
| **Where it lands** | **a declared personal channel of whoever must act**, not a shared one read by whoever happens to pass. ⚠️ A loud alert with no declared recipient isn't loud |
| **What separates it from a transient** | **duration, and the READER judges it.** The producer always writes: it knows it's broken *now*, not for how long |

⚠️ **And the duration filter has a hard prerequisite, without which the rule isn't executable: a `since`
field, written ONCE and never rewritten.** If the producer rewrites the date on every round, a five-hour
fault keeps saying *"today"*, and the reader **has nothing to measure against**. Whoever writes an alert
writes `since` the first time and never touches it again: **the date of the first cry, not of the
latest one.**

**Plus THREE rules that aren't questions** — ⚠️ and they are three, counted right here: for a while this
line said *two* while listing three, which is the exact signature this skill teaches you to spot.

- ⚠️ **And no `set -e`**: it aborts halfway, leaving the work **half done and saying nothing**, which
  is worse than a loud error. You check the outcome command by command. **The exit code is part of the
  definition**: `0` = it worked, `≠0` = it broke. ⚠️ **A finding is not
  `≠0`**, and ⚠️ **a process that always exits 0 cannot fail by construction**: its crash is
  indistinguishable from *all fine*.
  ⚠️ **And the convention gets PROVED, not assumed**: break the process on purpose and look at the code
  it actually returns. A wrapper that swallows the child's exit makes the convention true in the code
  and false in fact, and nothing says so.
- **Severity is declared by the boundary contract** (`CONTRACT.md`); ⚠️ **if the contract says nothing,
  it's high.** You start at maximum alert and downgrade **by writing it into the contract**. Intended
  consequence: a process with a written contract never cries wolf, one without a contract cries, and
  that's the pressure that gets contracts written.

⚠️ **[OURS] An "I'm done" notice is not proof of delivery.** It says the worker stopped, not that anybody
received. Two different facts, and the sources cover only the first: proof of delivery is **the file on
the other side**, not the message claiming it was sent.

⚠️ **And here is the only exception to the two noises: the watchdog is a THIRD channel, declared.**
The two noises are written by whoever works; *"it didn't run at all"* cannot be written by them: they
are dead. The third channel is the precondition of the rule of two rather than an inconsistency with it, and it
must be named or somebody will remove it to simplify.

⚠️ **And the watchdog has TWO MOUTHS, plus a periodic HEARTBEAT even on a healthy estate.** ⚠️ **Not a
fourth noise**: it's the same third channel **delivered over two paths**. Two mouths because with a
single path the watchdog **becomes the single point** it was placed there to cover: the two are chosen
so they **can't die together** — not the same process, not the same machine, not the same channel — and
an *"already alerted"* field stops the same thing from sounding twice. The heartbeat because **a
guard's silence must not mean two things**: without it, *"all fine"* and *"the guard is dead"* read the
same. The project declares the period.

⚠️ **The failure channel cannot live inside the thing that breaks.** If the channel carrying everyone's
failures dies, the alerts it would have carried die silently with it: it's the single blind spot of any
system, and it's also the **cheapest** place to put a judge: it computes nothing, it assembles and
sends.

**Two proofs, ranked:**

- the **silence proof** end to end (break the process **for real** and check the alert arrives) is
  **once per process**, and **it's the one that counts**;
- the **self-test** is repeatable and **it's the one you repeat**.

⚠️ **On its own the second certifies a mouth speaking in an empty room.** And ⚠️ **a green self-test
proves nothing**: break the rule **on purpose** and the check must shout. If it doesn't shout, it
wasn't there.

⚠️ **What you PROVE is the process that executes, not the objective**: an objective has no mouth, the
process does, and one process can cover four objectives. **The verdict stays per objective, the proof
is done per process.**

⚠️ **The four ways of going quiet, all measured, and none looks like a fault**: *it asked something of
nobody* (stuck on a prompt nobody sees) · *it delivered to nobody* (finished, message never arrived) ·
*it never finishes* (open-ended mandate) · *it always exits 0*.

⚠️ **And a fifth, which is about configuration**: **the secret is also the off switch**. If removing a
credential stops the process **silently**, the switch exists and nobody knows.

### B — How context gets spent

Judges **the way of working**, not a produced thing. That's why it isn't one more rubric.

| id | Rule | Rejects |
|---|---|---|
| **CTX-01** | **Programmatic tool calling** | dumping twenty tool results into context when the model can write the code that runs the chain and return **only the result** |
| **CTX-02** | **Memory ≠ context engineering** | keeping them in the same drawer |
| **CTX-03** | **One worktree per session** | two sessions stepping on the same files |
| **CTX-04** | **An agent inside a hook** | putting one there without restraint: *you'll burn a lot of tokens very fast* |

⚠️ **Every line carries an id, and it isn't decoration: it's what makes "the judge cites the id, not the
talk" executable.** Without an id the judge cites the source, and whoever reads the verdict has to go
reread a talk to understand the objection. **With the id, a finding is checked in one line.**

⚠️ **And here the ids are `CTX-…`, not `B-…`**: the sound rubric's eight groups run through `A` to `H`,
and until this fix these four lines were called `B-01`…`B-04` — **the same label as four other lines in
that rubric, which say different things.** An id that means two different things in two files removes
exactly what it exists for: checking a finding in one line. A judge asked to cite the id has no way to
say which of the two it means.

### The "sound" rubric, and why it isn't shipped here

The loop's fourth parameter (*sound*) needs its own list, or it's an adjective: the judge has
nothing to cite and invents the criterion each time. **That list is extracted once, from your own
sources**, and it lives next to these files.

**Eight groups**: `A` who builds isn't who judges · `B` how you judge · `C` what enters context ·
`D` how you decompose · `E` the shell · `F` the trigger · `G` measurement · `H` how you build.

**How it gets built** — the same rules as everything else here:

| Rule | In one line |
|---|---|
| **Every line is falsifiable** | it says **what it rejects**, with a concrete case. A line that rejects nothing you can name is a slogan |
| **Every line carries an id** | `E-11`, `B-01`. ⚠️ It's what makes *"the judge cites the id, not the talk"* executable |
| **Every line carries a pointer to the source line** | not to the source: **to the line** |
| **It ships without weights** | on purpose, and declared. An invented weight is worse than no weight; real weights arrive with each line's historical FALSE rate |
| **A line that rejects everyone is kept with a way out** | ⚠️ **and the exception comes from the source, not from you** |
| **Where two sources give different numbers** | you declare the disagreement and **the wider threshold applies**: rejecting on the narrower one would be inventing a rule |

⚠️ **Why it isn't in this repository**: the extracted lines quote engineering talks line by line, and
those transcripts aren't ours to republish. **The method is here; the rows come from your sources.**
Reference size, measured on one real extraction: **73 lines across the eight groups**, roughly a
seventh of the length of the material they came from, and that reduction is what makes them usable
in a verdict rather than in a reading.

---

## How a rubric grows, and how it gets pruned

**Criteria are collected from OUT-OF-RUBRIC findings rather than written.** A judgment that falls
outside the rubric that produced it is the material for the next rule, measured at **25.9%** of all
findings.

⚠️ **Discovery fires at ≥2 out-of-rubric findings in one judgment, and the judge runs it**, since the judge
is the one who produces them: 44 out of 44. **It may only add criteria, never remove them.**

**You prune with a number**: a rule goes when it rejects **0% or 100%** of applicable cases on a real
corpus. Measured once: **47% of the rules produced no information at all.**

⚠️ **But before the count: has this line ever had a chance to fire?** A rule that's never been wired up
rejects 0% **by construction**, and that zero is not a proof — it's a decision to build it or drop it,
never a count (`SKILL.md`, "The law that governs everything else"; `CALIBRATION.md`, "How you prune").

⚠️ **And whoever touches a line marks it on the line itself — who · when · on whose instruction — in the
same act as the edit**, not in a separate log nobody reopens (`CALIBRATION.md`, "Who may rewrite a
rubric"). It holds here too, which is where a line actually gets touched.
