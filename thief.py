import pygame
import constants as const
import math

class Thief(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.thief_frames = self.load_thief_frames()
        self.dead_thief_frames = self.load_dead_thief_frames()
        self.current_frames = self.thief_frames.copy()
        self.current_frame = 0
        self.image = self.current_frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2
        self.is_fighting = False
        self.is_dead = False

    def rotate_thief(self):
        for frame in self.current_frames:
            self.current_frames[frame] =  mirrored_image = pygame.transform.flip(self.current_frames[frame], True, False)
        self.image =  mirrored_image = pygame.transform.flip(self.image, True, False)

    def update(self, walls):
        # Move the thief
        self.current_frame += 0.2
        if math.floor(self.current_frame) == len(self.current_frames): #if images in frames completed, restart the process.
            self.current_frame = 0

        self.image = self.current_frames[math.floor(self.current_frame)]
        self.rect = self.image.get_rect(center = self.rect.center)

        if self.is_fighting:
            if not self.is_dead:
                self.current_frames = self.dead_thief_frames.copy()
                self.current_frame = 0
                self.is_dead = True
            return

        self.rect.x -= self.speed

        # Check for collisions with walls
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rotate_thief()
                # Change direction to right if a collision occurs
                self.rect.x += self.speed * 2  # Move back to avoid overlapping with the wall
                self.speed *= -1
                break

    def load_dead_thief_frames(self):
        images = {}
        images[0] = pygame.image.load("./assets/thief_sprites/DeadThief1.png").convert_alpha()
        images[0] = pygame.transform.scale(images[0], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[1] = pygame.image.load("./assets/thief_sprites/DeadThief2.png").convert_alpha()
        images[1] = pygame.transform.scale(images[1], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[2] = pygame.image.load("./assets/thief_sprites/DeadThief3.png").convert_alpha()
        images[2] = pygame.transform.scale(images[2], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        return images

    def load_thief_frames(self):
        images = {}
        images[0] = pygame.image.load("./assets/thief_sprites/Thief1.png").convert_alpha()
        images[0] = pygame.transform.scale(images[0], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[1] = pygame.image.load("./assets/thief_sprites/Thief2.png").convert_alpha()
        images[1] = pygame.transform.scale(images[1], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[2] = pygame.image.load("./assets/thief_sprites/Thief3.png").convert_alpha()
        images[2] = pygame.transform.scale(images[2], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[3] = pygame.image.load("./assets/thief_sprites/Thief4.png").convert_alpha()
        images[3] = pygame.transform.scale(images[3], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[4] = pygame.image.load("./assets/thief_sprites/Thief5.png").convert_alpha()
        images[4] = pygame.transform.scale(images[4], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[5] = pygame.image.load("./assets/thief_sprites/Thief6.png").convert_alpha()
        images[5] = pygame.transform.scale(images[5], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[6] = pygame.image.load("./assets/thief_sprites/Thief7.png").convert_alpha()
        images[6] = pygame.transform.scale(images[6], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[7] = pygame.image.load("./assets/thief_sprites/Thief8.png").convert_alpha()
        images[7] = pygame.transform.scale(images[7], (const.PLAYER_SIZE, const.PLAYER_SIZE))
        images[8] = pygame.image.load("./assets/thief_sprites/Thief9.png").convert_alpha()
        images[8] = pygame.transform.scale(images[8], (const.PLAYER_SIZE, const.PLAYER_SIZE))

        for frame in images:
            images[frame] =  mirrored_image = pygame.transform.flip(images[frame], True, False)
        return images