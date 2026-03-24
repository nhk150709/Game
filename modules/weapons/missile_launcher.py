"""
Missile Launcher — fires a slower, homing projectile that deals heavy damage.

Great for cruisers; too slow for fighters.
"""
from modules.base_module import BaseModule
from components.transform import Transform
from components.ship import Ship


class MissileLauncher(BaseModule):
    name = "Missile Launcher"

    def __init__(self, damage: float = 60.0, range: float = 500.0,
                 fire_rate: float = 0.4):
        super().__init__()
        self.damage    = damage
        self.range     = range
        self.fire_rate = fire_rate
        self._cooldown = 0.0

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

        target_id = self._find_target(world, entity_id, my_ship.team, my_tf)
        if target_id is None:
            return

        from components.health import Health
        target_health = world.get_component(target_id, Health)
        if target_health:
            target_health.take_damage(self.damage)

        target_tf = world.get_component(target_id, Transform)
        if target_tf:
            from factories.projectile_factory import spawn_projectile
            spawn_projectile(
                world,
                ox=my_tf.x, oy=my_tf.y,
                tx=target_tf.x, ty=target_tf.y,
                color=(255, 140, 0),   # orange missile
                speed=300,
                lifetime=1.5,
            )

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
                continue
            other_tf = world.get_component(eid, Transform)
            dist = my_tf.distance_to(other_tf)
            if dist < closest_dist:
                closest_dist = dist
                closest_id   = eid
        return closest_id
