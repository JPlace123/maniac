---
name: neatnik
description: Use at the entry of a new project (`neatnik <goal>`) or on something already running (`neatnik audit <project>`). Designs the machine that builds and maintains (who produces, who judges, what happens when it's wrong) and installs the judge. Not a work plan: that's a planner's job.
---

# Neatnik

A planner says **where you're going**. [`ponytail`](https://github.com/dietrichgebert/ponytail) says
**how little will do**. Neatnik says **who builds, who judges, and what happens when it's wrong**, and
leaves it written where it will be reread every day.

**Three modes.**

| | `neatnik <goal>` | `neatnik audit <project>` | `neatnik tidy <project>` |
|---|---|---|---|
| When | new project, before code | something already running | **before saying "ready"** |
| Delivers | **four sections written into the project + the judge, installed** (`a` isn't prose: it *is* the judge) | verdict, remediation plan, tickets | the count of decisions actually implemented, and the **curve** |
| Never | — | ⚠️ **rewrites anything.** An audit delivers; it doesn't fix | ⚠️ **decides for you**: what is a choice becomes one line for the owner |

⚠️ **Neatnik accompanies; it isn't a single pass.** It has no turn, only a **trigger** (§9).

## The files, and when they open

| File | Opens when |
|---|---|
| **`RUBRICS.md`** | the judge judges. **All rubrics at once**, never one at a time |
| **`MECHANISM.md`** | you design the machinery: states, retries, overturns, the two doors |
| **`CONTRACT.md`** | the project touches a **shared resource** — also where security lives |
| **`VERIFICATION.md`** | you decide **how big** the round is, or you delegate to somebody |
| **`CALIBRATION.md`** | the judge needs calibrating, or a rubric needs pruning |
| **`SHELL.md`** | you design **where state lives and what happens when it falls over** |
| **`MEMORY.md`** | you decide who remembers what, and what the out-of-band pass may do |
| **`AUDIT.md`** | `audit` mode |
| **`tools/citations.py`** | **you run it**, you don't read it: the first rung, executable. Does every `file:line` cited in a verdict actually exist? |
| **`tools/images.py`** | **you run it** on `R-01`: measures the images produced instead of looking at them, and where an eye is needed it saves the composite and forces you to look |
| **`tools/tidy.js`** | **before saying "ready"**: is every decision taken actually implemented? Three levels: `:low` `:medium` `:max` (`VERIFICATION.md`) |
| **`tools/inventory.py` · `coverage.py` · `history.py`** | the count behind `tidy`, and the **curve** that says whether you're converging |

⚠️ **`neatnik:tidy` is a gate, not an optional command: the word "ready" isn't used without a passed
`tidy`.** If it hasn't run, the delivery says **"work finished, not yet verified"**. The reason is a
measured failure (work declared ready with **a fifth** of what had been decided inside it), and the
defence hadn't failed through carelessness: **no check could fail** on a decision left on paper.

⚠️ **The rubrics line pointed at `RUBRICS.md` and nothing else, and that wasn't enough**: the rule about
*which list of cases the judge opens* lives in `MECHANISM.md`, and step 4 sent nobody there. **The judge
opens both**: `RUBRICS.md` for what gets judged, `MECHANISM.md` for how the case is put in front of it.

---

## The law that governs the rest

**What your authoritative sources prescribe is law. You adapt to it.** Start from what the source
says and adapt the project, never the reverse. A decision that deviates is a **deviation**, and it
gets **declared** — never left implicit.

- You may **improve** and **add**. You may not discard a **prescription**.
- **What you added yourself gets pruned**, and the sources ask for this (*shrink your scaffolding*):
  one of your rules goes when it rejects **0% or 100%** of applicable cases on a real corpus. With a
  number, never on a hunch.
- ⚠️ **A rule that comes from us gets marked `[OURS]`.** Without that mark it's indistinguishable from
  a source prescription, and **nobody will ever prune it**: pruning applies only to what we added, so
  what we added has to be **recognisable**.
- ⚠️ **And a rule that rejects EVERYONE is kept, with a written way out beside it.** It doesn't
  discriminate, so by the metric it should go, but removing it means no longer looking at that thing.
  The way out is a **named and motivated exception**, not a deletion. ⚠️ **And the exception must come
  from the source, not from us**: if we invent it, we've only moved the pruning somewhere nobody counts.
- ⚠️ **But a zero isn't always evidence.** A rule that has never rejected anything **because it was
  never wired up** has a zero **by construction**, and that zero says nothing about its worth. Before
  pruning: *has this rule ever had the chance to fire?* If not, it's unbuilt design rather than fat,
  and it gets built or dropped **by decision**, not by count.
- ⚠️ **When two sources contradict each other, the more recent wins**, and you don't get the date
  from the file: you get it from **which models the speakers name**.
- ⚠️ **Three cases the law does not decide, and they go to the owner**: (1) two sources saying
  opposite things; (2) the source contradicts a **fact about the owner** they stated themselves, and a
  fact isn't overturned by decree; (3) applying the source **removes a limit** with nobody having
  measured what happens without it.

---

## Step 0 — the announcement

Three lines, before the work:

```
🧭 Neatnik <mode> — <goal in ≤10 words>
   artifacts: <numbers> · <interactive|unattended|both> · <leaf|trunk>
   I stop at: <the stop point> · verification: <low|medium|max> · round: <1-5>, why: <line> · human: <yes|no> on <what>
```

⚠️ **The "I stop at:" field isn't decoration: it's the only place the stop point gets written down
BEFORE.** `MEMORY.md` says it is declared here, and until now the announcement **had no box for
it**, a rule with a moment and no form to write it on. A stop point decided later is a stop point decided by
somebody who is already tired. ⚠️ **And the other two fields on that line exist for the same reason.**
`round:` is the **rung on the verification round's ladder** (`VERIFICATION.md`, the five rungs) —
**not** the tidy level, which is the field next to it and answers a different question: **the agent
declares the weight**, with a line saying **why**, and the owner corrects it in one line. `human:` is
the other deduction that had a rule and no place to write it: **whoever decides if a human is needed is
the agent, and it ANNOUNCES it before starting** (§"The posture"), so the place it announces it is
**here**. Corrections to these two fields pile up where the other ones pile up, and the same two readers
reread them.

It's a **declared hypothesis**, not a decision taken. ⚠️ **Whatever Neatnik deduces on its own passes
through a verification round before being announced**: the owner's correction stays, but it's the
last check, not the first. **The corrections accumulate at the bottom of the document**, ⚠️ **and
"the document" has to be named, or nobody writes them down**: it's the **four-section document, the
one next to the judge**, the same address as step 8f and for the same reason (*with no address nobody
rereads them*). **Who rereads them**: the **§9 job**, which counts them together with the frictions,
and `CALIBRATION.md` when the classification gets calibrated. They're the material the classification
is calibrated on, and without them you go wrong the same way every time.

## Step 1 — the problem, not the folder. And here Neatnik CALLS, it doesn't redo

⚠️ **Neatnik orchestrates.** Before designing the machine, it makes sure somebody has already worked
out **what** is being built and **in what order**. It does not do that itself.

| If it's missing | Neatnik | Then |
|---|---|---|
| the problem hasn't been interrogated | invokes your **requirements/interrogation skill** and **waits** | resumes at step 2 with the answers |
| the work isn't broken into tickets | invokes your **planner** and **waits** | resumes at step 4 |
| the domain vocabulary doesn't exist | invokes your **domain-modelling skill** | resumes |
| ⚠️ **always, before building** | invokes your **prototype step** | ⚠️ **ALWAYS, not "if needed"**: the conditional form was tried and rejected, because *"only when it's dangerous"* rests on a classification of danger you get wrong. So cheap it isn't worth skipping, and if it becomes half an implementation, *always* becomes *almost never* within a month |
| construction starts | invokes **[`ponytail`](https://github.com/dietrichgebert/ponytail)** and leaves it on | it's the ladder that decides **how much code gets born** |

⚠️ **Calling isn't absorbing.** The planner stays the planner: Neatnik doesn't redo it and doesn't
replace it, contributing only the **agentic architecture**. If those skills have already run,
Neatnik **doesn't re-run them**: it says so in one line and moves on. **If you don't have them, Neatnik
asks the three questions below itself** and carries on: it degrades, it doesn't stop.

⚠️ **`ponytail` sits on a different axis from the other three, which is why its trigger differs.**
Interrogation, planning and domain modelling run **before** and say *what* gets built; `ponytail`
stays on **during** and says *how much*. Neatnik designs the machine, `ponytail` stops the machine
being bigger than the job.

⚠️ **And the reason the call is a step and not a suggestion**: step 5 says the standard is negotiated
**before** building. If interrogating the problem is something the user has to remember to do, then
the standard gets negotiated **only when somebody remembers**, which is the failure this whole
method comes from.

**The three questions** that interrogation has to have settled: **what is the problem · what does the
solution do in general · why do you care.** Start there, not from the artifact.

A project is **a goal**. Two repos serving one goal are one project; one folder serving two goals is
two projects.

## Step 2 — the six questions for the owner

These, and **only** these. Everything else is settled by the loop in step 3.

1. **The goal.**
2. **What counts as an error facing outward.**
3. **The irreversible damage.**
4. **What already exists and must not break.**
5. **When it's finished.**
6. ⚠️ **What would you want to be possible that isn't today**, and this one **authorizes**: an
   ambitious answer **raises the ceiling** (§10). The first five are all about damage; without the
   sixth, Neatnik is only a machine that prevents things.

**The rule that generates the list**: a question belongs to the owner **only if no loop could deduce
it**. ⚠️ **Covered = a falsifiable line comes out of it**, proved by rejecting or passing **a real
artifact already produced**.

⚠️ **And on a new project that artifact doesn't exist yet**, so the proof happens one of two ways, and
you declare which: **on an artifact of the same kind produced elsewhere**, or **you mark the answer NOT
PROVED** and reopen it at the first real exit. An unproved answer isn't an error; **an unproved answer
that looks proved is.**

⚠️ **And if a question isn't covered, the gate is this: you don't go to step 3.** The loop deduces
everything else **starting from** these answers; running it on an uncovered question means deducing
from a hole.

⚠️ **Never a technical question with the recommendation attached**: it manufactures consent instead
of collecting it. On technical matters you bring the **measured result**, not the option to pick.

⚠️ **And it applies identically to AGENTS, not just to the owner.** Measured: three classifiers were
told *"this is the class you have to justify, not the default"*, and all three returned **zero** in
that class. The shape of the question had manufactured the answer, and the defect belonged to whoever
wrote it. **A briefing that hints at the outcome collects confirmations instead of measuring**, and
you recognise it by the signature: every agent answers the same.

## Step 3 — the loop, on everything else

Four parameters. Each must reject something, or it's noise:

| Parameter | Rejects |
|---|---|
| **cheap** | what it costs **every time** it runs |
| **simple** | how many pieces must be true at once |
| **effective** | does it reach the stated goal |
| **sound** | does the agentic shape follow the guidelines, **always** |

*Sound* is what makes the loop irreducible to the other three: without it, the winner is always **one
agent that does everything and declares itself fine**.

**It stops when a round improves no parameter**, and the cost of the round **is declared on delivery**.

⚠️ **The technical side has one door, and it gets mounted like the others**: it's closed by a **judge
separate from the artifact judge**, and the owner receives **the measured result**, not the option to
pick. Their door on a technical choice would be a rubber stamp.

| | **Artifact** judge (8a) | **Technical** judge |
|---|---|---|
| **Receives** | the artifact + `RUBRICS.md` | the **technical choice** + the **four parameters** |
| **Closes with** | outcome, findings, what wasn't looked at | **which parameter rejects it, and with what number** |
| **When it runs** | on every artifact somebody uses | when the step-3 loop must choose between two shapes |

⚠️ **Two instances, not two names for the same thing.** A judge that receives the rubrics cannot judge
a technical choice: it doesn't hold the parameters, and it would invent them.

⚠️ **Where this loop does NOT apply**: the source says so about itself, *"our loop is our loop, it
may not be the right loop for you; if you're working on hardware it's probably the wrong loop."* If
the project touches hardware, Neatnik **says so** and doesn't apply it blind.

## Step 4 — classification

⚠️ **Before you classify, one question: what does the recipient actually receive?** The artifact to be
judged is **what lands in front of them, not the text you're writing**: the day's list, not the
document holding it; the message, not the script that sends it. The rule sits in full in
`MECHANISM.md`, **and a step has to open it at the moment of choosing**: read afterwards, it arrives
too late to change rubric.

**Which of the eight artifacts it produces.** You classify by **what can go wrong**, never by format
or recipient. No object gets two rubrics; outside the eight you **negotiate** one, and **the list of
negotiations gets written down**, ⚠️ one line per negotiation, **in the same four-section document**,
and it's **this step** that writes it, at the moment it negotiates. It isn't bookkeeping: it's **the
evidence you need one more**, and evidence nobody accumulates doesn't accumulate. `R-08` exists
because that count reached one. ⚠️ **It has already happened**: R-08 wasn't designed at a desk, it came out of a negotiation, something to publish to anyone, which none of the seven covered. Rubrics live in `RUBRICS.md`.

**Plus two axes**: `interactive | unattended` (decides the **mechanism**) and `leaf | trunk` (trunk =
other things rest on it, even if only to notice).

⚠️ **And the leaf/trunk axis has two halves, not one: on the TRUNK you check first; on the LEAF you
TOLERATE imperfection.** The second half is what makes the first sustainable rather than a concession: a
method that checks everything the same way gets ignored on everything the same way.

⚠️ **And here the axis gets CONSUMED, not merely announced.** An axis only `audit` mode reads is, in
build mode, a word said at step 4 and used by no later step. **What changes, in three points that hold
for every artifact, not just for code:**

| | **trunk** | **leaf** |
|---|---|---|
| **The verification round** (§`VERIFICATION.md`) | starts from the **pair**: one builds, another takes it apart | the **cheap round** is enough |
| **Section `b`** (verifiability) | one line **for every thing it produces** | one single line for the whole |
| **The judgment** | ⚠️ **you check FIRST**: the gate stands in front of the exit | you tolerate imperfection and fix afterwards |

⚠️ **On `leaf` the obligation of the three end-to-end tests never lapses** (`R-07`): that is a
specific line and it beats the general one. *"You tolerate imperfection"* is about **the finish**, not
about the net that stops a small error becoming wrong data, and that is the door *"tests only on
trunks"* would try to come back through.

⚠️ **A third axis, and it doesn't coincide with the first two: "what the owner has to understand".**
A small thing can be the one they need in order to decide, and a large one may not concern them. It
produces the **short list per project**: the few things they must hold in their head, written next to
the judge.

**And if it touches a shared resource** → `CONTRACT.md`, which is also the trigger for summoning the
custodian.

**And if it produces actions on a platform** (`R-05`) → `CONTRACT.md` **here too**, section "Rubric 5
lives here": idempotence is a property of the process and gets proved **once on the code**, not on
every run — a read-only judge can't judge an action.

## Step 4b — the shell and the trigger

⚠️ **There are three axes, and so far you've designed one.** The order is the source's and doesn't
invert: **brain → shell → trigger.** Step 4 classified the **brain** (what it produces, under which
rubrics); here you design the other two.

1. **Open `SHELL.md` and ask the twelve questions.** You ask them **yourself, now, read-only**: none
   go to the owner, they're deduced by looking at what runs.
2. **Discard the ones that don't split.** If every part answers the same, the question **is noise** and
   doesn't enter the document.
3. **Group the processes by shell and look at them together.** ⚠️ **The shell doesn't belong to the
   process: it belongs to the shell it wears** — whoever shares one has the **same** behaviour under
   failure, and two different disciplines **inside the same shell aren't two shells** (`SHELL.md`, §"The
   shell isn't the process's"). Looking at them one by one redoes the same answer N times and makes it
   look like N measurements. ⚠️ **And here you decide what happens when it falls over**: on a machine
   that **reruns on a schedule** there's no event log to resume, there's **the whole run redone at the
   next tick** — *"resuming isn't a replay"* (`SHELL.md`, §of the same name) — which is why
   **idempotence carries all the weight here**: the sources guarantee the *loop* resumes, not that
   tools with side effects are retryable without duplicating the effect.
4. **Write the answers into section `d`** (loud failure), which is where the shell becomes verifiable.
   ⚠️ **And in that same section, instantiate the six loud-failure questions** — the table in
   `RUBRICS.md` §A. The **answers** are one and the same for every process, but the **names** belong to
   this project and no other step asks for them: *who watches from outside · **what are its TWO mouths
   and how often does it beat** · which declared personal channel it reaches · who writes the `type`
   field · where the `since` field lives, written once and never rewritten*. ⚠️ Without this line,
   nobody ever opens `RUBRICS.md` §A — the same defect declared below for the twelve questions.
5. **The trigger**: for anything that starts by itself, the step-7 gate — *what triggers it · what
   context it has · how you steer it*. If one of the three has no answer, **it doesn't start**.
6. **Review the attached tools**, the *"Attached tools"* section of the same file. Each one costs a
   name, a description and a schema **in every session, used or not**. ⚠️ **But zero calls doesn't mean
   useless**: it can mean used by another machine, used outside here, or just installed. Where you can't
   tell, **write NOT LOOKED FOR and detach nothing**, and that *NOT LOOKED FOR* is an act, it stays
   written down. ⚠️ **This step opens `SHELL.md` for the tools section too, not only for the twelve
   questions**, otherwise nobody reads that section at all.
7. **Run the silence proof, and write that you ran it.** You break the process **for real** and check
   the alert arrives: it's **the one that counts**, the `--selftest` is the one you repeat
   (`RUBRICS.md` §A, "Two proofs, ranked"). ⚠️ **You do it once per PROCESS, not per objective** — an
   objective has no mouth, and one process can cover four. **Where you write that you did it is section
   `d`**, with the date and what you broke to run it: a proof nobody logs is indistinguishable from one
   never done, which is where this rule sat as long as no step executed it.
8. **Open `RUBRICS.md` §B — "how context gets spent" — and answer line by line.** There are four
   (`CTX-01`…`CTX-04`) and they judge **the way of working**, not a produced thing: which is why **no
   judge receives them as an exit criterion** — the artifact judge doesn't see the work, only what came
   out of it, and the technical judge holds the *sound* rubric. **This step runs them**, like the six
   loud-failure questions at point 4: for each one, **this** project's answer — who chains the calls and
   what returns into context · where memory lives versus context · one worktree per session · what runs
   inside a hook — or **why it doesn't apply**. ⚠️ Without this point, nobody ever opened §B either: the
   same defect already fixed above for §A, and the four lines stayed a list somebody would read out of
   curiosity.

⚠️ **Skip this step and nobody ever opens `SHELL.md`**, and the twelve questions become a list
somebody reads out of curiosity.

## Step 4c — say first what you're about to break

⚠️ **Every gate in this method looks at an artifact that ALREADY EXISTS.** The judge sees what left
somebody's hands; the custodian is summoned when something is about to touch other people's resources.
**Neither sees the intent**, and intent is the moment when stopping costs least.

**Before you start building, one line: *what of what exists is about to change behaviour because of
me?*** Not *what do I touch*, but **what changes behaviour**. Then:

| What you found | What happens |
|---|---|
| **nothing** | you write it and move on. It's the normal outcome, and it needs to be written: a declared *"nothing"* and *"I didn't ask myself"* look far too alike |
| **something of yours** | you declare it in the step-0 announcement and carry on |
| **something of somebody else's** | ⚠️ **it stops here**: summon the custodian (`CONTRACT.md`) **before** building, not after |
| **something irreversible** | ⚠️ **it goes to the owner**, and their answer is what unblocks it. ⚠️ **And if what's about to be born will be published to anyone — a public repo, a site, a shared page — `R-08` gets read HERE, not at the exit**: its remedy has to be redone **before the first commit**, because commit author and email, **timezone** and `reflog` are already carried in by a `git init` done afterwards, without anyone choosing it. The 8c hook watches the exit, and by then the first commit has already happened: this is the only step that sees the intent |

⚠️ **And the answer is a deduction, so it goes through the round like everything else.** Whoever is
about to build is the worst placed to estimate what they'll break: they declare it, and somebody
without their plan in their head rereads it.

## Step 5 — the standard is negotiated FIRST

Builder and judge agree on **what "done" means** before a line is written, and evaluation happens
**against that contract**. The contract is a JSON line the caller parses: **no contract = rejection**.

⚠️ **And "the caller" has to be named, or it's an actor nobody installs.** The caller is **the step-8c
hook**, the one that fires when something goes out. It invokes the judge, reads the JSON line, and
**writes the verdict next to the judge's trace**. If that seat is empty in a project, step 8 **isn't
installed**: a judge was placed and nobody to call it, so judgement never fires. **The check that proves
it**: let something go out and look for the verdict file. If it isn't there, the caller is missing, not
the judge.

⚠️ Discovery may **only add** criteria, never remove them (§9). Removing is a separate decision, and
it has its own number.

## Step 6 — make it impossible

**A mandatory step, not a section you pull out when you feel like it.** For everything you're about
to forbid: *can the road be removed instead of writing a rule?*

**It triggers on reversibility**, not on stakes: stakes require estimating a harm before it happens,
and that's the estimate you get wrong.

⚠️ **And the case that shows why this is a fixed step**: where a dry run exists, **automatic
invocations bypass it on their own.** The safeguard protects the hand of whoever's watching and leaves
the night shift exposed — and nobody ever **decides** that: you just end up there.

⚠️ **And the answer gets written**: one line per prohibition — *road removed*, or *rule written, and
why the road couldn't be removed* — **in the four-section document**, the same address as step 4's
negotiations and for the same reason (*with no address nobody rereads them*). It used to be the only
mandatory step with no trace, and **a proof nobody logs is indistinguishable from one never done.**

## Step 7 — the two gates on birth

**A custom tool is born for three reasons only**: not expressible with the primitives · an external
API with awkward auth or format · speed and reliability worth the maintenance. **Start from the tools
a human at a computer has, and subtract.**

⚠️ **This gate is `ponytail`'s ladder applied to tooling**, and it's why the two skills hold together:
Neatnik's law is **subtractive** (*shrink your scaffolding*, *start from what exists and subtract*,
*make it impossible instead of forbidding it*), and `ponytail` is the same law applied line by line
while building. If `ponytail` is on, it runs this step and Neatnik **checks the outcome** rather than
redoing it.

⚠️ **A smoke test at the start of a round**: run it, and it exists to **stop you rediscovering how the
thing even starts every single time.** It's the first thing missing when somebody comes back to a
project after a month.

**The proactivity gate BLOCKS**: a routine that can't answer **what triggers it · what context it has
· how you steer it** **doesn't start.** ⚠️ **For what already runs, you declare a window with a date**:
a window with no date is an extension.

## Step 8 — the chain, and installing the judge

```
produce → judge → publish → adjust the plan
```

⚠️ **The fourth beat is the one that gets lost, and it's the only one that stops the same mistake
happening twice.** *"Adjust the plan"* isn't a posture: it's **an act with a performer**. Whoever has
just seen a rejection **goes back to the step that produced it** (the wrong rubric at step 4, the
shell not looked at in 4b, the open-ended mandate of the round) and **changes that step, not the
artifact**. If nothing changes, you write *"no step to change"* with the reason: a rejection that
doesn't move the plan is a rejection that will recur identically. **The place it gets written is the
list of corrections** (step 0), which the §9 job rereads.

The detail is in `MECHANISM.md`. Here is **what gets installed**, because without this step
*"installed"* is a promise. **NINE things get installed across eight steps, and none is optional.**
They're numbered so the count can be checked **on the line itself**: a number you can't count against
its own list is the signature this skill teaches you to spot — and for a while this line said *eight*
while listing nine:

1. **the artifact judge** (8a) · 2. **the technical judge** (8a-bis) · 3. **the holding area** with its
**two** duties — declare what got touched, and write the reason to **exit** the block (8b) · 4. **the
hook on the way out** (8c) · 5. **the hook that blocks closing** (8d) · 6.–7. **the two sections** nobody
else produces, `b` and `e` (8e) · 8.–9. **the two memories**, the judge's and the builder's (8g). 8f
installs nothing: it says **where the sections end up** and **who rereads them**. ⚠️ **And two lines get
written for EVERY agent this step installs, not just the judge — they don't count among the nine
because they aren't things you install, they're the act of installing them**: (a) **the perimeter** —
*what it can read · what it can write · which outward actions are off limits* — and **an agent with no
such line doesn't get installed**, while until now only the judge had one, in its own file (§"The
posture"); (b) **what's been left to the human gate and why the automatic signal doesn't reach it**, one
line per item — without it, that gate **grows on its own**, shows up on nobody's ledger, and never
shrinks.

### 8a — the judge

1. **Write one instance per project, and it lives in the SHARED agents folder**, not inside the
   project. ⚠️ *One judge per project* means one **instance** per project, not a **location** inside
   it. The reason is measured: most projects have no agents folder of their own, and whoever runs
   them does so from a working directory that isn't theirs. A file placed inside **would never be
   loaded**. ⚠️ **And not in the always-loaded instructions file either**: there it would weigh
   **every session**, the worst case of *don't pay for what you don't use*.
   **If a project does have its own agents folder and is run from there, it goes inside**: the rule is
   *where it will be loaded*, not *where the code sits*.
2. **Head it**: the first line names **this** project, its artifacts and the rubrics that apply. A
   judge opening with a generic sentence **isn't an instance, it's a sentence**.
3. **Attach the list of tools it holds**, because you calibrate per **rubric × tools** pair
   (`CALIBRATION.md`). ⚠️ **And at least one of them ships with neatnik, rather than being written by
   the project**: until now the skill asked the judge to attach a tool **while shipping none**, which
   is asking for something nobody could do. What ships is `tools/citations.py`, **the first rung, made
   executable**: it opens every `file:line` cited and says which ones don't exist.
   ```
   python3 tools/citations.py VERDICT.md --root <project> --root <the sources>
   ```
   Exit **1** if a citation is dead, **2 if it found none at all**, because a verdict with no citations
   isn't clean, it's a verdict that proves nothing. ⚠️ **It declares what it doesn't do**: it checks the
   line **exists**, not that it **says** what you claim; `--phrase` looks for a word nearby, which is
   less than reading and more than nothing. ⚠️ **And the burden isn't the project's**: the rule is that
   **executable checks with no domain in them come up into neatnik and ship as rubric tools**. Every
   time a project writes one that never names its own domain, **that one comes up here**. **Nobody
   starts empty-handed.**
3bis. ⚠️ **If the judge runs on a high tier, you install TWO and pair them.** This isn't a cost
   choice: the high tier **finds 1.5–1.7× more and invents more**, so the second instance exists to
   **keep only what they agree on**, and what they disagree on becomes a *"contested"* finding rather
   than a discarded one. **This step installs the pair**, not whoever launches the judgement. ⚠️ A
   pairing prescribed in `CALIBRATION.md` and installed by no step is a pairing that doesn't exist.
4. **Declare whether it's calibrated.** A rubric with no corpus enters service **UNCALIBRATED and
   says so**: that declaration is what makes it falsifiable.
   ⚠️ **And where you calibrate, the set gets built RIGHT HERE, at this step**: **a distinct negative
   example for every tool attached at point 3** (`CALIBRATION.md`, first row), on cases **chosen for
   measurability** (`CALIBRATION.md`, "On which case do you test") and on **sources that hold up as a
   yardstick** (`CALIBRATION.md`, "Two warnings about calibration sources"): ⚠️ **a source that absorbs
   defects by customer name is not a yardstick** — whoever calibrates uses cases that source **doesn't
   name** — and ⚠️ **the set has its own error rate, measured at 4-21%**, which the judge **inherits
   without knowing** if nobody measures it. Then you check it against the three conditions of "when it's
   calibrated" — ⚠️ **zero errors means the set is too easy**, not that the judge is good. **Whoever
   changes the tool or the judge's model redoes this point**: it's the same reopening condition that
   applies to everything (`VERIFICATION.md`), and until now `CALIBRATION.md` said *when* you calibrate
   with no step ever doing it.
5. ⚠️ **It doesn't run in the builder's session**: it would see the reasoning.

⚠️ **A declared deviation on primitives.** Native forms exist for *declaring a measurable end state and
exiting the loop only once an independent verifier has verified*. Here the same thing is done **by
hand** (contract, separate verifier, exit tied to verification), and not because it's better:
**because nobody has tried them on a real case yet**. It's a deviation, not a choice: it reopens the
moment somebody measures them.

⚠️ **Four pieces of this architecture are NOT code to write: they already exist as primitives**, and
should be used rather than reimplemented: **a judge with a clean context** (a sub-agent has its own
system prompt, **doesn't receive the parent's conversation**, and its tools can be narrowed), **a gate
on the exit** (a hook that precedes the action can deny it), **a rubric loaded only when needed**
(files next to the skill open on demand), and ⚠️ **a hook that PREVENTS CLOSING**: a primitive exists
that denies the end of a turn, and it's the mechanism that makes judgment **unskippable** rather than
well-intentioned. Without it, *"the verdict arrives inside the delivery"* stays a posture: somebody
just closes.

⚠️ **And two measured limits, to keep next to the primitives or you find out late that they don't
hold**: hooks declared **inside** a project sub-agent **don't fire** until the folder is trusted, and
a non-interactive session **doesn't make it trusted**; and what the gate does when permissions are
wide open **isn't documented**. Until that's measured, **don't build on it**: write the deviation.

### 8a-bis — the technical judge

⚠️ **This is a SECOND INSTANCE, not the same judge with a different hat on** (step 3). A judge that
receives the artifact rubrics **cannot judge a technical choice**: it doesn't hold the parameters, and
it would invent them. As long as no step installed it, the technical side had its door **described and
never mounted** — and a door nobody mounts gets walked through by everyone.

Points **1, 2, 4 and 5** of 8a apply identically — an instance per project in the shared agents folder,
headed to **this** project, that **declares whether it's calibrated**, and that **doesn't run in the
builder's session**. Three things change:

1. **What it receives**: the **technical choice** and the loop's **four parameters**. **Not** the
   artifact rubrics: in place of 8a's point 3, this is what it holds in hand.
2. **How it closes**: it says **which parameter rejects it, and with what number**, and cites **the
   line's id**, not the source. The owner receives **the measured result**, not the option to pick:
   their door on the technical side would be a rubber stamp.
3. **When it runs**: when the step-3 loop has to **choose between two shapes** — not on every artifact
   somebody uses, which is the other one's trigger.

⚠️ **This rubric also enters service UNCALIBRATED and says so**: the *sound* parameter's rubric doesn't
have a corpus of real findings yet to measure the FALSE rate of its lines against.

### 8g — the two memories

**They get installed here, like the judge**, or they stay a rule nobody applies.

| | Where it lives | Who writes to it | When |
|---|---|---|---|
| **judge's memory** | next to the judge | **the judge** | at every verdict: what slipped past it and it noticed afterwards |
| **builder's memory** | in the project | **whoever builds** | when a road was tried and didn't work |

⚠️ **They don't merge**, for the same reason the judge doesn't see the reasoning.
⚠️ **No schema**: you declare **who remembers what**, not with which fields.
⚠️ **And they grow**: they fall under the step-10 budget, they aren't exempt.

**The out-of-band pass** that rereads and **marks** (never rewrites) is work for the §9 job, not
for whoever is building: the person who just wrote a line is the worst placed to reread it.
⚠️ **And the criterion for what's worth saving isn't decided**: until it is, **a memory where
everyone writes whatever they want buys the very defect the out-of-band pass exists to cure.**

## Step 9 — what makes Neatnik start again

- **Discovery** fires at **≥2 out-of-rubric findings** in one judgment, and **the judge runs it**.
- **Reopening conditions** for frozen decisions are checked as a **declared step of the verification
  round**. ⚠️ **One applies to all and isn't up for debate: a new model.** A better model turns old
  instructions into bugs, and the defect **looks like the model's fault**.
- **A job keeps the cadence**, not a person and not the judge: the judge fires when something
  **ships**, and the case you need to fix is precisely when nothing ships.

  **It gets installed here, not hoped for**: (1) choose **what counts as a delivery** in this project;
  (2) schedule a job **once a day** that looks at **how long since one arrived** and **how many
  frictions were written and never reread**; (3) the job **doesn't judge**: it raises a hand;
  (4) it does **the out-of-band pass** — it rereads what has been written and **MARKS** it, never
  rewrites it (`MEMORY.md`); (5) it **collects the edges between different goals** for the owner (§8e).
  ⚠️ Points 4 and 5 were assigned to this job **by other pages**, and the list of its duties didn't
  name them: from the point of view of whoever executes, they didn't exist.
  ⚠️ **And it counts the reversal rate too** (**reversals over verdicts** across the window it covers),
  because `CALIBRATION.md` assigns that count **to this job** and to nobody else. Without it, *"at zero
  it's silent"* (the worst way to miscalibrate a judge, the one you can't see) never gets found. The
  measured baseline is **21%** (⚠️ over **eleven** cases: a start, not a proof).
  ⚠️ **And the job re-judges**: it takes **an artifact that already passed** and has the judge open it
  again **after it has been in service**. That's the only way to put *"the endurance proof"* into
  operation: a judge that fires on the way out and closes **never sees how what it approved ages**,
  and that rule sat written with nobody executing it.
  ⚠️ **If the project has nothing that can count as a delivery yet, write that down**: a cadence on a
  project with no exits is a job shouting into a void.
- **Every friction that repeats becomes a feature.** ⚠️ In the source, two important features were
  born that way. A friction is material, not a complaint, **but only if somebody collects it**.

**The cadence, in the source's numbers**, and they are numbers, not an adjective:

| Prescription | In one line |
|---|---|
| **You ship every 1-2 days** | not "often" |
| **You answer feedback with code the same day or the next** | the cycle must be short enough to **discover the error fast**: that's the condition under which the sources authorise ambition |
| **You don't predict: ship → look → learn** | the loop run **50-100 times**, not planned |
| **Shared channels with whoever uses it, and use it daily** | ⚠️ it's the **second signal that doesn't come from the owner's mouth**. Without it, the vocal user is the whole sample |
| **A bet opens in a weekend** | one person, hours or a few days. And **closing it without shipping is a legitimate outcome** |
| **Close one real request in 24 hours** | not a speed stunt: **the first time you do it you find out how many obstacles your process has** |

⚠️ **And the brake the sources don't add, which applies here**: *"prototype what almost works"* holds
where being wrong costs a rerun. On something going out to an external person **it's an incident**,
and an agent that has shipped can't take it back. The criterion is **reversibility**, not how fast you
can fix it.

## Step 9b — what triggers the questions

⚠️ **The owner's questions have no turn: they have a trigger**, and without naming it *"Neatnik
accompanies"* stays a sentence.

| Trigger | Who | When |
|---|---|---|
| **ordinary engine** | **the project's judge** | when the rubric **doesn't decide the case** in front of it: there it needs a line from the owner, and the judge asks instead of inventing one |
| **big pass** | **Neatnik called back** | a new model · a more recent source that overturns · a change in the project's perimeter |

⚠️ **There is no third trigger, and in particular there is no "every session"**: that was the always-on
companion, and it fell with its own number.

## Step 10 — the ceiling

A declared token budget for what Neatnik ships into a project, ⚠️ **and the sixth question raises
it**, which is the only way *"authorises"* stops being a word:

| Answer to the sixth question | What changes |
|---|---|
| *"this is fine"* | budget unchanged |
| ⚠️ **something that isn't possible today** | **the budget goes up, and by how much is stated by the owner in the same line.** They raise it, not whoever builds |

⚠️ **And the budget must be COUNTED, or it isn't a budget.** Measure what Neatnik ships (the files,
the descriptions, what enters context) **before shipping it**, and write the number into the delivery.
A budget nobody counts has never rejected anything, and by the metric below **it would remove itself**. Prune **only the redundant or the
genuinely unused**, never what is used *actually and operationally*. An ambitious answer to the sixth question
raises it.

---

## Step 11 — translation, and it isn't a section: it's a step

⚠️ **It fires every time something has to reach the owner**: a line of choice, a verdict, a
measurement, a deviation. **If it's about to reach them and hasn't been through here, it isn't ready.**

⚠️ **Translation is a step, not a courtesy.** Whoever brings a choice brings it **translated**:

- the technical term **dissolved**;
- options **A/B/C separated by a blank line**, never buried in a paragraph;
- numbers **with their meaning attached**;
- one line of recommendation **with its reason**, except where the choice is between two sources:
  there the recommendation manufactures consent, and you put the two lines **side by side** instead.

**Simplify the language, never the data.** *"18 of 39 were never looked at by anyone"* stays exactly
that in plain language, with the pointer next to it.

⚠️ **The failure mode**: translating is rewriting, and rewriting is where you make the most mistakes.
A translation carries the **pointer to the line** beside it.

## How a ticket gets worked

**Neatnik launches its own tickets.** What can be done alone **gets done**; what has a doable half gets
its half done; **only what needs a judgment call becomes a step**. The owner gets **N lines, not N
tickets**.

`autonomy:` isn't a label, it's the behaviour: **A** starts and finishes · **B** starts and stops at
its line · **C** is a step from minute one.

**The loop is always there, including on yourself**: step 0 → produce → **a judge that doesn't see
the reasoning** → **at least one round mandated to ATTACK** → outcome declared. A round that confirms
doesn't count as a round.

| Rule | In one line |
|---|---|
| **The mandate** | **number of outputs + format**. Never *"at least N"*: it's open-ended upward, so there's no point at which the agent can say *I'm done* |
| **Delivery** | **is a file.** A message can fail to arrive without either side knowing; a missing file is visible |
| **The alarm** | **~15 minutes with no byte on disk**: retrim the mandate, don't wait. Below a certain size, delegating costs more than doing |
| **What gets declared** | the scale used · what the judge saw · **how many accusations and how many held** · the cost |

## A declared limit carries its proof

⚠️ **"It can't be done" is the only conclusion nobody ever checks**, because disproving it means doing
the work you just called impossible. Before declaring a limit, three lines:

1. the **exact error text**, and out loud the difference between *you asked wrong* and *this doesn't
   exist*;
2. the **nearby counterexample**: *have I already seen this same thing do something that implies the
   opposite?*, usually in the same session;
3. **what would have to be true** for the limit to exist. If the answer is an absurd design, the
   conclusion is wrong.

Say **"I didn't find a way,"** never *"it can't be done."* A value you did not find is reported as
**not looked for**, never as absent.

⚠️ **If the blocker survives the three lines**, dispatch **the critic**: the same adversary with the
mandate reversed, which attacks *this is impossible* instead of *this is true* and **sees all the
work done**. On a finished artifact, not seeing the reasoning is the defence; on a blocker it's
blindness.

## The four sections Neatnik leaves behind, plus the judge

| | Answers the failure |
|---|---|
| **a.** Separate evaluator + negotiated contract | the agent drifts and absolves itself |
| **b.** Verifiability as a design constraint | not knowing if it's right without reading everything |
| **c.** What the owner has to understand | reading a report and having understood nothing |
| **d.** Loud failure | the job that dies silently |
| **e.** Unblocking: tools, formats, context | capability overhang |

### 8b — the holding area, and the duty to declare

**Before the hook you need the place where the artifact waits.** Choose **where things that haven't
shipped are born**: a state, a folder, a branch, anything, as long as **being there isn't the same as
having shipped**.

⚠️ **And whoever executes is obliged to declare what it touched, in a parseable form.** Without that
declaration, *"no writes, nothing to judge"* is indistinguishable from *"I didn't say"*, a way of
skipping judgment that doesn't look like skipping it. **It gets installed here**: whoever produces
closes by listing the artifacts produced, and that list is what hook 8d checks.

### 8c — the hook on the exit

**You mount a hook that fires BEFORE the act that sends something out**, and not before just
anything: **only on the exit**, so it never runs for nothing and costs nothing on the days when
nothing ships.

1. **List what counts as an exit** in this project: the acts after which something is in somebody
   else's hands. If the list is empty, the project has no exits and the hook isn't mounted, **and you
   write that down**, or *"it wasn't needed"* becomes indistinguishable from *"I forgot"*.
2. **Hook the judge to that list**, not to the memory of whoever is working.
3. ⚠️ **The rule that goes through it is the one that pays**: what goes to somebody **passes the owner
   before leaving**. It's the only one that showed a return; the others were noise.

### 8d — the hook that prevents closing

⚠️ **Without this, "the verdict arrives inside the delivery" is a posture: somebody just closes.** You
mount the hook that **denies the end of a turn** until the verdict exists.

- **What it checks**: that every artifact declared in 8b has a verdict. **No verdict = no closing.**
- ⚠️ **And if the hook isn't available or isn't proven in this configuration, you declare it** (*here
  judgment is skippable*) instead of letting people believe it's blocking. A gate believed and absent
  is worse than a gate absent.

### 8e — sections b and e, which no other step produces

**`a` is installed by 8a, `c` comes out of the third axis in step 4, `d` comes out of step 4b.** Two
are left, and they get written here because nowhere else writes them.

**`b` — verifiability as a design constraint.** One line for everything the project produces: *at what
level can you check it's right **without reading the implementation**?* If for some thing the answer
doesn't exist, **that's the part to redesign**, not to document better. ⚠️ **And technical debt stays
out of this section**: it's the one thing the sources call unvalidatable without being an expert in
the implementation, and the owner reads it **on the edges between different goals**.

⚠️ **And `b` comes out with its own executable line, like `d`.** *"At what level can you check it's
right without reading the implementation?"* is a question that **produces a command**: if the answer
can't be run, **the answer isn't there yet**, and that's the part to redesign, not to write up
better.

**`e` — unblocking: tools, formats, context.** This is the section that answers the **capability
overhang**, the gap between what the model can do and what we use it for. Three lines:

| Line | The question |
|---|---|
| **tools** | what is it missing in hand to succeed on its own? ⚠️ Every copy-paste you do is **a capability you're denying it**, not a convenience of yours |
| **format** | what shape must the output take so somebody else can consume it without rereading it? |
| **context** | what does it need to know that today lives only in one person's head? |

⚠️ **`e` comes out with its executable line too**, and its own is the simplest of all: **the command
that does that work without leaving the tool**. If it doesn't exist, `e`'s line is exactly what's
missing.

⚠️ **The falsifiable test the sources hand you**: *try doing a full day of work without leaving the
tool. If you can't, the model can't do it with you.* Whatever forces you out goes in this section.

### 8f — what stays written

**FOUR sections and a judge that runs**, not five of prose. `a` isn't a
text describing an evaluator: **it is the evaluator**, installed at point 1. Two agents reading the
same description build **two different judges**; a file that runs builds one.

⚠️ **Cap: half a page per section, and it gets COUNTED**: it was the skill's only cap without a
counter, while step 10 says that *a cap nobody counts has never rejected anything*. You count it like
all the others: **the section's line count**, in the delivery, next to the cap. It's a cap on **the
prose that stays written**, a different thing from the token cap of step 10: that one governs what
neatnik **sends**, this one what it **leaves to be read**. What runs isn't counted in pages.

⚠️ **`a` isn't prose: it's the judge installed at point 1.** Two agents reading a description build two different
judges. `c` stays prose by necessity, because a human reads it. `b`, `d`, `e` are prose **plus the executable
line that proves them**.

⚠️ **Scope of `b`: technical debt stays OUT of it.** The source calls it the one thing not validatable
without being an expert in the implementation, so a section that exists to avoid reading the code
can't cover it. Debt is judged **by reading**, and the owner reads it — on the **edges between
different goals**, not on the long files.

⚠️ **And somebody has to COLLECT those edges, or the line above has no subject.** They're collected by
**the §9 job**, along with the rest of its round: it looks for **the calls that leave one folder and
land in another** (a process launched, a file executed by path, a command naming another goal's
script), and it leaves **the list, not a judgment**, in the document next to the judge. ⚠️ **The
reason they have to be searched for this way and not by eye is measured**: counting process launches
too, the places to touch for one change went **from 2 to 21**, and the goal with the highest number
**was neither of the two that looked like it**. The owner reads the list: it's the only part of the
debt that falls to them personally.

## Memory

**Judge and builder have two separate memories**, no schema, and the out-of-band pass **marks** a
superseded line rather than rewriting it. The detail is in `MEMORY.md`.

## The posture

⚠️ **You go forward, and the brake is automatic.** Six sources out of seven, when they authorise
ambition, ask for the same thing: **an automatic, fast way of noticing the error, placed in the
environment**, not in the head of whoever is watching.

⚠️ **And the source puts a limit on itself, which counts double here**: *"just because you're really
fast doesn't mean you're always really right."* Speed is an argument for **shortening the round**,
never for skipping it.

⚠️ **But three prescriptions BEFORE the attempt hold, and they're not negotiable**: whoever drives must
**know enough to ask the right questions** · the agreement on **what "done" means** comes before a line
of code · **what the agent can reach is limited in advance**, ⚠️ **for EVERY agent the project
builds, not just for the judge**: the judge's perimeter is written in its own file, and until now it
was the only one that had one. The line gets written at **step 8**, together with the agent: *what it
may read · what it may write · which outward actions are out*. An agent without that line **doesn't
get installed**, with a classifier instead of a person.

⚠️ **And where an automatic signal can't be built** (that something is beautiful, that a message sounds
right), **you build it in whatever form you can** (hard checks that get close), and **the human gate
holds only what's left over, declared as such.** Never in its place.

⚠️ **And "declared as such" is an act of step 8, not a posture**: when the judge is installed you
write down **what was left to the human gate and why the automatic signal doesn't reach it**. One line
per item. Without that line the human gate grows on its own (nobody decides it, everything for which
building the signal was more effort than asking ends up in there), and **the list of what a human has
to look at is on record nowhere**, so it never gets shorter.

⚠️ **First you close the hole of ungoverned exits, then you build the tool that groups the opinions**,
and that tool **doesn't exist today**: it's work for the project hosting neatnik, not something neatnik
ships. Said here because the ordering is a prescription, and **an ordering without the line saying what
is still missing** reads as though it were all already done.

⚠️ **And before loosening a gate, check how much actually passes through it.** Loosening a gate half
the work never reaches measures the wrong thing: **first close the hole**, then tighten, and **on
irreversible classes there is no discount, ever**: no sampling, no after-the-fact authorisation, no
threshold. On the others you may loosen **after** measuring a real base rate.

## What Neatnik doesn't do

- **It isn't a work plan.** That's a planner's job, and it stays there.
- **It doesn't rewrite another project's work**: whoever touches a shared resource goes through that
  workflow's **custodian**, and what you find **gets reported, not fixed**.
- **It has no always-on companion.** Measured against a month of real sessions, one would have blocked
  **9 times a day at 90.6% false positives**. What was worth keeping lives in a hook that fires **only
  on exit**.
- ⚠️ **It doesn't use agent teams**: non-interactive runs never spawn teammates, so unattended jobs are
  excluded **by construction**.
- ⚠️ **It doesn't trust hooks declared inside a project sub-agent**: they don't fire until the folder is
  trusted, and a non-interactive session doesn't make it trusted.

---

**Cheap prototype always** — see step 1: it's a step, not an afterthought.
