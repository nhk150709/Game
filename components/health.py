"""
Health — hit points and shield points.
"""


class Health:
    def __init__(self, hp: float = 100.0, max_hp: float = 100.0,
                 shields: float = 0.0, max_shields: float = 0.0,
                 shield_regen: float = 5.0):
        self.hp           = hp
        self.max_hp       = max_hp
        self.shields      = shields
        self.max_shields  = max_shields
        self.shield_regen = shield_regen   # shield HP recovered per second

    def is_dead(self) -> bool:
        return self.hp <= 0

    def take_damage(self, amount: float):
        """Shields absorb damage first, then hull."""
        if self.shields > 0:
            absorbed = min(self.shields, amount)
            self.shields -= absorbed
            amount -= absorbed
        self.hp -= amount
        self.hp = max(self.hp, 0)

    def fraction_hp(self) -> float:
        return self.hp / self.max_hp if self.max_hp > 0 else 0.0

    def fraction_shields(self) -> float:
        return self.shields / self.max_shields if self.max_shields > 0 else 0.0
