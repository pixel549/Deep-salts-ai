# Deep Salts Sim

A persistent, asymmetric-information TTRPG simulation. GM, Player A, and Player B are
separate agents with separate context — no agent sees another agent's private state
unless it's earned in-fiction. State lives in JSON, dice live in Python, every turn
gets committed to git.

Seeded with Maren Solvig (an auditor secretly hunting for her missing brother) and Corwin
Tarrow (a trader who needs primordial-grade salt his granddaughter's illness) as a working
example — see `sessions/session_000.md` for how they were built. Swap `characters/*.json`
and `world/*.json` for your own setup.

## Folder structure

```
world/            public_state.json (everyone knows) + hidden_state.json (GM only: truths + triggers)
characters/       character_a.json, character_b.json — sheets, updated by resolved actions only
memory/
  gm/             gm_memory.md, plus recaps/ and fix_logs/ subfolders
  player_a/       memory.md, plus recaps/ and fix_logs/
  player_b/       same
  dm_review/      God's flag reports + DM's rulings (contains reasoning — DM/God eyes only,
                  agents never read from here directly)
sessions/         append-only session_NNN.md logs — this is the objective "what happened" record
prompts/          system prompts per role
schemas/          JSON schemas enforced via structured outputs on every model call
config/models.json   which Gemini model + API key each role uses — swap models freely for
                      comparison runs, see its "_notes" for per-role key splitting
orchestrator/     the actual game loop, in Python
```

## Setup

1. `pip install -r requirements.txt`
2. Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com/apikey) — no credit card
   needed. Set it locally: `export GEMINI_API_KEY=...`, or add it as a repo secret named
   `GEMINI_API_KEY` (Settings → Secrets and variables → Actions) for GitHub Actions. Never
   commit a key to the repo.
3. `git init && git add -A && git commit -m "seed campaign"` if you haven't already,
   then push to a new GitHub repo.

Gemini's free tier is tracked per Google Cloud project, not per API key — generating more
keys under the same project doesn't get you more quota. If you ever want to split quota
across roles, create keys from separate projects, point a role's `api_key_env` in
`config/models.json` at a new name (e.g. `GEMINI_API_KEY_PLAYER_A`), and add that as a
second GitHub secret. At a several-hours-between-turns cadence you almost certainly don't
need this — one key easily covers it.

## Running it

**Locally**, one call at a time so you can actually watch what happens the first few times:

```
python -m orchestrator.main turn          # runs one full turn (scene -> actions -> resolution)
python -m orchestrator.main end-session    # runs the memory audit, rolls session_number forward
```

**Via GitHub Actions**, this now runs on its own — two scheduled workflows:

- `run_turn.yml` — every 4 hours, runs one turn (~4 API calls)
- `run_session_end.yml` — once daily, runs the memory audit (up to 5 more calls, only if
  there's actually something to adjudicate)

Both also support manual `workflow_dispatch` if you want to trigger one on demand, and
both share a `concurrency` group so they can never run simultaneously and race on the
same state files. Adjust the cron schedules in each workflow file if 4 hours/turn or
once-daily review doesn't match how you want this to run — nothing else needs to change
to adjust the pace.

## The memory-audit flow, in one paragraph

At session end, GM/Player A/Player B each write a private recap. God checks each recap
against the public session log only — flags "confabulation" (contradicts what actually
happened) or "leak" (agent knows something it has no in-fiction way of knowing). God never
flags a belief just for being wrong or for disagreeing with another agent's recap — that's
the asymmetric-information mechanic working as intended, not a bug. DM (full-context GM)
rules on each flag with a plain-assertion `instruction` plus an `internal_reasoning` field;
code strips `internal_reasoning` before anything is written to an agent's folder — that
stripping happens in Python, not by asking a model to politely omit it, so it holds even if
a call misbehaves. Corrections get appended to `memory.md` as a literal text block rather
than having the model "rewrite its memory to incorporate feedback" — letting a model freely
rewrite memory in response to a correction is exactly the failure mode this whole pipeline
exists to catch.

## What I tested, and what I didn't

I mocked every model call end-to-end (schema-shaped fake responses) and confirmed: HP/inventory/
location updates apply correctly, hidden triggers mark as fired, session logs and memory files
write to the right places, and — the part that mattered most — the correction that reached
`player_a`'s memory.md contained only the plain instruction, never the DM's reasoning that
referenced Character B's secret. The plumbing works.

What I have *not* done, because it requires your real API key: an actual live call. First
session, read the output closely before trusting it.

## Known limitations, unforced

- **DM's `instruction` field is a prompt-level trust boundary, not a code-enforced one.**
  Code guarantees `internal_reasoning` never leaks. It can't guarantee the DM never writes a
  leak *into* the instruction text itself. Worth spot-checking `dm_review/` against what
  actually lands in each agent's memory every so often.
- **Structured outputs guarantee shape, not truth.** A schema-valid response can still be a
  confidently wrong one. This doesn't replace reading the sessions.
- **Long-campaign memory drift is still unsolved.** This catches per-session confabulation
  and leaks; it does not compact 40 sessions of accumulated `memory.md` into anything shorter.
  That's a real next problem, not a small one — worth its own design pass before you run this
  for a long stretch.
- **Cost.** Each turn is 4 calls (GM scene, Player A, Player B, GM resolution); each
  session-end is up to 5 more (3 recaps + God + DM, only if something's flagged). Check
  current model pricing before deciding how often to run this.
- **Gemini's free tier trains on your data by default.** Google states free-tier inputs and
  outputs may be used to improve their models, unlike the paid tier. For a fictional TTRPG
  campaign this is probably fine, but it's a real trade-off, not a hidden one — worth knowing
  you're making it.
- **Gemini's model lineup and free-tier rules have been changing fast.** The model names in
  `config/models.json` were current as of when this was built; if a call 404s, check the
  current model list before assuming the code is broken.
- **This now runs unattended, on a schedule, pushing to your repo without a human in the
  loop per-turn.** The `concurrency` group in both workflows stops two runs from racing on
  the same state files, but nothing stops a bad run from committing a bad turn — check in on
  it periodically rather than treating "set and forget" as "never look again."
