"""
ProjectileSystem — moves visual projectile entities and removes expired ones.
"""
import math
from components.transform import Transform


class _Projectile:
    """Component attached to projectile entities."""
    def __init__(self, vx, vy, lifetime, color, length=8):
        self.vx       = vx
        self.vy       = vy
        self.lifetime = lifetime
        self.color    = color
        self.length   = length


# Make it importable from components
import sys, types
_mod = types.ModuleType("components.projectile")
_mod.Projectile = _Projectile
sys.modules["components.projectile"] = _mod

Projectile = _Projectile


class ProjectileSystem:
    def update(self, world, dt: float, events: list):
        for eid in list(world.get_entities_with(Transform, Projectile)):
            proj = world.get_component(eid, Projectile)
            tf   = world.get_component(eid, Transform)

            tf.x += proj.vx * dt
            tf.y += proj.vy * dt
            proj.lifetime -= dt

            if proj.lifetime <= 0:
                world.destroy_entity(eid)
