"""
All randomness and success/failure resolution lives here, not in any prompt.
The GM narrates the consequence of a roll; it never invents whether a roll
succeeded.
"""

import random
from dataclasses import dataclass


@dataclass
class CheckResult:
    roll: int
    modifier: int
    total: int
    dc: int
    degree: str  # "critical_fail" | "fail" | "success" | "critical_success"

    def as_dict(self) -> dict:
        return {
            "roll": self.roll,
            "modifier": self.modifier,
            "total": self.total,
            "dc": self.dc,
            "degree": self.degree,
        }


def resolve_check(skill_modifier: int, dc: int) -> CheckResult:
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
    """
    Placeholder difficulty table. Tune per-campaign -- this is deliberately
    simple so it's obvious where to edit it.
    """
    table = {
        "stealth": 13,
        "perception": 12,
        "persuasion": 14,
        "athletics": 13,
        "investigation": 13,
        "chemistry": 15,
    }
    return table.get(skill, 13)
