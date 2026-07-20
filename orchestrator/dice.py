"""
All randomness, formulas, and success/failure resolution live here, not in any
prompt. The GM narrates the consequence of a roll or a formula's output; it
never invents whether something succeeded or how much damage landed. This is
the load-bearing principle of the whole simulation -- see gm_system.md.

Formulas below are transcribed directly from deep-salts-v8.1.md (the actual
Deep Salts ruleset, in rules/deep-salts-v8.1.md) -- section numbers in
comments refer to that document. Two things in this file are NOT from the
ruleset and are this project's own adaptation, clearly marked where they
occur:
  1. Which attribute governs each non-combat "uncertain action" skill
     (stealth/perception/persuasion/athletics/investigation/chemistry) --
     the ruleset's five attributes (VIG/END/STR/SKI/RES) are built for a
     physical/psychological-horror combat crawl and never actually assign
     governing attributes to social/mental skills. See SKILL_ATTRIBUTE_MAP.
  2. The stopwatch->table-fallback DC curve. The ruleset says "replace any
     stopwatch with d20 + Insight-as-modifier, same outcomes" but doesn't
     give explicit DCs for a no-real-time context (obviously -- it's written
     for a human with an actual stopwatch). See stopwatch_fallback_dc().
"""

import math
import random
from dataclasses import dataclass, field


# --- §3 Core Resolution: Attribute Modifier table -----------------------

def attribute_modifier(score: int) -> int:
    """§3. Applies to attribute-driven checks. Does NOT apply to the Save
    Roll formula (§5), which has its own scaling."""
    if score <= 1:
        return -3
    if score <= 4:
        return -2
    if score <= 9:
        return -1
    if score <= 19:
        return 0
    if score <= 39:
        return 1
    if score <= 79:
        return 2
    return 3  # 80-99


# --- §4 Character Creation & Progression ---------------------------------

def hp_max(vigor: int) -> int:
    """§4. Max HP = 60 + (Vigor x 6)."""
    return 60 + vigor * 6


def movement_budget(endurance: int) -> int:
    """§4. Movement budget = 8 + floor(Endurance / 15) meters."""
    return 8 + endurance // 15


def insanity_influence_save_bonus(resolve: int) -> int:
    """§4. Insanity/Influence save bonus = floor(Resolve / 10)."""
    return resolve // 10


_ESV_BANDS = [
    (1, 20, 1.0),
    (21, 40, 0.65),
    (41, 60, 0.4),
    (61, 80, 0.2),
    (81, 99, 0.1),
]


def esv(score: int) -> float:
    """§4. Effective Scaling Value -- marginal/bracketed, not a flat
    multiply. Score 99 -> ~46.9 (~47), matching the ruleset's worked
    example. Weapon/combat scaling uses this, never the raw attribute."""
    score = max(1, min(99, score))
    total = 0.0
    for lo, hi, rate in _ESV_BANDS:
        if score < lo:
            break
        band_points = min(score, hi) - lo + 1
        total += band_points * rate
    return total


_WEAPON_GRADES = {"E": 0.3, "D": 0.5, "C": 0.7, "B": 0.9, "A": 1.1, "S": 1.3}


def weapon_damage(base: int, governing_attribute_score: int, grade: str, heavy: bool = False) -> int:
    """§4. Damage = Base + (ESV x grade). Heavy ~= 2xBase + ESV x grade x 1.5.
    Fractional results round UP (session 6 ruling, applies throughout, not
    just Fists)."""
    grade_mult = _WEAPON_GRADES[grade.upper()]
    esv_value = esv(governing_attribute_score)
    if heavy:
        raw = 2 * base + esv_value * grade_mult * 1.5
    else:
        raw = base + esv_value * grade_mult
    return math.ceil(raw)


# --- §5 Status Tracks: the Save Roll --------------------------------------

@dataclass
class SaveResult:
    roll: int
    dc: int
    success: bool

    def as_dict(self) -> dict:
        return {"roll": self.roll, "dc": self.dc, "success": self.success}


def insanity_influence_save(track_value: int, resolve: int, insight: int, situational_mod: int = 0) -> SaveResult:
    """§5. Succeed on d20 >= 10 + track_value - floor(Resolve/10) +
    floor(Insight/2) (+ situational mods). This is a flat roll vs DC --
    unlike §3 checks, nothing is added to the die itself."""
    dc = 10 + track_value - insanity_influence_save_bonus(resolve) + (insight // 2) + situational_mod
    roll = random.randint(1, 20)
    return SaveResult(roll=roll, dc=dc, success=roll >= dc)


# --- §10 Limbs, Precision & Mutation ---------------------------------------

STANDARD_HUMANOID_LIMBS = {
    # name: (damage_multiplier, stagger/sever threshold, enemy_stagger_turns)
    # Player stagger duration is always fixed at 1 turn (§10); enemy stagger
    # duration is variable per Monster Template -- the values below are the
    # design bible's stated defaults for standard (non-boss) humanoids.
    "head":  {"multiplier": 1.5, "threshold": 180, "enemy_stagger_turns": 1},
    "torso": {"multiplier": 1.0, "threshold": 800, "enemy_stagger_turns": None},  # n/a, stagger is just heavy dmg
    "arm":   {"multiplier": 0.65, "threshold": 200, "enemy_stagger_turns": 2},
    "leg":   {"multiplier": 0.75, "threshold": 300, "enemy_stagger_turns": 2},
}


@dataclass
class LimbHitResult:
    limb: str
    raw_damage: int
    effective_damage: int
    new_stagger_meter: int
    sever: bool          # threshold crossed in one hit -> permanent
    stagger_crossed: bool  # threshold crossed cumulatively -> limp/staggered
    hp_after: int

    def as_dict(self) -> dict:
        return {
            "limb": self.limb, "raw_damage": self.raw_damage,
            "effective_damage": self.effective_damage,
            "new_stagger_meter": self.new_stagger_meter,
            "sever": self.sever, "stagger_crossed": self.stagger_crossed,
            "hp_after": self.hp_after,
        }


def resolve_limb_hit(raw_damage: int, limb: str, current_hp: int, current_stagger_meter: int,
                      limb_table: dict = None) -> LimbHitResult:
    """§10. Effective damage = raw x limb multiplier -- chips HP AND fills
    the limb's stagger meter. Threshold crossed in ONE hit -> SEVER
    (permanent; severing torso/head kills regardless of remaining HP).
    Threshold crossed over SEVERAL hits -> STAGGER (limp)."""
    table = limb_table or STANDARD_HUMANOID_LIMBS
    spec = table[limb]
    effective = int(raw_damage * spec["multiplier"])
    new_stagger = current_stagger_meter + effective
    hp_after = max(0, current_hp - effective)

    sever = effective >= spec["threshold"]  # crossed in one hit
    stagger_crossed = (not sever) and new_stagger >= spec["threshold"] and current_stagger_meter < spec["threshold"]

    return LimbHitResult(
        limb=limb, raw_damage=raw_damage, effective_damage=effective,
        new_stagger_meter=min(new_stagger, spec["threshold"]),
        sever=sever, stagger_crossed=stagger_crossed, hp_after=hp_after,
    )


# --- §9 Visceral System / §10 Precision -- table fallback for AI-vs-AI ----

def stopwatch_fallback_dc(tolerance_seconds: float) -> int:
    """NOT from the ruleset -- this project's own table-fallback DC curve
    (see module docstring, point 2). Tighter tolerance (smaller number) =
    a harder read = higher DC. Calibrated so the ruleset's own tolerance
    bands land in a sane 10-19 DC range:
      0.25s (loosest parry/precision tolerance) -> DC 10
      0.04s (tightest precision tolerance)      -> DC 18
    """
    dc = round(20 - tolerance_seconds * 40)
    return max(8, min(19, dc))


@dataclass
class StopwatchResult:
    roll: int
    insight_modifier: int
    total: int
    dc: int
    outcome: str  # "parry" | "whiff" (or "hit" | "miss" for precision calls)

    def as_dict(self) -> dict:
        return {
            "roll": self.roll, "insight_modifier": self.insight_modifier,
            "total": self.total, "dc": self.dc, "outcome": self.outcome,
        }


def resolve_stopwatch_fallback(insight: int, tolerance_seconds: float,
                                success_label: str = "parry", fail_label: str = "whiff") -> StopwatchResult:
    """§9/§10 table fallback: 'replace any stopwatch with d20 +
    Insight-as-modifier, same outcomes.' Used for every parry and every
    precision called-shot in this simulation, since there are no human
    reflexes in the loop to time a real stopwatch against."""
    roll = random.randint(1, 20)
    total = roll + insight
    dc = stopwatch_fallback_dc(tolerance_seconds)
    outcome = success_label if total >= dc else fail_label
    return StopwatchResult(roll=roll, insight_modifier=insight, total=total, dc=dc, outcome=outcome)


# --- §3 "Anything genuinely uncertain" -- unchanged generic check ---------

@dataclass
class CheckResult:
    roll: int
    modifier: int
    total: int
    dc: int
    degree: str  # "critical_fail" | "fail" | "success" | "critical_success"

    def as_dict(self) -> dict:
        return {"roll": self.roll, "modifier": self.modifier, "total": self.total, "dc": self.dc, "degree": self.degree}


def resolve_check(skill_modifier: int, dc: int) -> CheckResult:
    """§3: d20 + modifier vs DC, for stealth/forcing a door/reading the
    unreadable/etc -- anything that isn't combat or a Save Roll."""
    roll = random.randint(1, 20)
    total = roll + skill_modifier

    if roll == 1:
        degree = "critical_fail"
    elif roll == 20:
        degree = "critical_success"
    elif total >= dc:
        degree = "success"
    else:
        degree = "fail"

    return CheckResult(roll=roll, modifier=skill_modifier, total=total, dc=dc, degree=degree)


def default_dc_for(skill: str) -> int:
    """Placeholder difficulty table for non-combat checks. Tune per-campaign."""
    table = {
        "stealth": 13, "perception": 12, "persuasion": 14,
        "athletics": 13, "investigation": 13, "chemistry": 15,
    }
    return table.get(skill, 13)


# This project's own mapping (NOT from the ruleset -- see module docstring,
# point 1) of each non-combat skill to the attribute whose modifier applies.
SKILL_ATTRIBUTE_MAP = {
    "stealth": "skill",
    "perception": "resolve",
    "persuasion": "resolve",
    "athletics": "strength",
    "investigation": "skill",
    "chemistry": "skill",
}


# --- §16 Default Monster Table / §17 Scaling ------------------------------

DEFAULT_ARCHETYPES = {
    "shambler": {
        "tier": "mook", "hp_range": (200, 1200), "move": "slow (3m)",
        "parryable": False,
        "tell": "None -- tell-less grab applying Influence or a track. Comes in groups.",
    },
    "lunger": {
        "tier": 1, "hp_range": (500, 700), "move": "medium (5m)",
        "parryable": True,
        "tell": "Raises blade, steps in (~1.4s).",
    },
    "burster": {
        "tier": "1-2", "hp_range": (400, 600), "move": "burst (8m surge / ~1m recover)",
        "parryable": True,
        "tell": "Coils before leap. Strikes only at the lunge's end, then recovers.",
    },
    "chanter": {
        "tier": "caster", "hp_range": (300, 500), "move": "slow (3m), hangs back",
        "parryable": False,
        "tell": "No melee. Ranged Influence/Insanity pressure each turn. Soft limbs, priority target.",
    },
    "spitter": {
        "tier": 1, "hp_range": (400, 600), "move": "medium (4m), keeps distance",
        "parryable": True,
        "tell": "Swells, draws back (~1.6s). Ranged Corrosion, stacks fast.",
    },
    "brute": {
        "tier": 2, "hp_range": (1500, 2500), "move": "slow (4m)",
        "parryable": True,
        "tell": "Overhead wind-up (~2.0s). Huge slow heavies -- sever a leg to neutralise its approach.",
    },
    "flailer": {
        "tier": 3, "hp_range": (600, 900), "move": "medium, erratic",
        "parryable": True,
        "tell": "Limbs draw back in unison, multiple windows in sequence. Multi-track (Corrosion + Blood Loss).",
    },
}

_HP_SCALING_BANDS = [
    (1, 20, 1.0), (21, 40, 1.5), (41, 60, 2.25), (61, 80, 3.5), (81, 100, 5.0),
]


def monster_hp_scaling(player_level: int) -> float:
    """§17. Standard limb thresholds do NOT scale with level -- only HP
    does. Bosses are hand-set and exempt from this table entirely."""
    for lo, hi, mult in _HP_SCALING_BANDS:
        if lo <= player_level <= hi:
            return mult
    return _HP_SCALING_BANDS[-1][2]  # cap at the highest band past level 100


# This project's own adaptation (see module docstring, point 2): rather than
# threading a GM-declared tolerance across turns to match the real-time
# tell-then-react choreography, parry attempts resolve same-turn using a
# tolerance keyed to the archetype's tell (a reasonable read of the tells
# described in §16, since the ruleset only gives 3 illustrative examples --
# Lunge 1.50s+-0.20, Overhead 2.00s+-0.15, Sweep 1.20s+-0.25 -- not a full
# table). Called shots on the head use the exact Precision Strike band the
# ruleset gives for a 1.26-1.50 multiplier (head = 1.5): +-0.13s. Torso/arm/
# leg multipliers are all <=1.0, so per §10 they're never subject to the
# precision tax at all -- free called shots, no stopwatch needed.
PARRY_TOLERANCE_BY_ARCHETYPE = {
    "lunger": 0.20, "burster": 0.20, "brute": 0.15, "flailer": 0.20,
}
DEFAULT_PARRY_TOLERANCE = 0.20
HEAD_PRECISION_TOLERANCE = 0.13


# Monster basic-attack damage. NOT from the ruleset -- it explicitly says
# enemy attack damage is "generated live" by an AI DM's judgment each
# encounter (§2, §16), which doesn't translate to a fully autonomous
# Python-resolved combat loop without SOME concrete number. These are a
# reasonable placeholder scaled roughly to each archetype's tier/HP band,
# respecting the Damage Floor (20, §4). Tune freely -- exactly the kind of
# number the ruleset's own closing line says is "yours to change."
MONSTER_BASE_ATTACK_DAMAGE = {
    "shambler": 20, "lunger": 35, "burster": 30, "chanter": 15,
    "spitter": 25, "brute": 60, "flailer": 40,
}


def resolve_combat_action(actor_sheet: dict, action_type: str, swing: str, target_limb: str, monster: dict) -> dict:
    """
    Resolves one player's combat_action against the current encounter's
    monster (player-vs-monster only in this simulation -- PvP combat would
    need its own targeting path and isn't built here). actor_sheet is the
    acting character's full sheet (attributes/weapon/insight); monster is
    encounter_state()['monster']. Returns a plain dict for the caller to
    apply to state and to hand the GM as an already-resolved result --
    never let the GM re-decide any of these numbers.
    """
    weapon = actor_sheet["weapon"]
    gov_score = actor_sheet["attributes"][weapon["governing_attribute"]]
    insight = actor_sheet["insight"]

    if action_type == "attack":
        # §10: "No free called shots on a standing, alert, unstaggered
        # enemy... Default swings land torso."
        raw = weapon_damage(weapon["base_damage"], gov_score, weapon["grade"], heavy=(swing == "heavy"))
        hit = resolve_limb_hit(raw, "torso", monster["hp"], monster["limbs"]["torso"]["stagger_meter"])
        return {"type": "attack", "raw_damage": raw, "limb_hit": hit.as_dict()}

    if action_type == "ambush_called_shot":
        # §10: genuine unaware/stealth opening -- free, no stopwatch, AND
        # stacks with the 1.5x visceral multiplier.
        raw = weapon_damage(weapon["base_damage"], gov_score, weapon["grade"], heavy=(swing == "heavy"))
        raw = int(raw * 1.5)
        limb = target_limb or "torso"
        hit = resolve_limb_hit(raw, limb, monster["hp"], monster["limbs"][limb]["stagger_meter"])
        return {"type": "ambush_called_shot", "raw_damage": raw, "limb_hit": hit.as_dict()}

    if action_type == "called_shot":
        raw = weapon_damage(weapon["base_damage"], gov_score, weapon["grade"], heavy=(swing == "heavy"))
        limb = target_limb or "torso"
        multiplier = STANDARD_HUMANOID_LIMBS[limb]["multiplier"]
        if multiplier <= 1.0:
            # §10: at/below 1.0, never subject to the precision tax -- free.
            hit = resolve_limb_hit(raw, limb, monster["hp"], monster["limbs"][limb]["stagger_meter"])
            return {"type": "called_shot", "limb_hit": hit.as_dict()}
        # Standard humanoid: only the head (1.5x) is ever >1.0.
        sw = resolve_stopwatch_fallback(insight, HEAD_PRECISION_TOLERANCE, "hit", "miss")
        if sw.outcome == "miss":
            # §10 miss-punishment table, 1.26-1.50 band: torso, no sever, + off-balance.
            redirected = resolve_limb_hit(raw, "torso", monster["hp"], monster["limbs"]["torso"]["stagger_meter"])
            return {"type": "called_shot", "stopwatch": sw.as_dict(), "redirected_to_torso": True,
                     "off_balance": True, "limb_hit": redirected.as_dict()}
        hit = resolve_limb_hit(raw, limb, monster["hp"], monster["limbs"][limb]["stagger_meter"])
        return {"type": "called_shot", "stopwatch": sw.as_dict(), "limb_hit": hit.as_dict()}

    if action_type == "parry_attempt":
        archetype = monster["archetype"] if monster else None
        tolerance = PARRY_TOLERANCE_BY_ARCHETYPE.get(archetype, DEFAULT_PARRY_TOLERANCE)
        sw = resolve_stopwatch_fallback(insight, tolerance, "parry", "whiff")
        result = {"type": "parry_attempt", "stopwatch": sw.as_dict()}
        if sw.outcome == "whiff":
            # §9: "Eat the heavy in full plus a punish (DM's pick)."
            result["damage_taken"] = MONSTER_BASE_ATTACK_DAMAGE.get(archetype, 20)
        else:
            # §9 Tier 1 (default for non-boss archetypes): parry floors it --
            # opened, no second stopwatch.
            result["enemy_opened"] = True
        return result

    raise ValueError(f"unknown combat_action type: {action_type}")


def spawn_monster(archetype_key: str, player_level: int, name: str = None) -> dict:
    """§16/§17. Rolls HP within the archetype's band, scales it to the
    player's level, and sets up standard-humanoid limb tracking (§10) --
    every default archetype uses the standard limb table; bosses would
    need their own hand-set values, not built here (see build summary)."""
    spec = DEFAULT_ARCHETYPES[archetype_key]
    lo, hi = spec["hp_range"]
    base_hp = random.randint(lo, hi)
    scaled_hp = int(base_hp * monster_hp_scaling(player_level))

    return {
        "name": name or archetype_key.capitalize(),
        "archetype": archetype_key,
        "tier": spec["tier"],
        "move": spec["move"],
        "parryable": spec["parryable"],
        "tell": spec["tell"],
        "max_hp": scaled_hp,
        "hp": scaled_hp,
        "limbs": {
            limb: {"stagger_meter": 0, "severed": False, "staggered_turns_remaining": 0}
            for limb in STANDARD_HUMANOID_LIMBS
        },
    }
