"""
SelectionSystem — Homeworld-style unit selection.

Controls
--------
Left-click          : select single unit (deselects others)
Left-click + drag   : box-select all friendly units in rectangle
Ctrl + left-click   : add/remove unit from selection
Right-click (space) : move selected units to cursor (formation)
Right-click (enemy) : attack order on clicked enemy

1-5 keys            : recall/assign fleet group
Ctrl + 1-5          : assign selected ships to fleet group N
"""
import math
import pygame
from components.transform import Transform
from components.selectable import Selectable
from components.ship import Ship
from components.orders import Orders
from components.health import Health


class SelectionSystem:
    def __init__(self, camera):
        self.camera        = camera
        self._drag_start   = None   # screen-space start of box drag
        self._dragging     = False
        # Fleet groups: {1: [entity_id, …], 2: […], …}
        self._groups: dict = {i: [] for i in range(1, 10)}

    # ------------------------------------------------------------------
    # Public surface: call this to draw the selection box each frame
    # ------------------------------------------------------------------

    def draw_selection_box(self, surface: pygame.Surface):
        if not self._dragging or self._drag_start is None:
            return
        mx, my = pygame.mouse.get_pos()
        x1, y1 = self._drag_start
        rect = pygame.Rect(
            min(x1, mx), min(y1, my),
            abs(mx - x1), abs(my - y1)
        )
        box_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        box_surf.fill((0, 255, 100, 40))
        surface.blit(box_surf, (rect.x, rect.y))
        pygame.draw.rect(surface, (0, 255, 100), rect, 1)

    # ------------------------------------------------------------------
    # System update
    # ------------------------------------------------------------------

    def update(self, world, dt: float, events: list):
        ctrl_held = pygame.key.get_mods() & pygame.KMOD_CTRL

        for event in events:
            # ---- Mouse button down ----
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left click
                    self._drag_start = event.pos
                    self._dragging   = False

                elif event.button == 3:  # right click
                    self._handle_right_click(world, event.pos, ctrl_held)

            # ---- Mouse motion ----
            elif event.type == pygame.MOUSEMOTION:
                if self._drag_start:
                    dx = event.pos[0] - self._drag_start[0]
                    dy = event.pos[1] - self._drag_start[1]
                    if math.sqrt(dx*dx + dy*dy) > 4:
                        self._dragging = True

            # ---- Mouse button up ----
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self._dragging:
                        self._finish_box_select(world, event.pos, ctrl_held)
                    else:
                        self._handle_click(world, self._drag_start, ctrl_held)
                    self._drag_start = None
                    self._dragging   = False

            # ---- Keyboard ----
            elif event.type == pygame.KEYDOWN:
                self._handle_key(world, event, ctrl_held)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _handle_click(self, world, pos, ctrl_held: bool):
        clicked = self._entity_at_screen(world, pos)
        if clicked is None:
            if not ctrl_held:
                self._deselect_all(world)
            return

        clicked_ship = world.get_component(clicked, Ship)
        if not clicked_ship or clicked_ship.team != "player":
            return

        if not ctrl_held:
            self._deselect_all(world)

        sel = world.get_component(clicked, Selectable)
        if sel:
            sel.selected = not sel.selected if ctrl_held else True

    def _finish_box_select(self, world, end_pos, ctrl_held: bool):
        if not self._drag_start:
            return
        x1, y1 = self._drag_start
        x2, y2 = end_pos
        box = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))

        if not ctrl_held:
            self._deselect_all(world)

        for eid in world.get_entities_with(Transform, Selectable, Ship):
            ship = world.get_component(eid, Ship)
            if ship.team != "player":
                continue
            tf = world.get_component(eid, Transform)
            sx, sy = self.camera.world_to_screen(tf.x, tf.y)
            if box.collidepoint(sx, sy):
                world.get_component(eid, Selectable).selected = True

    def _handle_right_click(self, world, pos, ctrl_held: bool):
        # Check if right-clicked on an enemy
        target = self._entity_at_screen(world, pos)
        if target is not None:
            target_ship = world.get_component(target, Ship)
            if target_ship and target_ship.team == "enemy":
                self._order_attack(world, target)
                return

        # Move order to world position
        wx, wy = self.camera.screen_to_world(*pos)
        self._order_move(world, wx, wy)

    def _order_move(self, world, wx: float, wy: float):
        """Send selected ships to (wx, wy) in a loose formation."""
        selected = self._get_selected(world)
        n = len(selected)
        if n == 0:
            return

        # Offset ships in a grid so they don't all pile on same spot
        cols  = math.ceil(math.sqrt(n))
        spacing = 40
        for i, eid in enumerate(selected):
            col = i % cols
            row = i // cols
            offset_x = (col - cols / 2) * spacing
            offset_y = (row - cols / 2) * spacing
            ord_ = world.get_component(eid, Orders)
            if ord_:
                ord_.set_move(wx + offset_x, wy + offset_y)

    def _order_attack(self, world, target_id: int):
        for eid in self._get_selected(world):
            ord_ = world.get_component(eid, Orders)
            if ord_:
                ord_.set_attack(target_id)

    def _handle_key(self, world, event, ctrl_held: bool):
        if event.key in range(pygame.K_1, pygame.K_6):  # keys 1-5
            group_num = event.key - pygame.K_0
            if ctrl_held:
                # Assign selected ships to group
                self._groups[group_num] = [
                    eid for eid in self._get_selected(world)
                ]
            else:
                # Recall group
                self._deselect_all(world)
                for eid in self._groups.get(group_num, []):
                    if world.is_alive(eid):
                        sel = world.get_component(eid, Selectable)
                        if sel:
                            sel.selected = True

    def _entity_at_screen(self, world, pos):
        wx, wy = self.camera.screen_to_world(*pos)
        for eid in world.get_entities_with(Transform, Ship):
            ship = world.get_component(eid, Ship)
            tf   = world.get_component(eid, Transform)
            dx   = wx - tf.x
            dy   = wy - tf.y
            if math.sqrt(dx*dx + dy*dy) <= ship.radius:
                return eid
        return None

    def _deselect_all(self, world):
        for eid in world.get_entities_with(Selectable):
            world.get_component(eid, Selectable).selected = False

    def _get_selected(self, world) -> list:
        return [
            eid for eid in world.get_entities_with(Selectable, Ship)
            if world.get_component(eid, Selectable).selected
        ]
