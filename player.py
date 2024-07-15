import pygame.math

from img_load import *
from config import *
from math import ceil


player_images = {
    "idle": load_images("animated/player/idle"),
    "running": load_images("animated/player/running"),
    "hurt": load_images("animated/player/hurt")
}


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_images["idle"][0]
        self.image = pygame.transform.scale(self.image, (24, 40))
        self.rect = self.image.get_rect()
        self.frame = 0

        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_airborne = False
        self.charging_jump = False
        self.player_in_door = False
        self.is_dead = False
        self.state = "idle"
        self.hp = 5

        self.gravity, self.friction = 0.3, -0.1
        self.position, self.velocity = pygame.math.Vector2(pos_x, pos_y), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

        self.collision_rects = {"top": pygame.Rect(0, 0, self.rect.width, 3),
                                "bottom": pygame.Rect(0, 0, self.rect.width, 5),
                                "left": pygame.Rect(0, 0, 3, self.rect.height),
                                "right": pygame.Rect(0, 0, 3, self.rect.height)}
        self.colliding = {"top": False, "bottom": False, "left": False, "right": False}

    def move(self, dt, frame):
        self.check_contact()
        self.animate(frame)
        self.vertical_movement(dt)
        if not self.is_dead:
            self.adjust_face_direction()
            self.horizontal_movement(dt)
            self.adjust_coll_boxes()
            self.interact()

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.is_airborne:
            self.friction = -0.00
        else:
            self.friction = -0.1

        if self.LEFT_KEY:
            self.FACING_LEFT = True
            if not self.is_airborne:
                self.acceleration.x -= 2

        elif self.RIGHT_KEY:
            self.FACING_LEFT = False
            if not self.is_airborne:
                self.acceleration.x += 2

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.limit_position()

        if self.colliding["left"] and self.velocity.x < 0:
            self.velocity.x = 0
            self.acceleration.x = 0
        elif self.colliding["right"] and self.velocity.x > 0:
            self.velocity.x = 0
            self.acceleration.x = 0
        self.position.x += self.velocity.x * dt + (dt ** 2 * self.acceleration.x) * 0.5
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 10: self.velocity.y = 10

        if self.colliding["top"] and self.velocity.y < 0:
            self.velocity.y = -self.velocity.y * self.friction
        elif self.colliding["bottom"] and self.velocity.y > 0:
            if self.velocity.y > 9:
                self.hurt()
            self.velocity.y = -self.velocity.y * self.friction
            self.acceleration.y = 0
        else:
            self.acceleration.y = self.gravity

        self.position.y += self.velocity.y * dt + (dt ** 2 * self.acceleration.y) * 0.5
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        min(-max_vel, max(self.velocity.x, max_vel))
        if abs(self.velocity.x) < 0.01: self.velocity.x = 0

    def limit_position(self):
        if self.rect[0] >= WIDTH:
            self.rect[0] = WIDTH
        elif self.rect[0] <= 0:
            self.rect[0] = 0

    def jump(self):
        if not self.is_airborne:
            self.velocity.y -= 10
            self.is_airborne = True

    def hurt(self):
        self.hp -= 1
        self.state = "hurt"
        if self.hp <= 0:
            self.state = "dead"
            self.is_dead = True

    def check_contact(self):
        # Проверка дополнительных хитбоксов на коллизию
        self.colliding = {"top": False, "bottom": False, "left": False, "right": False}
        self.is_airborne = True

        for sprite in borders_group:
            if sprite.rect.colliderect(self.collision_rects["top"]):
                self.colliding["top"] = True
                self.is_airborne = True
                if self.velocity.y < 0:
                    self.rect.top = sprite.rect.bottom

            elif sprite.rect.colliderect(self.collision_rects["bottom"]):
                self.colliding["bottom"] = True
                self.is_airborne = False
                if self.velocity.y > 0:
                    self.rect.bottom = sprite.rect.top

            if sprite.rect.colliderect(self.collision_rects["right"]):
                self.is_airborne = False
                self.colliding["right"] = True
                if self.velocity.x > 0:
                    self.rect.right = sprite.rect.left

            elif sprite.rect.colliderect(self.collision_rects["left"]):
                self.is_airborne = False
                self.colliding["left"] = True
                if self.velocity.x < 0:
                    self.rect.left = sprite.rect.right

    def interact(self):
        # Взаимодействие с анимированными объектами
        for sprite in animated_group:
            if sprite.rect.colliderect(self.rect) and player_group.has(self):
                if not sprite.anim_finished:
                    sprite.animate()
                    sprite.anim_finished = True
            else:
                if sprite.anim_finished:
                    sprite.animate(True)
                    sprite.anim_finished = False
            if sprite.event_rect.colliderect(self.rect) and player_group.has(self):
                self.player_in_door = True
                print("touch")

    def adjust_coll_boxes(self):
        # Корректирование положения дополнительных хитбоксов
        self.collision_rects["top"].x = self.rect.x
        self.collision_rects["top"].y = self.rect.top - 3
        self.collision_rects["bottom"].x = self.rect.x
        self.collision_rects["bottom"].y = self.rect.bottom
        self.collision_rects["right"].x = self.rect.right
        self.collision_rects["right"].y = self.rect.y
        self.collision_rects["left"].x = self.rect.left - 3
        self.collision_rects["left"].y = self.rect.y

    def adjust_face_direction(self):
        if not self.FACING_LEFT:
            self.image = player_images[self.state][self.frame % len(player_images[self.state])]
        else:
            self.image = pygame.transform.flip(player_images[self.state][self.frame % len(player_images[self.state])],
                                               1, 0)
        self.image = pygame.transform.scale(self.image, (24, 40))

    def update_state(self):
        if self.velocity.x == 0 and self.velocity.y == 0 or self.is_airborne:
            self.state = "idle"
        elif self.velocity.x != 0 and not self.is_airborne:
            self.state = "running"

    def animate(self, frame=0):
        self.update_state()
        self.frame = frame % len(player_images[self.state])
        self.image = player_images[self.state][self.frame]


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, level_y):
        self.offset = pygame.math.Vector2(0, HEIGHT)
        self.level_y = level_y * tile_height
        self.level_sections = ceil(self.level_y / HEIGHT)

    def adjust(self, player):
        # персонаж не должен покидать границы экрана
        if player.position.y < 0:
            for sprite in all_sprites:
                self.apply(sprite, 1)
            player.position.y %= HEIGHT
            self.level_sections -= 1

        elif player.position.y > HEIGHT:
            for sprite in all_sprites:
                self.apply(sprite, -1)
            player.position.y %= HEIGHT
            self.level_sections += 1

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, direction):
        obj.rect.y += self.offset.y * direction


def draw_interface(screen, time, hp):
    text = [f'Здоровье {hp}',
            f'Время {round(time, 2)}']
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

