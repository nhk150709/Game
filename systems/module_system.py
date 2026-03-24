"""
ModuleSystem — calls update() on every module attached to every ship.
"""
from components.ship import Ship


class ModuleSystem:
    def update(self, world, dt: float, events: list):
        for eid in world.get_entities_with(Ship):
            ship = world.get_component(eid, Ship)
            for module in ship.modules:
                if module.enabled:
                    module.update(world, eid, dt)
