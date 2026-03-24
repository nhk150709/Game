"""
Transform — position and rotation of any game object.
"""
import math


class Transform:
    def __init__(self, x: float = 0.0, y: float = 0.0, angle: float = 0.0):
        self.x     = x       # world-space X
        self.y     = y       # world-space Y
        self.angle = angle   # degrees, 0 = pointing right

    def position(self) -> tuple:
        return (self.x, self.y)

    def distance_to(self, other) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def angle_to(self, tx: float, ty: float) -> float:
        """Return angle in degrees toward target point."""
        return math.degrees(math.atan2(ty - self.y, tx - self.x))
