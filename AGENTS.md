# Using Neatnik with any agent

Neatnik is three markdown files and no runtime. Any agent that can read files can run it.

| File | What it is |
|---|---|
| `skills/neatnik/SKILL.md` | the method. Load this when the agent is asked to design or audit a project |
| `skills/neatnik/RUBRICS.md` | what gets judged. The **judge** loads this, all rules at once |
| `skills/neatnik/MECHANISM.md` | how a case gets presented to the judge: which list to open, what a rejection does, when the loop exits. The judge loads this too — it's two files, not one |
| `agents/neatnik-judge.md` | the judge's system prompt. It runs in a **separate context** |

## The one thing you must not collapse

⚠️ **The judge must not see the builder's reasoning.** If your harness has no way to spawn a
sub-agent with its own context, you can still run Neatnik, but run the judge in a **fresh session**
that receives the artifact, `RUBRICS.md` and `MECHANISM.md`, and nothing else. A judge that reads the
justification isn't a judge; that's the whole mechanism, and everything else is detail.

## Neatnik designs the loop, not just the check

`SKILL.md` step 3 runs a four-parameter loop over every technical choice a project makes: **cheap,
simple, effective, and *sound*** — sound meaning the agentic shape itself follows the field's own
build guidance, judged by a **second, separate judge** that never sees the artifact rubrics, only the
technical choice. `tidy` (below) is the part most people reach for daily; the loop and the two-judge
split are what stop a project from just being one agent that does everything and calls itself done.

## Claude Code

```bash
cp -R skills/neatnik ~/.claude/skills/neatnik
cp agents/neatnik-judge.md ~/.claude/agents/
```

## Anything else

Point the agent at `SKILL.md` and give it a goal. For the judging step, start a clean context with
`agents/neatnik-judge.md` as the system prompt and hand it the artifact plus `RUBRICS.md`.
