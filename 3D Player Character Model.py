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