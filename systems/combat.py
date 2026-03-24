"""
CombatSystem — handles shield regeneration and removes dead ships.
Weapons fire is handled by individual weapon modules.
"""
from components.health import Health
from components.ship import Ship
from components.selectable import Selectable


class CombatSystem:
    def update(self, world, dt: float, events: list):
        for eid in world.get_entities_with(Health, Ship):
            hp = world.get_component(eid, Health)

            # Regen shields
            if hp.shields < hp.max_shields:
                hp.shields = min(
                    hp.shields + hp.shield_regen * dt,
                    hp.max_shields
                )

            # Remove dead ships
            if hp.is_dead():
                world.destroy_entity(eid)
