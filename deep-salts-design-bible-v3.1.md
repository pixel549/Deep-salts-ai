# THE DEEP SALTS
**Design Bible — Entity Templates**

Companion to the ruleset. **Load this plus the ruleset and character sheet when running the game.** Mechanic index/book plan/known gaps live in the dev log — do NOT load that during play.

*Version 3.0 — full lean rewrite. All entities and numbers from v2.8 preserved; session attribution and redundant flavor prose cut. Full history in the dev log.*

Every monster/weapon/item/NPC/status/currency gets one complete page. Copy the blank template to add an instance.

**Status effect types:** *Immediate* (lands on hit, resolves before next turn) · *Track* (builds 0–10, compounds) · *Tick* (applied at a value, counts down 1/turn automatically).

Each section leads with its **floor entry** — the weakest legal instance of that type. Nothing ships below it without a deliberate reason.

---

# 1. Monster Template

One page per monster — everything a DM needs to run that fight, nowhere else to look.

**Enemy-variety discipline:** no archetype spawns 3 rerolls running for the same recipe unless deliberately farmed. Reskins across different recipes aren't repeats.

**Standard humanoid stagger durations (default, applies wherever "standard humanoid defaults" is referenced):** Head 1 turn · Arm 2 turns · Leg 2 turns · Torso n/a. Elites/bosses set bespoke durations.

## Monster 1 — Waterlogged Guest *(floor entry)*

- **Archetype:** Shambler (mook) · **Level Range:** 1–15 · **HP:** 200 · **Move:** 3m constant shuffle, no burst/recovery beat · **Scale Band:** 1–20 (×1.0)
- **Flavour:** A guest who came for the waters and never left the pool. Robe fused to grey skin. Drifts toward warmth rather than hunting.
- **Limbs:** standard defaults, no deviations. Not sever-immune.

| Attack | Type | Tell | Window | Tier | Hit Effect | Retaliation | Miss Punish |
|---|---|---|---|---|---|---|---|
| Waterlogged Grasp | Light | None — unparryable, no windup | N/A | N/A | 0 raw; 1 Influence stack | N/A | N/A — outside 3m it just doesn't land |

- **Kitable:** Y — slowest move budget in the game.
- **Assess 0–1:** "It's slow. It won't hit hard. Watch the others behind it." · **Assess 2+:** "No damage on the grab, just Influence, no tell. Stagger a leg to ground it; head's open after."
- **Influence effect capped:** pull one step toward source (movement cost only), never an action loss, at any stack height.
- **White Salts drop:** 5 (the floor). **Insight:** +1 first sighting / +0 thereafter.

## Monster 2 — Chapel Penitent

- **Archetype:** Lunger (mook) · **Level Range:** 1–20 · **HP:** 300 · **Move:** 3m stalking pace, single 5m lunge after a short pause then a recovery beat · **Scale Band:** 1–20 (×1.0)
- **Flavour:** A pilgrim whose knees wore grooves into the stone before death. Still bows before every attack.
- **Limbs:** standard defaults, no deviations.

| Attack | Type | Tell | Window | Tier | Hit Effect | Retaliation | Miss Punish |
|---|---|---|---|---|---|---|---|
| Penitent Rush | Heavy | "It bows deeply, then drives forward in a desperate sprint." | Target 1.2s, ±0.20s | Heavy | 40 raw | Standard | Long recovery (~2 player actions before it fully re-engages, guideline not a hard count) |

- **Kitable:** Y. **Assess 0–1:** "It only becomes dangerous once it commits." · **Assess 2+:** "Wait for the bow. Dodge the charge, punish the recovery."
- **White Salts drop:** 8. **Insight:** +1/+0. **Habit punished:** panic-dodging too early. **Dismember threat:** Moderate. **Retreat always reachable:** Y.

## Monster 3 — Drowned Bellkeeper

- **Archetype:** Chanter (mook) · **Level Range:** 1–20 · **HP:** 280 · **Move:** 2m slow walk, rarely closes · **Scale Band:** 1–20 (×1.0)
- **Flavour:** A ruined attendant dragging a cracked handbell beneath the waterline. Every ring reaches inside the skull.
- **Limbs:** standard defaults, plus non-standard: **Bell** — multiplier ~2.0, sever ~40 raw (placeholder anchor, resolved historically as a pure timing check rather than a computed figure). Breaking it permanently disables Hollow Bell for the encounter (Sever, no partial state).

| Attack | Type | Tell | Window | Tier | Hit Effect | Retaliation | Miss Punish |
|---|---|---|---|---|---|---|---|
| Hollow Bell | Aura | "It slowly raises the bell before a dull, submerged toll." | Target | Light | 20 raw; 1 Influence stack | Standard | Long delay before next toll |

- **Kitable:** Y. **Assess 0–1:** "That bell feels worse than it sounds." · **Assess 2+:** "Interrupt the toll by staying aggressive. Left alone it keeps building Influence."
- **White Salts drop:** 8. **Insight:** +1/+0. **Habit punished:** ignoring support enemies. **Dismember threat:** Low.

## Monster 4 — Salt-Eaten Custodian

- **Archetype:** Shambler (elite) · **Level Range:** 5–20 · **HP:** 650 · **Move:** 3m relentless walk, never sprints · **Scale Band:** 1–20 (×1.0)
- **Flavour:** Once tasked with cleaning the baths, now drags an iron scraper large enough to serve as a coffin lid.
- **Limbs:** standard defaults, no deviations.

| Attack | Type | Tell | Window | Tier | Hit Effect | Retaliation | Miss Punish |
|---|---|---|---|---|---|---|---|
| Iron Scrape | Heavy | "The scraper screeches across the floor before a wide sweep." | Target | Heavy | 60 raw | Standard | Long recovery dragging weapon free |

- **Kitable:** Y. **Assess 0–1:** "That thing is slow, but don't stand in front of it." · **Assess 2+:** "The scrape announces everything. Dodge late, punish hard."
- **White Salts drop:** 15. **Insight:** +1/+0. **Habit punished:** greedy attacks after the tell begins. **Dismember threat:** High.

## Monster 5 — Brine Spitter

- **Archetype:** Spitter (mook) · **Level Range:** 1–20 · **HP:** 260 · **Move:** 3m retreating shuffle, keeps distance · **Scale Band:** 1–20 (×1.0)
- **Flavour:** Jaw hangs permanently open, overflowing with glittering saltwater that never runs dry.
- **Limbs:** standard defaults, no deviations.

| Attack | Type | Tell | Window | Tier | Hit Effect | Retaliation | Miss Punish |
|---|---|---|---|---|---|---|---|
| Brine Jet | Ranged | "Its throat swells until the skin stretches taut." | Target | Light | 30 raw | Standard | Stands exposed while coughing seawater |

- **Kitable:** N. **Assess 0–1:** "It's safer up close than far away." · **Assess 2+:** "Rush it during the inhale. The spit leaves it wide open."
- **White Salts drop:** 8. **Insight:** +1/+0. **Habit punished:** backpedalling constantly. **Dismember threat:** Low.

## Monster 6 — Bathhouse Flailer

- **Archetype:** Flailer (elite) · **Level Range:** 10–20 · **HP:** 700 · **Move:** 4m erratic, unpredictable direction changes · **Scale Band:** 1–20 (×1.0)
- **Flavour:** Wrapped in soaking towels that whip through the air like living tentacles when it panics.
- **Limbs:** standard defaults, no deviations.

| Attack | Type | Tell | Window | Tier | Hit Effect | Retaliation | Miss Punish |
|---|---|---|---|---|---|---|---|
| Towel Lash | Light | "The dripping cloth suddenly snaps tight." | Target | Light | 25 raw | Standard | Brief stumble |
| Frenzied Whirl | Heavy | "It throws both arms wide before spinning violently." | Target | Heavy | 70 raw | Standard | Extended dizzy recovery |

- **Kitable:** N. **Assess 0–1:** "Stay calm. It isn't." · **Assess 2+:** "The spin has the real threat. Let it commit, then strike."
- **White Salts drop:** 18. **Insight:** +1/+0. **Habit punished:** staying glued to its sides. **Dismember threat:** High.

## Monster 7 — Marble Effigy

- **Archetype:** Effigy (elite) · **Level Range:** 10–20 · **HP:** 800 · **Move:** 2m deliberate advance, pauses after every attack · **Scale Band:** 1–20 (×1.0)
- **Flavour:** A carved attendant statue animated by centuries of absorbed prayers. Marble chips fall with every step.
- **Limbs:** standard defaults, no deviations.

| Attack | Type | Tell | Window | Tier | Hit Effect | Retaliation | Miss Punish |
|---|---|---|---|---|---|---|---|
| Marble Fist | Heavy | "Stone cracks loudly through its arm before the punch." | Target | Heavy | 80 raw | Standard | Long stationary recovery |

- **Kitable:** Y. **Assess 0–1:** "Every hit hurts. Every swing is slow." · **Assess 2+:** "Its recovery is longer than its attack. Survive one blow, answer with several."
- **White Salts drop:** 20. **Insight:** +1/+0. **Habit punished:** trading hits. **Dismember threat:** Very High.

## Monster 8 — The Singer *(boss, Choir Deep)*

- **Archetype:** Choir (boss) · **HP:** 900 (hand-set, exempt from scaling) · **Move:** 0m — fully rooted, never advances or retreats.
- **Flavour:** A pilgrim shape whose face gave way to a vertical opening that doesn't sing so much as *is* the sound. Sustains an unbroken note that draws the faithful into a ring around it, never approaching its own devotion.
- **Limbs:** standard defaults + **The Open Throat** (weak point) — multiplier ×2.0, sever 400.

| Attack | Type | Tell | Window | Hit Effect |
|---|---|---|---|---|
| Choir Pulse | Ranged/Aura | "The layered note sharpens, aims itself." | Unparryable, always lands | 2 Influence stacks/pulse |

- **Kitable:** N/A — never moves. Breaking line of sight is the counter.
- **Assess 0–1:** "It's not hunting. Whatever it's doing, it's not going to chase." · **Assess 2+:** "The note itself is the attack. The opening where its face should be is real, but boss-high, not mook-high."
- **White Salts drop:** 60. **Insight:** +1/+1.
- **Boss Gimmick:** Sever the Open Throat (400 raw-equivalent, one hit) and the fight ends regardless of remaining HP. Otherwise pure attrition — the Singer never physically attacks; danger comes secondhand from its Penitent congregation, while Influence climbs the whole time, save DC rising with stack count.
- **Habit punished:** tanking pulses in the open, or fighting through the ring instead of around it. **Dismember threat:** Low (no melee of its own). **Retreat always reachable:** Y.

## Monster Template (blank)

- **Archetype:** · **Level Range:** · **HP:** · **Move Budget/Pattern:** · **Scale Band:** · **Flavour:**
- **Limbs** (standard defaults: Head ×1.5/180 · Torso ×1.0/800 · Arm ×0.65/200 · Leg ×0.75/300 — list only deviations/non-standard):

|Limb|Multiplier|Stagger Threshold|Stagger Duration|Sever Threshold|Sever Immune?|
|-|-|-|-|-|-|
|||||||

Small high-value targets (bell, crack, eye) go in this table as non-standard limb entries with a high multiplier — Sever only, no partial stagger state.

**Attacks:**

|Attack|Type|Tell|Window|Tier|Hit Effect|Status Type|Retaliation?|Miss Punish|
|-|-|-|-|-|-|-|-|-|
||||||||||

- **Kitable:** · **Assess 0–1:** · **Assess 2+:** · **White Salts drop:** · **Insight granted:**
- **Boss Gimmick (else N/A):** · **Habit Punished:** · **Falls-For-It Result:** · **Dismember Threat:** · **Retreat Reachable:**

---

# 2. Weapon Template

One page per weapon — identity, damage, passive, sever maths together.

**Formula:** Damage = Base + (ESV × grade). E ×0.3 · D ×0.5 · C ×0.7 · B ×0.9 · A ×1.1 · S ×1.3. Heavy = 2×Base + (ESV × grade × 1.5).

**Sever reference:** min raw = threshold ÷ multiplier. Head 180→120 raw · Arm 200→~308 raw · Leg 300→400 raw.

**ESV touchpoints:** raw 8→ESV 8 · raw 20→ESV 20 · raw 40→ESV 33 · raw 99→ESV ~47.

## Weapon 1 — Paring Knife *(floor entry)*

- **Type:** Quick · **Stat/Grade:** Skill/E · **Hands:** One
- **Acquisition:** not found — the mechanical floor a backstory weapon lands at or above.
- **Base:** 20 (Damage Floor). Light = 20+ESV×0.3 · Heavy = 40+ESV×0.45.
- **Worked rows:** ESV 8 → 22/44 · ESV 47 → 34/61.
- **Passive:** none — the baseline everything else compares against. **Insight Gate:** none.
- **Sever viability:** none at any ESV — floor weapons never sever, at any Strength.

## Weapon 2 — The Salvage Launcher

- **Type:** Reach · **Stat/Grade:** Skill/D · **Hands:** Two
- **Acquisition:** commissioned (hub engineer), not found — built to fire existing Powder Charge capsules. Character-specific.
- **Base:** 30, single shot type (no Light/Heavy split). Shot = 30+ESV×0.5.
- **Worked rows:** ESV 8 → 34 · ESV 17 → 38 · ESV 47 → 53.
- **Passive — Powder Charge (ranged variant):** fires loaded only, no capsule = no shot. Loading = universal Fast Action (0m). No timing check — guaranteed detonation, traded for finite ammo. On hit: 1 Discombobulation, automatic.
- **Range:** 8m. **Movement cost to fire:** 1m (Light-tier, no Heavy variant to price separately). **Ammo:** drawn from Hub Kit capsule stock (4 standard). Empty = treat as Fists.
- **Sever viability:** none at any ESV — concussive, not bladed, not built for it.

## Weapon Template (blank)

- **Type (Quick/Heavy/Reach/Trick):** · **Stat/Grade:** · **Hands:** · **Acquisition:**
- **Base:** · **Light:** Base+ESV×grade · **Heavy:** 2×Base+ESV×grade×1.5
- **Worked rows:** ESV 8 → __/__ · ESV 47 → __/__
- **Passive:** · **Status Applied:** · **Insight Gate:**

**Sever viability:**

|Target|Min Raw|Viable at ESV|Notes|
|-|-|-|-|
|Head|120|||
|Arm|~308|||
|Leg|400|||

---

# 3. Player Character Sheet

Moved to its own live-state file — `deep-salts-character-sheet.md`. DM rewrites it after any significant change; single source of truth for HP, tracks, charges, limbs, Insight, inventory.

---

# 4. NPC Template

One page per NPC.

## NPC 1 — Robe Attendant *(floor entry)*

Zero mechanical function, zero dialogue, zero lore thread. *Not the reception clerk*, who is the recurring antagonist and always narrated as a DM moment, never a stat block.

- **Role:** background hub functionary. **Location:** hub only. **Fightable:** N.
- **Fixed appearance:** waxed-canvas apron, sleeves rolled, no eye contact. **Never changes** — the one exception to the hub's one-detail-changes rule.
- **On arrival:** hands over a towel, points once, says nothing. **Never** speaks first, answers, or acknowledges anything's wrong.
- **Dialogue:** non-verbal only — a nod, a shrug, a point at the exit, a slow head-shake. Never a spoken line.
- **Mechanical function:** robe/towel on first hub visit only, cosmetic. **Lore:** connects to nothing.

## NPC 2 — The Memory Vendor

- **Role:** deep-recess entity, not a hub fixture. Trades power for Insight, collects like a loan shark. **Location:** unconfirmed, not hub-accessible — "not a room, a depth. You get deep enough that it stops being able to avoid you." **Fightable:** N.
- **Fixed appearance:** undefined, genuinely unmet. **On arrival:** offers trades — permanent buffs or Scar removal, Insight only. **Never** accepts Salts/items/favors as payment.
- **Dialogue:** measured, transactional, unbothered by refusal · treats a missed payment as fact not threat · never raises its voice about invasion — it's just what happens next.
- **Mechanical function:**
  - **Buy-in trades:** spend Insight (score/tier/floor drop immediately) for a permanent effect, negotiated case-by-case, no fixed menu.
  - **Scar removal:** only route. Scar 1 = 6 Insight, Scar 2 = 10, Scar 3+ = higher — deliberately unpayable past the first in one sitting.
  - **Debt/toll:** larger trades can be a payment plan (e.g. "13 Insight across 2 runs"). Tracked as bookkeeping — no track, no rolls.
    - Missing a scheduled payment: flat 10% of that run's Vault banking, no escalation.
    - Refusing the toll (not just missing schedule): next reroll of that recipe comes back quietly worse (HP bump, extra body, seeded hazard).
    - Full repayment closes the debt clean regardless of missed payments along the way.
    - No interest accrues in Insight specifically (a scarce, non-renewable resource — avoids a softlock).
- **Lore:** tangled with the reception clerk's "brother" hook. Never revealed: true name, appearance, location.

## NPC Template — Persistent Companion variant

Same fields as standard, plus once recruited:
- **Recruited:** session/run + the hook that closed the deal. **Accompanies into:** which recipes (not necessarily all).
- **Stat block:** HP band, 1–2 actions, any gimmick — generated live on first accompanied run, recorded as canon.
- **Status:** Active / Held at hub / **Dead (permanent, no respawn).**

## NPC 3 — Maud

- **Role:** hub salt/item identifier and appraiser. Doesn't pry — except when something on her own personal list crosses the counter. **Location:** hub only. **Fightable:** N.
- **Fixed appearance:** undefined, never described in play. **On arrival:** IDs salts (5 Salts first ID, doubling per subsequent) or off-catalog items (8 Salts, separate scale). Has three standing salvage requests: sealed items, source-water, packing cloth.
- **Never** asks where an item came from or whose it was, as part of a standard ID. **Never says directly** why the three categories matter to her, or what a certain ring's symbol means.
- **Dialogue:** professional and unhurried on anything routine · goes still and flat the moment something personal surfaces · direct refusals, not deflection — "that's not mine to want" · asks to revisit rather than pretends it doesn't matter.
- **Mechanical function:** salt ID (5→10→20→40... doubling) · off-catalog ID (8 Salts flat) · buys sealed/found items outright, case-by-case (paid 20 for a sealed vessel unprompted) · salvage requests have no defined mechanical reward yet — relationship/lore thread, not a transaction.
- **Lore:** recognized a scratched symbol on a found ring on sight. Confirmed: she's buried someone who wore that mark, exactly once. Won't confirm/deny a connection to "Mirel" or the reception clerk's brother thread. Asked to be asked again another time — live, not closed.

## NPC Template (blank)

- **Role:** · **Level Range:** · **Location(s):** · **Fightable (Y/N):**
- **Fixed appearance:** · **What changes between appearances:** · **On arrival:** · **Never does:** · **Never says directly:**
- **Dialogue seeds:** 3–5 fragments, tone not scripts.
- **Mechanical function:** services/items/gated info/behaviour shifts.
- **Lore thread:** connects to · piece together over time · never revealed.

---

# 5. Item Template

## Item 1 — Scour *(floor entry)*

- **Type:** Quick · **Action Cost:** Fast Action
- **Effect:** removes exactly 1 Corrosion stack, nothing else.
- **Duration:** instant · **Consumable:** Y · **Carry Limit:** 5 (mirrors Corrosion's cap)
- **Insight Gate:** none. **Limb Requirement:** a working hand/arm.
- **Acquisition:** mineral scrapings from the source-spring terraces; cheap/free at the apothecary stall.

## Item 2 — The Beckoner

Lloyd's, currently lost with the Singer. First item to ever push Influence onto an enemy — no prior mechanic covered this.

- **Type:** Passive-while-uncovered (session 6 redefinition — supersedes the old "Action Item, targeted" version below) · **Consumable:** N (Constant, unlimited uses)
- **Effect:** always active in lore; mechanically inert while wrapped. **Uncovered, it applies 1 Influence stack/turn to Lloyd and every enemy within an 8m radius**, no targeting needed, no Action cost to sustain — just to physically wrap or unwrap it (Fast Action, in hand). Re-wrapping stops it dead, immediately, for everyone in range.
- **Intended play pattern:** carry it uncovered near an enemy to weaken them, then re-cover it to stop affecting the area — including stepping outside the 8m radius, which has the same effect as re-wrapping for anyone who leaves it.
- **Status Type:** Track (Influence), both sides, per turn while uncovered and in range
- **Mechanical gap, now resolved (session 6):** enemy Influence overload rule now exists — see Ruleset §5. **Residual Influence on Lloyd is sticky** — see Ruleset §5, doesn't clear on wrap/distance like normal sources, only on rest or fully divesting the item.
- **Narrative hook:** while anyone (Lloyd included) is within its uncovered radius, the idol presses for a name spoken to it. He's been warned not to. Consequences unspecified — deliberately unresolved, do not invent an answer ahead of the table.
- **Superseded original text (kept for reference, no longer active):** ~~Type: Action Item (activated), full Action, 2m. Effect: applies 1 Influence stack to a targeted enemy AND 1 to Lloyd, simultaneously, on use.~~

## Item 3 — The Charm

Lloyd's, currently lost with the Singer.

- **Type:** Action Item · **Consumable:** Y, Uses: 1, destroyed on use · **Insight Gate:** Tier 3 (Insight 6+)
- **Effect (player's choice at moment of use):** either +1 bonus damage die on the next attack (sized ~base÷4, same convention as the Bloody visceral mod), or widen the next parry/precision window by +0.10s.

## Item 4 — Clean Source-Water Flask

Lloyd's, currently lost with the Singer — the "clean variant" referenced generically in the ruleset's Action Items list, this specific instance's numbers pinned down.

- **Type:** Action Item · **Action Cost:** full Action, 2m · **Consumable:** Y, Uses: 1
- **Effect:** heals 75% of Max HP. **No Influence stack** — unlike the standard source-water flask, this is the power without the vulnerability tax. Rarer for exactly that reason.

## Item Template (blank)

**Type:** · **Action Cost:** · **Effect:** · **Status Applied:** · **Duration:** · **Consumable:** · **Carry Limit:** · **Insight Gate:** · **Limb Requirement:** · **Acquisition:**

---

# 6. Status Effect Template

## Status Effect 1 — Off-Balance *(floor entry, Immediate)*

- **Type:** Immediate · **Affects:** currently only produced by the player's own missed Precision Strike (band 1.26–1.50). **Resisted on application:** N.
- **Effect:** −1m movement, next turn only. **Duration:** 1 turn, expires automatically.
- **Combos:** compounds tactically with a staggered leg or Discombobulation's movement scrambling.

## Status Effect 2 — Blood Loss *(Track)*

- **Type:** Track (0–10) · **Affects:** Both.
- **Stacks:** +1 per qualifying slashing/piercing hit or hazard. **Effect per stack:** new stack deals immediate bonus damage = stack total (5th cut = +5, no per-turn drain).
- **Cap:** 10 → triggers Rupture, resets to 0.
- **Clear:** bandage/cautery/pressure; Wrap clears 2.

## Status Effect 3 — Rupture *(Immediate, triggered)*

- **Type:** Immediate, triggered at Blood Loss 10 · **Effect:** 25% Max HP direct damage + staggered a beat. **Duration:** instant, resolves once.
- **Sources:** currently only the player's own Blood Loss cap.

## Status Effect Template (blank)

**Type (Immediate/Track/Tick):** · **Affects:** · **Resisted on application:**
**If Immediate:** effect · duration · cleared early?
**If Track:** stacks per application · effect per stack/turn · cap · overflow effect · clear condition
**If Tick:** applied value · effect while active (counts down 1/turn automatically)
**Interactions:** dangerous combos · countered by · sources

---

# 7. Currency / Collectible Template

## Currency/Collectible 1 — The Token That Isn't Yours *(floor entry)*

Not White Salts — the weakest possible Key Item, seeded and currently doing nothing on purpose.

- **Category:** Key Item (bordering Story). **Risk Status:** neither Purse nor Vault — stays with you. **Lost on death/retreat:** N/N.
- **Acquisition:** one-time only, found in the robe pocket entering the deep cure. No known second copy or way to lose the first.
- **Spend options:** none yet — fits no slot, opens nothing, deliberately.
- **Flavour:** worn brass, warm to the touch even when nothing else is. Doesn't match the clerk's own token; nobody at the hub will take it back.

**Template fields:** Category · Risk Status · Lost on Death?/Retreat? · Acquisition (base drop / bonus conditions) · Spend Options · Flavour.

---

*Sections 8–10 (Mechanic Index, Book Plan, Known Gaps) live in the dev log.*
