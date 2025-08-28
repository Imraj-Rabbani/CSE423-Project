# Global variables to store Pac-Man's position
pacman_x, pacman_y, pacman_z = 0, 10, 0 # Example starting position
pacman_radius = 15 # Size of the Pac-Man sphere

def draw_pacman():
    """
    Draws a yellow sphere to represent Pac-Man at its current location.
    This logic is based on the draw_shapes function in 3D_OpenGL_Intro.py.
    """
    glPushMatrix() # Save the current matrix state
    
    # Set Pac-Man's color to yellow
    glColor3f(1.0, 1.0, 0.0) #
    
    # Move to Pac-Man's current position in the 3D world
    glTranslatef(pacman_x, pacman_y, pacman_z) #
    
    # Create the sphere
    # gluSphere(quadric, radius, slices, stacks)
    gluSphere(gluNewQuadric(), pacman_radius, 32, 32) #
    
    glPopMatrix() # Restore the previous matrix state

# This function would then be called from within your main display callback (e.g., showScreen)
# glutDisplayFunc(showScreen) -> showScreen() calls draw_pacman()