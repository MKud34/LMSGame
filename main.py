import pygame.rect

from map_stuff import *
from scenes import *
import time

levels = os.listdir("data/maps")


class Game:
    def __init__(self, num: int, fails=0):
        pygame.init()
        self.level_num = num
        self.player, level_x, level_y = generate_level(load_level(levels[num]))
        self.camera = Camera(level_y)

        self.stats = {
            "jumps": 0,
            "fails": fails
        }
        self.state = "running"
        self.running = True

    def run(self):
        start_screen(self.level_num)
        frame = 0
        start = time.time()
        while self.running:
            screen.fill((0, 0, 0))
            """ благодаря delta_time физика игры не зависит от
                производительности компьютера игрока"""
            delta_time = clock.tick(60) * 0.001 * TARGET_FPS
            frame += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                ##################### УПРАВЛЕНИЕ ##########################

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.LEFT_KEY = True
                    elif event.key == pygame.K_RIGHT:
                        self.player.RIGHT_KEY = True
                    elif event.key == pygame.K_UP:
                        self.player.jump()
                        self.stats["jumps"] += 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.LEFT_KEY = False
                    elif event.key == pygame.K_RIGHT:
                        self.player.RIGHT_KEY = False
                    elif event.key == pygame.K_UP:
                        if self.player.is_airborne:
                            self.player.velocity *= 0.25

            ################### СОСТОЯНИЕ ИГРОКА #####################

            self.player.move(delta_time, frame)
            self.camera.adjust(self.player)

            if self.player.player_in_door:
                self.running = False
                self.state = "win"
                continue
            if self.player.is_dead:
                fail_screen("смерть")
                self.running = False
                self.stats["fails"] += 1
                self.state = "fail"
                continue
            elif time.time() - start > 35:
                fail_screen("время")
                self.running = False
                self.stats["fails"] += 1
                self.state = "fail"
                continue

            ################### ОБНОВЛЕНИЕ ЭКРАНА #####################

            all_sprites.update()
            all_sprites.draw(screen)
            animated_group.draw(screen)
            player_group.draw(screen)
            draw_interface(screen, time.time() - start, self.player.hp)
            pygame.display.flip()
            clock.tick(60)
        if self.state != "fail":
            end_screen(time.time() - start, self.stats)

        all_sprites.empty()
        borders_group.empty()
        tiles_group.empty()
        player_group.empty()
        animated_group.empty()
        decor_group.empty()
        interface.empty()

        self.player.rect.move(9999, 9999)


if __name__ == "__main__":
    giga_start = time.time()
    giga_stats = {
        "jumps": 0,
        "fails": 0
    }
    res = "fail"
    for i, val in enumerate(levels):
        while res != "win":
            session = Game(i)
            session.run()
            res = session.state
            giga_stats["jumps"] += session.stats["jumps"]
            giga_stats["fails"] += session.stats["fails"]
        res = "fail"
    end_screen(time.time() - giga_start, giga_stats, True)
