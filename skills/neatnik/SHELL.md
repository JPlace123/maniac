# The shell, and the three axes

**The order is the source's, and it doesn't invert: `brain → shell → trigger`.**

| Axis | What it covers |
|---|---|
| **brain** | prompt, skills, tools, sub-agents |
| **shell** | where state lives, what happens when it falls over |
| **trigger** | when it starts by itself, how far it acts |

⚠️ **Neatnik designs all three**, even when one is occupied by infrastructure you can't rewrite: there
it **measures and reports**, and the verdict goes to whoever owns it.

## The twelve shell questions

⚠️ **None of these go to the owner.** They're deduced **read-only** from the real jobs.

⚠️ **And these twelve are a proof on one case, not a theorem.** They came from looking at a real
estate, and **their perimeter is declared incomplete by the measurements themselves**: a different
estate will produce others, and some of these will split nothing. Use them as a starting point, **and
write the thirteenth when a project demands it**.

**The bar for a question to make the list**: ⚠️ **it gets in only if it SPLITS the estate.** If every
job answers the same, the question **is noise**, not coverage, even when the answer is interesting.

1. **Where state lives** between runs, and who else reads it.
2. **What happens if the process dies halfway**: is there a mark on disk, or does it start over?
3. ⚠️ **Ordering**: does the outward effect fire **before or after** the mark on disk?
4. **Who decides it's this process's turn** and not another doing the same thing.
   ⚠️ **And whatever decides it (a lease, a lock, a turn) is a MUTEX, not a health certificate.**
   Using it as proof the process is fine promotes its expiry into an alarm threshold, and produces
   **one false alarm a day by construction**. The health question is a different one, and it's asked
   like this: **"did it run TODAY?"**, not *"is somebody holding it right now?"*.
5. **What happens if two start at once**: is there a lock, and at what granularity?
6. **How it stops**, and who can stop it.
7. ⚠️ **Is the secret also the off switch?** If removing a credential stops the process **silently**
   (`exit 0`, indistinguishable from *nothing to do*), then the switch exists and nobody knows.
8. **Which copy of the code it runs**, and how that copy stays current.
9. **How long it can be down** before anyone notices.
10. **What it reads that it didn't write**, and what happens if it isn't there.
11. **What it writes that somebody else reads**, and with what guarantee.
12. **Who notices it didn't run at all**, and ⚠️ **that somebody must sit outside the thing that
    breaks.**

⚠️ **The finding worth more than the twelve**: *"is the job idempotent?"* comes back the same for
everyone: they all claim it in the comments, **and two of them aren't**. The question that
discriminates doesn't ask about quality: it asks about **ordering** (no. 3).

## One brain governing many hands

⚠️ **Decomposition also has a second shape beyond isolating context, and it stays unwritten
until you write it.** **One brain** governing **many hands** (several containers, machines or
sessions), with state in one place and execution in many.

**What differs from "many agents"**: the hands are **interchangeable and stateless**, the brain is
**one** and holds the state. If a hand dies, another starts and nothing is lost; if the brain dies,
you're stopped, and that's where the guarding goes.

⚠️ **And the decoupling is also the defence on secrets**: credentials stay **with the brain**, outside
the container that executes. The source says it whole: *giving an agent a bunch of your secrets and
letting it run for ten hours while you're not watching can be a little spooky*. The cure is **not
giving it the secrets**, rather than watching harder.

## Resuming is not a replay

⚠️ **On a machine that re-runs on a schedule there is no event log to resume: there's the whole run
done again at the next tick.** That's why **idempotence carries all the weight here**, and the
sources never name it, because they guarantee the *loop* resumes, not that tools with side effects are
retryable without duplicating the effect.

## The shell isn't the process's: it's the shell it wears

Processes sharing a shell behave the same under failure and get looked at together. Two different
disciplines **inside the same shell** are not two shells.

⚠️ **Only one of the questions isn't deducible (what a missed run costs), and it still doesn't go
to the owner**: it is already **the third of the six owner questions** (the irreversible damage), and
the shell **consumes that answer** instead of asking for it again. Asking twice in different words is
the fastest way to stop being believed on the first ask.

## Attached tools

**Every attached tool costs its name, description and schema in EVERY session, used or not.**

⚠️ **But zero calls doesn't mean useless**: it can mean *used from another machine*, *used outside
here*, or *just installed*. Where you can't tell, **declare it NOT SEARCHED and remove nothing**: a
partial measurement doesn't authorise a removal.

⚠️ **This is a declared deviation from the source**, which prescribes not multiplying tools. It holds
as long as the measurement on the other machine stays undone — and once it's done, this reopens.
