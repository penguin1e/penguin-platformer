"""
Game settings and configuration constants.
Contains screen dimensions, level settings, player parameters, and color definitions.
"""

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Level dimensions
LEVEL_WIDTH = SCREEN_WIDTH * 10  # 10 times screen width
LEVEL_HEIGHT = SCREEN_HEIGHT

# Camera settings
CAMERA_OFFSET = 300  # Space to keep ahead of player in the direction they're facing

# Game settings
FPS = 60

# Player settings
PLAYER_SPEED = 5
PLAYER_JUMP_FORCE = -18.5
PLAYER_GRAVITY = 1.0

# Colors
SKY_COLOR = '#87CEEB'  # Light blue for sky
SNOW_COLOR = '#FFFFFF'  # White for snow
ICE_COLOR = '#ADD8E6'  # Light blue for ice 