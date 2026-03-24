"""
AISystem — simple enemy behaviour.

Each enemy ship:
  - Looks for the nearest player ship
  - Moves toward it until in weapon range
  - Weapons fire automatically via their modules
"""
import math
import random
from components.transform import Transform
from components.ship import Ship
from components.orders import Orders
from components.health import Health


class AISystem:
    def __init__(self):
        self._update_interval = 1.5  # seconds between target re-evaluation
        self._timers: dict = {}      # {entity_id: time_until_next_update}

    def update(self, world, dt: float, events: list):
        for eid in world.get_entities_with(Transform, Ship, Orders):
            ship = world.get_component(eid, Ship)
            if ship.team != "enemy":
                continue

            # Throttle AI updates to avoid every-frame recomputation
            self._timers[eid] = self._timers.get(eid, 0.0) - dt
            if self._timers[eid] > 0:
                continue
            self._timers[eid] = self._update_interval + random.uniform(0, 0.5)

            target_id = self._find_nearest_player(world, eid)
            ord_ = world.get_component(eid, Orders)

            if target_id is None:
                ord_.set_idle()
            else:
                ord_.set_attack(target_id)   # move + attack handled together

    def _find_nearest_player(self, world, enemy_id):
        my_tf = world.get_component(enemy_id, Transform)
        best_dist = float("inf")
        best_id   = None
        for eid in world.get_entities_with(Transform, Ship, Health):
            ship = world.get_component(eid, Ship)
            if ship.team != "player":
                continue
            tf   = world.get_component(eid, Transform)
            dist = my_tf.distance_to(tf)
            if dist < best_dist:
                best_dist = dist
                best_id   = eid
        return best_id
