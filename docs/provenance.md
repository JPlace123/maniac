# Provenance

Where the rules come from, and what it cost to find out.

Neatnik wasn't designed and then justified. It was built by measuring, being wrong repeatedly, and
having someone else prove it. This file is the accounting, including the parts that make the method
look bad, because a methodology that only publishes its successes is exactly what rule 5 exists to
catch.

## The two sources of every rule

**Seven engineering talks on agent systems**, read line by line, and **measurements on a real
production system**: dozens of automations and scheduled jobs, several of them running unattended.

The provenance rule is strict, and it is the reason the result is worth anything:

> **Every number comes from a rerunnable command, never from a previous document.**
> **Quotation marks are for literal citation only. Our own words go in italics.**

Both rules exist because both were broken.

## The coverage check

Once the method was written, each of the seven sources was re-read **against** it, one agent per
source, going **from the source to the method**, never the reverse. The reverse direction only finds
what you already know you have, which is the failure one of the sources calls a *saturated eval*.

**260 prescriptive teachings** extracted. Then each grading was attacked by a second agent with a
mandate to demolish it.

| | Claimed |
|---|---:|
| Covered | 134 |
| Partial (the name is there, not the step that implements it) | 85 |
| Absent | 33 |
| Discarded with a written reason | 8 |

⚠️ **Then the attack rounds: 70 claims reopened, 53 defective. That's 76%.** The highest defect rate
measured anywhere in the project, and the defect had a direction:

- of **42 "covered" labels reopened, 33 didn't hold**: 13 collapsed entirely, 20 were downgraded.
  **9 survived as written.**
- but **9 of the 22 "absent" labels weren't absent either**: the thing existed and the checker hadn't
  found it.

Both extremes were inflated, in opposite directions. **The label that holds is the middle one.** The
honest reading: of what the sources prescribe, the method had usually taken **the name and not the
step**.

⚠️ And the other 92 "covered" labels were never attacked at all. That means **not checked**, not
*fine*.

## The half-quotation

Ten times across five days, a claim turned out to be a **half-quotation**: a real sentence, cut short
or glossed, producing a plausible and false conclusion. Four were the author's own.

The pattern is worth naming because it's the tax on this kind of work:

> ⚠️ **The citation is usually correct. The error lives in the sentence next to it.**

Three of the last four were exactly that: our own gloss written beside a correctly quoted line.
Examples that survived for days:

- *"regression evals measure the harness, not the model"* — the source says *"whether your harness
  **or** future models can do the same things."* Both.
- *"the counterintuitive **fact** that more thinking upfront costs less"* — the source retracts it on
  itself: the comparison demo never aired.
- *"none of the seven sources asks for caution before trying"* — false. Three do, and they were found
  by an agent whose only job was to look for the opposite.

An automated citation checker catches the drifted line number and the fabricated quote. It does not
catch the gloss. **Tools look where they know how to look**, which is also rule 3.

## The recurring defect, named

Five instances in two days of one mechanism:

| Case | Reported | Actually |
|---|---|---|
| A dependency scan | 16 places to touch | **21** — the regex saw one of three call styles |
| A coverage measure | 100% of outputs reviewed | **54%** — "output" was defined as "output that already had a review" |
| An age calculation | *not computable* | **~70 days** — the value was inside a file the script had written itself |
| An API field | *not writable* | writable — the same integration already wrote ten other fields on the same object |
| A judge's blind spot | *structurally can't see outside its rubric* | it produced **44 out of 44** out-of-rubric findings |

> **A tool looks at too little, and whoever runs it promotes its narrow field of view into a property
> of the world.** The mistake sits in the absence someone deduced, never in the arithmetic.

**All five were caught by a round mandated to attack. None by the agent that produced the work.**
That asymmetry is the single strongest empirical result here, and it's why rule 5 is not negotiable.

## Two mandates, same day, same model

| Mandate | Result |
|---|---|
| *N rows × 19 objects, 4-column TSV* — countable before starting | **1,387 verdicts in ~15 minutes**, full coverage, 0.4% undecidable |
| *"at least 20 verdicts"* + *"attack at least these 5 fronts"* | **0 bytes in 57 minutes**, no response to status checks, killed by hand |

⚠️ And the follow-up that stops this from being a tidy story: a third agent was given **12 numbered
verdicts** and still returned **0 bytes in 31 minutes**. A closed mandate is necessary and **not
sufficient**. What closed that round was doing it by hand in a few minutes. Below a certain size,
delegating costs more than doing.

## Where two sources contradict each other

Thirty-five collisions were found between the seven sources and the method. Sixteen were open. The
rule that resolved them:

> **The more recent source wins, and you date it by the models the speaker names.**

The first case: one talk prescribes keeping the context window lean and loading only what's needed;
another prescribes the opposite. The first places itself two model versions back and never mentions
two model families the second treats as already shipped. That ordering reversed a decision made four hours earlier.

⚠️ **Three kinds of collision the rule cannot decide**, and they go to a human: two sources saying
opposite things with no recency gap; a source contradicting a **fact** the owner stated about
themselves; and applying a source **removing a limit** nobody has measured the absence of.

## What this cost

42 decisions, each measured and adversarially attacked before being taken. Defect rates per round
ranged from **25% to 90%**. The best round, the cleanest measurement in the project, still had
2 of 8 claims downgraded.

That's the number to keep if you keep one: **on a good day, a quarter of what a careful agent reports
does not survive someone whose only job is to take it apart.**
