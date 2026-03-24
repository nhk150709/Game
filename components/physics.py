"""
Physics — velocity and movement properties.
"""


class Physics:
    def __init__(self, max_speed: float = 150.0, acceleration: float = 80.0,
                 turn_speed: float = 120.0, drag: float = 0.92):
        self.vx          = 0.0           # current velocity X
        self.vy          = 0.0           # current velocity Y
        self.max_speed   = max_speed     # pixels/second
        self.acceleration= acceleration  # pixels/second²
        self.turn_speed  = turn_speed    # degrees/second
        self.drag        = drag          # velocity multiplier each frame (< 1 = slowdown)
