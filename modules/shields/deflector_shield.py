"""
Deflector Shield — adds shield HP that regenerate over time.

Shields absorb incoming damage before hull HP is reduced.
(The logic lives in Health.take_damage — this module just grants the points.)
"""
from modules.base_module import BaseModule
from components.health import Health


class DeflectorShield(BaseModule):
    name = "Deflector Shield"

    def __init__(self, shield_hp: float = 80.0, regen_rate: float = 8.0):
        super().__init__()
        self.shield_hp  = shield_hp
        self.regen_rate = regen_rate
        self._applied   = False

    def on_attach(self, world, entity_id: int):
        hp = world.get_component(entity_id, Health)
        if hp:
            hp.max_shields  += self.shield_hp
            hp.shields      += self.shield_hp
            hp.shield_regen += self.regen_rate
            self._applied = True

    def on_detach(self, world, entity_id: int):
        if self._applied:
            hp = world.get_component(entity_id, Health)
            if hp:
                hp.max_shields  -= self.shield_hp
                hp.shields       = min(hp.shields, hp.max_shields)
                hp.shield_regen -= self.regen_rate

    def update(self, world, entity_id: int, dt: float):
        # Regen is handled by CombatSystem; nothing to do here
        pass
