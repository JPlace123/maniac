# The boundary contract

**It's what the judge cites when it says no to someone arriving from outside.**

⚠️ **Who writes it: whoever designs the project, at step 4, the moment they discover it touches
somebody else's resource.** Not later, not "when someone asks": at that moment they know **why** they
touch it, and it's the only time they do. Every project that
touches a shared resource writes one. **Five sections, one screenful.**

| Section | What it's for |
|---|---|
| **I read** | what I take from the resource, and **what happens if it isn't there** |
| **I write** | what I write, **by which path**, with which guard, and different paths are different guards |
| **I assume — and here's the check** | the heart: **one line per assumption**, with what happens if it breaks and **the executable check that proves it** |
| **Summon me for** | a **closed** list of triggers, plus an explicit **"don't summon me for"** |
| **I don't cover** | the boundary with the other contracts |

⚠️ **And where there is no check, you write "NOBODY TODAY".** You don't leave the cell blank: a blank
cell reads as *I didn't think about it*, and `nobody today` reads as **a known hole**. It's the
difference between an uncovered assumption somebody eventually covers and one that stays mute forever.

⚠️ **Every clause carries the check that proves it, and that isn't pedantry.** A contract written as a
comment **rots**: one file declared that renaming a dataset would reset its history, while another
script rewrote that dataset **whole** on every run. Nobody noticed for weeks, because a comment has no
check.

⚠️ **A comment is not a tool.** If an assumption lives only in prose, nothing is guarding it.

## Where it lives, and who updates it

| Rule | In one line |
|---|---|
| **Where** | in the **project**, where whoever can update it lives. Plus a **per-resource index**, in one place, which is **the trigger for summoning**: without that index nobody knows who to call |
| **Where the index lives** | ⚠️ **outside the projects, in one place that sees them all: `contracts/index.tsv`, next to the folder judges are installed from.** One address only, written out in full, ⚠️ **and it has to exist**: a trigger with two addresses, or with an address nobody ever created, isn't a trigger. Inside a project it would only be visible to whoever is already inside, and the index exists **precisely for whoever arrives from outside**. One line per resource: *resource → who touches it → where its contract lives* |
| **Who creates it, and when** | ⚠️ **Neatnik, at step 4**, the moment it classifies a project that touches a shared resource: it adds **one line**: *resource → project → contract*. That's a side effect of classifying, not separate work. **If the index doesn't exist, it creates it the first time it's needed** |
| **When the contract gets updated** | ⚠️ **at every judge verdict on that project**, not when somebody remembers: the judge has just looked at the artifact, and that's the moment it knows whether an assumption stopped holding. The self-test runs **with the other checks**, not on its own |
| **Who updates it** | **the judge plus a self-test**: the check takes the measurable clauses, the judge the rest |
| **Who does NOT** | the owner who **remembers**. A contract maintained from memory is one that ages |
| **If it doesn't cover the case** | you **negotiate**: two rounds, then the owner decides. A flat no on a new contract would block everything |
| **What keeps the cost down** | the **"don't summon me for"**. It's what lets most summons close themselves: without it, changing one column becomes five negotiations |
| **Who writes the self-test, where it lives, when it's born** | ⚠️ **whoever writes the clause writes it, in the same act: at step 4, together with the "I assume" line it has to prove.** Not separate work: it's the **executable check** that line already carries beside it ("every clause carries the check that proves it", at the top of this file). **Where it lives**: next to the **code that proves it** — the process's own code for rubric 5's clauses (see "Rubric 5 lives here"), the piece that touches the resource for the others — **never inside the contract**, which is prose and doesn't run. **When it's born**: with the clause. A measurable clause with no check next to it isn't half-written: it's a cell that says **"NOBODY TODAY"**, and reads as a known hole. ⚠️ Until this fix this half was **named as an actor in six places and installed by none**, while the other half — the judge — was installed and dated |

## The contract is the regression suite

⚠️ **The "I assume" section is, line by line, the proof of the boundary.** The self-test proves the
**piece**; the contract proves the **boundary**. When you touch a shared resource, **re-run the checks
in everyone else's contracts**, not yours.

## Security lives here, not in the negotiated standard

⚠️ Security **doesn't change from one job to the next**: it's a standing property, and this file
already has the right shape. Putting it in the per-job agreement means rewriting it every time and
**forgetting it one time in ten**.

| Line | The check that proves it |
|---|---|
| **what of this project is reachable from outside** | the list of public entry points, regenerated by a command |
| **which of those sit on an end user's path** | ⚠️ those are the ones that count: a broken internal entry point is a fault, one on a user's path is harm |
| **which secrets it touches, and where they live** | never in the repo, never in the document |
| **what it leaves behind** | the data that remains after the job is done |

⚠️ **Retention: the MINIMUM that's needed, declared case by case.** A fixed number borrowed from
elsewhere is convenient for whoever writes it and indefensible when someone asks.
*"The minimum needed"* forces you to say **what it's needed for**, and that's where you discover it
often isn't needed at all.

⚠️ **And a security document is only worth something if its findings have a written ending**: an audit
closed with *"no fix applied"*, with the fixes then made **without updating the document**, is worse
than no audit: the next reader believes they're still open.

## Rubric 5 lives here, not in the judge

⚠️ **Idempotence is a property of the PROCESS, not of what it produces.** A read-only judge cannot judge
an action — on one real corpus, `R-05` never produced **a single finding across 21 reports** — and no
amount of examples calibrates a judge on what it can't see. So `R-05` (`RUBRICS.md`, "The eight")
declares itself **here**, once on the process's code, instead of on every run.

**Three lines of the "I assume" section, each with the executable check that proves it:**

| Line | The check that proves it |
|---|---|
| **what if it fires twice?** | a self-test on the process's own code that **breaks the rule on purpose** and must shout: a green run on its own proves nothing |
| **can you undo it?** | how you reverse the effect, and who runs it. Where you can't, you write **NOT REVERSIBLE**, a known hole, not a blank cell |
| **ordering**: does the outward effect fire **before or after** the mark on disk? | a test on the state after a dead run — the invariant that on one real estate was **a comment**, and no test would have failed re-queuing a non-idempotent run |

⚠️ **Step 4 of `SKILL.md` is what requires this**, sending here whoever produces actions on a platform:
for a while the rule said *"lives in the contract"* while **the contract never received it** — an
address with nobody bringing the mail.

## The severity of the alert is declared here

⚠️ **This is the severity of the ALERT — how loud a fault in this process must sound — not the
`severity` field of a verdict**, which stays **binary and on the instance** and the judge writes it
(`RUBRICS.md`, "How to read a rubric"). Same word, two different things: here it's about **who has to
wake up**.

⚠️ **`RUBRICS.md` §A sends you here** — *"severity is declared by the boundary contract; if the contract
says nothing, it's high"* — and until this fix the contract had no cell for it: a rule with an address
and no form to write it on. The cell is **one line of the "I assume" section**, not a sixth section: the
sections stay five.

| Line | The check that proves it |
|---|---|
| **what does the silence of this process cost** — `high` (immediately, to a declared personal channel) or `low` (**self-cancelling**: one alert a day that switches off on its own) | the **harm** that justifies it, written beside it in one line: *what happens to whoever's outside if this stays quiet for a day*. Without that line the downgrade isn't written, and the default applies |

⚠️ **The default is `high`, and you don't downgrade it out loud**: you start at maximum alert and step
down **only by writing it here**, with the reason. Intended consequence: a process with a written
contract never cries wolf, one without a contract cries, and that's the pressure that gets contracts
written.

⚠️ **Not a knob on the six questions of "failure must be loud".** The six answers stay **one, the same
for every process** (`RUBRICS.md` §A): this line changes none of them, it's **the data the fourth one —
*within how long* — answers with**, because that one says *"the damage decides"* and the damage is the
one thing that changes from process to process.

⚠️ **`RUBRICS.md` §A is what requires this, and whoever writes the contract writes it**: at step 4, in
the same act as the other "I assume" lines.

## The custodian

**Whoever wants to touch something another workflow uses goes through that workflow's judge.**

| Rule | In one line |
|---|---|
| **What triggers the summons** | touching a **shared resource**, not shared files: six jobs writing to the same sheet share no file at all |
| **What gets defended** | **the written contract**, not the checks. ⚠️ Measured: a renamed stage in a CRM breaks no check and stops a job **silently** |
| **What happens at a no** | you negotiate **two rounds**, then, whatever the outcome, it goes to the owner |
| **Does it apply to the owner too** | ⚠️ **yes.** The two most expensive silent failures measured on this estate started from **a hand**, not a job |
| **What you do with what you find** | **report it to the custodian, don't fix it.** Even when the fix is two lines |
