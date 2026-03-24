"""
BattleScene — the main gameplay scene.

Spawns ships, registers systems, and drives the game loop.
Win/lose conditions are checked here.
"""
import random
import pygame
from ecs.world import World
from core.camera import Camera

from systems.render      import RenderSystem
from systems.movement    import MovementSystem
from systems.combat      import CombatSystem
from systems.module_system import ModuleSystem
from systems.selection   import SelectionSystem
from systems.ai          import AISystem
from systems.projectile  import ProjectileSystem

from factories.ship_factory import spawn_ship
from ui.hud      import HUD
from ui.minimap  import Minimap

from components.ship import Ship
from config import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT


class BattleScene:
    def __init__(self, screen: pygame.Surface):
        self.screen   = screen
        self.camera   = Camera()
        self.world    = World()
        self.font     = pygame.font.SysFont("monospace", 16)
        self.font_lg  = pygame.font.SysFont("monospace", 36)

        # UI
        self.hud     = HUD(self.font)
        self.minimap = Minimap()

        # Selection system needs camera reference
        self.selection_sys = SelectionSystem(self.camera)

        # Register systems (order matters!)
        self.world.add_system(self.selection_sys)
        self.world.add_system(AISystem())
        self.world.add_system(MovementSystem())
        self.world.add_system(ModuleSystem())
        self.world.add_system(CombatSystem())
        self.world.add_system(ProjectileSystem())
        self.world.add_system(RenderSystem(self.camera, screen))

        # Spawn initial ships
        self._spawn_scenario()

        # Point camera at player fleet
        self.camera.x = WORLD_WIDTH  * 0.25
        self.camera.y = WORLD_HEIGHT * 0.5

        self.game_over   = False
        self.player_won  = False

    # ------------------------------------------------------------------
    # Public interface called by main game loop
    # ------------------------------------------------------------------

    def update(self, dt: float, events: list):
        if not self.game_over:
            self.camera.update(dt, events)
            self.world.update(dt, events)
            self._check_win_lose()

    def draw(self):
        # World + ships are drawn by RenderSystem inside world.update()
        # Draw selection drag box on top
        self.selection_sys.draw_selection_box(self.screen)

        # UI
        self.hud.draw(self.screen, self.world, self.camera)
        self.minimap.draw(self.screen, self.world, self.camera)

        if self.game_over:
            self._draw_game_over()

    # ------------------------------------------------------------------
    # Scenario setup
    # ------------------------------------------------------------------

    def _spawn_scenario(self):
        cx = WORLD_WIDTH  / 2
        cy = WORLD_HEIGHT / 2

        # --- Player fleet (left side) ---
        player_x = cx * 0.5
        spawn_ship(self.world, "fighter", player_x - 60, cy - 80, "player")
        spawn_ship(self.world, "fighter", player_x,      cy - 40, "player")
        spawn_ship(self.world, "fighter", player_x - 60, cy + 80, "player")
        spawn_ship(self.world, "cruiser", player_x - 20, cy,      "player")

        # --- Enemy fleet (right side) ---
        enemy_x = cx * 1.5
        spawn_ship(self.world, "fighter", enemy_x + 60,  cy - 80, "enemy")
        spawn_ship(self.world, "fighter", enemy_x,       cy - 40, "enemy")
        spawn_ship(self.world, "fighter", enemy_x + 60,  cy + 80, "enemy")
        spawn_ship(self.world, "cruiser", enemy_x + 20,  cy,      "enemy")

        # Optional: uncomment to add carriers
        # spawn_ship(self.world, "carrier", player_x - 100, cy, "player")
        # spawn_ship(self.world, "carrier", enemy_x  + 100, cy, "enemy")

    # ------------------------------------------------------------------
    # Win / lose
    # ------------------------------------------------------------------

    def _check_win_lose(self):
        player_alive = any(
            world_has_team(self.world, "player")
        )
        enemy_alive = any(
            world_has_team(self.world, "enemy")
        )
        if not player_alive:
            self.game_over  = True
            self.player_won = False
        elif not enemy_alive:
            self.game_over  = True
            self.player_won = True

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - HUD_HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        if self.player_won:
            msg   = "VICTORY"
            color = (100, 255, 120)
        else:
            msg   = "DEFEAT"
            color = (255, 80, 80)

        txt = self.font_lg.render(msg, True, color)
        self.screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2,
                               SCREEN_HEIGHT // 2 - 60))
        sub = self.font.render("Press R to restart  |  ESC to quit", True,
                               (180, 180, 200))
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2,
                               SCREEN_HEIGHT // 2))


def world_has_team(world, team: str):
    for eid in world.get_entities_with(Ship):
        s = world.get_component(eid, Ship)
        if s.team == team:
            yield eid
