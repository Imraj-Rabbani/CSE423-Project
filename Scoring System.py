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