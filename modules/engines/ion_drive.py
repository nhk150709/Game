"""
Ion Drive — boosts the ship's max speed and acceleration.

Attach multiple Ion Drives to go faster (stacks additively).
"""
from modules.base_module import BaseModule
from components.physics import Physics


class IonDrive(BaseModule):
    name = "Ion Drive"

    def __init__(self, speed_bonus: float = 30.0, accel_bonus: float = 20.0):
        super().__init__()
        self.speed_bonus = speed_bonus
        self.accel_bonus = accel_bonus
        self._applied    = False

    def on_attach(self, world, entity_id: int):
        phys = world.get_component(entity_id, Physics)
        if phys:
            phys.max_speed   += self.speed_bonus
            phys.acceleration+= self.accel_bonus
            self._applied = True

    def on_detach(self, world, entity_id: int):
        if self._applied:
            phys = world.get_component(entity_id, Physics)
            if phys:
                phys.max_speed   -= self.speed_bonus
                phys.acceleration-= self.accel_bonus

    def update(self, world, entity_id: int, dt: float):
        # Stats are applied once in on_attach, nothing to do each frame
        pass
