import pygame
import sys
import random
import os
import math
from player import Player
from wall import Wall
from coin import Coin
from trap import Trap
from portal import Portal
from thief import Thief
from finish_line import FinishLine
import constants as const
 
# Initialize Pygame
pygame.init()

def draw_total_stars():
    global level1_stars
    global level2_stars
    global level3_stars
    global level4_stars

    global total_stars

    total_stars = level1_stars + level2_stars + level3_stars + level4_stars

    font = pygame.font.Font(None, 70)
    stars_text = font.render(f"Total stars: {total_stars}", True, const.PURPLE)
    stars_rect = stars_text.get_rect(topleft=(10, 10))
    screen.blit(stars_text, stars_rect)


def show_game_over_screen():
    game_over_image = pygame.image.load("./assets/backgrounds/game_over.png").convert()
    game_over_image = pygame.transform.scale(game_over_image, (const.WIDTH, const.HEIGHT))
    game_over_rect = game_over_image.get_rect()
    screen.blit(game_over_image, game_over_rect)
    font = pygame.font.Font(None, 400)
    game_over_text = font.render("Game Over", True, const.RED)
    game_over_rect = game_over_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2))
    screen.blit(game_over_text, game_over_rect)
    
    pygame.display.flip()
    pygame.time.wait(2000)  # Display game over screen for 2 seconds

def calculate_stars(coin_count, level):
    global level1_stars
    global level2_stars
    global level3_stars
    global level4_stars
    global total_coins
    percentage = (coin_count / total_coins) * 100

    if percentage >= 80:
        stars = 3
    elif percentage >= 50:
        stars =  2
    else:
        stars =  1

    if level == 1:
        if stars > level1_stars:
            level1_stars = stars
    if level == 2:
        if stars > level2_stars:
            level2_stars = stars
    if level == 3:
        if stars > level3_stars:
            level3_stars = stars
    if level == 4:
        if stars > level4_stars:
            level4_stars = stars

    return stars

def show_game_won_screen(stars):
    game_won_image = pygame.image.load("./assets/backgrounds/game_won.jpg").convert()
    game_won_image = pygame.transform.scale(game_won_image, (const.WIDTH, const.HEIGHT))
    game_won_rect = game_won_image.get_rect()
    screen.blit(game_won_image, game_won_rect)

    font = pygame.font.Font(None, 400)
    game_over_text = font.render("You won!", True, const.RED)
    game_over_rect = game_over_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2))
    screen.blit(game_over_text, game_over_rect)

    font = pygame.font.Font(None, 100)
    # Display stars based on the number of coins collected
    star_text = font.render(f"Stars: {stars}/3", True, const.PURPLE)
    star_rect = star_text.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2 + 200))
    screen.blit(star_text, star_rect)

    pygame.display.flip()
    pygame.time.wait(2000)  # Display game over screen for 2 seconds

def get_map_1():
    map1 = [
        "********************************",
        "* ##**##**####################$*",
        "*# #**###########**********  ***",
        "*# ##### #******#****####*******",
        "*##***###****** #****#  #*******",
        "*##************ #*####**#######*",
        "**#*************#*#*###########*",
        "*##*************###*****##****#*",
        "*###############*********#****#*",
        "*###   *       #*****   *#*#**#*",
        "*###*  ***     #  *** * *#*#  #*",
        "*###********** #*****   *#*####*",
        "*###*######**  ####** ***#**  **",
        "***#*#****#**###**#** ***#******",
        "***#*###**#***#***#** ***#******",
        "***#******#***############******",
        "***########*******  ** *********",
        "********************************" 
    ]
    return map1

def get_map_2():
    map2 = [
        "********************************",
        "* #######**********@####   ***#*",
        "*@******#***********#***   *** *",
        "*@***####***********######**** *",
        "*@*####******************#**** *",
        "*@*# *********@@@@@@@@@@@#@@@* *",
        "*@######****###################*",
        "*@#**  #**###*@@@@@@@@@@@#@@@*#*",
        "**##############**@@@@@@*#****#*",
        "** *******#****#**@ *   *####*#*",
        "*# #############@*@    # #**#*#*",
        "*# *******#*******@*     ##*###*",
        "*# ########*******@@@@@@@*#*****",
        "** *******#**************@#*  **",
        "*# ########**************@#   **",
        "*# #************************ @**",
        "**@*$####################### ***",
        "********************************"

    ]
    return map2

def get_map_3():
    map3 = [
        "********************************",
        "* *@@@****####                @*",
        "* #####**######*****************",
        "**#    * #*#####*$########******",
        "*@#  *##########*@*@@@@@@#@@@@**",
        "**######*######**@###########***",
        "**##*********##**@#@*@@@@#@@#@**",
        "*************#***@#@######*@#@**",
        "*@#############**@#*#########@**",
        "**#@@@@@@@@@@*#**@#@@@@@@@@@*@**",
        "**#############***#############*",
        "**############****************#*",
        "*************####****###*###**#*",
        "*********   *## #*  *#*#*#*#**1*",
        "*********   *## #*  *#*#*#*#****",
        "*1           #########*#*#*#**@*",
        "************ ##**#####*###*####*",
        "********************************"
    ]
    return map3

def get_map_4():
    map4 = [
        "*@************@*****************",
        "* #*###*###*###*@4             *",
        "*M# # # # # # #**M   *****M    *",
        "* # # # # # # #**M#############*",
        "* # # # # # #M#**#    ***      *",
        "* # # # # # # #**#    *** @@@@**",
        "* #M# # # # # #**######*       *",
        "*@###*###*###*1@**@@@@#*   @@@2*",
        "********************************",
        "@@@@@@@@@@@@@@@@****************",
        "@5       *     @*6M      @#####*",
        "*M            *@*#********#***#*",
        "@       *      @*#*##*###*###*#*",
        "@ *            @*#*##*#*#*#*#*#*",
        "*M           * @*#*####*###*#*#*",
        "*M             **#**********#*#*",
        "@  *          3@*############*$*",
        "@@@@@@@@@@@@@@@@****************"
    ]
    return map4

def set_portal_destinations(portal_group):
    portal_list = list(portal_group)

    for i in range(0, len(portal_list)):
        for j in range(i + 1, len(portal_list)):
            if portal_list[i].pair == portal_list[j].pair:
                portal_list[i].sibling = portal_list[j]
                portal_list[j].sibling = portal_list[i]
                portal_list[i].destination = portal_list[j].rect.topleft
                portal_list[j].destination = portal_list[i].rect.topleft
                break


def load_level(map):
    # Create sprites
    global walls
    walls = pygame.sprite.Group()
    global traps
    traps = pygame.sprite.Group()
    global money
    money = pygame.sprite.Group()
    global player
    player = Player(const.PLAYER_SIZE, const.PLAYER_SIZE)
    global portals
    portals = pygame.sprite.Group()
    global thieves
    thieves = pygame.sprite.Group()
    global finish_line

    # Create walls based on the map1
    for j, row in enumerate(map):
        for i, char in enumerate(row):
            if char == "*":
                wall = Wall(i * const.CELL_SIZE, j * const.CELL_SIZE)
                walls.add(wall)
            elif char == "#":
                coin = Coin(i * const.CELL_SIZE, j * const.CELL_SIZE)
                money.add(coin)
            elif char == "@":
                trap = Trap(i * const.CELL_SIZE, j * const.CELL_SIZE)
                traps.add(trap)
            elif char == "1":  # Define portal locations in the map
                portal = Portal(i * const.CELL_SIZE, j * const.CELL_SIZE, 1, 0)  # The destination will be set later
                portals.add(portal)
            elif char == "2":  # Define portal locations in the map
                portal = Portal(i * const.CELL_SIZE, j * const.CELL_SIZE, 2, 0)  # The destination will be set later
                portals.add(portal)
            elif char == "3":  # Define portal locations in the map
                portal = Portal(i * const.CELL_SIZE, j * const.CELL_SIZE, 3, 0)  # The destination will be set later
                portals.add(portal)
            elif char == "4":  # Define portal locations in the map
                portal = Portal(i * const.CELL_SIZE, j * const.CELL_SIZE, 1, 180)  # The destination will be set later
                portals.add(portal)
            elif char == "5":  # Define portal locations in the map
                portal = Portal(i * const.CELL_SIZE, j * const.CELL_SIZE, 2, 180)  # The destination will be set later
                portals.add(portal)
            elif char == "6":  # Define portal locations in the map
                portal = Portal(i * const.CELL_SIZE, j * const.CELL_SIZE, 3, 180)  # The destination will be set later
                portals.add(portal)
            elif char == "M":
                thief = Thief(i * const.CELL_SIZE, j * const.CELL_SIZE)
                thieves.add(thief)
            elif char == "$":
                finish_line = FinishLine(i * const.CELL_SIZE, j * const.CELL_SIZE)
    set_portal_destinations(portals)  # Set the destination for each portal pair
    global total_coins
    total_coins = len(money)
    

def main_menu(events):
    global is_in_level
    global is_in_menu
    global level

    global total_stars

    global level1_clicked
    global level2_clicked
    global level3_clicked
    global level4_clicked

    keys = pygame.key.get_pressed()

    if level1_clicked:
        map = get_map_1()
        load_level(map)
        is_in_menu = False
        is_in_level = True
        level = 1

        level1_clicked = False
    if level2_clicked:
        map = get_map_2()
        load_level(map)
        is_in_menu = False
        is_in_level = True
        level = 2
    
        level2_clicked = False
    if level3_clicked:
        map = get_map_3()
        load_level(map)
        is_in_menu = False
        is_in_level = True
        level = 3
    
        level3_clicked = False
    if level4_clicked:
        map = get_map_4()
        load_level(map)
        is_in_menu = False
        is_in_level = True
        level = 4
    
        level4_clicked = False
    if keys[pygame.K_ESCAPE]:
        is_in_level = False
        is_in_menu = True
        level = 0

    if is_in_level:
        # Check if game over
        if player.game_over:
            pygame.time.wait(500)
            show_game_over_screen()
            is_in_level = False
            is_in_menu = True
            level = 0
            return

        if player.game_won:
            pygame.time.wait(500)
            stars = calculate_stars(player.coin_count, level)
            show_game_won_screen(stars)
            is_in_level = False
            is_in_menu = True
            level = 0
            return
        
        # Blit the background image
        screen.blit(background_image, background_rect)
    
        # Update
        player.update(walls, money, traps, portals, thieves, finish_line)
        portals.update()
        thieves.update(walls)

        # Update camera position to keep player in the center
        camera_x = player.rect.centerx - (const.WIDTH / 2) + (const.PLAYER_SIZE / 2)
        camera_y = player.rect.centery - (const.HEIGHT / 2) + (const.PLAYER_SIZE / 2)

        # Draw walls (relative to camera)
        for wall in walls:
            screen.blit(wall.image, (wall.rect.centerx - camera_x, wall.rect.centery - camera_y))

        # Draw traps (relative to camera)
        for trap in traps:
            screen.blit(trap.image, (trap.rect.centerx - camera_x, trap.rect.centery - camera_y))

        # Draw coins (relative to camera)
        for coin in money:
            screen.blit(coin.image, (coin.rect.centerx - camera_x, coin.rect.centery - camera_y))

        # Draw portals (relative to camera)
        for portal in portals:
            screen.blit(portal.image, (portal.rect.centerx - camera_x, portal.rect.centery - camera_y))
        
        # Draw thieves (relative to camera)
        for thief in thieves:
            screen.blit(thief.image, (thief.rect.centerx - camera_x, thief.rect.centery - camera_y))

        # Draw win sprite
        screen.blit(finish_line.image, (finish_line.rect.centerx - camera_x, finish_line.rect.centery - camera_y))

        # Draw the player's trail
        player.draw_trail(screen, camera_x, camera_y)

        # Draw player (relative to camera)
        screen.blit(player.image, (player.rect.centerx - camera_x, player.rect.centery - camera_y))

        # Update timer
        player.update_timer()
        player.draw_timer(screen)

        # Draw coin count
        player.draw_coin_count(screen)
    elif is_in_menu:
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # Check if the mouse is over the button area and change cursor shape
                button1_collided = button1_rect.collidepoint(event.pos)
                button2_collided = button2_rect.collidepoint(event.pos)
                button3_collided = button3_rect.collidepoint(event.pos)
                button4_collided = button4_rect.collidepoint(event.pos)
                button_exit_collided = button_exit_rect.collidepoint(event.pos)
                if button1_collided or button2_collided or button3_collided or button4_collided or button_exit_collided:
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if the mouse click is inside any button area
                    if button1_rect.collidepoint(event.pos):
                        level1_clicked = True
                    elif button2_rect.collidepoint(event.pos):
                        if total_stars >= 2:
                            level2_clicked = True
                    elif button3_rect.collidepoint(event.pos):
                        if total_stars >= 4:
                            level3_clicked = True
                    elif button4_rect.collidepoint(event.pos):
                        if total_stars >= 7:
                            level4_clicked = True
                    elif button_exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
        # Blit the main menu image
        screen.blit(main_menu_image, main_menu_rect)

        if total_stars < 2:
            button2_color = const.RED
        else:
            button2_color = const.GREEN
        if total_stars < 4:
            button3_color = const.RED
        else:
            button3_color = const.GREEN
        if total_stars < 7:
            button4_color = const.RED
        else:
            button4_color = const.GREEN

        # Drawing the buttons
        pygame.draw.rect(screen, const.GREEN, button1_rect, 200)
        pygame.draw.rect(screen, button2_color, button2_rect, 200)
        pygame.draw.rect(screen, button3_color, button3_rect, 200)
        pygame.draw.rect(screen, button4_color, button4_rect, 200)
        pygame.draw.rect(screen, const.BYZANTIUM, button_exit_rect, 200)
        screen.blit(button1_text, button1_rect.topleft)
        screen.blit(button2_text, button2_rect.topleft)
        screen.blit(button3_text, button3_rect.topleft)
        screen.blit(button4_text, button4_rect.topleft)
        screen.blit(button_exit_text, button_exit_rect.topleft)

        # Draw number of stars
        draw_total_stars()

# Initialize game window
screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
pygame.display.set_caption("Curse of The Pharaoh")

# Load level background image
background_image = pygame.image.load("./assets/backgrounds/BG.jpg").convert()
background_image = pygame.transform.scale(background_image, (const.WIDTH, const.HEIGHT))
background_rect = background_image.get_rect()

# Load main menu background image
main_menu_image = pygame.image.load("./assets/backgrounds/MM.jpg").convert()
main_menu_image = pygame.transform.scale(main_menu_image, (const.WIDTH, const.HEIGHT))
main_menu_rect = main_menu_image.get_rect()

# Font for the button text
font = pygame.font.Font(None, 60)

# Texts to display on the buttons
button1_text = font.render('Level 1', True, const.BLACK)
button2_text = font.render('Level 2', True, const.BLACK)
button3_text = font.render('Level 3', True, const.BLACK)
button4_text = font.render('Level 4', True, const.BLACK)
button_exit_text = font.render('Exit Game', True, const.BLACK)

# Rectangles for buttons
button_width, button_height = 160, 60
button1_rect = pygame.Rect(1140, 250, button_width, button_height)
button2_rect = pygame.Rect(1140, 400, button_width, button_height)
button3_rect = pygame.Rect(1140, 550, button_width, button_height)
button4_rect = pygame.Rect(1140, 700, button_width, button_height)
button_exit_rect = pygame.Rect(1700, 950, button_width + 50, button_height)

 
# Create sprites
walls = []
traps = []
money = []
player = []
portals = []
finish_line = []

is_in_level = False
is_in_menu = True

level = 0

total_stars = 0

level1_stars = 0
level2_stars = 0
level3_stars = 0
level4_stars = 0

level1_clicked = False
level2_clicked = False
level3_clicked = False
level4_clicked = False


def main():
    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Main Menu
        main_menu(events)

        # Refresh screen
        pygame.display.flip()
    
        # Cap the frame rate
        clock.tick(const.FPS)

    # Quit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()