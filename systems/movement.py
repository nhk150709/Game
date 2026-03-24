"""
MovementSystem — steers ships toward their current order destination.

For each ship with Orders + Physics + Transform:
  1. Point toward destination
  2. Accelerate
  3. Apply drag
  4. Clamp to max speed
  5. Move position
"""
import math
from components.transform import Transform
from components.physics import Physics
from components.orders import Orders
from components.ship import Ship


class MovementSystem:
    def update(self, world, dt: float, events: list):
        for eid in world.get_entities_with(Transform, Physics, Orders, Ship):
            tf   = world.get_component(eid, Transform)
            phys = world.get_component(eid, Physics)
            ord_ = world.get_component(eid, Orders)

            tx, ty = self._resolve_target(world, eid, ord_, tf)

            if tx is None:
                # No destination — apply drag and stop
                phys.vx *= phys.drag
                phys.vy *= phys.drag
            else:
                dx = tx - tf.x
                dy = ty - tf.y
                dist = math.sqrt(dx * dx + dy * dy)

                if dist < ord_.arrival_radius:
                    # Arrived
                    if ord_.order_type == "move":
                        ord_.set_idle()
                    phys.vx *= phys.drag
                    phys.vy *= phys.drag
                else:
                    # Turn toward target
                    desired_angle = math.degrees(math.atan2(dy, dx))
                    angle_diff    = _angle_diff(desired_angle, tf.angle)
                    max_turn      = phys.turn_speed * dt
                    if abs(angle_diff) < max_turn:
                        tf.angle = desired_angle
                    else:
                        tf.angle += math.copysign(max_turn, angle_diff)

                    # Accelerate in facing direction
                    rad = math.radians(tf.angle)
                    phys.vx += math.cos(rad) * phys.acceleration * dt
                    phys.vy += math.sin(rad) * phys.acceleration * dt

                    # Clamp speed
                    speed = math.sqrt(phys.vx ** 2 + phys.vy ** 2)
                    if speed > phys.max_speed:
                        scale = phys.max_speed / speed
                        phys.vx *= scale
                        phys.vy *= scale

            # Move
            tf.x += phys.vx * dt
            tf.y += phys.vy * dt

            # Clamp to world bounds
            from config import WORLD_WIDTH, WORLD_HEIGHT
            tf.x = max(0, min(tf.x, WORLD_WIDTH))
            tf.y = max(0, min(tf.y, WORLD_HEIGHT))

    def _resolve_target(self, world, eid, ord_, tf):
        """Return (tx, ty) or (None, None) for idle."""
        if ord_.order_type == "idle":
            return None, None
        if ord_.order_type == "move":
            return ord_.target_x, ord_.target_y
        if ord_.order_type in ("attack", "follow"):
            tid = ord_.target_entity
            if tid is None or not world.is_alive(tid):
                ord_.set_idle()
                return None, None
            other_tf = world.get_component(tid, Transform)
            if other_tf:
                return other_tf.x, other_tf.y
        if ord_.order_type == "patrol":
            if not ord_.waypoints:
                ord_.set_idle()
                return None, None
            wx, wy = ord_.waypoints[0]
            dx, dy = wx - tf.x, wy - tf.y
            if math.sqrt(dx*dx + dy*dy) < ord_.arrival_radius:
                ord_.waypoints.append(ord_.waypoints.pop(0))  # cycle
            return ord_.waypoints[0]
        return None, None


def _angle_diff(target: float, current: float) -> float:
    """Return shortest signed difference between two angles (degrees)."""
    diff = (target - current + 180) % 360 - 180
    return diff
