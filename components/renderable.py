"""
Renderable — describes how to draw a ship when there is no sprite.

Shapes are drawn procedurally so the game runs without any art assets.
Once you have real sprites, swap the render system to use pygame.image instead.
"""


class Renderable:
    def __init__(self, shape: str = "triangle", size: float = 14.0,
                 color: tuple = (60, 160, 255)):
        """
        shape : "triangle"  — pointed in the direction of travel (fighters)
                "rect"      — wider body (cruisers)
                "diamond"   — large carrier shape
        size  : radius/half-size of the shape in world pixels
        color : (R, G, B) tuple
        """
        self.shape = shape
        self.size  = size
        self.color = color
