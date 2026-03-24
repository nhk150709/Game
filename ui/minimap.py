"""
Minimap — shows positions of all ships in the bottom-right corner.
"""
import pygame
from components.transform import Transform
from components.ship import Ship
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT,
                    MINIMAP_SIZE, MINIMAP_ALPHA, WORLD_WIDTH, WORLD_HEIGHT,
                    TEAM_COLORS)


class Minimap:
    def __init__(self):
        self.size   = MINIMAP_SIZE
        self.rect   = pygame.Rect(
            SCREEN_WIDTH - self.size - 8,
            SCREEN_HEIGHT - HUD_HEIGHT - self.size - 8,
            self.size, self.size
        )

    def draw(self, surface: pygame.Surface, world, camera):
        # Background
        mm = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        mm.fill((5, 10, 25, MINIMAP_ALPHA))

        # Draw all ships as dots
        for eid in world.get_entities_with(Transform, Ship):
            tf   = world.get_component(eid, Transform)
            ship = world.get_component(eid, Ship)
            mx   = int(tf.x / WORLD_WIDTH  * self.size)
            my   = int(tf.y / WORLD_HEIGHT * self.size)
            color = TEAM_COLORS.get(ship.team, (180, 180, 180))
            pygame.draw.circle(mm, color, (mx, my), 3)

        # Draw camera viewport rectangle
        vw = (SCREEN_WIDTH  / camera.zoom) / WORLD_WIDTH  * self.size
        vh = (SCREEN_HEIGHT / camera.zoom) / WORLD_HEIGHT * self.size
        vx = (camera.x / WORLD_WIDTH  * self.size) - vw / 2
        vy = (camera.y / WORLD_HEIGHT * self.size) - vh / 2
        pygame.draw.rect(mm, (100, 200, 100),
                         (int(vx), int(vy), int(vw), int(vh)), 1)

        surface.blit(mm, self.rect.topleft)
        pygame.draw.rect(surface, (40, 80, 120), self.rect, 1)
