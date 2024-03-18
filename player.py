import pygame
import constants as const
import math

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.player_frames = self.load_player_frames()
        self.og_player_frames = self.player_frames.copy()
        self.current_frame = 0
        self.image = self.player_frames[0]
        self.trail = []  # List to store the trail positions
        self.trail_length = const.WIDTH  # Adjust the length of the trail as needed
        self.can_draw_trail = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.coin_count = 0
        self.game_over = False
        self.game_time = 0
        self.start_time = pygame.time.get_ticks()
        self.is_in_portal = False
        self.portal = None
        self.move_cooldown_start = 0
        self.game_won = False
        self.is_fighting = False
        self.continue_direction = None
        self.thief = None
    
    def load_player_frames(self):
        images = {}
        images[0] = pygame.image.load("./assets/player_sprites/1.png").convert_alpha()
        images[0] = pygame.transform.scale(images[0], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[1] = pygame.image.load("./assets/player_sprites/2.png").convert_alpha()
        images[1] = pygame.transform.scale(images[1], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[2] = pygame.image.load("./assets/player_sprites/3.png").convert_alpha()
        images[2] = pygame.transform.scale(images[2], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[3] = pygame.image.load("./assets/player_sprites/4.png").convert_alpha()
        images[3] = pygame.transform.scale(images[3], (const.PLAYER_SIZE, const.PLAYER_SIZE))

        for frame in images:
            images[frame] = pygame.transform.rotate(images[frame], 270)

        return images

    def rotate_player(self, angle):
        self.player_frames = self.og_player_frames.copy()
        self.image = self.player_frames[math.floor(self.current_frame)]
        for frame in self.player_frames:
            self.player_frames[frame] = pygame.transform.rotate(self.player_frames[frame], angle)
        self.image = pygame.transform.rotate(self.image, angle)

 
    def update(self, walls, money, traps, portals, thieves, finish_line):
        # Update current player frame every 5 ticks
        self.current_frame += 0.2
        if math.floor(self.current_frame) == len(self.player_frames): #if images in frames completed, restart the process.
            self.current_frame = 0
        self.image = self.player_frames[math.floor(self.current_frame)]
        self.rect = self.image.get_rect(center = self.rect.center)

        keys = pygame.key.get_pressed()
        new_rect = self.rect.copy()

        if self.is_in_portal:
            # While in portal rotate to first portal angle
            self.rotate_player(self.portal.angle + 90)
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.move_cooldown_start) // 1000
            if elapsed_time >= const.MOVE_COOLDOWN:
                self.is_in_portal = False
                self.move_cooldown_start = 0
                self.rect.topleft = self.portal.destination
                # When exiting portal rotate to sibling portal angle
                self.rotate_player(self.portal.sibling.angle + 90)
                self.portal = None
            return

        if self.is_fighting:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.move_cooldown_start) // 1000
            if elapsed_time >= const.MOVE_COOLDOWN:
                # Remove thief
                thieves.remove(self.thief)

                self.is_fighting = False
                self.move_cooldown_start = 0
                if self.continue_direction == "left":
                    new_rect = self.teleport_to_wall(new_rect, walls, traps, money, portals, thieves, finish_line, "left")
                elif self.continue_direction == "right":
                    new_rect = self.teleport_to_wall(new_rect, walls, traps, money, portals, thieves, finish_line, "right")
                elif self.continue_direction == "up":
                    new_rect = self.teleport_to_wall(new_rect, walls, traps, money, portals, thieves, finish_line, "up")
                elif self.continue_direction == "down":
                    new_rect = self.teleport_to_wall(new_rect, walls, traps, money, portals, thieves, finish_line, "down")
                # Update position
                self.rect = new_rect
            return

        if keys[pygame.K_LEFT]:
            self.rotate_player(0)
            new_rect = self.teleport_to_wall(new_rect, walls, traps, money, portals, thieves, finish_line, "left")
        if keys[pygame.K_RIGHT]:
            self.rotate_player(180)
            new_rect = self.teleport_to_wall(new_rect, walls, traps, money, portals, thieves, finish_line, "right")
        if keys[pygame.K_UP]:
            self.rotate_player(270)
            new_rect = self.teleport_to_wall(new_rect, walls, traps, money, portals, thieves, finish_line, "up")
        if keys[pygame.K_DOWN]:
            self.rotate_player(90)
            new_rect = self.teleport_to_wall(new_rect, walls, traps, money, portals, thieves, finish_line, "down")
 
        # Update position
        self.rect = new_rect

    def draw_trail(self, screen, camera_x, camera_y):
        if not self.can_draw_trail:
            return

        offset_x = const.PLAYER_SIZE // 2
        offset_y = const.PLAYER_SIZE // 2
        
        # Draw the trail on the screen
        for point in self.trail:
            #print(point)
            pygame.draw.circle(screen, const.YELLOW, (point[0] - camera_x + offset_x, point[1] - camera_y + offset_y), 10)  # Adjust circle size as needed
        
        self.trail = []
        self.can_draw_trail = False

    def teleport_to_wall(self, rect, walls, traps, money, portals, thieves, finish_line, direction):
        self.can_draw_trail = True
        is_collided = False
        while 1 :
            if rect.colliderect(finish_line.rect):
                self.game_won = True
                break
            
            if self.game_won:
                break

            for trap in traps:
                if rect.colliderect(trap.rect):
                    self.game_over = True
                    break
            
            if self.game_over:
                break

            for portal in portals:
                if portal.can_teleport:
                    if rect.colliderect(portal.rect):
                        rect.topleft = portal.rect.topleft
                        self.is_in_portal = True
                        self.portal = portal
                        self.move_cooldown_start = pygame.time.get_ticks()
                        portal.can_teleport = False
                        portal.sibling.can_teleport = False
                        portal.teleport_cooldown_start = pygame.time.get_ticks()
                        portal.sibling.teleport_cooldown_start = pygame.time.get_ticks()
                        break
            if self.is_in_portal:
                break

            for thief in thieves:
                if rect.colliderect(thief.rect):
                    self.coin_count -= 5
                    self.coin_count = max(0, self.coin_count)
                    self.move_cooldown_start = pygame.time.get_ticks()
                    thief.is_fighting = True
                    self.is_fighting = True
                    self.continue_direction = direction
                    self.thief = thief

            if self.is_fighting:
                break
    
            for wall in walls:
                if rect.colliderect(wall.rect):
                    is_collided = True
                    break
            
            # Append current position to the trail
            self.trail.append((rect.centerx, rect.centery))

            # Keep the trail length within the specified limit
            if len(self.trail) > self.trail_length:
                self.trail.pop(0)

            # Collect the money
            self.collect_money(rect, money)

            if direction == "left":
                if is_collided:
                    rect.x += 1
                    break
                rect.x -= 1
            elif direction == "right":
                if is_collided:
                    rect.x -= 1
                    break
                rect.x += 1
            elif direction == "up":
                if is_collided:
                    rect.y += 1
                    break
                rect.y -= 1
            elif direction == "down":
                if is_collided:
                    rect.y -= 1
                    break
                rect.y += 1

        return rect

    def collect_money(self, rect, money):
        for coin in money:
            if rect.colliderect(coin.rect):
                money.remove(coin)
                self.coin_count += 1

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000
        self.game_time = const.START_TIME - elapsed_time

        if self.game_time == 0:
            self.game_over = True

    def draw_timer(self, screen):
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {self.game_time} seconds", True, const.PURPLE)
        timer_rect = timer_text.get_rect(topleft=(10, 10))
        screen.blit(timer_text, timer_rect)

    def draw_coin_count(self, screen):
        font = pygame.font.Font(None, 36)
        coin_count_text = font.render(f"Coins: {self.coin_count}", True, const.WHITE)
        coin_count_rect = coin_count_text.get_rect(topleft=(10, 50))
        screen.blit(coin_count_text, coin_count_rect)
 