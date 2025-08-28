# --- State Management Variables ---
TILE_SIZE = 30 # The size of one grid square in world coordinates
player_direction = 'STOP' # Can be 'UP', 'DOWN', 'LEFT', 'RIGHT', 'STOP'
player_grid_x, player_grid_z = 0, 0 # Player's position on the grid
is_moving = False # Flag to prevent changing direction mid-move

# --- Input Handling ---
def specialKeyListener(key, x, y):
    """
    Handles arrow key inputs to set the player's direction.
    Based on the specialKeyListener in Lets_draw_sth.py.
    """
    global player_direction
    # Only accept new input if not currently moving between tiles
    if not is_moving:
        if key == GLUT_KEY_UP:
            player_direction = 'UP'
        elif key == GLUT_KEY_DOWN:
            player_direction = 'DOWN'
        elif key == GLUT_KEY_LEFT:
            player_direction = 'LEFT'
        elif key == GLUT_KEY_RIGHT:
            player_direction = 'RIGHT'

# --- Movement Logic ---
def animate():
    """
    Updates Pac-Man's position one step at a time to move between tiles.
    This function is registered with glutIdleFunc.
    """
    global pacman_x, pacman_z, player_grid_x, player_grid_z, player_direction, is_moving
    
    # Calculate the target world coordinates based on grid position
    target_x = player_grid_x * TILE_SIZE
    target_z = player_grid_z * TILE_SIZE
    
    # If Pac-Man is at the target tile, check for a new direction
    if pacman_x == target_x and pacman_z == target_z:
        is_moving = False
        if player_direction == 'UP':
            player_grid_z -= 1
        elif player_direction == 'DOWN':
            player_grid_z += 1
        elif player_direction == 'LEFT':
            player_grid_x -= 1
        elif player_direction == 'RIGHT':
            player_grid_x += 1
        
        # Reset direction after setting the new target grid cell
        if player_direction != 'STOP':
            is_moving = True
            player_direction = 'STOP'

    # Code to smoothly move pacman_x and pacman_z towards target_x and target_z
    # (This involves incrementing the position by a small 'speed' value each frame)
    # ...
    
    glutPostRedisplay() # Request a screen redraw


# --- Registration in main function ---
# glutSpecialFunc(specialKeyListener)
# glutIdleFunc(animate)