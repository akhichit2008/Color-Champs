import pygame
import sys
from concurrent.futures import ThreadPoolExecutor
from qlearning import ColorChampsQLearnig

# Define grid properties
grid_width = 10
grid_height = 10
block_size = 50 # Size of each grid block in pixels
screen_width = grid_width * block_size
screen_height = grid_height * block_size

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((grid_width * block_size, grid_height * block_size))
pygame.display.set_caption("Grid Click Example")

# Create a grid to store block colors
grid_colors = [[(0, 0, 0) for _ in range(grid_height)] for _ in range(grid_width)]

start_time = pygame.time.get_ticks()
timer_duration = 60000*5


player1_color = (255,0,0)
player2_color = (0,255,0)

red_colored_blocks = []
green_colored_blocks = []

game_over = [False,0]

p1 = 0 # initial scores
p2 = 0

font = pygame.font.SysFont("arial", 36)  # You can choose a different font and size

def start_game():
    screen.fill((255,255,255))
    title = font.render("Color Champs", True, (0, 0, 255))
    title_rect = title.get_rect()

    # Blit the timer onto the screen
    screen.blit(title,title_rect)
    pygame.display.flip()


def get_state(grid_colors,player1_lock,player2_lock):
    state = []

    for x in range(grid_width):
        for y in range(grid_height):
            if grid_colors[x][y] == (0,0,0):
                state.append(0) # Black Block
            elif grid_colors[x][y] == player1_color:
                state.append(1) # Red block
            elif grid_colors[x][y] == player2_color:
                state.append(2) # Green block
    if player1_lock:
        state.append(0) # Player 1's turn
    else:
        state.append(1) # Player 2's turn

    return tuple(state)

def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            rect = pygame.Rect(x * block_size, (y * block_size)-10, block_size, block_size)
            pygame.draw.rect(screen, grid_colors[x][y], rect)
            pygame.draw.rect(screen, (255,255,255), rect, 1)

player1_lock = True
player2_lock = False

def get_neighbors(x, y):
    neighbors = []
    
    # Right and left neighbors
    if x > 0:
        neighbors.append([x - 1, y])
    if x < grid_width - 1:
        neighbors.append([x + 1, y])
    
    # Top and bottom neighbors
    if y > 0:
        neighbors.append([x, y - 1])
    if y < grid_height - 1:
        neighbors.append([x, y + 1])
    
    return neighbors



def get_valid_moves(player_color):
    valid_moves = []

    colored_blocks = red_colored_blocks if player_color == player1_color else green_colored_blocks

    for x in range(grid_width):
        for y in range(grid_height):
            if grid_colors[x][y] == (0, 0, 0):
                valid = True
                neighbors = get_neighbors(x, y)
                for nx, ny in neighbors:
                    neighbor_color = grid_colors[nx][ny]
                    if neighbor_color != (0, 0, 0) and neighbor_color != player_color:
                        valid = False
                        break
                if valid:
                    valid_moves.append((x, y))

    return valid_moves




def checkGameOver(player_color):
    valid_moves = get_valid_moves(player_color)

    if not valid_moves:
        print("Game Over")
        sys.exit()
    else:
        return

def handleTurn(mouse_x, mouse_y):
    global player1_lock, player2_lock

    # Calculate the grid block coordinates
    grid_x = mouse_x // block_size
    grid_y = mouse_y // block_size

     # Calculate the current player's valid moves
    if player1_lock:
        player_color = player1_color
    elif player2_lock:
        player_color = player2_color


    valid_moves = get_valid_moves(player_color)
    print(valid_moves)

    if not valid_moves:
        # The current player has no valid moves, so the other player wins
        if player1_lock:
            print("Player 2 Wins")
            game_over[0] = True
            game_over[1] = 2
        else:
            print("Player 1 Wins")
            game_over[0] = True
            game_over[1] = 1


    if player1_lock:
        player_color = player1_color
        state = get_current_game_state()
        action = q_player1.action(state)
        if makeMove(grid_x, grid_y, player_color):
            player1_lock = False
            player2_lock = True
    elif player2_lock:
        player_color = player2_color
        state = get_current_game_state()
        action = q_player2.action(state)
        if makeMove(grid_x, grid_y, player_color):
            player1_lock = True
            player2_lock = False


def makeMove(grid_x, grid_y, player_color):
    # Check if the move is valid, update the grid, and return True
    # If the move is not valid, return False
    valid_moves = get_valid_moves(player_color)
    if (grid_x, grid_y) in valid_moves:
        grid_colors[grid_x][grid_y] = player_color
        return True
    return False



def blockClick(mouse_x,mouse_y,player_color):
    # Calculate the grid block coordinates
    grid_x = mouse_x // block_size
    grid_y = mouse_y // block_size
            
    # Change the color of the clicked block
    if grid_colors[grid_x][grid_y] == (0, 0, 0):
        neighbors = get_neighbors(grid_x, grid_y)

    # Now you can work with the neighboring blocks and their colors
        for (neighbor_x, neighbor_y), neighbor_color in neighbors:
            if any(neighbor_color != player_color and neighbor_color != (0, 0, 0) for (_, _), neighbor_color in neighbors):
                return 0
            else:
                grid_colors[grid_x][grid_y] = player_color  # Change to player's color
                if player1_lock:
                    player_color = player1_color
                elif player2_lock:
                    player_color = player2_color

                if player_color == player1_color:
                    red_colored_blocks.append((grid_x, grid_y))
                elif player_color == player2_color:
                    green_colored_blocks.append((grid_x, grid_y))
    else:
        # The block is already colored, so you can add your own logic or just skip it
        pass

running = True
while running:

    #screen.fill((0, 0, 0))
    # start_game()
    
    draw_grid()
    
    '''
    player1_text = font.render("Player 1: " + str(p1), True, (0,0,255))
    player1_rect = player1_text.get_rect()
    player1_rect.topleft = (10, 10)

    # Render the text for Player 2's score
    player2_text = font.render("Player 2: " + str(p2), True, (0, 0 ,255))
    player2_rect = player2_text.get_rect()
    player2_rect.topright = (screen_width - 10, 10)

    # Blit the text onto the screen
    screen.blit(player1_text, player1_rect)
    screen.blit(player2_text, player2_rect)
    '''

    inital_state = get_state(grid_colors,player1_lock,player2_lock)
    num_states = len(inital_state)
    num_actions = len(get_valid_moves())

    q_player1 = ColorChampsQLearning(num_states,num_actions)
    q_player2 = ColorChampsQLearning(num_states,num_actions)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            handleTurn(mouse_x,mouse_y)


    current_time = pygame.time.get_ticks()
    remaining_time = max(0, timer_duration - (current_time - start_time))

    # Render the timer
    timer_text = font.render(f"Time: {remaining_time // 1000} seconds", True, (0, 0, 255))
    timer_rect = timer_text.get_rect()
    timer_rect.topleft = (10, screen_height - 50)

    # Blit the timer onto the screen
    screen.blit(timer_text, timer_rect)

    # End the game if the timer runs out
    
    if remaining_time == 0:
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont("arial", 48)
        text = "Draw !"
        text_surface = font.render(text, True, (0, 0, 0))  # You can choose a different color
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)

    if game_over[0] == True:
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont("arial", 36)
        text = "Player " + str(game_over[1]) + " Wins !"
        text_surface = font.render(text, True, (0, 0, 0))  # You can choose a different color
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()


pygame.quit()
sys.exit()
