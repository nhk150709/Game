# Space RTS

A 2D real-time strategy game with Homeworld-style fleet control, built in Python + Pygame.

## Quick Start

```bash
pip install pygame
python main.py
```

## Controls

| Action | Key / Mouse |
|---|---|
| Pan camera | WASD or Arrow keys |
| Zoom | Mouse scroll wheel |
| Select ship | Left-click |
| Box select | Left-click + drag |
| Add to selection | Ctrl + left-click |
| Move order | Right-click on empty space |
| Attack order | Right-click on enemy ship |
| Assign fleet group | Ctrl + 1–5 |
| Recall fleet group | 1–5 |
| Restart | R |
| Quit | ESC |

## Architecture

```
Game/
├── main.py                    ← Run this to start
├── config.py                  ← Global settings (speed, colors, screen size …)
│
├── ecs/
│   └── world.py               ← Entity-Component-System engine
│
├── components/                ← Data attached to entities
│   ├── transform.py           ←   position & rotation
│   ├── physics.py             ←   speed, acceleration
│   ├── health.py              ←   HP & shields
│   ├── ship.py                ←   ship class, team, module list
│   ├── renderable.py          ←   how to draw the ship
│   ├── selectable.py          ←   can the player click it?
│   └── orders.py              ←   current command (move/attack/patrol…)
│
├── modules/                   ← ★ Add new ship abilities here ★
│   ├── base_module.py         ←   interface all modules must implement
│   ├── weapons/
│   │   ├── laser_cannon.py    ←   fast, light damage
│   │   └── missile_launcher.py←  slow, heavy damage
│   ├── engines/
│   │   └── ion_drive.py       ←   speed & acceleration boost
│   └── shields/
│       └── deflector_shield.py←  regenerating shield HP
│
├── systems/                   ← Logic that runs every frame
│   ├── render.py              ←   draw everything
│   ├── movement.py            ←   steer ships toward their orders
│   ├── selection.py           ←   handle mouse clicks & drag-select
│   ├── combat.py              ←   shield regen, remove dead ships
│   ├── module_system.py       ←   run each ship's modules
│   ├── ai.py                  ←   enemy AI
│   └── projectile.py          ←   move & expire bullets
│
├── factories/
│   ├── ship_factory.py        ←   create ship entities from presets
│   └── projectile_factory.py  ←   create bullet entities
│
├── scenes/
│   └── battle.py              ←   the main battle scene
│
├── ui/
│   ├── hud.py                 ←   bottom panel (selected ship info)
│   └── minimap.py             ←   overview map (bottom-right)
│
├── core/
│   ├── game.py                ←   main loop & scene management
│   └── camera.py              ←   pan/zoom the view
│
└── data/
    └── ships/                 ←   ship stat files (JSON)
        ├── fighter.json
        ├── cruiser.json
        └── carrier.json
```

## How to Add a New Module

1. Create a file in `modules/weapons/`, `modules/engines/`, or `modules/shields/`
2. Subclass `BaseModule` and implement `update()`
3. Add its name to a ship preset in `factories/ship_factory.py`
4. Register it in `ship_factory._build_module()`

Example — a repair nanobots module:

```python
# modules/support/repair_nanobots.py
from modules.base_module import BaseModule
from components.health import Health

class RepairNanobots(BaseModule):
    name = "Repair Nanobots"

    def __init__(self, repair_rate: float = 5.0):
        super().__init__()
        self.repair_rate = repair_rate   # HP per second

    def update(self, world, entity_id, dt):
        hp = world.get_component(entity_id, Health)
        if hp:
            hp.hp = min(hp.hp + self.repair_rate * dt, hp.max_hp)
```

## How to Add a New Ship Type

Add a new entry to `SHIP_PRESETS` in `factories/ship_factory.py`:

```python
"battleship": {
    "radius": 30,
    "shape": "rect",
    "size": 30,
    "hp": 500,
    "shields": 150,
    "max_speed": 70,
    "acceleration": 40,
    "turn_speed": 45,
    "modules": ["laser_cannon", "missile_launcher", "deflector_shield"],
},
```

Then spawn it: `spawn_ship(world, "battleship", x, y, "player")`
