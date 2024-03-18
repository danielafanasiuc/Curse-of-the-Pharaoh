import pygame
import constants as const
# Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./assets/wall_sprite/StoneBlock.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (const.CELL_SIZE, const.CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)