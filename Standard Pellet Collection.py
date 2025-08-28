# --- Feature 4: Full Code for Pellet Collection ---

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- 1. State Management Variables ---
# A list of tuples for each pellet's (x, z) grid coordinate.
# This would be generated based on your maze design.
pellets_list = [(1, 0), (2, 0), (3, 0), (1, 2), (2, 2), (3, 2)]
pellets_remaining = len(pellets_list)

# Player and maze properties (assumed to exist from other features)
player_grid_x, player_grid_z = 0, 0
is_moving = False # A flag that should be True while moving, False when on a tile
TILE_SIZE = 30
PELLET_RADIUS = 3

# Player score (part of Feature 14, but required here)
player_score = 0

# --- 2. Drawing Function ---
def draw_pellets():
    """
    Renders all pellets in the pellets_list as small white spheres.
    This function should be called from your main display callback.
   
    """
    glColor3f(1.0, 1.0, 1.0) # Set pellet color
    
    for grid_x, grid_z in pellets_list:
        # Convert grid coordinates to world coordinates for drawing
        world_x = grid_x * TILE_SIZE
        world_z = grid_z * TILE_SIZE
        
        glPushMatrix() # Save matrix state
        glTranslatef(world_x, 10, world_z) # Position the pellet
        gluSphere(gluNewQuadric(), PELLET_RADIUS, 16, 16) # Draw the pellet sphere
        glPopMatrix() # Restore matrix state

# --- 3. Game Logic for Collection ---
def check_and_collect_pellet():
    """
    Checks if the player is on a tile with a pellet and collects it.
    This function should be called in your main game loop (e.g., animate)
    ONLY when the player is stationary on a tile (is_moving == False).
    """
    global pellets_remaining, player_score
    
    current_tile = (player_grid_x, player_grid_z)
    
    if current_tile in pellets_list:
        pellets_list.remove(current_tile) # Remove pellet from the list
        pellets_remaining = len(pellets_list) # Update the counter
        
        # Add points for the pellet, as required by Feature 14 
        player_score += 10
        
        print(f"Pellet collected! Score: {player_score}, Remaining: {pellets_remaining}")

# --- Example of how to integrate into your animate/idle function ---
def animate():
    # ... (code for moving the player from one tile to the next) ...
    
    # This check happens once the player has arrived at a new tile.
    if not is_moving:
        check_and_collect_pellet()

    glutPostRedisplay() # Redraw the screen