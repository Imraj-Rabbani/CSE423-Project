from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random
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
player_last_direction = (0, 0)
power_pellets = []
special_pellet_pos = None
is_vulnerable = False
vulnerable_timer = 0
VULNERABILITY_DURATION = 7000 
BLINK_THRESHOLD = 2000       
GHOST_HOUSE_POS = (12, 11) 
can_break_walls = False
wall_break_timer = 0
WALL_BREAK_DURATION = 7000 

ghosts = []
GHOST_RADIUS = 25
GHOST_MOVE_DELAY = 500  
last_ghost_move_time = 0

current_level = 1
BASE_GHOST_MOVE_DELAY = 500 

def is_game_over():
    return player_lives <= 0 or len(pellets) == 0

class Ghost:
    def __init__(self, x, y, color, ghost_type=1):
        self.x = x
        self.y = y
        self.color = color
        self.ghost_type = ghost_type
        self.patrol_path = []
        self.patrol_index = 0
        self.is_chasing = False
        self.state = 'CHASING'
        if ghost_type == 3:
            self.init_patrol_path()
    
    def init_patrol_path(self):
        patrol_points = []
        quadrant_x_start = 12
        quadrant_x_end = 24
        quadrant_y_start = 12
        quadrant_y_end = 24
        
        for x in range(quadrant_x_start, quadrant_x_end + 1):
            for y in range(quadrant_y_start, quadrant_y_end + 1):
                if can_move_to(x, y):
                    patrol_points.append((x, y))
        
        if len(patrol_points) >= 4:
            self.patrol_path = [
                patrol_points[0],
                patrol_points[len(patrol_points)//3],
                patrol_points[len(patrol_points)//2],
                patrol_points[-1]
            ]
        else:
            self.patrol_path = patrol_points
    
    def find_path_to_player(self):
        if self.ghost_type == 1:
            return self.find_pursuit_path()
        elif self.ghost_type == 2:
            return self.find_intercept_path()
        elif self.ghost_type == 3:
            return self.find_patrol_or_chase_path()
    
    def find_patrol_or_chase_path(self):
        player_x, player_y = player_pos
        if player_x >= 12 and player_y >= 12:
            self.is_chasing = True
            return self.find_pursuit_path()
        else:
            self.is_chasing = False
            return self.find_patrol_path()
    
    def find_patrol_path(self):
        if not self.patrol_path:
            return None
        
        target_x, target_y = self.patrol_path[self.patrol_index]
        
        if self.x == target_x and self.y == target_y:
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_path)
            if len(self.patrol_path) > 1:
                target_x, target_y = self.patrol_path[self.patrol_index]
        
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
            
            if x == target_x and y == target_y:
                return first_move
            
            for dx, dy in directions:
                new_x = x + dx
                new_y = y + dy
                
                if (new_x, new_y) not in visited and can_move_to(new_x, new_y):
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, distance + 1, first_move))
        
        return None
    
    def find_pursuit_path(self):
        player_x, player_y = player_pos
        from collections import deque
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
    
    def find_intercept_path(self):
        player_x, player_y = player_pos
        last_dx, last_dy = player_last_direction
        
        prediction_steps = 3
        target_x = player_x + (last_dx * prediction_steps)
        target_y = player_y + (last_dy * prediction_steps)
        
        if target_x < 0 or target_x >= MAZE_WIDTH or target_y < 0 or target_y >= MAZE_HEIGHT or is_wall(target_x, target_y):
            target_x, target_y = player_x, player_y

        from collections import deque
        
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
            if x == target_x and y == target_y:
                return first_move
            for dx, dy in directions:
                new_x = x + dx
                new_y = y + dy
                
                if (new_x, new_y) not in visited and can_move_to(new_x, new_y):
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, distance + 1, first_move))
        
        return self.find_pursuit_path()
    
    def update(self):
        move = self.find_path_to_player() # Ghost only needs to find the player now
            
        if move:
            dx, dy = move
            new_x, new_y = self.x + dx, self.y + dy
            if can_move_to(new_x, new_y):
                self.x, self.y = new_x, new_y


def next_level():
    global current_level, GHOST_MOVE_DELAY, player_pos, player_last_direction
    current_level += 1
    print(f"--- LEVEL {current_level} START ---")

    player_pos = [12, 12]

    init_pellets()
    init_power_pellets()
    init_ghosts()
    GHOST_MOVE_DELAY = max(100, BASE_GHOST_MOVE_DELAY - (current_level - 1) * 50)



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

def init_ghosts():
    global ghosts
    ghosts = []
    if can_move_to(1, 1):
        ghosts.append(Ghost(1, 1, (1.0, 0.0, 0.0), ghost_type=1))
    if can_move_to(23, 1):
        ghosts.append(Ghost(23, 1, (1.0, 0.5, 1.0), ghost_type=2))
    if can_move_to(23, 23):
        ghosts.append(Ghost(23, 23, (0.0, 1.0, 0.0), ghost_type=3))

def check_ghost_collision():
    global player_lives, player_pos, player_score
    
    for ghost in ghosts:
        if ghost.x == player_pos[0] and ghost.y == player_pos[1]:
            
            if ghost.state == 'VULNERABLE':
                player_score += 200
                
                if ghost.ghost_type == 1:
                    ghost.x, ghost.y = 1, 1
                elif ghost.ghost_type == 2:
                    ghost.x, ghost.y = 23, 1
                elif ghost.ghost_type == 3:
                    ghost.x, ghost.y = 23, 23
                
                ghost.state = 'CHASING'
                print("Ghost eaten and has instantly regenerated!")

            elif ghost.state == 'CHASING':
                player_lives -= 1
                player_pos = [12, 12] 
            
                for g in ghosts:
                    if g.ghost_type == 1: g.x, g.y = 1, 1
                    elif g.ghost_type == 2: g.x, g.y = 23, 1
                    elif g.ghost_type == 3: g.x, g.y = 23, 23
                    g.is_chasing = False; g.patrol_index = 0
                print("Caught by a ghost! Life lost.")
                break

def update_ghosts():
    global last_ghost_move_time
    
    if is_game_over():
        return
    
    current_time = time.time() * 1000
    if current_time - last_ghost_move_time > GHOST_MOVE_DELAY:
        for ghost in ghosts:
            ghost.update()
        last_ghost_move_time = current_time

def draw_ghosts():
    for ghost in ghosts:
        glPushMatrix()
        world_x = (ghost.x - MAZE_WIDTH//2) * TILE_SIZE; world_y = (ghost.y - MAZE_HEIGHT//2) * TILE_SIZE
        glTranslatef(world_x, world_y, GHOST_RADIUS)

        if ghost.state == 'VULNERABLE':
            time_left = vulnerable_timer - (time.time() * 1000)
            if time_left < BLINK_THRESHOLD and int(time.time() * 4) % 2 == 0: glColor3f(1.0, 1.0, 1.0)
            else: 
                glColor3f(1.0, 0.5, 0.0)
        else: 
            glColor3f(*ghost.color)
        
        gluSphere(gluNewQuadric(), GHOST_RADIUS, 15, 15)
        
        glPushMatrix()
        glTranslatef(-8, 8, 10); glColor3f(1, 1, 1); gluSphere(gluNewQuadric(), 3, 8, 8)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(8, 8, 10); glColor3f(1, 1, 1); gluSphere(gluNewQuadric(), 3, 8, 8)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-8, 8, 12); glColor3f(0, 0, 0); gluSphere(gluNewQuadric(), 1, 6, 6)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(8, 8, 12); glColor3f(0, 0, 0); gluSphere(gluNewQuadric(), 1, 6, 6)
        glPopMatrix()
        
        glPopMatrix()

def init_pellets():
    global pellets
    pellets = []
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 0:  
                pellets.append([x, y])

def init_power_pellets():
    global power_pellets
    power_pellets = [[1, 1], [23, 1], [1, 23], [23, 23]]

def spawn_special_pellet():
    global special_pellet_pos
    
    if not pellets and not power_pellets:
        special_pellet_pos = None
        return

    valid_positions = []
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 0 and (player_pos[0] != x or player_pos[1] != y):
                valid_positions.append((x, y))
    
    if valid_positions:
        special_pellet_pos = list(random.choice(valid_positions))

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

def collect_power_pellet(x, y):
    global power_pellets, is_vulnerable, vulnerable_timer, can_break_walls, wall_break_timer
    for i, pp in enumerate(power_pellets):
        if pp[0] == x and pp[1] == y:
            power_pellets.pop(i)
            
            is_vulnerable = True
            vulnerable_timer = time.time() * 1000 + VULNERABILITY_DURATION
            for g in ghosts:
                g.state = 'VULNERABLE'

            can_break_walls = True
            wall_break_timer = time.time() * 1000 + WALL_BREAK_DURATION

            print("Power Pellet collected! Ghosts are vulnerable and walls can be broken.") 
            break

def collect_special_pellet(x, y):
    global player_score, special_pellet_pos
    if special_pellet_pos and special_pellet_pos[0] == x and special_pellet_pos[1] == y:
        player_score += 50 
        print("Special Pellet collected for 50 points!")
        spawn_special_pellet()

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
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 2, 10, 10)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(6, 6, 12)
    glColor3f(0, 0, 0)
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


def draw_power_pellets():
    glColor3f(0.8, 1.0, 0.8)
    
    for pp in power_pellets:
        glPushMatrix()
        world_x = (pp[0] - MAZE_WIDTH//2) * TILE_SIZE
        world_y = (pp[1] - MAZE_HEIGHT//2) * TILE_SIZE
        glTranslatef(world_x, world_y, 12)
        gluSphere(gluNewQuadric(), 8, 10, 10)
        glPopMatrix()

def draw_special_pellet():
    if special_pellet_pos:
        glColor3f(0.0, 1.0, 1.0) 
        
        glPushMatrix()
        world_x = (special_pellet_pos[0] - MAZE_WIDTH//2) * TILE_SIZE
        world_y = (special_pellet_pos[1] - MAZE_HEIGHT//2) * TILE_SIZE
        glTranslatef(world_x, world_y, 12)
        gluSphere(gluNewQuadric(), 10, 12, 12) 
        glPopMatrix()


def draw_game_info():
    draw_text(10, 770, f"Score: {player_score}")
    draw_text(10, 740, f"Lives: {player_lives}")
    draw_text(10, 710, f"Level: {current_level}")
    draw_text(10, 680, f"Pellets: {len(pellets)}")
    draw_text(10, 650, "WASD: Move | Arrows: Camera | R: Reset")

    if can_break_walls:
        draw_text(370, 770, "WALL BREAKER ACTIVE!")

    if player_lives <= 0:
        draw_text(350, 400, "GAME OVER!")
        draw_text(320, 370, "Press R to restart")


def move_player(dx, dy):
    global player_pos, player_last_direction, maze, can_break_walls
    
    if is_game_over():
        return
    
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    
    if can_move_to(new_x, new_y):
        player_last_direction = (dx, dy)
        player_pos[0] = new_x
        player_pos[1] = new_y
        collect_pellet(new_x, new_y)
        collect_power_pellet(new_x, new_y)
        collect_special_pellet(new_x, new_y)

    elif is_wall(new_x, new_y) and can_break_walls:
        maze[new_y][new_x] = 0 
        can_break_walls = False 
        
        player_last_direction = (dx, dy)
        player_pos[0] = new_x
        player_pos[1] = new_y
        print("Wall broken!")

def reset_game():
    global player_pos, player_lives, player_score, player_last_direction, current_level
    global is_vulnerable, vulnerable_timer, can_break_walls, wall_break_timer
    player_pos = [12, 12]
    player_lives = 3
    player_score = 0
    player_last_direction = (0, 0)
    is_vulnerable = False
    vulnerable_timer = 0
    can_break_walls = False
    wall_break_timer = 0
    current_level = 1
    init_maze()
    init_pellets()
    init_power_pellets()
    spawn_special_pellet()
    init_ghosts()  

def keyboardListener(key, x, y):
    global player_lives
    
    if key == b'r':
        reset_game()
        return
    
    if is_game_over():
        return
    
    if key == b'w':
        move_player(0, -1)
    
    if key == b's':
        move_player(0, 1)
    
    if key == b'a':
        move_player(1, 0)
    
    if key == b'd':
        move_player(-1, 0)

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
    

def update_vulnerability():
    global is_vulnerable, vulnerable_timer
    
    if is_game_over():
        return
        
    if is_vulnerable:
        current_time = time.time() * 1000
        if current_time > vulnerable_timer:
            is_vulnerable = False
            for g in ghosts:
                if g.state == 'VULNERABLE':
                    g.state = 'CHASING'
            print("Vulnerability has worn off!")

def update_wall_break_timer():
    global can_break_walls, wall_break_timer
    
    if is_game_over():
        return
        
    if can_break_walls:
        current_time = time.time() * 1000
        if current_time > wall_break_timer:
            can_break_walls = False

def idle():
    update_vulnerability()
    update_wall_break_timer()
    update_ghosts()
    check_ghost_collision()

    if len(pellets) == 0 and player_lives > 0:
        next_level()

    glutPostRedisplay()


def showScreen():
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
    draw_power_pellets()
    draw_special_pellet()
    draw_pacman()
    draw_ghosts() 
    draw_game_info()
    
    glutSwapBuffers()

def main():
    init_maze()
    init_pellets()
    init_power_pellets()
    spawn_special_pellet()
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