"""
RenderSystem — draws everything onto the screen.

Drawing order (back to front):
  1. Starfield background (static)
  2. Projectiles
  3. Ships (shapes, selection rings, health bars)
  4. UI overlay (HUD, minimap) — drawn by the scene, not here
"""
import math
import pygame
from components.transform import Transform
from components.renderable import Renderable
from components.selectable import Selectable
from components.health import Health
from components.ship import Ship
from config import TEAM_COLORS, SELECTION_RING_COLOR


class RenderSystem:
    def __init__(self, camera, screen: pygame.Surface):
        self.camera = camera
        self.screen = screen
        self._stars = self._generate_stars(300)

    def update(self, world, dt: float, events: list):
        self._draw_background()
        self._draw_projectiles(world)
        self._draw_ships(world)

    # ------------------------------------------------------------------

    def _draw_background(self):
        self.screen.fill((5, 5, 15))   # near-black space
        for sx, sy, brightness in self._stars:
            # Stars are in screen-fixed positions (parallax can be added later)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness),
                               (sx, sy), 1)

    def _draw_projectiles(self, world):
        from systems.projectile import Projectile
        for eid in world.get_entities_with(Transform, Projectile):
            tf   = world.get_component(eid, Transform)
            proj = world.get_component(eid, Projectile)
            sx, sy = self.camera.world_to_screen(tf.x, tf.y)
            # Draw as a short line in velocity direction
            speed = math.sqrt(proj.vx**2 + proj.vy**2)
            if speed > 0:
                nx = proj.vx / speed
                ny = proj.vy / speed
                length = proj.length * self.camera.zoom
                ex = sx + nx * length
                ey = sy + ny * length
                pygame.draw.line(self.screen, proj.color,
                                 (int(sx), int(sy)), (int(ex), int(ey)), 2)

    def _draw_ships(self, world):
        for eid in world.get_entities_with(Transform, Renderable, Ship):
            tf   = world.get_component(eid, Transform)
            rend = world.get_component(eid, Renderable)
            ship = world.get_component(eid, Ship)
            sel  = world.get_component(eid, Selectable)

            sx, sy = self.camera.world_to_screen(tf.x, tf.y)
            size   = max(4, rend.size * self.camera.zoom)
            color  = TEAM_COLORS.get(ship.team, rend.color)

            # Selection ring
            if sel and sel.selected:
                pygame.draw.circle(self.screen, SELECTION_RING_COLOR,
                                   (int(sx), int(sy)), int(size * 1.6), 1)

            # Ship shape
            self._draw_shape(rend.shape, sx, sy, size, tf.angle, color)

            # Health / shield bars
            hp = world.get_component(eid, Health)
            if hp:
                self._draw_health_bar(sx, sy, size, hp)

    def _draw_shape(self, shape: str, cx, cy, size, angle_deg, color):
        """Draw a polygon representing the ship hull."""
        rad = math.radians(angle_deg)

        if shape == "triangle":
            pts = _rotate_points([
                ( size,     0),
                (-size * 0.6,  size * 0.5),
                (-size * 0.6, -size * 0.5),
            ], rad, cx, cy)
            pygame.draw.polygon(self.screen, color, pts)
            # darker outline
            dark = tuple(max(0, c - 60) for c in color)
            pygame.draw.polygon(self.screen, dark, pts, 1)

        elif shape == "rect":
            pts = _rotate_points([
                ( size,      size * 0.4),
                ( size,     -size * 0.4),
                (-size,     -size * 0.4),
                (-size,      size * 0.4),
            ], rad, cx, cy)
            pygame.draw.polygon(self.screen, color, pts)
            dark = tuple(max(0, c - 60) for c in color)
            pygame.draw.polygon(self.screen, dark, pts, 1)
            # engine glow dot at rear
            ex = cx - math.cos(rad) * size
            ey = cy - math.sin(rad) * size
            pygame.draw.circle(self.screen, (100, 180, 255), (int(ex), int(ey)),
                                max(2, int(size * 0.25)))

        elif shape == "diamond":
            pts = _rotate_points([
                ( size,     0),
                ( 0,        size * 0.55),
                (-size,     0),
                ( 0,       -size * 0.55),
            ], rad, cx, cy)
            pygame.draw.polygon(self.screen, color, pts)
            dark = tuple(max(0, c - 60) for c in color)
            pygame.draw.polygon(self.screen, dark, pts, 1)

    def _draw_health_bar(self, sx, sy, size, hp):
        bar_w = int(size * 2.4)
        bar_h = 4
        bx    = int(sx - bar_w // 2)
        by    = int(sy - size - 10)

        # Background
        pygame.draw.rect(self.screen, (60, 0, 0),
                         (bx, by, bar_w, bar_h))
        # HP fill
        fill_w = int(bar_w * hp.fraction_hp())
        pygame.draw.rect(self.screen, (50, 200, 50),
                         (bx, by, fill_w, bar_h))

        # Shield bar (above HP bar)
        if hp.max_shields > 0:
            pygame.draw.rect(self.screen, (0, 0, 80),
                             (bx, by - bar_h - 2, bar_w, bar_h))
            sfill = int(bar_w * hp.fraction_shields())
            pygame.draw.rect(self.screen, (80, 120, 255),
                             (bx, by - bar_h - 2, sfill, bar_h))

    # ------------------------------------------------------------------

    def _generate_stars(self, count: int):
        import random
        from config import SCREEN_WIDTH, SCREEN_HEIGHT
        return [
            (random.randint(0, SCREEN_WIDTH),
             random.randint(0, SCREEN_HEIGHT),
             random.randint(80, 200))
            for _ in range(count)
        ]


def _rotate_points(pts, rad, cx, cy):
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    result = []
    for x, y in pts:
        rx = x * cos_a - y * sin_a + cx
        ry = x * sin_a + y * cos_a + cy
        result.append((int(rx), int(ry)))
    return result
