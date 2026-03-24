"""
Helpers for spawning projectile entities.
"""
import math
from components.transform import Transform
from systems.projectile import Projectile


def spawn_projectile(world, ox: float, oy: float,
                     tx: float, ty: float,
                     color=(0, 200, 255),
                     speed: float = 600,
                     lifetime: float = 0.5):
    """Spawn a visual projectile from (ox,oy) aimed at (tx,ty)."""
    dx = tx - ox
    dy = ty - oy
    dist = math.sqrt(dx*dx + dy*dy) or 1
    vx = dx / dist * speed
    vy = dy / dist * speed

    eid = world.create_entity()
    world.add_component(eid, Transform(ox, oy))
    world.add_component(eid, Projectile(vx, vy, lifetime, color))
    return eid
