"""
Selectable — marks an entity as something the player can click/box-select.
"""


class Selectable:
    def __init__(self):
        self.selected: bool = False
