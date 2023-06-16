# importing modules
import pygame
from pygame.locals import *
import random

pygame.init()

# window dimensions
window_width = 700
window_height = 700

# game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Dads side of the family')

# defining variables
cell_size = 12
direction = 1 # 1 is up, 2 is right, 3 is down adn 4 is left
update_snake = 0
food = [0,0]
new_food = True
new_piece = [0,0]
score = 0
game_over = False
clicked = False

# creating snake
snake_position = [[int(window_width / 2), int(window_height / 2)]]
snake_position.append([int(window_width / 2), int(window_height / 2) + cell_size])
snake_position.append([int(window_width / 2), int(window_height / 2) + cell_size * 2])
snake_position.append([int(window_width / 2), int(window_height / 2) + cell_size * 3])

# defining font
font = pygame.font.SysFont(None, 35)

# defining colors
background = (144, 187, 240)
body_inner = (245, 230, 137)
body_outer = (245, 219, 51)
orange = (240, 133, 67)
food_color = (200, 50, 50)
black = (0, 0, 0)

# setup rectangle for play again
again_rectangle = Rect(window_width // 2 - 80, window_height // 2, 160, 50)

def draw_screen():
    window.fill(background)
    
    
def draw_score():
    score_text = 'Score: ' + str(score)
    score_image = font.render(score_text, True, black)
    window.blit(score_image, (0,0))
    
def check_game_over(game_over):   
    # check if snake has eaten itself
    head_count = 0
    for segment in snake_position:
        if snake_position[0] == segment and head_count > 0:
            game_over = True
        head_count += 1
        
    # check of snake has gone out of window
    if snake_position[0][0] < 0 or snake_position[0][0] > window_width or snake_position[0][1] < 0 or snake_position[0][1] > window_height:
        game_over = True
        
    return game_over 
 
def draw_game_over():
    over_text = 'Game Over!'
    over_image = font.render(over_text, True, black) 
    pygame.draw.rect(window, orange, (window_width // 2 - 80, window_height // 2 - 60, 160, 50))
    window.blit(over_image, (window_width // 2 - 80, window_height // 2 - 50)) 
    
    again_text = 'Play Again?'
    again_image = font.render(again_text, True, black)  
    pygame.draw.rect(window,  orange, again_rectangle) 
    window.blit(again_image, (window_width // 2 - 80, window_height // 2 + 10))   
        
# setup loop and exit event handler
run = True
while run:
    
    draw_screen()
    # iterate through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1 
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2 
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 4
    
    # create food 
    if new_food == True:
        new_food = False
        food[0] = cell_size * random.randint(0, (window_width / cell_size) - 1)
        food[1] = cell_size * random.randint(0, (window_height / cell_size) - 1)
        
    # draw food
    pygame.draw.rect(window, food_color, (food[0], food[1], cell_size, cell_size))
    
    
    #check if food has been eaten
    if snake_position[0] == food:
        new_food = True
        # create a new piece at the last part of the snakes tail
        new_piece = list(snake_position[-1])
        
        if direction == 1:
            new_piece[1] += cell_size
        if direction == 3:
            new_piece[1] -= cell_size
        if direction == 2:
            new_piece[0] -= cell_size
        if direction == 4:
            new_piece[0] += cell_size
            
        # attach new piece to the end of the snake
        snake_position.append(new_piece)
        
        score += 1 
    
    if game_over == False:
        if update_snake > 99:
            update_snake = 0            
            snake_position = snake_position[-1:] + snake_position[:-1]
            # heading up 
            if direction == 1:
                
                snake_position[0][0] = snake_position[1][0]
                snake_position[0][1] = snake_position[1][1] - cell_size
            if direction == 3:
                snake_position[0][0] = snake_position[1][0]
                snake_position[0][1] = snake_position[1][1] + cell_size
            if direction == 2:
                snake_position[0][1] = snake_position[1][1]
                snake_position[0][0] = snake_position[1][0] + cell_size
            if direction == 4:
                snake_position[0][1] = snake_position[1][1]
                snake_position[0][0] = snake_position[1][0] - cell_size                
            game_over = check_game_over(game_over)
            
    if game_over == True:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            mouse_position = pygame.mouse.get_pos()
            if again_rectangle.collidepoint(mouse_position):
                # reset all variables
                direction = 1 # 1 is up, 2 is right, 3 is down adn 4 is left
                update_snake = 0
                food = [0,0]
                new_food = True
                new_piece = [0,0]
                score = 0
                game_over = False

                # creating snake
                snake_position = [[int(window_width / 2), int(window_height / 2)]]
                snake_position.append([int(window_width / 2), int(window_height / 2) + cell_size])
                snake_position.append([int(window_width / 2), int(window_height / 2) + cell_size * 2])
                snake_position.append([int(window_width / 2), int(window_height / 2) + cell_size * 3])

    # drawing snake
    head = 1
    for i in snake_position:
        if head == 0:
            pygame.draw.rect(window, body_outer, (i[0], i[1], cell_size, cell_size))
            pygame.draw.rect(window, body_inner, (i[0] + 1, i[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(window, body_outer, (i[0], i[1], cell_size, cell_size))
            pygame.draw.rect(window, orange, (i[0] + 1, i[1] + 1, cell_size - 2, cell_size - 2))
            head = 0
        
    # updates the window
    pygame.display.update()
    
    update_snake += 15
    
# end game
pygame.quit()