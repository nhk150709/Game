"""
Laser Cannon — fires a fast projectile at the nearest enemy in range.

Stats you can tweak
-------------------
damage      : HP removed per hit
range       : maximum shooting distance (world pixels)
fire_rate   : shots per second
"""
import math
from modules.base_module import BaseModule
from components.transform import Transform
from components.orders import Orders
from components.ship import Ship


class LaserCannon(BaseModule):
    name = "Laser Cannon"

    def __init__(self, damage: float = 20.0, range: float = 300.0,
                 fire_rate: float = 1.5):
        super().__init__()
        self.damage    = damage
        self.range     = range
        self.fire_rate = fire_rate      # shots per second
        self._cooldown = 0.0            # seconds until next shot

    def update(self, world, entity_id: int, dt: float):
        if not self.enabled:
            return

        self._cooldown -= dt
        if self._cooldown > 0:
            return

        my_ship = world.get_component(entity_id, Ship)
        my_tf   = world.get_component(entity_id, Transform)
        if not my_ship or not my_tf:
            return

        # Find closest enemy in range
        target_id = self._find_target(world, entity_id, my_ship.team, my_tf)
        if target_id is None:
            return

        # Deal damage
        from components.health import Health
        target_health = world.get_component(target_id, Health)
        if target_health:
            target_health.take_damage(self.damage)

        # Spawn a visual projectile
        self._spawn_projectile(world, my_tf, target_id)

        self._cooldown = 1.0 / self.fire_rate

    def _find_target(self, world, my_id, my_team, my_tf):
        from components.health import Health
        closest_dist = self.range
        closest_id   = None
        for eid in world.get_entities_with(Transform, Ship, Health):
            if eid == my_id:
                continue
            other_ship = world.get_component(eid, Ship)
            if other_ship.team == my_team:
                continue   # don't shoot friendlies
            other_tf = world.get_component(eid, Transform)
            dist = my_tf.distance_to(other_tf)
            if dist < closest_dist:
                closest_dist = dist
                closest_id   = eid
        return closest_id

    def _spawn_projectile(self, world, origin_tf, target_id):
        """Create a short-lived projectile entity."""
        from components.health import Health
        target_tf = world.get_component(target_id, Transform)
        if not target_tf:
            return

        from factories.projectile_factory import spawn_projectile
        spawn_projectile(
            world,
            ox=origin_tf.x, oy=origin_tf.y,
            tx=target_tf.x, ty=target_tf.y,
            color=(0, 200, 255),   # cyan laser
            speed=600,
            lifetime=0.5,
        )
