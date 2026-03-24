"""
ECS World — the heart of the engine.

An Entity is just an integer ID.
A Component is a plain data object attached to an entity.
A System is logic that runs on all entities that have certain components.

Example usage
-------------
world = World()

# Create a ship entity
ship = world.create_entity()
world.add_component(ship, Transform(x=100, y=200))
world.add_component(ship, Health(hp=100))

# Query all entities that have both Transform and Health
for eid in world.get_entities_with(Transform, Health):
    t = world.get_component(eid, Transform)
    h = world.get_component(eid, Health)
    ...
"""


class World:
    def __init__(self):
        self._next_id: int = 0
        self._alive: set = set()
        # _components[entity_id][ComponentType] = component_instance
        self._components: dict = {}
        self._systems: list = []
        # Entities queued for deletion at end of frame
        self._to_destroy: list = []

    # ------------------------------------------------------------------
    # Entity management
    # ------------------------------------------------------------------

    def create_entity(self) -> int:
        eid = self._next_id
        self._next_id += 1
        self._alive.add(eid)
        self._components[eid] = {}
        return eid

    def destroy_entity(self, entity_id: int):
        """Queue entity for removal at end of frame (safe during iteration)."""
        self._to_destroy.append(entity_id)

    def _flush_destroyed(self):
        for eid in self._to_destroy:
            self._alive.discard(eid)
            self._components.pop(eid, None)
        self._to_destroy.clear()

    def is_alive(self, entity_id: int) -> bool:
        return entity_id in self._alive

    # ------------------------------------------------------------------
    # Component management
    # ------------------------------------------------------------------

    def add_component(self, entity_id: int, component):
        """Attach a component to an entity."""
        self._components[entity_id][type(component)] = component

    def remove_component(self, entity_id: int, component_type):
        self._components.get(entity_id, {}).pop(component_type, None)

    def get_component(self, entity_id: int, component_type):
        """Return the component, or None if the entity doesn't have it."""
        return self._components.get(entity_id, {}).get(component_type)

    def has_component(self, entity_id: int, *component_types) -> bool:
        comps = self._components.get(entity_id, {})
        return all(ct in comps for ct in component_types)

    def get_entities_with(self, *component_types) -> list:
        """Return a list of entity IDs that have ALL of the given component types."""
        return [
            eid for eid in self._alive
            if self.has_component(eid, *component_types)
        ]

    # ------------------------------------------------------------------
    # System management
    # ------------------------------------------------------------------

    def add_system(self, system):
        """Register a system. Systems run in the order they are added."""
        self._systems.append(system)

    def update(self, dt: float, events: list):
        """Advance every system by dt seconds, then remove dead entities."""
        for system in self._systems:
            system.update(self, dt, events)
        self._flush_destroyed()
