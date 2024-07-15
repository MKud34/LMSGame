import pygame.time

from player import *

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'closed_door': load_image("animated/door/door1.png")
}

animated = {
    "finish": load_images("animated/door")
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        if tile_type == "wall":
            borders_group.add(self)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, animated_group)
        self.images = animated[tile_type]
        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        self.event_rect = self.rect.copy()
        self.event_rect.w *= 0.3
        self.anim_finished = False

    def animate(self, reverse=False):
        placeholder = list(self.images)
        if reverse:
            placeholder.reverse()
        for i in placeholder:
            self.image = i
            self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.anim_finished = True


def load_level(filename):
    filename = "data/maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                Door('finish', x, y)
            elif level[y][x] == '-':
                Tile('empty', x, y)
                Tile('closed_door', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player((x + 1) * tile_width, (y + 1) * tile_height - 5)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y
