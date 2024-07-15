import pygame

####################################

size = WIDTH, HEIGHT = 500, 500
TARGET_FPS = 60
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Башня")

#####################################

all_sprites = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
animated_group = pygame.sprite.Group()
decor_group = pygame.sprite.Group()
interface = pygame.sprite.Group()

#####################################

tile_width = tile_height = 50

