"""
BaseModule — the interface every ship module must implement.

To create a new module:
1. Create a new .py file in modules/weapons/, modules/engines/, modules/shields/, etc.
2. Subclass BaseModule
3. Override update() with your logic
4. Attach it to a ship via ship_component.add_module(MyModule())

The world and entity_id let your module read/write any component.
"""


class BaseModule:
    """Abstract base class for all ship modules."""

    # Human-readable name shown in the HUD
    name: str = "Unknown Module"

    def __init__(self):
        self.enabled: bool = True   # can be toggled off without removing

    def on_attach(self, world, entity_id: int):
        """Called once when the module is added to a ship."""
        pass

    def on_detach(self, world, entity_id: int):
        """Called once when the module is removed from a ship."""
        pass

    def update(self, world, entity_id: int, dt: float):
        """
        Called every frame by the ModuleSystem.

        world      : the ECS World — use it to read/write components
        entity_id  : the ship this module is attached to
        dt         : seconds since last frame
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement update()"
        )
