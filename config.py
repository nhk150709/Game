"""
Global game configuration.
Tweak these values to change how the game feels.
"""

# --- Window ---
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
WINDOW_TITLE  = "Space RTS"
FPS           = 60

# --- World (the full map size) ---
WORLD_WIDTH  = 6000
WORLD_HEIGHT = 6000

# --- Camera ---
CAMERA_PAN_SPEED  = 400   # pixels per second
CAMERA_EDGE_ZONE  = 40    # pixels from edge that trigger panning
CAMERA_ZOOM_MIN   = 0.25
CAMERA_ZOOM_MAX   = 2.5
CAMERA_ZOOM_SPEED = 0.15  # zoom per scroll tick

# --- Colors ---
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREY       = (120, 120, 120)
RED        = (220, 50,  50)
GREEN      = (50,  220, 50)
BLUE       = (50,  120, 220)
YELLOW     = (255, 220, 0)
CYAN       = (0,   220, 220)
ORANGE     = (255, 140, 0)
PURPLE     = (160, 60,  200)

# Team colors (feel free to add more for multiplayer later)
TEAM_COLORS = {
    "player": (60,  160, 255),   # blue
    "enemy":  (255, 70,  70),    # red
    "neutral":(180, 180, 180),   # grey
}

# --- Selection ---
SELECTION_BOX_COLOR = (0, 255, 100)
SELECTION_BOX_ALPHA = 40           # 0=transparent, 255=opaque
SELECTION_RING_COLOR = (0, 255, 100)

# --- UI ---
HUD_HEIGHT      = 130   # pixels, at the bottom
MINIMAP_SIZE    = 200   # square pixels, bottom-right
MINIMAP_ALPHA   = 180

# --- Combat ---
PROJECTILE_SPEED = 500  # pixels per second (world space)
