"""
Ship — identity and module slots for a spaceship.

The 'modules' list holds active BaseModule instances.
The ship class (fighter / cruiser / carrier) is stored here so
systems can query it quickly.
"""


class Ship:
    def __init__(self, ship_class: str = "fighter", team: str = "player",
                 radius: float = 12.0):
        self.ship_class = ship_class   # "fighter", "cruiser", "carrier", …
        self.team       = team         # "player" or "enemy"
        self.radius     = radius       # collision / selection circle radius

        # Modules attached to this ship (list of BaseModule instances)
        self.modules: list = []

        # Which fleet group this ship belongs to (None = ungrouped)
        self.fleet_group: int | None = None

    def add_module(self, module):
        """Attach a module to this ship."""
        self.modules.append(module)

    def remove_module(self, module):
        self.modules.remove(module)

    def get_modules_of_type(self, module_type) -> list:
        return [m for m in self.modules if isinstance(m, module_type)]
