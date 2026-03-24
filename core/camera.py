"""
Camera — translates between world coordinates and screen coordinates.

World : the large game map (e.g. 6000 × 6000 pixels)
Screen: the visible window (e.g. 1280 × 720 pixels)

Usage
-----
camera.world_to_screen(world_x, world_y) → (screen_x, screen_y)
camera.screen_to_world(screen_x, screen_y) → (world_x, world_y)
"""
import pygame
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT,
                    CAMERA_PAN_SPEED, CAMERA_EDGE_ZONE,
                    CAMERA_ZOOM_MIN, CAMERA_ZOOM_MAX, CAMERA_ZOOM_SPEED)


class Camera:
    def __init__(self):
        # Camera looks at this world-space point (center of screen)
        self.x    = WORLD_WIDTH  / 2
        self.y    = WORLD_HEIGHT / 2
        self.zoom = 1.0

    # ------------------------------------------------------------------
    # Coordinate conversion
    # ------------------------------------------------------------------

    def world_to_screen(self, wx: float, wy: float) -> tuple:
        sx = (wx - self.x) * self.zoom + SCREEN_WIDTH  / 2
        sy = (wy - self.y) * self.zoom + SCREEN_HEIGHT / 2
        return (sx, sy)

    def screen_to_world(self, sx: float, sy: float) -> tuple:
        wx = (sx - SCREEN_WIDTH  / 2) / self.zoom + self.x
        wy = (sy - SCREEN_HEIGHT / 2) / self.zoom + self.y
        return (wx, wy)

    # ------------------------------------------------------------------
    # Update (call every frame)
    # ------------------------------------------------------------------

    def update(self, dt: float, events: list):
        self._pan_keyboard(dt)
        self._pan_edge(dt)
        self._handle_zoom(events)
        self._clamp()

    def _pan_keyboard(self, dt: float):
        keys = pygame.key.get_pressed()
        speed = CAMERA_PAN_SPEED / self.zoom * dt
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]:
            self.y -= speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]:
            self.y += speed

    def _pan_edge(self, dt: float):
        """Pan when the mouse is near the window edge."""
        mx, my = pygame.mouse.get_pos()
        speed  = CAMERA_PAN_SPEED / self.zoom * dt
        if mx < CAMERA_EDGE_ZONE:
            self.x -= speed
        if mx > SCREEN_WIDTH - CAMERA_EDGE_ZONE:
            self.x += speed
        if my < CAMERA_EDGE_ZONE:
            self.y -= speed
        if my > SCREEN_HEIGHT - CAMERA_EDGE_ZONE:
            self.y += speed

    def _handle_zoom(self, events: list):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.zoom = min(self.zoom + CAMERA_ZOOM_SPEED, CAMERA_ZOOM_MAX)
                elif event.y < 0:
                    self.zoom = max(self.zoom - CAMERA_ZOOM_SPEED, CAMERA_ZOOM_MIN)

    def _clamp(self):
        half_w = (SCREEN_WIDTH  / 2) / self.zoom
        half_h = (SCREEN_HEIGHT / 2) / self.zoom
        self.x = max(half_w, min(self.x, WORLD_WIDTH  - half_w))
        self.y = max(half_h, min(self.y, WORLD_HEIGHT - half_h))
