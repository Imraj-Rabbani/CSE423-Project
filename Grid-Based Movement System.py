# --- Feature 2: Full Code for Grid-Based Movement ---

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- 1. State Management Variables ---
# Grid and movement properties
TILE_SIZE = 30.0
MOVE_SPEED = 2.0 # How fast Pac-Man moves between tiles

# Player state
# The 'direction' variable stores the next intended move from keyboard input.
direction = "STOP"
# 'is_moving' prevents new moves while one is in progress.
is_moving = False
# Player's position in grid units.
player_grid_x, player_grid_z = 0, 0
# Player's position in world coordinates (matches the variables from Feature 1).
pacman_x, pacman_z = 0.0, 0.0

# --- 2. Input Handling ---
def specialKeyListener(key, x, y):
    """
    Captures arrow key presses to set the player's next direction.
    Based on the input handling in Lets_draw_sth.py.
    """
    global direction
    # A new direction can only be set if Pac-Man is not already moving.
    if not is_moving:
        if key == GLUT_KEY_UP:
            direction = "UP"
        elif key == GLUT_KEY_DOWN:
            direction = "DOWN"
        elif key == GLUT_KEY_LEFT:
            direction = "LEFT"
        elif key == GLUT_KEY_RIGHT:
            direction = "RIGHT"

# --- 3. Animation and Movement Logic ---
def animate():
    """
    The main game loop for handling movement logic.
    This function should be registered with glutIdleFunc.
    """
    global pacman_x, pacman_z, player_grid_x, player_grid_z, is_moving, direction
    
    # If a move is not in progress, check if a new direction has been set.
    if not is_moving:
        if direction == "UP":
            player_grid_z -= 1
            is_moving = True
        elif direction == "DOWN":
            player_grid_z += 1
            is_moving = True
        elif direction == "LEFT":
            player_grid_x -= 1
            is_moving = True
        elif direction == "RIGHT":
            player_grid_x += 1
            is_moving = True
        # After processing the direction, reset it to "STOP"
        direction = "STOP"

    # If a move is in progress, smoothly update world coordinates towards the target tile.
    if is_moving:
        target_x = player_grid_x * TILE_SIZE
        target_z = player_grid_z * TILE_SIZE

        # Move horizontally
        if pacman_x < target_x:
            pacman_x = min(pacman_x + MOVE_SPEED, target_x)
        elif pacman_x > target_x:
            pacman_x = max(pacman_x - MOVE_SPEED, target_x)
        
        # Move vertically (on the Z-axis)
        if pacman_z < target_z:
            pacman_z = min(pacman_z + MOVE_SPEED, target_z)
        elif pacman_z > target_z:
            pacman_z = max(pacman_z - MOVE_SPEED, target_z)

        # If Pac-Man has reached the center of the target tile, stop moving.
        if pacman_x == target_x and pacman_z == target_z:
            is_moving = False
            
    # Tell GLUT that the screen needs to be redrawn.
    glutPostRedisplay() #


# --- Example of how to register the callbacks in your main function ---
# glutSpecialFunc(specialKeyListener) #
# glutIdleFunc(animate)             #