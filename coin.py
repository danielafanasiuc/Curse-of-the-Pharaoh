import pygame
import constants as const

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((const.CELL_SIZE, const.CELL_SIZE), pygame.SRCALPHA)
        coin_image = pygame.image.load("./assets/coin_sprite/coin.png").convert_alpha()
        coin_image = pygame.transform.scale(coin_image, (const.MONEY_SIZE, const.MONEY_SIZE))
        image_x = (const.CELL_SIZE - const.MONEY_SIZE) // 2
        image_y = (const.CELL_SIZE - const.MONEY_SIZE) // 2
        self.image.blit(coin_image, (image_x, image_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)