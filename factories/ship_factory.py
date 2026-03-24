"""
ShipFactory — creates ship entities from preset definitions.

Adding a new ship type
----------------------
1. Add a key to SHIP_PRESETS below (or load from data/ships/*.json)
2. Call spawn_ship(world, "my_ship_type", x, y, team="player")

The preset dict keys map directly to component properties.
"""
from components.transform import Transform
from components.physics import Physics
from components.health import Health
from components.renderable import Renderable
from components.selectable import Selectable
from components.ship import Ship
from components.orders import Orders
from config import TEAM_COLORS

# ---------------------------------------------------------------------------
# Ship presets — tweak stats here or load from JSON
# ---------------------------------------------------------------------------

SHIP_PRESETS = {
    "fighter": {
        "radius":       10,
        "shape":        "triangle",
        "size":         10,
        "hp":           60,
        "max_speed":    180,
        "acceleration": 120,
        "turn_speed":   150,
        "modules":      ["laser_cannon"],
    },
    "cruiser": {
        "radius":       22,
        "shape":        "rect",
        "size":         22,
        "hp":           250,
        "shields":      80,
        "max_speed":    90,
        "acceleration": 50,
        "turn_speed":   60,
        "modules":      ["laser_cannon", "missile_launcher", "deflector_shield"],
    },
    "carrier": {
        "radius":       35,
        "shape":        "diamond",
        "size":         35,
        "hp":           600,
        "shields":      200,
        "max_speed":    55,
        "acceleration": 30,
        "turn_speed":   30,
        "modules":      ["missile_launcher", "deflector_shield"],
    },
}


def spawn_ship(world, ship_type: str, x: float, y: float,
               team: str = "player") -> int:
    """Create and return a ship entity."""
    preset = SHIP_PRESETS.get(ship_type)
    if preset is None:
        raise ValueError(f"Unknown ship type: '{ship_type}'. "
                         f"Valid types: {list(SHIP_PRESETS)}")

    color  = TEAM_COLORS.get(team, (180, 180, 180))
    eid    = world.create_entity()

    world.add_component(eid, Transform(x=x, y=y, angle=-90))
    world.add_component(eid, Physics(
        max_speed    = preset.get("max_speed",    150),
        acceleration = preset.get("acceleration", 80),
        turn_speed   = preset.get("turn_speed",   120),
    ))
    world.add_component(eid, Health(
        hp          = preset.get("hp", 100),
        max_hp      = preset.get("hp", 100),
        shields     = preset.get("shields", 0),
        max_shields = preset.get("shields", 0),
    ))
    world.add_component(eid, Renderable(
        shape = preset.get("shape", "triangle"),
        size  = preset.get("size", 12),
        color = color,
    ))
    world.add_component(eid, Ship(
        ship_class = ship_type,
        team       = team,
        radius     = preset.get("radius", 12),
    ))
    world.add_component(eid, Selectable())
    world.add_component(eid, Orders())

    # Attach modules
    ship_comp = world.get_component(eid, Ship)
    for mod_name in preset.get("modules", []):
        module = _build_module(mod_name)
        if module:
            module.on_attach(world, eid)
            ship_comp.add_module(module)

    return eid


def _build_module(name: str):
    """Instantiate a module by name string."""
    try:
        if name == "laser_cannon":
            from modules.weapons.laser_cannon import LaserCannon
            return LaserCannon()
        if name == "missile_launcher":
            from modules.weapons.missile_launcher import MissileLauncher
            return MissileLauncher()
        if name == "deflector_shield":
            from modules.shields.deflector_shield import DeflectorShield
            return DeflectorShield()
        if name == "ion_drive":
            from modules.engines.ion_drive import IonDrive
            return IonDrive()
    except ImportError as e:
        print(f"[ShipFactory] Could not load module '{name}': {e}")
    return None
