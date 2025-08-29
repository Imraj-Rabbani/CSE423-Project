from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_pos = (0, 500, 500)
fovY = 120
GRID_LENGTH = 600

# Game constants
TILE_SIZE = 60
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
PLAYER_RADIUS = 25

# Game state variables
player_pos = [7, 7]  # Grid position (x, y)
player_lives = 3
player_score = 0
pellets = []
maze = []

def init_maze():
    """Initialize the maze with walls (1) and empty spaces (0)"""
    global maze
    maze = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,0,1,0,1,0,1,0,1,0,1,0,1,1],
        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [1,1,0,1,0,1,0,1,0,1,0,1,0,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

def init_pellets():
    """Initialize pellets in empty maze spaces"""
    global pellets
    pellets = []
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 0:  # Empty space
                pellets.append([x, y])

def is_wall(x, y):
    """Check if position is a wall"""
    if x < 0 or x >= MAZE_WIDTH or y < 0 or y >= MAZE_HEIGHT:
        return True
    return maze[y][x] == 1

def can_move_to(x, y):
    """Check if player can move to this position"""
    return not is_wall(x, y)

def collect_pellet(x, y):
    """Collect pellet at position if it exists"""
    global player_score, pellets
    for i, pellet in enumerate(pellets):
        if pellet[0] == x and pellet[1] == y:
            pellets.pop(i)
            player_score += 10
            break

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Draw text on screen"""
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_pacman():
    """Draw the 3D Pac-Man character (Feature 1: 3D Player Character Model)"""
    glPushMatrix()
    
    # Convert grid position to world coordinates
    world_x = (player_pos[0] - MAZE_WIDTH//2) * TILE_SIZE
    world_y = (player_pos[1] - MAZE_HEIGHT//2) * TILE_SIZE
    
    glTranslatef(world_x, world_y, PLAYER_RADIUS)
    
    # Draw Pac-Man as a yellow sphere
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    gluSphere(gluNewQuadric(), PLAYER_RADIUS, 20, 20)
    
    # Add some detail - draw eyes
    glPushMatrix()
    glTranslatef(-8, 8, 15)
    glColor3f(0, 0, 0)  # Black eyes
    gluSphere(gluNewQuadric(), 3, 10, 10)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(8, 8, 15)
    glColor3f(0, 0, 0)  # Black eyes
    gluSphere(gluNewQuadric(), 3, 10, 10)
    glPopMatrix()
    
    glPopMatrix()

def draw_maze():
    """Draw the 3D maze walls"""
    glColor3f(0.0, 0.0, 1.0)  # Blue walls
    
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:  # Wall
                glPushMatrix()
                world_x = (x - MAZE_WIDTH//2) * TILE_SIZE
                world_y = (y - MAZE_HEIGHT//2) * TILE_SIZE
                glTranslatef(world_x, world_y, TILE_SIZE//2)
                glutSolidCube(TILE_SIZE)
                glPopMatrix()

def draw_pellets():
    """Draw pellets (Feature 4: Standard Pellet Collection)"""
    glColor3f(1.0, 1.0, 1.0)  # White pellets
    glPointSize(8)
    
    for pellet in pellets:
        glPushMatrix()
        world_x = (pellet[0] - MAZE_WIDTH//2) * TILE_SIZE
        world_y = (pellet[1] - MAZE_HEIGHT//2) * TILE_SIZE
        glTranslatef(world_x, world_y, 10)
        gluSphere(gluNewQuadric(), 5, 8, 8)
        glPopMatrix()

def draw_game_info():
    """Draw game information (Features 13 & 14: Life System and Scoring)"""
    # Draw score
    draw_text(10, 770, f"Score: {player_score}")
    
    # Draw lives
    draw_text(10, 740, f"Lives: {player_lives}")
    
    # Draw pellets remaining
    draw_text(10, 710, f"Pellets: {len(pellets)}")
    
    # Game over message
    if player_lives <= 0:
        draw_text(400, 400, "GAME OVER!")
        draw_text(350, 370, "Press R to restart")
    
    # Victory message
    if len(pellets) == 0:
        draw_text(400, 400, "YOU WIN!")
        draw_text(350, 370, "Press R to restart")

def move_player(dx, dy):
    """Move player with grid-based movement (Feature 2: Grid-Based Movement System)"""
    global player_pos
    
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    
    # Check if movement is valid
    if can_move_to(new_x, new_y):
        player_pos[0] = new_x
        player_pos[1] = new_y
        
        # Collect pellet if present
        collect_pellet(new_x, new_y)

def reset_game():
    """Reset the game to initial state"""
    global player_pos, player_lives, player_score
    player_pos = [7, 7]
    player_lives = 3
    player_score = 0
    init_maze()
    init_pellets()

def keyboardListener(key, x, y):
    """Handle keyboard input for player movement"""
    global player_lives
    
    if player_lives <= 0:
        return
    
    # Move up (W key)
    if key == b'w':
        move_player(0, 1)
    
    # Move down (S key) 
    if key == b's':
        move_player(0, -1)
    
    # Move left (A key)
    if key == b'a':
        move_player(-1, 0)
    
    # Move right (D key)
    if key == b'd':
        move_player(1, 0)
    
    # Reset game (R key)
    if key == b'r':
        reset_game()

def specialKeyListener(key, x, y):
    """Handle special key inputs for camera movement"""
    global camera_pos
    x, y, z = camera_pos
    
    # Move camera up
    if key == GLUT_KEY_UP:
        z += 20
    
    # Move camera down
    if key == GLUT_KEY_DOWN:
        z -= 20
    
    # Move camera left
    if key == GLUT_KEY_LEFT:
        x -= 20
    
    # Move camera right
    if key == GLUT_KEY_RIGHT:
        x += 20
    
    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    """Handle mouse input"""
    pass

def setupCamera():
    """Configure camera settings"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    x, y, z = camera_pos
    gluLookAt(x, y, z,
              0, 0, 0,
              0, 0, 1)

def idle():
    """Idle function for continuous updates"""
    glutPostRedisplay()

def showScreen():
    """Main display function"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    
    # Draw floor
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)  # Dark gray floor
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glEnd()
    
    # Draw game elements
    draw_maze()
    draw_pellets()
    draw_pacman()
    draw_game_info()
    
    glutSwapBuffers()

def main():
    """Initialize and start the game"""
    # Initialize game state
    init_maze()
    init_pellets()
    
    # Initialize OpenGL
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Pac-Man 3D Game")
    
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    
    # Register callback functions
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main()