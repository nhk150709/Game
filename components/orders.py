"""
Orders — the current command a ship is executing.

Order types
-----------
"idle"   : do nothing
"move"   : fly to (target_x, target_y)
"attack" : attack entity target_entity_id
"patrol" : move between waypoints (list of (x,y) tuples)
"follow" : maintain position relative to target_entity_id
"""


class Orders:
    def __init__(self):
        self.order_type:     str   = "idle"
        self.target_x:       float = 0.0
        self.target_y:       float = 0.0
        self.target_entity:  int | None = None
        self.waypoints:      list  = []   # for patrol
        self.arrival_radius: float = 20.0  # stop this close to destination

    def set_move(self, x: float, y: float):
        self.order_type   = "move"
        self.target_x     = x
        self.target_y     = y
        self.target_entity = None

    def set_attack(self, entity_id: int):
        self.order_type    = "attack"
        self.target_entity = entity_id

    def set_patrol(self, waypoints: list):
        self.order_type = "patrol"
        self.waypoints  = list(waypoints)

    def set_follow(self, entity_id: int):
        self.order_type    = "follow"
        self.target_entity = entity_id

    def set_idle(self):
        self.order_type    = "idle"
        self.target_entity = None
