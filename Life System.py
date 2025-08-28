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