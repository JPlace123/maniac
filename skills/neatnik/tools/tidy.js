export const meta = {
  name: 'neatnik-tidy',
  description: 'Before saying «ready»: is every decision the project took really implemented?',
  whenToUse: 'before declaring a piece of work finished. Three levels: low, medium, max',
  phases: [
    { title: 'Read', detail: 'one slice of decisions per agent — all of them, always' },
    { title: 'Attack', detail: 'the full boxes get reopened, and at the max level the holes too' },
    { title: 'Remedy', detail: 'what is mechanical gets closed; what is a choice becomes one line for the owner' },
    { title: 'History', detail: 'one row per round, and that is the curve' },
  ],
}

// ⚠️ THE DIRECTION. You start FROM THE DECISION and look for it in the artifact. The opposite
//    direction — reading the artifact and looking for its decision — finds only what is there, and
//    it is the defect one source calls «saturated eval». Measured on this very method: the «covered»
//    boxes were inflated to 79% when someone went and reopened them.
//
// ⚠️ COVERAGE IS NEVER CUT. All three levels read ALL the decisions on the first pass: what changes
//    is only how hard you attack and how many times you go round again. A level that looks at less
//    is not cheaper, it is more of a liar — «I did not look at it» and «I looked at it and it was
//    fine» look far too much alike.

const A = args || {}
const PROJECT = A.project || process?.cwd?.() || '.'
const SLICES = A.slices || []                  // [{id, where}] — where the decisions are read from
const ARTIFACTS = A.artifacts || []            // the files the decision must have ended up in
// ⚠️ **Every round writes to a folder of its own.** A round's files have the SAME names as the round
//    before (`tidy-CP-p2.md`, `tidy-attack-p3.md`), so staying in the same place makes them fall into
//    the new round's glob and the attacker tears them apart as if they were its own. Measured: at
//    pass 2 of one round the attacker reopened **five** checks, four of which were leftovers from the
//    round before. It does not raise an error — it raises an attack on dead material, and the rate
//    that comes out of it measures nothing about the round that is actually running.
const OUTDIR = A.out || `${PROJECT}/tidy/${A.round || 'round'}`
const HISTORY = A.history || `${PROJECT}/tidy/history.tsv`
// ⚠️ The tools live where the skill lives, which is NOT where the project under check lives: without
//    this line the round looked for `history.py` inside the project and never found it.
const TOOLS = A.tools || `${PROJECT}/tools`
const LEVELS = ['low', 'medium', 'max']
let level = LEVELS.includes(A.level) ? A.level : 'medium'   // ⚠️ with no word said: medium

// floor, ceiling and stopping rule for the sample at the low level
const FLOOR = 8, CEILING = 20, IN_A_ROW = 5
// how many passes at most, because a round that does not converge has to end all the same
const MAX_PASSES = { low: 1, medium: 6, max: 12 }

if (!SLICES.length) {
  log('⛔ no slice of decisions: tidy does not start. It is not an «all clear», it is a check with no list.')
  return { error: 'no slice', read: 0 }
}

const SCHEMA = { type: 'object', required: ['outcome'], properties: { outcome: {
  type: 'object', required: ['file', 'decisions', 'implemented', 'partial', 'absent', 'holes'],
  properties: {
    file: { type: 'string' }, decisions: { type: 'integer' },
    implemented: { type: 'integer' }, partial: { type: 'integer' }, absent: { type: 'integer' },
    holes: { type: 'array', maxItems: 12, items: { type: 'string' },
      description: 'ABSENT and PARTIAL: the decision in one line + where it is written + what is missing in the artifact' },
  } } } }

const SCHEMA_ATT = { type: 'object', required: ['rechecked', 'defective', 'error_rate', 'claims'], properties: {
  rechecked: { type: 'integer' }, defective: { type: 'integer' }, error_rate: { type: 'string' },
  ceiling_reached: { type: 'boolean', description: 'true if I hit the ceiling without ever seeing 5 in a row that hold' },
  claims: { type: 'array', maxItems: 24, items: { type: 'object', required: ['claim', 'verdict'], properties: {
    claim: { type: 'string' }, verdict: { type: 'string', enum: ['HOLDS', 'FALLS', 'DOWNGRADED'] }, line: { type: 'string' } } } } } }

const SCHEMA_REMEDY = { type: 'object', required: ['closed', 'owner_lines'], properties: {
  closed: { type: 'integer', description: 'how many mechanical holes I really closed, with the edit written to disk' },
  not_closed: { type: 'array', maxItems: 20, items: { type: 'string' }, description: 'the ones I left open, and why' },
  owner_lines: { type: 'array', maxItems: 12, items: { type: 'string' },
    description: 'one line for every item that IS A CHOICE, not a mechanical remedy: what it says today, what would change, and the options' } } }

const FORM = `
⚠️ **One line per decision, and ALWAYS in this form** — it is not a style, it is what makes the file
countable by a script:

    **<id> · <title of the decision>** (<where it is written>) — **<BOX>** · <the proof, with file:line>

where <BOX> is exactly one of **IMPLEMENTED · PARTIAL · ABSENT · OUT OF SCOPE**.
⚠️ Measured: the agents change form at every round, and every time the tally loses some of them in
silence — once an entire slice, **88 verdicts written and 0 counted**. Whoever chases the forms loses.

**The delivery IS THE FILE, and it is written AS YOU GO**: create the file **immediately** with the
heading and **append one line for every decision the moment you have decided it**. If the file only
shows up at the end, *«zero bytes»* is the normal state for the whole duration and whoever is watching
**cannot tell «it is working» from «it is dead»**. A file that grows is a heartbeat.`

// ⚠️ **Coverage is never cut: it is NEVER REPEATED.** Two different things, and for twelve passes I
//    confused them: pass 1 reads everything, and the other eleven reread the same 441 decisions from
//    scratch — at the twelfth pass you were paying to re-verify 433 items already confirmed by the
//    first. Measured: **1.15 million tokens per pass**, almost all of it spent re-confirming.
//    From the second pass on you read **the delta**, and the delta is TWO things added together:
//      (a) what FELL at the last attack — declared solid and it was not;
//      (b) what was TOUCHED after that pass had already read it.
//    ⚠️ Without (b), every correction made after the last reading would enter the count as **already
//    verified**: it is the very defect the round exists to find, committed by the round itself.
function delta(items, pass, since) {
  return `Recheck **only what changed or fell**, not everything.${summary}

⚠️ **Why only this, and why it is not a cut in coverage**: the full coverage pass was pass 1. Rereading
everything every time adds nothing and costs everything. Here you look at **the delta**.

**(a) The items that fell or stayed open** (${items.length}), one by one, with the same yardstick as
pass 1 — the box and the proof with \`file:line\`:
${items.slice(0, 30).map((v, i) => `${i + 1}. ${v}`).join('\n')}

**(b) Everything that has been TOUCHED since the previous pass read.** Find it yourself, do not trust a
prepared list:
\`\`\`
find ${ARTIFACTS.map(x => `'${x}'`).join(' ')} -newermt '${since}' -type f 2>/dev/null
\`\`\`
For **every** file that comes out, reread **the decisions that live inside it** and put them back into a
box from scratch. ⚠️ A decision whose proof sits in a changed file **is no longer verified**: the cited
line may have moved, or a remedy may have rewritten the rule.

**The boxes are the same** — IMPLEMENTED · PARTIAL · ABSENT · OUT OF SCOPE — and the same rules as pass
1 apply: \`file:line\` on every line, an ABSENT only after a search that **could have found it**
(\`grep -rniE\`, and the counter-check on a term that must be there).

**The file to write**: \`${OUTDIR}/tidy-delta-p${pass}.md\`
${FORM}

At the bottom: how many items you rechecked, how many are still below 100%, and **which touched files
you found with \`find\`** — if you find zero, say so: it means the remedy wrote nothing.`
}

// ⚠️ **The summary says WHERE to look, never WHAT to conclude.** A summary is the word of whoever
//    wrote it, and this round exists because that word is not enough: whoever reads it reopens the
//    `file:line` anyway. A summary that replaces the reading is the very defect we are hunting for,
//    served on a plate.
function makeSummary(pass, tally, att, rem) {
  return `

**Where you pick up from — summary of pass ${pass}.** ⚠️ **Says where to look, not what to conclude**:
whatever you use from it, you reopen its \`file:line\` — this list is not a proof.
- decisions: ${tally.decisions} · full ${tally.implemented} · half ${tally.partial} · empty ${tally.absent}
- attack: ${att?.defective ?? 0} defective out of ${att?.rechecked ?? 0} reopened
- the remedy closed ${rem?.closed ?? 0} items; the ones still open are below
`
}

function remedy(toClose, pass) {
  return `**Close what is mechanical. Leave standing what is a choice.**${summary}

⚠️ **The line that splits the two, and it is the only one that matters here**: it is **mechanical**
when there is a single correct shape — a pointer to the wrong file, a number that does not match its
own list, a rule written with no step that executes it, two lines saying different things about the
same fact. It is **a choice** when more than one defensible shape exists: dropping or keeping a rule,
changing a threshold, overturning a decision the owner already made. ⚠️ **When in doubt, it is a
choice**: a wrong mechanical remedy goes in silently and stays there.

**The artifacts to correct are EXACTLY these paths**, and no other:
${ARTIFACTS.map(x => `- \`${x}\``).join('\n')}

⚠️ **Write on THESE paths, not on a copy that looks like the same thing.** A method like this one often
lives in two places — where it is written and where it runs — and they are different files with the
same content. Measured: a remedy wrote its correction **only in the copy in service**, and it was not
in the repo: without someone noticing, the first sync would have wiped it out. **If you find two
copies, correct the one listed here and DECLARE the other** among the not-closed items.

Edit them **for real**, on disk: an item declared closed and not written is worse than one left open.

**What to close** (${toClose.length} items, from pass ${pass}):
${toClose.slice(0, 24).map((b, i) => `${i + 1}. ${b}`).join('\n')}

⚠️ **And after every correction look at the NEW lines, not only the one you touched.** Measured twice
on the same object: a correction applied **in one place out of five**, with the other four lines still
saying the old thing — and two checks citing them as proof **without seeing the contradiction**. A
remedy that opens another one counts as not done.

⚠️ **Do not touch what is a choice.** For each one write a line for the owner: **what it says today ·
what would change · the options.** Do not decide in their place and do not leave it half-done.`
}

function reading(s, pass) {
  return `Check **which decisions of the project really ended up in the artifact, and which did not**.

**The direction**: you start **FROM THE DECISION** and look for it in the artifact. Never the other
way round: reading the artifact and looking for its decision **finds only what is there**.

**Your slice of decisions**: ${s.where}

**Where it must have ended up** — and you look at **all** of them, not only the one that looks right:
${ARTIFACTS.map(x => `- \`${x}\``).join('\n')}

**The boxes are three plus one**:
- **IMPLEMENTED** — it is there, and the line says **who does what and when**.
- **PARTIAL** — the name or half the rule is there, but **not the step that puts it into operation**.
  ⚠️ Without this box everything turns into *«it is there»*, and **the dominant defect is exactly here**.
- **ABSENT** — it is in none of the files. ⚠️ Before writing it, **search across all the artifacts** and
  report the command: an ABSENT with no search is an absence deduced, not measured.
  ⚠️ **And the command must be able to FIND it**, or it proves nothing. Measured defect: more than one
  check tried to prove an absence with \`grep -rn "a|b|c"\` — **without \`-E\` the \`|\` is a literal
  character**, the search looks for the string \`a|b|c\` and returns **0 on any corpus**. A zero that
  could not have been anything else is not a proof, it is a broken command that looks like one. **Use
  \`grep -rniE\`**, and before trusting a zero run the counter-check: **the same search on a term that
  MUST be there**. If that also comes back zero, the broken thing is the command.
- **OUT OF SCOPE** — it was not meant to enter the artifact (it is project material, not a rule the
  artifact executes). **You write it down and it does not count as a hole.**

**Rules**: every line carries \`file:line\` · the guillemets «» only for literal quotations · a piece
of data you did not find is reported as **NOT SEARCHED**, never as absent.

⚠️ **Before you start, note the time and the size of every artifact; redo it at the end.** If something
changed while you were reading, **say so at the top of the file**: *«the artifact changed during the
check, the pointers hold for the version as of HH:MM»*. Measured: a round that read while someone was
correcting produced **whole blocks of off-by-one findings** — true as observation, useless as work, and
indistinguishable from real defects to whoever reads the delivery.

**The file to write**: \`${OUTDIR}/tidy-${s.id}-p${pass}.md\`
${FORM}

At the bottom, when you are done: the list of the ABSENT and the PARTIAL ones.`
}

function attack(holes, pass, attackHoles) {
  const oldSample = pass > 1 ? `

**(1b) Plus a fixed handful: ${OLD_SAMPLE_SIZE} boxes already confirmed in earlier passes**, picked at
random among the ones this pass did NOT touch. ⚠️ **Not zeal: a box confirmed at pass 1 can stop being
true** if a remedy from a later pass moved the line that proved it, and without this handful **nobody
would ever look at it again**. The number is fixed on purpose: that way one pass's rate can sit in the
same column as the pass before's.` : ''

  const sample = level === 'low'
    ? `**Reopen the IMPLEMENTED boxes one at a time, and STOP WHEN ${IN_A_ROW} IN A ROW HOLD.**
Minimum ${FLOOR}, maximum ${CEILING}. ⚠️ **The condition for stopping is finding it clean, not having
found enough**: that way digging does not pay, and it is the defence against the round that invents
work to justify itself. If you get to ${CEILING} **without** ever having seen ${IN_A_ROW} in a row that
hold, **do not insist**: set \`ceiling_reached: true\` and stop — it means the count is too inflated for
a low level, and the round will raise its own level.`
    : `**Reopen ALL the IMPLEMENTED boxes.** Not a sample: all of them.`

  const onHoles = level === 'max' && attackHoles && holes.length
    ? `

**(2) The declared holes — reopen them and look for the OPPOSITE**: does something exist somewhere in
the artifacts that covers them and that the check did not find? ⚠️ Measured: **9 holes out of 22 were
not holes.** The two extreme columns are inflated in opposite directions, and whoever checks only one
of them takes home a number that is wrong in one direction only.
${holes.slice(0, 14).map((b, i) => `${i + 1}. ${b}`).join('\n')}`
    : ''

  return `Your mandate is to **TAKE APART**, not to confirm.${summary}

**The artifacts to attack**: \`${OUTDIR}/tidy-*-p${pass}.md\` — the checks that declare which decisions
ended up in the artifact and which did not.

**(1) The IMPLEMENTED boxes of THIS pass.** ${sample}${oldSample}

For each one go to the \`file:line\` that is cited and ask: does that line **really put the decision
into operation**, or does it **only name the concept**? A line that says *what must be true* without
saying **who does it and when** is a PARTIAL in disguise, and it is the most expensive defect
**because it closes the search on top of a hole**. ⚠️ Measured: out of 42 boxes reopened, **33 did not
hold**.

⚠️ **The defect that survives the longest, and has to be hunted by name: THE RULE IS WRITTEN AND NO
STEP EXECUTES IT.** It survives because \`grep\` finds it. The signs: a file **no step opens**, a line
with no subject, a pointer to a section that does not describe what it promises.${onHoles}

⚠️ When the thesis is an **absence**, a \`grep\` that finds nothing **is** the proof: run it and write
the command. Demanding a line that proves an absence pushes people to invent one.

**Delivery — one file**: \`${OUTDIR}/tidy-attack-p${pass}.md\`, one line per claim, and at the bottom
\`rechecked N, defective M, error rate X%\`.`
}

// ── the round ─────────────────────────────────────────────────────────────────
const history = []
let pass = 0, raised = null, rem = null
// ⚠️ There is no clock inside the round's scripts: the caller passes the date, in `args.now`. Without
//    it, the delta pass's `find -newermt` has no «since when» and looks at everything.
//    ⚠️ **Declared ceiling**: with no clock, this «since when» does **not** move forward between
//    passes — it stays the instant the round started. So from the third pass on, `find` is
//    **over-inclusive**: it also finds what the previous pass's remedy had already made you recheck.
//    It is the right direction of error — **rechecking twice costs, missing a change lies** — but it
//    has to be said instead of letting people believe the window narrows.
const clock = () => A.now || '2000-01-01'
let lastRead = clock()
let toRecheck = []
// ⚠️ The acceptance threshold. «Hands entirely empty» is unreachable by construction: the attacker
//    ALWAYS finds something non-blocking, because that is its job. A threshold nobody can ever meet
//    is not rigour, it is a round that never ends — measured: twelve passes without ever stopping,
//    and it was the ceiling that stopped it, not cleanliness.
const CLEAN_IN_A_ROW = 2, ACCEPTED_RATE = 10
let clean = 0
// ⚠️ Fixed, not a quota: a count that changes every pass makes the rates incomparable, and the curve
//    — the whole reason the history exists — stops saying anything.
const OLD_SAMPLE_SIZE = 8
// what the remedy declares «is a choice» LEAVES the round and becomes a line for the owner
let forOwner = []
let summary = ''

while (pass < MAX_PASSES[level]) {
  pass++
  phase('Read')

  // ⚠️ A single agent on the delta, not four: slices are for splitting a LARGE corpus, and the delta
  //    is not large. Four agents on thirty items is three contexts paid for and unused.
  const outcomes = pass === 1
    ? (await parallel(SLICES.map(s => () =>
        agent(reading(s, pass), { label: `reads:${s.id}·p1`, phase: 'Read', schema: SCHEMA })
      ))).filter(Boolean).filter(e => e.outcome)
    : [await agent(delta(toRecheck, pass, lastRead), { label: `delta·p${pass}`, phase: 'Read', schema: SCHEMA })]
        .filter(Boolean).filter(e => e && e.outcome)
  lastRead = clock()

  if (!outcomes.length) {
    log('⛔ no slice delivered: the round did NOT happen. It is not a «no hole».')
    return { error: 'no delivery', pass, level }
  }

  const sum = k => outcomes.reduce((a, e) => a + (e.outcome[k] || 0), 0)
  const holes = outcomes.flatMap(e => e.outcome.holes || [])
  const tally = { decisions: sum('decisions'), implemented: sum('implemented'),
                  partial: sum('partial'), absent: sum('absent') }

  // ⚠️ Holes are attacked on the FIRST pass and the LAST, not on every round. First, because if a
  //    third of the holes are not holes the remedy spends three passes chasing work that does not
  //    exist. Last, because it is the certification. In between you would be attacking holes the
  //    remedy is still busy closing.
  const blockingNow = tally.partial + tally.absent
  const attackHoles = pass === 1 || blockingNow === 0 || pass >= MAX_PASSES[level]
  phase('Attack')
  const att = await agent(attack(holes, pass, attackHoles), { label: `attacks·p${pass}`, phase: 'Attack', schema: SCHEMA_ATT })

  // ⚠️ The ceiling does not limit the search: it says «this is no longer a low level» and hands over.
  //    Going up is automatic and needs no reason; going down would need a written line (and here it
  //    never happens).
  if (level === 'low' && att?.ceiling_reached) {
    raised = `at the ceiling of ${CEILING} without ${IN_A_ROW} clean in a row: the count is too inflated for a low level`
    level = 'medium'
    log(`⬆️  going up to medium — ${raised}`)
    history.push({ pass, level: 'low', ...tally, attack: att, raised })
    continue
  }

  const alive = (att?.claims || []).filter(a => a.verdict !== 'HOLDS')
  history.push({ pass, level, ...tally, attack: att })

  // ⚠️ THE PHASE THAT WAS MISSING, and its absence was the very signature this tool exists to catch:
  //    the prose said «tidy fixes what is mechanical and reruns to show it closed», and the round
  //    reread an UNCHANGED artifact — so the next pass found the same holes and the loop could not
  //    converge. A rerun with no remedy in between is not a second check: it is the same check twice.
  const toClose = [...holes, ...alive.map(a => `${a.claim} — ${a.line || ''}`)]
  if (toClose.length && (level === 'medium' || level === 'max')) {
    phase('Remedy')
    rem = await agent(remedy(toClose, pass), { label: `remedy·p${pass}`, phase: 'Remedy', schema: SCHEMA_REMEDY })
    // ⚠️ Choices LEAVE the round: they belong to the owner, not the round. Keeping them in does not
    //    move them forward an inch, and meanwhile it **inflates the count of open items**, so the
    //    «two clean passes in a row» threshold never fires because of stuff waiting on the owner.
    forOwner = forOwner.concat(rem?.owner_lines || [])
    log(`p${pass} · closed ${rem?.closed ?? 0} · sent to the owner ${rem?.owner_lines?.length ?? 0} (total ${forOwner.length})`)
  }
  log(`p${pass} · ${tally.decisions} decisions · ${tally.implemented} full · ${tally.partial} half · ${tally.absent} empty · ${alive.length} claims still standing`)

  const blocking = blockingNow                            // ⚠️ blocking = everything that is not at 100%
  // the rate is ALWAYS read with its denominator: «42%» on 73 reopened boxes and «12%» on 426 do NOT
  // belong in the same column; lining them up tells a curve that does not exist.
  const rate = att?.rechecked ? (att.defective / att.rechecked) * 100 : 0
  const isClean = blocking === 0 && rate < ACCEPTED_RATE
  clean = isClean ? clean + 1 : 0
  log(`p${pass} · blocking ${blocking} · attack ${att?.defective ?? 0}/${att?.rechecked ?? 0} = ${rate.toFixed(1)}% · clean in a row ${clean}/${CLEAN_IN_A_ROW}`)

  // ⚠️ The delta of the NEXT pass: what fell plus what is still open. What has been touched is found
  //    by the pass itself with `find`, because a list compiled here would forget the files a remedy
  //    changed without saying so.
  toRecheck = [...holes, ...alive.map(a => `${a.claim} — ${a.line || ''}`),
               ...(rem?.not_closed || [])]
  summary = makeSummary(pass, tally, att, rem)

  if (level === 'low') break                              // a single pass, and it cannot say «complete»
  if (level === 'medium' && blocking === 0) break         // it stops on the blocking ones
  if (level === 'max' && clean >= CLEAN_IN_A_ROW) break   // ⚠️ two clean passes in a row, not the empty hand
}

// ⚠️ **A ceiling that cuts things off in silence reads as «it finished».** If the round exits because
//    it ran out of passes — not because it found things clean — that has to be said, or the delivery
//    looks in every way like a successful one. It is the rule «no silent ceiling» applied to whoever
//    writes it.
const byCeiling = history.length >= MAX_PASSES[level] &&
  (history[history.length - 1].partial + history[history.length - 1].absent) > 0
if (byCeiling) log(`⛔ stopped by the ${MAX_PASSES[level]}-pass ceiling, NOT because it was clean: ${history[history.length - 1].partial + history[history.length - 1].absent} decisions remain below 100%`)

const last = history[history.length - 1]
const row = [
  `level=${level}`, `passes=${history.length}`,
  `decisions=${last.decisions}`, `full=${last.implemented}`,
  `half=${last.partial}`, `empty=${last.absent}`,
  `reopened=${last.attack?.rechecked ?? 0}`, `defective=${last.attack?.defective ?? 0}`,
].join('\t')

phase('History')
await agent(`Redo the count **from the files**, then append **one single row** to the history and show
me the curve.

⚠️ **The first two commands exist because this round's count comes from what the agents DECLARE**, and
it has to be checked against what they actually WROTE. If the two numbers do not match, the good one is
the second — it has already happened once: an entire slice with **88 verdicts written and 0 counted**.

\`\`\`
TIDY_TSV=${OUTDIR}/coverage.tsv python3 ${TOOLS}/inventory.py ${OUTDIR}/tidy-*-p${history.length}.md
TIDY_TSV=${OUTDIR}/coverage.tsv python3 ${TOOLS}/coverage.py
python3 ${TOOLS}/history.py --file ${HISTORY} --append "${row}"
python3 ${TOOLS}/history.py --file ${HISTORY} --curve
\`\`\`

⚠️ \`coverage.py\` exits **2** if the inventory is too small: **that is not «all clear»**, it is a check
that read nothing — report it as it is instead of ignoring it.

Delivery: the last lines of the curve, exactly as the tool prints them. Do not comment on them.`,
  { label: 'history', phase: 'History' })

// ⚠️ The low level CANNOT say «complete»: its attack is a sample, and the historical error rate on
//    these boxes is high. Saying «complete» on a thin base is the worst false ok there is.
const complete = level !== 'low' && last.partial === 0 && last.absent === 0

return {
  level, passes: history.length, raised_level: raised,
  tally: { decisions: last.decisions, implemented: last.implemented,
           partial: last.partial, absent: last.absent },
  attack: last.attack ? `${last.attack.rechecked} reopened, ${last.attack.defective} defective (${last.attack.error_rate})` : '⚠️ NO ATTACK',
  live_claims: (last.attack?.claims || []).filter(a => a.verdict !== 'HOLDS'),
  owner_lines: forOwner,
  not_closed: rem?.not_closed || [],
  stopped_by_ceiling: byCeiling || undefined,
  verdict: byCeiling
    ? `⚠️ STOPPED BY THE ${MAX_PASSES[level]}-PASS CEILING, not because it was clean — this is not a successful delivery`
    : complete
    ? 'READY — no decision below 100%'
    : level === 'low'
      ? '⚠️ I DO NOT SAY «COMPLETE»: level low, the attack is a sample and the historical error rate on these boxes is high'
      : '⚠️ NOT READY — decisions below 100% remain',
  history,
}
