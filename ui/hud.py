"""
HUD — the bottom panel showing selected ship info and game status.
"""
import pygame
from components.ship import Ship
from components.health import Health
from components.selectable import Selectable
from components.orders import Orders
from config import SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT, TEAM_COLORS


class HUD:
    def __init__(self, font: pygame.font.Font):
        self.font      = font
        self.font_sm   = pygame.font.SysFont("monospace", 13)
        self.panel_rect = pygame.Rect(0, SCREEN_HEIGHT - HUD_HEIGHT,
                                      SCREEN_WIDTH, HUD_HEIGHT)

    def draw(self, surface: pygame.Surface, world, camera):
        # Panel background
        panel = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
        panel.fill((10, 15, 30, 200))
        surface.blit(panel, self.panel_rect.topleft)
        pygame.draw.line(surface, (40, 80, 120),
                         (0, self.panel_rect.top),
                         (SCREEN_WIDTH, self.panel_rect.top), 1)

        selected = [
            eid for eid in world.get_entities_with(Selectable, Ship)
            if world.get_component(eid, Selectable).selected
        ]

        if not selected:
            self._draw_no_selection(surface)
        elif len(selected) == 1:
            self._draw_single(surface, world, selected[0])
        else:
            self._draw_multi(surface, world, selected)

        self._draw_controls_hint(surface)

    # ------------------------------------------------------------------

    def _draw_no_selection(self, surface):
        txt = self.font.render("No ships selected", True, (80, 100, 130))
        surface.blit(txt, (20, SCREEN_HEIGHT - HUD_HEIGHT + 20))

    def _draw_single(self, surface, world, eid):
        ship = world.get_component(eid, Ship)
        hp   = world.get_component(eid, Health)
        ord_ = world.get_component(eid, Orders)

        y0 = SCREEN_HEIGHT - HUD_HEIGHT + 14
        color = TEAM_COLORS.get(ship.team, (255,255,255))

        # Ship class
        label = self.font.render(ship.ship_class.upper(), True, color)
        surface.blit(label, (20, y0))

        # HP bar
        if hp:
            self._bar(surface, 20, y0 + 28, 180, 10,
                      hp.fraction_hp(), (50, 200, 50), "HP")
            if hp.max_shields > 0:
                self._bar(surface, 20, y0 + 44, 180, 10,
                          hp.fraction_shields(), (80, 120, 255), "SH")

        # Modules list
        modules = ship.modules
        mx = 220
        self.font_sm.render("MODULES", True, (100, 120, 160))
        surface.blit(self.font_sm.render("MODULES", True, (100,120,160)),
                     (mx, y0))
        for i, mod in enumerate(modules):
            clr = (80, 200, 80) if mod.enabled else (150, 60, 60)
            surface.blit(self.font_sm.render(f"• {mod.name}", True, clr),
                         (mx, y0 + 16 + i * 15))

        # Current order
        if ord_:
            order_str = f"Order: {ord_.order_type}"
            surface.blit(self.font_sm.render(order_str, True, (160,160,200)),
                         (20, y0 + 68))

    def _draw_multi(self, surface, world, selected):
        y0  = SCREEN_HEIGHT - HUD_HEIGHT + 14
        txt = self.font.render(f"{len(selected)} ships selected", True,
                               (160, 200, 255))
        surface.blit(txt, (20, y0))

        # Mini icons
        for i, eid in enumerate(selected[:12]):
            ship = world.get_component(eid, Ship)
            hp   = world.get_component(eid, Health)
            col  = TEAM_COLORS.get(ship.team, (255,255,255))
            bx   = 20 + i * 52
            by   = y0 + 30
            pygame.draw.rect(surface, col, (bx, by, 44, 44), 2)
            cls_txt = self.font_sm.render(ship.ship_class[:3].upper(), True, col)
            surface.blit(cls_txt, (bx + 4, by + 4))
            if hp:
                fill = int(44 * hp.fraction_hp())
                pygame.draw.rect(surface, (50, 180, 50), (bx, by + 38, fill, 4))

    def _draw_controls_hint(self, surface):
        hints = ("WASD/Arrows: pan  |  Scroll: zoom  |  "
                 "LClick: select  |  LDrag: box-select  |  "
                 "RClick: move/attack  |  Ctrl+1-5: group  |  1-5: recall")
        txt = self.font_sm.render(hints, True, (60, 80, 100))
        surface.blit(txt, (20, SCREEN_HEIGHT - 18))

    def _bar(self, surface, x, y, w, h, fraction, color, label=""):
        pygame.draw.rect(surface, (30, 30, 40), (x, y, w, h))
        pygame.draw.rect(surface, color, (x, y, int(w * fraction), h))
        pygame.draw.rect(surface, (60, 80, 100), (x, y, w, h), 1)
        if label:
            lbl = self.font_sm.render(label, True, (180, 180, 200))
            surface.blit(lbl, (x + w + 4, y - 1))
