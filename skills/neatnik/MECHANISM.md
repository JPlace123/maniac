# The mechanism: what happens when somebody judges

**The chain is `produce → judge → publish → adjust the plan`.** The artifact is born in a holding
area; only a ✅ lets it out. **Rejected = doesn't ship**, and the rejection itself is what reaches the
owner.

⚠️ **This holds even for reversible actions.** Distinguishing by reversibility rests on a
classification of danger that you get wrong.

⚠️ **The fourth beat**: the verdict **goes back to whoever planned**. If a finding says something
about the **plan** and not just the artifact, it travels back up. Without it, the rejection stops at a
state and nobody learns.

## The two forms

| | **Unattended** (a job, at night) | **Interactive** (a session, with a human) |
|---|---|---|
| **Who decides the exit** | a **state**, not a question | **two doors**: the agent applies the rubric, the owner authorises **the exit** |
| **When it fires** | on **every artifact somebody uses** | same. One rule for day and night |
| **When it rejects** | goes to the blocked state **with the reason** | **corrects, and shows both the findings and the corrections** |
| **The contract** | a JSON line the caller parses | **it is the rubric**: the agent declares in one line **which one it's applying, before building** |

⚠️ **And the trigger has a blocking half that must be written or the rule isn't executable: WHOEVER
EXECUTES IS OBLIGED TO DECLARE WHAT IT TOUCHED.** The judge fires on the artifact, so somebody must say
**which artifacts were produced**, in a parseable form, not prose in a log. Without that declaration
*"no writes, nothing to judge"* becomes indistinguishable from *"I didn't say"*, and that's a way of
skipping judgment that doesn't look like skipping it.

⚠️ **You don't invent a state: you pick one the system already has.** Adding a state for judgment
means everything that reads states must be updated, and something won't be.

⚠️ **On technical choices the two doors aren't the same.** There the door is closed by a **separate
judge** against the four parameters, and the owner receives **the measured result**, not the option to
pick: their door on a technical choice would be a rubber stamp.

## When you exit the loop

⚠️ **DECLARED DEVIATION.** The earlier form prescribed a **cap of 2 rounds**, then you stop and ask.
Here the cap **is gone**, and the reason is that a more recent source ties the exit to **verification**
rather than to a count. A more recent prescription replaced the previous one, and it should be read
as such, not as a simplification of ours.

⚠️ **When verification has happened. There is no retry counter.** The exit is tied to **verification**,
not to attempts: a retry cap is a counter that decides in the verifier's place, and closes the loop
**even when no verification happened**.

⚠️ **The floor is an outcome, not a counter.** If the verifier **cannot** verify, the loop still
ends: it exits **"not verifiable", with the list of what wasn't looked at**. Without that list the
outcome becomes the shortcut that hollows out the judgment; with it, it's a capability no script has.

**So the loop has no ceiling because it has a floor.**

⚠️ **Not to be confused with the two rounds of negotiation with a custodian** (`CONTRACT.md`): those
are still valid, and they're a negotiation between two projects, not a verification loop.

## No rushing

⚠️ **Judgment is not a step you can skip: the verdict arrives inside the delivery.** You can go around
it, but not without it showing. A gate that can be postponed **is postponed**, and it's the
first ceremony to go when there's a hurry.

## Retries

**Not a knob.** A consequence of idempotence:

- **transport** (network, timeout, 5xx) → retry, with a ceiling in **time**, never in count;
- **non-idempotent action** → ⚠️ **never alone.** A dead run goes to the blocked state, **never back
  in the queue**: re-queuing would repeat the outward effect.

## The overturned rejection

⚠️ **When somebody unblocks a rejection, they write a one-line reason, and that reason is data ABOUT
THE RUBRIC, not about the request.**

It's the **second signal**: the only one that doesn't come from the owner's own mouth. Without it,
*you end up switching the evaluator off instead of calibrating it*.

| | |
|---|---|
| **What counts** | somebody says **"the judge got it wrong"** |
| **What does NOT** | *"fix applied"* — there the judge **was right**, and a signal that confirms calibrates nothing |
| **Measured baseline** | **21%** (⚠️ over **eleven** cases: a start, not a proof) overturn rate on a real corpus. **Above** = severe judge; **at zero** = silent judge, which is worse |
| **Where it goes** | attached to the rubric line that produced it. If it leaves no trace on the rubric it's a vent, not a signal |

## What judgment does not cover

⚠️ **The hallucinated ✅ is the one failure no mechanism catches.** A script fails the same way every
time and is debuggable; an agent can fail **once, silently**. The contract closes *"report missing"*,
not *"report wrong"*. The only defence that isn't *trust me* is the **execution proof attached to the
verdict**.

⚠️ **Cost is not a reason to switch the judge off.** You can change the model tier, you can narrow what
it looks at, you can raise the threshold of what goes through it, but **you don't remove it**.
⚠️ **And that threshold isn't free**: step 10 of `SKILL.md` governs it (*"before you loosen a gate, check
how much actually goes through it"*). **On irreversible classes there is no threshold, ever**, and on
the others you raise it **only after** measuring a base rate. Without that pointer the line above read
like a free knob, which is exactly the knob the decision forbade. A judge
switched off isn't a cheaper judge: it's the absence of a judge, with the same name as before.

⚠️ **DECLARED DEVIATION, and it belongs here because this is where the knob gets read.** The decision on
the interactive judge said **on every exit, not on request and NOT ABOVE A THRESHOLD** — one rule for
day and for night. The first two thirds are intact: it fires on every exit, and the rule is the same
day and night. The third isn't: here a threshold does exist, **on the non-irreversible rubrics only and
only after a measured base rate.** That's less than the decision allowed, not more — but it's still a
deviation, and whoever reads it should know that instead of finding it written as if it were the
decision.

⚠️ **And the real cost of this architecture is splitting every job into *produce* and *publish*,
not the judge itself.** Many do both in the same line, and there's no place there to put a gate.

## The right artifact

⚠️ **You judge what the recipient receives, not what you produced.** The case that teaches it: for a
messaging campaign, the artifact to judge is **the day's recipient list**, not the text. A
perfect message sent to the wrong person is an outward error, and no rubric on the text sees it.

**The question to ask before choosing a rubric**: *what's the thing that, if wrong, still reaches
somebody?*
