#-------------------------------- 3D Player Character Model.py -------------------------------#

# --- Feature 1: Full Code for 3D Player Model ---

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- 1. State Management Variables ---
# These variables define Pac-Man's appearance and position in the world.
# They should be global so they can be updated by the movement logic.
pacman_x, pacman_y, pacman_z = 0.0, 10.0, 0.0
PACMAN_RADIUS = 15

# --- 2. Drawing Function ---
def draw_pacman():
    """
    Draws the Pac-Man character model at its current world coordinates.
    This function should be called from your main display callback (e.g., showScreen).
    """
    # Set the color for Pac-Man to yellow.
    glColor3f(1.0, 1.0, 0.0) #

    # Use matrix transformations to position the character.
    # glPushMatrix saves the current coordinate system.
    glPushMatrix() #

    # Move the drawing origin to Pac-Man's current position.
    glTranslatef(pacman_x, pacman_y, pacman_z) #

    # Draw a solid sphere to represent Pac-Man.
    # The function requires a quadric object, which we create on the fly.
    gluSphere(gluNewQuadric(), PACMAN_RADIUS, 32, 32) #

    # glPopMatrix restores the coordinate system to its previous state.
    glPopMatrix() #

# --- Example of how to integrate into your display function ---
# def showScreen():
#     # ... (clear screen and setup camera) ...
#
#     draw_pacman() # Call the drawing function
#
#     glutSwapBuffers() #


#-------------------------------- Grid-Based Movement System.py -------------------------------#

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

#-------------------------------- Standard Pellet Collection.py -------------------------------#

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

#-------------------------------- Scoring System.py -------------------------------#

# --- Feature 14: Full Code for Scoring System ---

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- 1. State Management Variables ---
player_score = 0
POINTS_PELLET = 10
POINTS_GHOST = 200

# --- 2. UI Display Function ---
# This requires a pre-existing draw_text function like the one in 3D_OpenGL_Intro.py
def draw_text(x, y, text):
    # (Implementation from 3D_OpenGL_Intro.py would go here)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_score_ui():
    """
    Displays the current score on the screen.
   
    """
    score_text = f"Score: {player_score}"
    draw_text(10, 770, score_text)

# --- 3. Game Logic for Updating the Score ---
def update_score(event_type):
    """
    Updates the player's score based on a game event.
    'event_type' can be "PELLET" or "GHOST".
    """
    global player_score
    
    if event_type == "PELLET":
        player_score += POINTS_PELLET
        print(f"Score increased by {POINTS_PELLET}! Total: {player_score}")
    elif event_type == "GHOST":
        player_score += POINTS_GHOST
        print(f"Score increased by {POINTS_GHOST}! Total: {player_score}")

# --- Example of how to integrate into your game logic ---
# Pellet collection would call this function:
def check_and_collect_pellet():
    global pellets_list
    current_tile = (0, 0) # Assumes player_grid_x, player_grid_z exist
    if current_tile in pellets_list:
        pellets_list.remove(current_tile)
        update_score("PELLET") # Call the score update function

# Eating a ghost would also call this function:
import random
def animate():
    # SIMULATION: 1 in 800 chance per frame to simulate eating a ghost
    if random.randint(0, 800) == 1:
        update_score("GHOST") # Call the score update function

    # ... (other game logic) ...
    glutPostRedisplay() # Redraw the screen

#-------------------------------- Life System.py -------------------------------#

# --- Feature 13: Full Code for Life System ---

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- 1. State Management Variables ---
player_lives = 3
game_over = False

# Player's starting position (assumed)
START_GRID_X, START_GRID_Z = 0, 0
player_grid_x, player_grid_z = START_GRID_X, START_GRID_Z

# --- 2. UI Display Function ---
# This requires a pre-existing draw_text function like the one in 3D_OpenGL_Intro.py
def draw_text(x, y, text):
    # (Implementation from 3D_OpenGL_Intro.py would go here)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_lives_ui():
    """
    Displays the current number of lives on the screen.
   
    """
    lives_text = f"Lives: {player_lives}"
    draw_text(10, 740, lives_text)
    
    if game_over:
        draw_text(450, 400, "GAME OVER")

# --- 3. Game Logic for Losing a Life ---
def handle_ghost_collision():
    """
    This function is called when a collision with a non-vulnerable ghost occurs.
    It reduces lives and checks for game over.
    """
    global player_lives, game_over, player_grid_x, player_grid_z

    if game_over:
        return

    player_lives -= 1
    print(f"Hit by a ghost! Lives remaining: {player_lives}")

    if player_lives <= 0:
        game_over = True
        print("Game Over")
    else:
        # Reset player to starting position
        player_grid_x = START_GRID_X
        player_grid_z = START_GRID_Z
        # (You would also reset the world coordinates pacman_x, pacman_z here)

# --- Example of how to integrate into your animate/idle function ---
# This is a simulation function. In the real game, you'd detect collision with ghost models.
import random
def animate():
    if game_over:
        glutPostRedisplay()
        return

    # SIMULATION: 1 in 500 chance per frame to simulate being hit by a ghost
    if random.randint(0, 500) == 1:
        handle_ghost_collision()

    # ... (other game logic) ...
    glutPostRedisplay() # Redraw the screen

    