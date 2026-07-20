# THE DEEP SALTS
**A horror exploration RPG**

System-agnostic ruleset (d20 base) for solo play with an AI DM. You trade humanity for power, and only see the trade once you've gone mad enough to look.

*Version 8.0 — full lean rewrite. All mechanics from v7.3 preserved; session-attribution history, rationale prose, and the redundant Quick Reference section (superseded by making the whole document reference-density) have been cut. Full change history lives in the dev log.*

---

## 1. The Premise

Salts dissolved in hot water transport you to another plane. Fight through, gather loot/materials/knowledge. Each area has a clean chalice (the anchor) — drink to wake at Stillwell Hydro with everything from that run, banked. Near death, focus your mind to exit immediately, losing everything on your person; retrieve it by re-entering the same recipe and beating the enemy that has it.

**Core loop:** brew a recipe → wake in that biome, blind → survive → return to the anchor and leave (or die, or bail) → bank at the hub → push deeper or brew elsewhere. No fast travel — the recipe is the travel (§18).

---

## 2. Running This With an AI DM

- Never explain the world fully. Let the player infer; answer lore questions in-fiction through an unreliable source, or not at all.
- Describe, don't signpost. No quest markers.
- Consistent hub, inconsistent everywhere else (§14).
- Track status, Insight, limbs, Salts, and inventory turn to turn. Surface when relevant; don't recite.
- Generate monsters live from the archetype table (§16), scaled to level (§17), never below the Damage Floor (§4), then record the filled Monster Template. Live generation is for first contact; the manual is canon after.
- Honour tells — parry/precision only work if a readable tell reliably precedes the attack.
- One recurring antagonist NPC, reappearing across warped locations, always slightly changed, never helpful (§14).
- Plain attacks to 0 HP always kill, on everything including bosses. Sever is a bonus fast-lane for high-HP fights, never a requirement — a basic mook should die to a few solid hits.
- **Verify before asserting.** If a named entity, item, rule, or number comes up that isn't already visible in this conversation, stop and check the actual repo files before stating anything — never rely on memory or invent a plausible value. If nothing exists, say so; don't fabricate an entry.

---

## 3. Core Resolution

d20 + modifier vs a DC. **Default attacks land** — no attack roll, either side. Rolls/stopwatches only for:

- **Called shots** on limbs with multiplier >1.0 → Precision stopwatch (§10), unless already parry-opened (§9).
- **Parries** and the heavies that invite them → Visceral stopwatch (§9).
- **Insanity/Influence saves** → d20 vs the Save Roll formula (§5).
- **Anything genuinely uncertain** (stealth, forcing a door, reading the unreadable) → d20 vs DC, modified by the Attribute Modifier table:

| Attribute score | Modifier |
|---|---|
| 0–1 | −3 |
| 2–4 | −2 |
| 5–9 | −1 |
| 10–19 | +0 |
| 20–39 | +1 |
| 40–79 | +2 |
| 80–99 | +3 |

(Doesn't apply to the Save Roll formula, §5 — that has its own scaling. Perks may stack extra situational bonuses on top.)

Enemy basic attacks land the same way — no enemy to-hit roll, defense is entirely the player's via timing/positioning/range.

**0 HP always kills** — mooks or bosses. Sever kills regardless of remaining HP and is the faster route once a pool would otherwise drag; it's never required.

---

## 4. Character Creation & Progression

### Backstory-Negotiated Creation

Player writes a short concept; DM negotiates the mechanical translation:
- **Attribute reallocation** — default flat 8×5 (40 total). A strong concept can redistribute unevenly; total stays 40 unless both sides agree it earns more.
- **A bespoke starting weapon** instead of the weapon table — type, governing stat, base damage placed in-range for the concept (never under the Damage Floor), one signature gimmick that costs something for something. Any risk/reward on the gimmick uses existing tools (stopwatch or d20), never a new resolution system.

### Attributes

Five buyable; Insight is separate, earned not bought (§11).

- **VIGOR** → max HP, Blood Loss resilience
- **ENDURANCE** → movement budget
- **STRENGTH** → heavy weapon damage, sever power
- **SKILL** → light weapon damage, parry/precision tolerance
- **RESOLVE** → Insanity/Influence saves

All start 8, cap 99. Starting Insight = 1.

**Derived stats:**
- Max HP = 60 + (Vigor × 6) → Vig 8 = 108, Vig 99 = 654
- Movement budget = 8 + ⌊Endurance ÷ 15⌋ m → End 8 = 8m, End 99 = 14m
- Insanity/Influence save bonus = ⌊Resolve ÷ 10⌋ → Resolve 8 = +0, Resolve 99 = +9

### Effective Scaling Value (ESV) — soft caps

Weapon/combat scaling uses ESV, not raw score:

| Score range | Each point worth |
|---|---|
| 1–20 | ×1.0 |
| 21–40 | ×0.65 |
| 41–60 | ×0.4 |
| 61–80 | ×0.2 |
| 81–99 | ×0.1 |

99 → ESV ~47. Smart stop is usually 40–60.

### White Salts

- **Purse** — earned this run, at risk. **Vault** — banked at hub, permanently safe.
- Hub arrival moves full Purse → Vault. Abandon-All, Retreat, Death (§12) only ever touch the Purse.
- Spend Vault Salts on attribute levels.

### Leveling

Level = total attribute points spent, lifetime. Cap 100. Cost of next point = 25 × current level.

| Checkpoint | Cumulative spent | Next point costs |
|---|---|---|
| Lvl 10 | 1,125 | 250 |
| Lvl 25 | 7,500 | 625 |
| Lvl 50 | 30,625 | 1,250 |
| Lvl 75 | 69,375 | 1,875 |
| Lvl 100 | 123,750 | 2,475 (final) |

### Perks — at 20/40/60/80/99 per stat

Granted per points invested in that specific stat.

**VIGOR**
- 20 *Resist Rupture:* rupture damage −25%.
- 40 *Second Wind:* once/hub cycle, a hit that would drop you to 0 leaves you at 1, clears one track.
- 60 *Thick Hide:* flat −2 damage on all incoming hits.
- 80 *Iron Lungs:* immune to Burning spread (direct Burning still applies).
- 99 *Unbreaking:* once/encounter, a rupture leaves you at 1 HP instead of resolving in full.

**ENDURANCE**
- 20 *Light Foot:* moving right after an attack costs 1m less.
- 40 *Overcharge:* **placeholder, needs sign-off** — orphaned by charge removal (§9). Proposed: a whiffed parry, once/encounter, becomes a chip hit instead of full whiff punishment.
- 60 *Quick Recovery:* track management becomes a Fast Action.
- 80 *Outrunner:* movement budget never drops below half, regardless of leg damage.
- 99 *Endless:* **placeholder, needs sign-off** — orphaned by charge removal. Proposed: once/encounter, immediately retry a failed stopwatch check with no whiff punishment.

**STRENGTH**
- 20 *Heavy Hand:* raw damage counts +5 solely for sever-threshold checks.
- 40 *Brute Force:* charged heavies treat boss stagger meters one tier lower.
- 60 *Render:* a successful sever dumps bonus stagger damage onto an adjacent limb.
- 80 *Executioner:* sever attempts vs a staggered target +10% raw damage.
- 99 *Annihilate:* once/encounter, declare a heavy an automatic sever if it meets the threshold — no precision check.

**SKILL**
- 20 *Steady Hand:* all precision windows widen +0.02s flat.
- 40 *Featherstep:* first Assess each turn costs 0 movement.
- 60 *Riposte:* a successful parry grants a free light attack before the visceral resolves.
- 80 *Untouchable:* missed-precision punishments reduced one band.
- 99 *Perfect Read:* once/encounter, auto-succeed one stopwatch check.

**RESOLVE**
- 20 *Iron Will:* reroll a failed Insanity save once.
- 40 *Unshaken:* Influence command duration −1 round.
- 60 *Clear Mind:* once/encounter, clear Insanity to 0.
- 80 *Silence the Hum:* immune to passive/ambient Influence (direct spoken commands still land).
- 99 *Indomitable:* on a failed Insanity save, act with disadvantage instead of losing control.

### Weapons

**Damage = Base + (ESV × grade).** Heavy ≈ 2×Base + ESV×grade×1.5. Grades: E ×0.3 · D ×0.5 · C ×0.7 · B ×0.9 · A ×1.1 · S ×1.3. **Fractional results round up** (session 6 ruling — applies to this formula throughout, not just Fists).

| Weapon | Type | Stat/Grade | Two-handed? | Gimmick |
|---|---|---|---|---|
| Tideglass Cleaver | Quick | Skill/C | Optional | Light swings twice, 2nd hit reduced |
| Cautery Saw | Heavy | Strength/B | Yes | Slow huge hits — best raw sever weapon |
| Birthing Hook | Reach | Skill/C | Optional | Wide sweeps; strong vs multiple limbs |
| Funicular Spike | Reach/thrust | Strength/B | Yes | Bonus dmg vs staggered targets |
| Brass Token Press | Trick | Skill↔Strength | Switches | Folds Quick/Heavy; full transform gated Insight Tier 1 |
| Fists (unarmed) | Quick | Skill/E | N/A | No gimmick, no ammo. Base 10 — deliberate sub-floor exception (session 6 ruling); never sever-capable, full stop, as the tradeoff. |

*Worked example — Cautery Saw heavy, base 30: Str 8→ESV 8→~71 dmg. Str 40→ESV 33→~105. Str 99→ESV ~47→~123, past the head's 120-raw sever line (§10).*

### Damage Floor & Scale

**20 is the practical floor** for any base number passing through a multiplier (weapon bases, enemy damage, DM-generated numbers) — keeps multiplier results whole and ensures even weak weapons can eventually sever. Doesn't bind flat unmodified numbers (Quick Item heals, status ticks).

Enemy HP/thresholds scale to match: archetype band × level multiplier (§17), attack damage proportionate to what Max HP and Rally (§6) absorb.

---

## 5. Status Tracks

Most conditions are tracks, 0–10, building rather than switching.

**BLOOD LOSS** — +1 stack per qualifying hit/hazard. Each new stack deals immediate bonus damage = new stack total (1st cut +1, 5th +5). No passive drain. Cap 10 → Rupture, resets to 0. Clear: bandage/cautery/pressure action (Wrap clears 2).

**RUPTURE** (triggered @ Blood Loss 10) — 25% Max HP direct damage, staggers a beat, resets Blood Loss to 0.

**INSANITY** — on taking damage / witnessing something wrong / failing a fear save: Save Roll (below). Fail → DM controls you one turn.

**BREAK** (triggered @ Insanity 10, automatic, no roll) — Insanity resets to 0. In exchange:
- **Blackout:** DM full narrative control, 3 turns. Broken World scene — false tells, fake Influence commands, wrong layouts, plus a hallucinated threat that deals real damage (floor 20).
- **Scar:** permanent trait attaches when the blackout ends — upside + downside, contextual to what triggered the Break (same shape as Corrupted Regrowth, §10). Full trade legible only at sufficient Insight. Scars stack uncapped.
- **Removal:** only via the Memory Vendor (design bible), Insight-priced, escalating: Scar 1 = 6 Insight, Scar 2 = 10, Scar 3+ = higher.

**BURNING** — ticking damage/turn, spreads to oil/cloth/steam-soaked surfaces. Smother = an action.

**DISCOMBOBULATION** — a Tick, not a track. Applied 1–3 by severity, counts down 1/turn automatically. While active: DM may misdescribe exits, reverse movement, strip reactions, scramble attack directions. Fresh application refreshes to the higher value. Cap 3. (Long-term cousin: Fugue, §13, a Track not a Tick.)

**INFLUENCE** — builds like Blood Loss but uncapped past 10, no overflow trigger. Compelled-effect severity scales with stack count, DM discretion (low = lingering/minor compulsion, high = dropping a weapon, fleeing, self-harm, striking an ally). Fail a save → obey the effect next turn.
- First save triggers at stack 2.
- A successful resist doesn't clear the stack while the source stays active — only full source elimination clears it (line of sight fully broken). Multiple simultaneous sources: ALL must be eliminated.
- A failed Influence save ticks Insanity only once the Influence stack is 3+.
- **Enemy-side Influence (session 6 ruling, v2 — revised same session):** enemies don't have a compel/save loop, so severity scales behaviorally instead of via a save, shaped like Blood Loss/Rupture (reuse, not a new system):

| Stack | Effect |
|---|---|
| 1–2 | Flavor only — restless, muttering, no mechanical change |
| 3–4 | 50% chance/turn: attacks the nearest creature (ally or Lloyd) instead of its declared target |
| 5–7 | Always redirects to the nearest creature instead — real damage, using its own normal attack numbers |
| 8–9 | As above, +50% damage on the redirected attack — fury bonus |
| 10 (cap) | **Overload Rupture:** 25% of that creature's Max HP as direct damage, staggers a beat, resets stack to 0. Can repeat as it re-climbs. |

Applies to bosses too — a boss with no attack to redirect (The Singer) skips the 3–9 tiers functionally but still hits Overload Rupture at cap, same 25%-Max-HP math, repeatable. This is what actually turns a congregation on itself and can wear a boss down passively, not the old flat-20/turn version (superseded, same session).
- **The Beckoner's residual Influence (session 6 clarification):** unlike normal Influence sources, stacks Lloyd picks up from the Beckoner become a **sticky baseline** — wrapping it or breaking distance stops *new* accumulation but does NOT clear what's already stuck (overrides the normal "source eliminated" clear for this item specifically). Clears only via a full rest/sleep cycle, or fully divesting the item (leaving it behind entirely, not just wrapped and carried). While a baseline is active, any new Influence-inducing encounter starts Lloyd's stack at that baseline instead of 0.

**CORROSION** — damage at start of your turn = stacks × 2. Cap 5 (10/turn). Ticks down 1 at end of turn only if you spent an action managing it; otherwise holds. Stacks viciously with Burning.

### The Save Roll (Insanity & Influence)

**Succeed on d20 ≥ 10 + (current track value) − ⌊Resolve÷10⌋ + ⌊Insight÷2⌋** (+ situational mods).

*Worked example: Resolve 8, Insight 1, 2nd Influence stack → 10+2−0+0 = 12. Later: Resolve 30, Insight 6, Influence 6 → 10+6−3+3 = 16.*

---

## 6. Rally

Damage taken becomes recoverable grey health. Land a qualifying hit on your very next turn to claw back a portion, or it fades.

- Default: 50% recovered.
- Big telegraphed boss haymakers: 75–100%.
- Chip/DoT (Burning, Corrosion, rupture): 0–25%.
- Set per-attack; overrides noted on the attack's own entry.

---

## 7. Movement & Positioning

Budget set by Endurance (8–14m) — the single per-turn currency; repositioning and actions both draw from it. Spend before/after your action up to the total minus the action's own cost (§8).

**Hard rule:** can't pay an action's movement cost → can't take it.

- **Hit-and-run** — attack and retreat beyond reach in one turn. No parry, no opening. Safe, slow, low-reward.
- **Kiting** — if your budget exceeds theirs, stay out of reach and chip.
- **Burst-movers** — some alternate a surge turn (huge ground, attacks only at the lunge's end) with a recovery turn. In during recovery, out before the surge.

**The triangle:** Trade (stand and swing — fast damage, eat hits) / Parry (high risk, high reward) / Kite (safe, slow, no openings). Good play flows between all three.

---

## 8. Action Economy & Items

**Movement** — your budget, splittable around your Action.

**Action** (one/turn, costs movement):

| Action | Movement cost |
|---|---|
| Light attack | 1m |
| Heavy attack | 3m |
| Hold (parry stance) | 2m |
| Manage a track | 1m |
| Use an Action Item | 2m |
| Assess | 1m |

Specific weapons/actions may price differently; perks may refund/grant/zero costs.

**Fast Action** (one/turn, always 0m):
- Use a Quick Item, load a capsule.
- Swap between two already-equipped weapons/options.

Quick Items are Fast Actions (vial-and-swing works); Action Items are strong but cost the whole turn.

**Reactions** sit outside all pools. Abandon-All lives here; Retreat cannot be used in active combat at all (§12).

### Limb-gating

| Requires | Staggered | Severed |
|---|---|---|
| Weapon arm | −1 die / heavies disabled this turn | Can't wield that side; off-hand only, two-handers unusable |
| Legs | Budget halved | Crawl only (1m), no kiting, prone (standing costs your Action) |
| Head | Dazed — Discombobulation 1 turn, can't Assess | Dead |
| Torso | n/a — stagger is just heavy damage | Dead |

### Items

**Durability tags** — every item carries exactly one:
- **Constant** — persists indefinitely (per-use costs still apply).
- **Hub Kit** — recharges/resets free on every hub return.
- **Uses: [N]** — works N times then spent, not hub-refilled.
- **Instance-specific** — can't leave the layout it was found in; expires with the instance (§18).

**Quick Items** (Fast Action):
- Wrap — clears 2 Blood Loss
- Camphor — clears 2 Insanity
- Tonic — small flat heal (~10% max HP)
- Scour — clears 1 Corrosion, no turn cost

**Action Items** (full Action):
- Source-water flask — big heal, adds 1 Influence stack. (Uses: 1 per flask.)
- Cautery iron — fully clears Blood Loss; costs full remaining movement budget on use. (Constant.)
- Thrown vial — Corrosion/Burning at range. (Uses: 1 per vial.)
- Charm — one-shot buff (extra die, widened parry window), Insight-gated. (Uses: 1.)

**Reactive/Instant** (no slot, usable anytime): Abandon-All (§12); distress flare/ally beacon (multiplayer hook, unbuilt).

**Passive/Equip** (no slot, always active): trinkets/build-around gear, often Insight-tier-gated.

---

## 9. The Visceral System (parry + stopwatch)

Needs a stopwatch.

**Assess** (1m): reveals an enemy's tell and rough timing of its next heavy, clarity scaling with Insight. You can then Hold to parry on its turn.

**The parry:**
1. Enemy telegraphs a heavy — target time + tolerance (e.g. Lunge 1.50s ±0.20 · Overhead 2.00s ±0.15 · Sweep 1.20s ±0.25).
2. Start the stopwatch — no charge cost, no attempt cap.
3. Pause inside the window.

**Outcomes:**
- **Inside → PARRY.** Enemy opened; next strike deals 1.5× (plus Insight mods), knocks it down, ends its turn, costs it movement.
- **Outside → WHIFF.** Eat the heavy in full plus a punish (DM's pick). Don't reuse a tell.

Insight widens windows and unlocks visceral mods (§11): Bloody, Sustaining, Quickening.

### Post-parry weak points — three tiers

- **Tier 1 — Open** (default, mooks/elites). Parry floors them; weak point's yours, no second stopwatch.
- **Tier 2 — Widened** (some bosses). Opened but not floored. Precision window (§10), widened one tier.
- **Tier 3 — Full double** (bosses, chaotic limbs). Parry stopwatch, then a full second precision stopwatch.

**Table fallback:** replace any stopwatch with d20 + Insight-as-modifier, same outcomes.

---

## 10. Limbs, Precision & Mutation

Every enemy still dies the ordinary way — plain attacks chip HP, 0 HP is dead. Everything below is an *additional*, faster route on tougher enemies.

### The limb model

Standard humanoid:

| Limb | Multiplier | Stagger threshold |
|---|---|---|
| Head | ×1.5 | 180 |
| Torso | ×1.0 | 800 |
| Arm (each) | ×0.65 | 200 |
| Leg (each) | ×0.75 | 300 |

- Effective damage = raw × multiplier — chips HP AND fills the limb's stagger meter.
- Threshold over several hits → **STAGGER** (limb goes limp). The hit that crosses it grants an immediate free called shot, same action. Player stagger duration: fixed 1 turn. Enemy stagger duration: variable, set per Monster Template.
- Threshold in one hit → **SEVER** (permanent). Severing torso/head kills regardless of remaining HP.
- No free called shots on a standing, alert, unstaggered enemy — needs an opening (stagger/knockdown/off-balance/parry) or takes a penalty. Default swings land torso.
- Small high-value targets (bell, crack, eye) are just non-standard limb entries with a high multiplier, using Sever only (no partial "stagger" state for an object).

*Worked example: leg (×0.75, 300) needs 400 raw in one hit to sever. Head (×1.5, 180) needs 120 raw.*

**Standard humanoid thresholds are fixed constants, never level-scaled.** Only HP scales, so raw damage climbing over time makes one-hit sever increasingly viable: head sever starts ~raw Str 60–80 with a real sever weapon. Arms (~308 raw) and legs (400 raw) stay out of one-hit reach even at 99 — staggered, not severed.

**Bosses get hand-set limb values** on their own Monster Template — high enough that clearing a weak point in one hit takes real specialization.

### Precision Strike — the greedy-target tax

Targeting a limb multiplier >1.0 triggers a precision stopwatch (at/below 1.0 — never affected):

| Multiplier | Tolerance (±) |
|---|---|
| 1.01–1.25 | ±0.25s |
| 1.26–1.50 (head) | ±0.13s |
| 1.51–1.75 | ±0.09s |
| 1.76–2.00 | ±0.06s |
| 2.01+ | ±0.04s |

Target time DM-set per opening (default ~1.50s, range 1.0–2.0s). Miss punishments scale with greed:

| Band | On a miss |
|---|---|
| 1.01–1.25 | Torso — full dmg, no mult, no sever |
| 1.26–1.50 | Torso, no sever, + off-balance (−1m next turn) |
| 1.51–1.75 | Wide — no dmg, enemy free reactive strike |
| 1.76+ | Whiff + exposed — enemy free heavy, or a track |

**Tier 1 parry removes the precision watch entirely** (free placed shot); Tier 2 widens it one tier; Tier 3 keeps it full.

**Self-initiated called shots** (no enemy tell — an unparryable grasp, a stationary target): tolerance tightens one band beyond the multiplier's own. A **miss ends the turn outright**, no repositioning; a **hit** lets remaining movement be used normally. **Limb multiplier only — no visceral ×1.5 stacking** (visceral is reserved for genuine parry/ambush openings).

**Ambush called shots** (genuine full unawareness — a real stealth approach): count as a Tier 1 parry-grade opening. Free, no stopwatch, AND stacks with visceral 1.5× (raw × visceral × limb multiplier compound).

### Corrupted Regrowth — the build engine

A lost limb regrows at hub with a chance of coming back changed — clear upside, clear downside (e.g. beastly arm: +damage/−parry window; tendril arm: +reach/−accuracy; carapace leg: +stagger resist/−movement). Full stat-line legible only at sufficient Insight; below threshold, vibes only.

**Regret options (hub):** Revert to human (Vault Salts or Insight) · Reroll (regrow again, Vault cost). Both run.

---

## 11. Insight — the Bargain

Separate sixth dial, earned through discovery (lore, dangerous sources tasted, things defeated) — never bought. Buys power, thins the wall between you and losing control.

**What it buys:**
- Threshold gates (some doors/paths require a score to perceive/enter — free to pass once there).
- A spendable currency (forcing gated doors, Insight-priced gear, summoning support, below).
- Sight of the board — DM tells you things others don't (tells, Influence commands, true layouts, truer parry timing).
- The visceral economy (mods below).
- Reading your own mutations (§10).

**Cost (passive):** each tier raises Insanity/Influence susceptibility via the +⌊Insight÷2⌋ Save Roll term.

**First-sighting trigger:** a complete Monster Manual entry for an archetype means you've already encountered it — no first-sighting bump, regardless of whether this specific fight is new. Bump reserved for genuinely new archetypes with no page yet.

### Insight Tiers

| Tier | Insight | Unlocks |
|---|---|---|
| 0 | 0–1 | Mundane start. Vague reads, no mods, base floor. |
| 1 | 2–3 | Bloody mod. Parry window +0.05s. Low-grade mutation reads. |
| 2 | 4–5 | Sustaining mod. See warp-thresholds. Window +0.10s. |
| 3 | 6–7 | Quickening mod. Full mutation stat-lines. Charm items usable. |
| 4 | 8–9 | Window +0.15s. Untranslatable lore becomes comprehensible. |
| 5 | 10 | Full sight. Deepest hub content unlocked. |

Window bonus is a flat total per tier, not additive across tiers crossed — a tier without its own number inherits the last stated value. Applies to any DM-set timing window, not just parries.

**Insight Re-Read.** Any recurring, already-encountered thing (a mook archetype, a hub fixture, a recipe's signature environmental detail) gets re-described through your *current* tier every time it comes up again:

- **Score 0–1:** surface read — what anyone would assume.
- **Score 2–5:** a reframing detail — the surface read was incomplete.
- **Score 6–10:** the truth, plainly legible.

Costs and grants nothing — the existing score doing narrative work on repeat contact. Applies to locations and NPCs the same as monsters.

### Spending Insight

Spending drops your current score immediately — drop a tier, lose its benefits until you earn back up. Insanity/Influence floor drops with it.

- Force a gated door/path where the location calls for a spend.
- Insight-priced weapons/equipment.
- Summon a support ally — default cost 2, for the current encounter only. Temporary, unreliable.
- Memory Vendor trades — permanent buffs or Scar removal, Insight only, negotiated case-by-case (design bible).

### Visceral Mods

- **Bloody** — landed visceral: roll one bonus damage die, sized ~base÷4 rounded to nearest standard die.
- **Sustaining** — while slotted, restore 15% of damage dealt as HP (any hit).
- **Quickening** — while slotted, movement budget +2m for the encounter.

---

## 12. Abandon-All, Retreat & Death — the Fail-States

**ABANDON-ALL.** Instant, free, mid-combat — between any two actions. Spoken/thought only. Keep character/levels/limbs; **forfeit everything carried — Purse and gear both.** Left-behind gear settles on a guaranteed enemy of that instance's archetype, recoverable in a future instance of the same biome — no expiry, doesn't compound. Countered only by rare boss-tier voice-severing/silence.

**RETREAT.** A few minutes of deliberate meditation — **cannot be used in active combat.** Keep character/levels/limbs/**all gear**; forfeit only the Purse.

**DEATH.** Respawn in the salt room you entered from. Keep character/levels/mutations.
- **Gear forfeit to your killer** — a guaranteed spawn until beaten. Doesn't compound across deaths.
- **Purse fully lost.** Vault untouched.
- **Fugue applied** (§13).

---

## 13. Fugue — When Your Sight Betrays You

Applied on death. Distinct from Discombobulation (scrambles navigation/action) — Fugue corrupts Insight reads: false tells, fake Influence commands, subtly wrong layouts.

Doesn't change your Insight number — makes it *lie*. Higher Insight hurts more from this since it relies more on accurate reads.

**Clearing:** spend the next Insight point you earn — it clears Fugue instead of joining your stack.

---

## 14. The Hub

The only stable thing — and even it should be slightly wrong.

- Full restoration always (regrowth per §10, possibly changed).
- **Hub Kit:** every arrival refills the standard loadout free — **2× Wrap, 2× Tonic, 1× Camphor, 1× Scour.** Doesn't stack past cap. Anything beyond is found/bought.
- Banking: Purse → Vault in full on arrival.
- Same room every visit, **one detail changed each time.**
- One recurring antagonist NPC — reappears warped, always unhelpful/hostile, never explained. (Starter: the reception clerk.)

---

## 15. Starter Location — Stillwell Hydro

A convalescent bath-house in a fog-drowned valley over hot mineral springs. Terraced pools, brass Salts, waxed-canvas attendants, no electric light, era deliberately slippery. Warm, quiet, almost pleasant. That's the trap.

**Mundane goal:** you came for the waters, or to collect a relative who checked in and stopped writing. Reception has your name; everything's in order.

**Beats, in order:**
1. **Funicular carriage** up through fog. Silent attendant. On arrival, the carriage is gone.
2. **Reception.** Clerk hands you token/robe/key, says your relative "is taking the deep cure and can't be disturbed" — word for word if asked twice.
3. **Changing rooms** full of other guests' clothes, far more than there are guests.
4. **First wrong note:** your pool is perfect, and the longer you sit, the less you want to leave (first Influence taste). Humming from a pool that isn't there.
5. **The doorway:** past the terraces, the source-spring stair — humid, then hot, then Discombobulation. At the bottom, the door behind you opens onto somewhere else. First warp threshold — death/respawn rules go live here.

**Seeds:** the reception clerk resurfaces impossibly elsewhere, still apologising word-for-word · a brass token in your pocket that isn't yours, fits no slot · the relative is still "taking the deep cure," and you will learn what that means.

---

## 16. Default Monster Table

Archetypes, reskin per location. Attack damage generated live (§2), scaled to level (§17), never below the Damage Floor.

1. **SHAMBLER** (mook) — HP ~200–1200 · Move slow (3m). Lights only, no parryable heavy — a tell-less grab applying Influence or a track. Comes in groups. Unparryable, no visceral loop; dies to plain attacks. Stagger a leg then take the head as a faster (never required) option.
2. **LUNGER** (elite) — HP ~500–700 · Move medium (5m). One telegraphed heavy + Blood Loss. Tell: raises blade, steps in (~1.4s). Tier 1.
3. **BURSTER** (skirmisher) — HP ~400–600 · Move burst (8m surge/~1m recover). Strikes only at the lunge's end, then recovers. Tell: coils before leap. Tier 1–2.
4. **CHANTER** (caster) — HP ~300–500 · Move slow (3m), hangs back. No melee; ranged Influence/Insanity pressure each turn. Unparryable, low HP, soft limbs — priority target.
5. **SPITTER** (controller) — HP ~400–600 · Move medium (4m), keeps distance. Ranged Corrosion, stacks fast. Tell: swells, draws back (~1.6s). Tier 1.
6. **BRUTE** (heavy) — HP ~1500–2500 · Move slow (4m). Huge slow heavies, can amputate/bisect an under-levelled player on a fully-landed combo. Tell: overhead wind-up (~2.0s). Tier 2. Sever a leg to neutralise its approach.
7. **FLAILER** (chaotic) — HP ~600–900 · Move medium, erratic. Multi-track (Corrosion + Blood Loss). Tell: limbs draw back in unison, multiple windows in sequence. Tier 3. Hardest non-boss to open.

**Standard archetypes cannot parry/visceral the player** — that loop is boss/hand-flagged-elite only.

**Bosses** are bespoke, built on three pillars: (1) a gimmick punishing a default habit, (2) a Tier-3 multi-parry ballistic chain as the real opening, (3) a dismember/bisect threat for the under-levelled, with a retreat threshold always reachable.

**EFFIGY** (boss, duellist/mirror) — HP hand-set · Move fast (7m+). Uses your own toolkit: parries, viscerals, hit-and-runs, out-moves you. The system-mastery check fight.

---

## 17. Running Notes — Turn Order, Recovery & Scaling

**Turn order.** Player always acts first, every round; enemies act as a block after. A single enemy turn can narrate a full tell-then-strike (bow, then lunge) as one continuous beat.

**Out-of-combat recovery.** A quiet moment (not the hub) allows: clear one track by one stack, OR recover a small flat HP chunk. Free, no item spent. Doesn't restore limbs/mutations — hub only.

**Scaling.** Enemy HP scales with player level (total points spent); standard limb thresholds don't (§10). Bosses hand-set, exempt.

| Player level | HP multiplier |
|---|---|
| 1–20 | ×1.0 |
| 21–40 | ×1.5 |
| 41–60 | ×2.25 |
| 61–80 | ×3.5 |
| 81–100 | ×5.0 |

**Insight-gain triggers:** first sighting of a new archetype, reading lore, surviving a near-death, tasting a dangerous source, defeating a boss. Usually +1 per trigger, once per discovery.

---

## 18. Salts Rooms & Biomes — Exploration Structure

**Instance Quests vs Quests.** Narrative content splits by anchor:
- **Instance Quests** — layout-anchored (environmental stories, one-off creatures, journals, unopened doors). Expire on exit, never tracked. Completing one in-run can convert its reward into something persistent (item/lore/Insight) — the only escape route.
- **Quests** — anchored to persistent entities (recurring NPCs, hub, recipes, carried items). These survive rerolls; the only threads worth tracking between sessions.
- Enemies never persist across instances — same *kind* possible, always a fresh instance at full pool.

**Recipes & biomes.** A recipe is a biome's permanent identity (fixed mapping). Everything inside rerolls — layout, wake-in point, loot, spawns. DM holds a biome overview per recipe (palette, reskins, hazards, loot tier, anchor flavour, sub-locale list) — never a map. Some recipes Insight-gated (threshold check, not a spend).

**Sub-locale variation.** A reroll can relocate within a biome's identity, not just reshuffle one floor plan — a flooded recipe's constant is the water/mould/palette, not literally "street level" every time. **Same sub-locale never repeats two rerolls in a row.** DM tracks a running sub-locale list per recipe.

**Instance flavour tagging.** Each reroll gets a private dominant tag — **Combat / Mystery-Lore / Puzzle / Social Encounter / Escape-Survival** — leaning generated content that direction. Floor: **at least 1 in 3 rerolls of an already-explored recipe skews non-combat-primary.**

**Enemy variety.** No archetype spawns 3 rerolls running for the same recipe unless deliberately farmed by choice. Reskins across different recipes don't count as repeats.

**Discovery escalation ratio.** Most Instance Quest resolutions should stay lore/reward-only. Reserve genuine permanent escalation (new debts, Scars, standing threats) for a deliberate minority.

**Salts economy.** Single-use, consumed on activation (not per trip) — opens the biome and holds it open. Active room reusable indefinitely until cleared at hub (no refund). Older biomes stay relevant as salt farms.

**Anchors.** Wake at a biome-flavoured fixture; location rerolls, always exists. Return + leave = clean exit (Purse banks). Assess/high Insight orients toward it.

**Death & gear recovery.** Respawn in the entry salt room, Purse forfeit. **Killer is a guaranteed spawn** until beaten. **Boss kills are permanent per biome** — one fixed landmark settles where it died, persists across rerolls. *(Session 6 clarification: this means a completed kill is permanent for that instance — a retreat or Abandon-All mid-fight doesn't carry damage forward, so the next reroll's boss of that archetype starts fresh at full HP. It's not a contradiction with "fresh full-HP boss per reroll"; a finished kill leaves its landmark and closes that thread, but the recipe can still generate a new instance of the same boss archetype in a future reroll — that's simply a different fight.)*

**Companions.** Two tracks:
- **Instance Companions** — Insight-summon (§11) or a found in-run ally. Instance Quest by nature: expires with the layout. Stats generated live like a monster.
- **Persistent Companions** — recruited at the hub, survive rerolls as a Quest. Recruitment is a relationship thread, not a purchase. Real stat block generated on first accompanied run, recorded as canon. Can die in-instance — permanent, no respawn-with-you.

---

*Working title, placeholder names, and starting numbers are yours to change. The skeleton is built to be tuned at the table.*
