from board import board
import pygame
import math
from random import randint

pygame.init()

# width and height of game screen
WIDTH = 500
HEIGHT = 300
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

n1 = HEIGHT // (len(board))
n2 = WIDTH // (len(board[0]))
PI = math.pi

# function to draw food and walls on screen
def draw_board():
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * n2 + (0.5 * n2), i * n1 + (0.5 * n1)), 4)
            # elif board[i][j] == 2:
            #     pygame.draw.circle(screen, 'white', (j * n2 + (0.5 * n2), i * n1 + (0.5 * n1)), 10)
            elif board[i][j] == 3:
                pygame.draw.line(screen, 'blue', (j * n2 + (0.5 * n2), i * n1),
                                 (j * n2 + (0.5 * n2), i * n1 + n1), 3)
            elif board[i][j] == 4:
                pygame.draw.line(screen, 'blue', (j * n2, i * n1 + (0.5 * n1)),
                                 (j * n2 + n2, i * n1 + (0.5 * n1)), 3)
            elif board[i][j] == 5:
                pygame.draw.arc(screen, 'blue', [(j * n2 - (n2 * 0.4)) - 2, (i * n1 + (0.5 * n1)), n2, n1],
                                0, PI / 2, 3)
            elif board[i][j] == 6:
                pygame.draw.arc(screen, 'blue',
                                [(j * n2 + (n2 * 0.5)), (i * n1 + (0.5 * n1)), n2, n1], PI / 2, PI, 3)
            elif board[i][j] == 7:
                pygame.draw.arc(screen, 'blue', [(j * n2 + (n2 * 0.5)), (i * n1 - (0.4 * n1)), n2, n1], PI,
                                3 * PI / 2, 3)
            elif board[i][j] == 8:
                pygame.draw.arc(screen, 'blue',
                                [(j * n2 - (n2 * 0.4)) - 2, (i * n1 - (0.4 * n1)), n2, n1], 3 * PI / 2,
                                2 * PI, 3)
            elif board[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * n2, i * n1 + (0.5 * n1)),
                                 (j * n2 + n2, i * n1 + (0.5 * n1)), 3)

# loads images of pacman
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'player_images/{i}.png'),(n2, n1)))

# starting position of pacman
px = 9
py = 5
score = 0
counter = 0

# function to draw pacman on screen
def draw_player():
    screen.blit(player_images[counter // 5], (px * n2, py * n1))

# function to check valid moves
allowed_turns = [True, False, False, False]
def check_position(px, py):
    allowed_turns = [False, False, False, False]

    # Check if the position is within the board and not a wall
    if (px < len(board[0]) - 1 and board[py][px + 1] < 3):
        allowed_turns[0] = True
    if (px > 0 and board[py][px - 1] < 3):
        allowed_turns[1] = True
    if (py > 0 and board[py - 1][px] < 3):
        allowed_turns[2] = True
    if (py < len(board) - 1 and board[py + 1][px] < 3):
        allowed_turns[3] = True
    
    return allowed_turns


# function to move pacman or ghost based on chosen direction
def move(x, y, direction):
    if direction == 0:
        x += 1
    if direction == 1:
        x -= 1
    if direction == 2:
        y -= 1
    if direction == 3:
        y += 1  

    return (x, y)


# loads ghosts images
ghosts = []
ghosts.append(pygame.transform.scale(pygame.image.load(f'ghosts_images/inky.png'),(n2, n1)))
ghosts.append( pygame.transform.scale(pygame.image.load(f'ghosts_images/clyde.png'),(n2, n1)))

# starting position of ghosts
ix = 9
iy = 2
cx = 10
cy = 2

# function to draw ghosts on screen
def draw_ghosts():
    screen.blit(ghosts[0], (ix * n2, iy * n1))
    screen.blit(ghosts[1], (cx * n2, cy * n1))


# implementation of minimax algorithms with alpha beta pruning
def minimax(state, depth, a, b, is_maximizer):
    if depth == 0:
        return e_utility(state), state

    if is_maximizer:
        best_score = float('-inf')
        best_state = None
        for child_state in get_possible_moves(state, depth):
            score, _ = minimax(child_state, depth - 1, a, b, False)
            if score > best_score:
                best_score = score
                best_state = child_state
            if best_score > b:
                break
            a = max(a, best_score)
        return best_score, best_state
    else:
        best_score = float('inf')
        best_state = None
        for child_state in get_possible_moves(state, depth):
            if depth % 3 == 1:
                score, _ = minimax(child_state, depth - 1, a, b, True) 
            else:
                score, _ = minimax(child_state, depth - 1, a, b, False) 
            if score < best_score:
                best_score = score
                best_state = child_state
            if best_score < a:
                break
            b = min(b, best_score)
        return best_score, best_state


# calculates manhattan distance between two given points
def manhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# evaluation function
def e_utility(state):
    pacman_position = state[0]
    ghost1_position = state[1]
    ghost2_position = state[2]
    score = 0

    # Calculate the Manhattan distance between Pacman and each ghost
    distance_to_ghost1 = abs(pacman_position[0] - ghost1_position[0]) + abs(pacman_position[1] - ghost1_position[1])
    distance_to_ghost2 = abs(pacman_position[0] - ghost2_position[0]) + abs(pacman_position[1] - ghost2_position[1])

    if board[pacman_position[1]][pacman_position[0]] == 1:
        score += 100
    else: # finds the distance to nearst food
        closest, _ = food(pacman_position)
        score += min(distance_to_ghost2, distance_to_ghost1) / (closest * 100)

    # checks wehther pacman is getting too close to ghosts
    if distance_to_ghost1 == 0 or distance_to_ghost2 == 0:
        score -= 100000
    elif distance_to_ghost1 <= 5 or distance_to_ghost2 <= 5:
        score -= 10000
    else:
        score += 1000

    # checks whether pacman is between ghosts and has no way out
    if py == iy and py == cy:
        if (px > ix and px < cx) or (px > cx and px < ix):
            score -= 1000
    if px == ix and px == cx:
        if (py > iy and py < cy) or (py > cy and py < iy):
            score -= 1000

# checks if pacman is stuck in a corner
    if len(get_possible_moves(state, 3)) <= 1:
        score -= 100

    return score
    

# finds the distance to closest food and also count of all foods
def food(pos):
    closest = float('inf')
    c = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if j == pos[0] and i == pos[1]:
                continue
            if (board[i][j] == 1):
                dis = manhattanDistance(pos, (j, i))
                if dis < closest:
                    closest = dis
                c += 1
    return closest, c


# finds all possible moves and states
def get_possible_moves(state, depth):
    pacman_position = state[0]
    ghost1_position = state[1]
    ghost2_position = state[2]
    possible_moves = []
    
    # Check all four possible directions for Pacman
    if depth % 3 == 0:
        for direction in range(4):
            new_pacman_position = move(pacman_position[0], pacman_position[1], direction)
            
            # Check if the new position is within the board and not a wall (less than 2)
            if (0 <= new_pacman_position[0] < len(board[0])) and (0 <= new_pacman_position[1] < len(board)) and (board[new_pacman_position[1]][new_pacman_position[0]] < 2):
                new_state = [new_pacman_position, ghost1_position, ghost2_position]
                possible_moves.append(new_state)
    # Check all four possible directions for ghost 1
    elif depth % 3 == 2:
        for direction in range(4):
            new_ghost1_position = move(ghost1_position[0], ghost1_position[1], direction)
            
            # Check if the new position is within the board and not a wall (less than 2)
            if (0 <= new_ghost1_position[0] < len(board[0])) and (0 <= new_ghost1_position[1] < len(board)) and (board[new_ghost1_position[1]][new_ghost1_position[0]] < 2):
                new_state = [pacman_position, new_ghost1_position, ghost2_position]
                possible_moves.append(new_state)
    
    # Check all four possible directions for ghost 2
    elif depth % 3 == 1:
        for direction in range(4):
            new_ghost2_position = move(ghost2_position[0], ghost2_position[1], direction)
            
            # Check if the new position is within the board and not a wall (less than 2)
            if (0 <= new_ghost2_position[0] < len(board[0])) and (0 <= new_ghost2_position[1] < len(board)) and (board[new_ghost2_position[1]][new_ghost2_position[0]] < 2):
                new_state = [pacman_position, ghost1_position, new_ghost2_position]
                possible_moves.append(new_state)        
    
    return possible_moves

# function for moving ghosts randomly
def move_randomly(x, y):
    allowed_turns = check_position(x, y)
    direction = randint(0, 3)
    while (allowed_turns[direction] == False):
        direction = randint(0, 3)
    x, y = move(x, y, direction)
    return x, y


if __name__ == '__main__':
    run = True
    st = 0 # 0 is for ongoing game, 1 for win and 2 for game over
    while run:
        # frame per second
        timer.tick(fps)
        # for contrlling pacman images and opening and closing its mouth
        if counter < 19:
            counter += 1
        else:
            counter = 0
        # fills the screen black then draws board, pacman and ghosts
        screen.fill('black')
        draw_board()
        draw_player()
        draw_ghosts()
        
        # if game is still going on
        if st == 0:

            state = [(px, py), (ix, iy), (cx, cy)]  # Current state
            _, best_move = minimax(state, 3, float('-inf'), float('inf'), True)  # Depth 3 and maximizing player (Pacman)
            px, py = best_move[0][0], best_move[0][1]  # Update Pacman's position
            score -= 1
            # update the board if pacman has eaten a food and increse the score
            if(board[py][px] == 1):
                board[py][px] = 0
                score += 10

            # moves ghosts randomly
            ix, iy = move_randomly(ix, iy)
            cx, cy = move_randomly(cx, cy)


        # checks wether collision with ghosts has occured and pacman lost the game
        if px == ix and py == iy:
            st = 2
        elif px == cx and py == cy:
            st = 2

        # checks wether pacman has won the game and no food is left
        _,c = food((0,0))
        if c == 0:
            st = 1

        # for printing out the score on screen
        score_text = font.render(f'Score: {score}', True, 'white')
        screen.blit(score_text, (10, 10))

        # if won, print won on screen
        if st == 1:  
            score_text = font.render(f'WON', True, 'yellow')
            screen.blit(score_text, (WIDTH//2 - 25, HEIGHT//2 - 20))
        # if lost, print game over on screen
        elif st == 2:
            score_text = font.render(f'GAME OVER', True, 'yellow')
            screen.blit(score_text, (WIDTH//2 - 60, HEIGHT//2 - 20))

        # for quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        pygame.display.flip()


    pygame.quit()