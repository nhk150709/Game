"""
Game — the top-level loop. Manages scenes and the Pygame clock.
"""
import sys
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, FPS


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock  = pygame.time.Clock()
        self._scene = None
        self._load_battle()

    def _load_battle(self):
        from scenes.battle import BattleScene
        self._scene = BattleScene(self.screen)

    def run(self):
        while True:
            dt     = self.clock.tick(FPS) / 1000.0   # seconds
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        self._load_battle()   # restart

            self._scene.update(dt, events)
            self._scene.draw()
            pygame.display.flip()
