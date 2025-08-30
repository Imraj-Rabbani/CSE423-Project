from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from collections import deque

camera_pos = (0, 500, 1300)
fovY = 90
GRID_LENGTH = 2000

TILE_SIZE = 80
MAZE_WIDTH = 25
MAZE_HEIGHT = 25
PLAYER_RADIUS = 30

player_pos = [12, 12]  
player_lives = 3
player_score = 0
pellets = []
maze = []

ghosts = []
GHOST_RADIUS = 25
GHOST_MOVE_DELAY = 500  
last_ghost_move_time = 0

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.target_x = x
        self.target_y = y

    #Using BFS to find the shortest path
    def find_path_to_player(self):
        player_x, player_y = player_pos
        queue = deque()
        visited = set()
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            
            if can_move_to(new_x, new_y):
                queue.append((new_x, new_y, 1, (dx, dy)))
                visited.add((new_x, new_y))
        
        if not queue:
            return None
        
        while queue:
            x, y, distance, first_move = queue.popleft()
            if x == player_x and y == player_y:
                return first_move
            
            for dx, dy in directions:
                new_x = x + dx
                new_y = y + dy
                
                if (new_x, new_y) not in visited and can_move_to(new_x, new_y):
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, distance + 1, first_move))
        
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            if can_move_to(new_x, new_y):
                return (dx, dy)
        
        return None
    
    def update(self):
        move = self.find_path_to_player()
        if move:
            dx, dy = move
            new_x = self.x + dx
            new_y = self.y + dy
            
            if can_move_to(new_x, new_y):
                self.x = new_x
                self.y = new_y

def init_ghosts():
    global ghosts
    ghosts = []
    ghost_color = (1.0, 0.0, 0.0)
    ghost_position = (1, 1)
    
    x, y = ghost_position
    if can_move_to(x, y):
        ghosts.append(Ghost(x, y, ghost_color))

def check_ghost_collision():
    global player_lives, player_pos
    
    for ghost in ghosts:
        if ghost.x == player_pos[0] and ghost.y == player_pos[1]:
            player_lives -= 1
            player_pos = [12, 12]
            ghost.x = 1
            ghost.y = 1
            break

def update_ghosts():
    global last_ghost_move_time
    current_time = glutGet(GLUT_ELAPSED_TIME)
    if current_time - last_ghost_move_time > GHOST_MOVE_DELAY:
        for ghost in ghosts:
            ghost.update()
        last_ghost_move_time = current_time

def draw_ghosts():
    for ghost in ghosts:
        glPushMatrix()
        world_x = (ghost.x - MAZE_WIDTH//2) * TILE_SIZE
        world_y = (ghost.y - MAZE_HEIGHT//2) * TILE_SIZE
        
        glTranslatef(world_x, world_y, GHOST_RADIUS)
        glColor3f(*ghost.color)
        gluSphere(gluNewQuadric(), GHOST_RADIUS, 15, 15)
        glPushMatrix()
        glTranslatef(-8, 8, 10)
        glColor3f(1, 1, 1)  
        gluSphere(gluNewQuadric(), 3, 8, 8)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(8, 8, 10)
        glColor3f(1, 1, 1)  
        gluSphere(gluNewQuadric(), 3, 8, 8)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-8, 8, 12)
        glColor3f(0, 0, 0)
        gluSphere(gluNewQuadric(), 1, 6, 6)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(8, 8, 12)
        glColor3f(0, 0, 0)  
        gluSphere(gluNewQuadric(), 1, 6, 6)
        glPopMatrix()
        
        glPopMatrix()

def init_maze():
    global maze
    maze = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,0,1,0,1,1,0,0,0,0,0,1,1,0,1,0,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
        [1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,1,0,1,0,0,0,0,0,1],
        [1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,0,0,0,0,1],
        [1,1,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
        [1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

def init_pellets():
    global pellets
    pellets = []
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 0:
                pellets.append([x, y])

def is_wall(x, y):
    if x < 0 or x >= MAZE_WIDTH or y < 0 or y >= MAZE_HEIGHT:
        return True
    return maze[y][x] == 1

def can_move_to(x, y):
    return not is_wall(x, y)

def collect_pellet(x, y):
    global player_score, pellets
    for i, pellet in enumerate(pellets):
        if pellet[0] == x and pellet[1] == y:
            pellets.pop(i)
            player_score += 10
            break

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
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
    glPushMatrix()
    world_x = (player_pos[0] - MAZE_WIDTH//2) * TILE_SIZE
    world_y = (player_pos[1] - MAZE_HEIGHT//2) * TILE_SIZE
    
    glTranslatef(world_x, world_y, PLAYER_RADIUS)
    glColor3f(1.0, 1.0, 0.0)
    gluSphere(gluNewQuadric(), PLAYER_RADIUS, 20, 20)

    glPushMatrix()
    glTranslatef(-6, 6, 12)
    glColor3f(0, 0, 0)  # Black eyes
    gluSphere(gluNewQuadric(), 2, 10, 10)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(6, 6, 12)
    glColor3f(0, 0, 0)  # Black eyes
    gluSphere(gluNewQuadric(), 2, 10, 10)
    glPopMatrix()
    
    glPopMatrix()

def draw_maze():
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:  
                glPushMatrix()
                world_x = (x - MAZE_WIDTH//2) * TILE_SIZE
                world_y = (y - MAZE_HEIGHT//2) * TILE_SIZE
                glTranslatef(world_x, world_y, TILE_SIZE//2)
                
                if (x + y) % 3 == 0:
                    glColor3f(0.0, 0.0, 1.0)
                elif (x + y) % 3 == 1:
                    glColor3f(0.0, 0.3, 0.8)
                else:
                    glColor3f(0.2, 0.2, 0.9)
                
                glutSolidCube(TILE_SIZE)
                glPopMatrix()

def draw_pellets():
    glColor3f(1.0, 1.0, 0.8)
    
    for pellet in pellets:
        glPushMatrix()
        world_x = (pellet[0] - MAZE_WIDTH//2) * TILE_SIZE
        world_y = (pellet[1] - MAZE_HEIGHT//2) * TILE_SIZE
        glTranslatef(world_x, world_y, 8)
        gluSphere(gluNewQuadric(), 4, 8, 8)
        glPopMatrix()

def draw_game_info():
    draw_text(10, 770, f"Score: {player_score}")
    draw_text(10, 740, f"Lives: {player_lives}")
    draw_text(10, 710, f"Pellets: {len(pellets)}")
    draw_text(10, 680, "WASD: Move | Arrows: Camera | R: Reset")
    
    if player_lives <= 0:
        draw_text(350, 400, "GAME OVER!")
        draw_text(320, 370, "Press R to restart")
    
    if len(pellets) == 0:
        draw_text(370, 400, "YOU WIN!")
        draw_text(320, 370, "Press R to restart")

def move_player(dx, dy):
    global player_pos
    
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    if can_move_to(new_x, new_y):
        player_pos[0] = new_x
        player_pos[1] = new_y
        collect_pellet(new_x, new_y)

def reset_game():
    global player_pos, player_lives, player_score
    player_pos = [12, 12]
    player_lives = 3
    player_score = 0
    init_maze()
    init_pellets()
    init_ghosts()

def keyboardListener(key, x, y):
    global player_lives
    
    if player_lives <= 0 and key != b'r':
        return

    if key == b'w':
        move_player(0, -1)
    
    if key == b's':
        move_player(0, 1)
    
    if key == b'a':
        move_player(1, 0)
    
    if key == b'd':
        move_player(-1, 0)
    
    if key == b'r':
        reset_game()

def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    
    if key == GLUT_KEY_UP:
        z += 50
    
    if key == GLUT_KEY_DOWN:
        z -= 50
    
    if key == GLUT_KEY_LEFT:
        y -= 50
    
    if key == GLUT_KEY_RIGHT:
        y += 50
    
    camera_pos = (x, y, z)



def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    x, y, z = camera_pos
    gluLookAt(x, y, z,
              0, 0, 0,
              0, 0, 1)

def idle():
    update_ghosts()
    check_ghost_collision()
    
    glutPostRedisplay()

def showScreen():
    """Main display function"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    
    glBegin(GL_QUADS)
    glColor3f(0.1, 0.1, 0.1)  
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glEnd()
    
    draw_maze()
    draw_pellets()
    draw_pacman()
    draw_ghosts()
    draw_game_info()
    
    glutSwapBuffers()

def main():
    init_maze()
    init_pellets()
    init_ghosts()
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Pac-Man 3D Game")
    
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()