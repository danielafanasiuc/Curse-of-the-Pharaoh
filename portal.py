import pygame
import constants as const
import math

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, pair, angle):
        super().__init__()
        # rotate to angle given
        self.angle = angle
        self.image = pygame.Surface((const.CELL_SIZE, const.CELL_SIZE), pygame.SRCALPHA)
        self.portal_frames = self.load_portal_frames()
        self.portal_cooldown_frames = self.load_portal_cooldown_frames()
        self.current_frames = self.portal_frames.copy()
        self.current_frame = 0
        self.image.blit(self.portal_frames[0], (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pair = pair
        self.sibling = None
        self.destination = None
        self.can_teleport = True
        self.teleport_cooldown_start = 0

    def rotate_portal(self, frames):
        for frame in frames:
            frames[frame] = pygame.transform.rotate(frames[frame], self.angle)
    
    def load_portal_frames(self):
        images = {}
        images[0] = pygame.image.load("./assets/portal_sprites/portal1.png").convert_alpha()
        images[0] = pygame.transform.scale(images[0], (const.CELL_SIZE, const.CELL_SIZE))
        images[1] = pygame.image.load("./assets/portal_sprites/portal2.png").convert_alpha()
        images[1] = pygame.transform.scale(images[1], (const.CELL_SIZE, const.CELL_SIZE))
        self.rotate_portal(images)
        return images

    def load_portal_cooldown_frames(self):
        images = {}
        images[0] = pygame.image.load("./assets/portal_sprites/portal_cooldown1.png").convert_alpha()
        images[0] = pygame.transform.scale(images[0], (const.CELL_SIZE, const.CELL_SIZE))
        images[1] = pygame.image.load("./assets/portal_sprites/portal_cooldown2.png").convert_alpha()
        images[1] = pygame.transform.scale(images[1], (const.CELL_SIZE, const.CELL_SIZE))
        self.rotate_portal(images)
        return images

    def update(self):
        # Update current portal frame every 5 ticks
        self.current_frame += 0.2
        if math.floor(self.current_frame) == len(self.current_frames): #if images in frames completed, restart the process.
            self.current_frame = 0
        self.image.blit(self.current_frames[math.floor(self.current_frame)], (0, 0))
        #self.sibling.image.blit(self.current_frames[math.floor(self.current_frame)], (0, 0))
        self.rect = self.image.get_rect(center = self.rect.center)

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.teleport_cooldown_start) // 1000
        if elapsed_time == const.TELEPORT_COOLDOWN:
            self.current_frames = self.portal_frames.copy()
            self.sibling.current_frames = self.sibling.portal_frames.copy()
            self.can_teleport = True
            self.sibling.can_teleport = True
            self.teleport_cooldown_start = 0
            self.sibling.teleport_cooldown_start = 0
        else:
            if not self.can_teleport:
                self.current_frames = self.portal_cooldown_frames.copy()
                self.sibling.current_frames = self.sibling.portal_cooldown_frames.copy()
