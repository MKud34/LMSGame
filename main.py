from map_stuff import *
from scenes import *
import time

levels = os.listdir("data/maps")


class Game:
    def __init__(self, num: int):
        pygame.init()
        self.level_num = num
        self.player, level_x, level_y = generate_level(load_level(levels[num]))
        self.camera = Camera(level_y)

        self.running = True
        self.stats = {
            "jumps": 0
        }

    def run(self):
        start_screen(self.level_num)
        frame = 0
        start = time.time()
        while self.running:
            """ благодаря delta_time физика игры не зависит от
                производительности компьютера игрока"""
            delta_time = clock.tick(60) * 0.001 * TARGET_FPS
            for event in pygame.event.get():
                frame += 1
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
            if self.player.player_in_door:
                self.running = False
            self.camera.adjust(self.player)

            screen.fill((0, 0, 0))
            all_sprites.update()
            all_sprites.draw(screen)
            animated_group.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        end_screen(time.time() - start, self.stats)


if __name__ == "__main__":
    giga_start = time.time()
    giga_stats = {
        "jumps": 0
    }

    for i, val in enumerate(levels):
        session = Game(i)
        session.run()

        giga_stats["jumps"] += session.stats["jumps"]
    end_screen(time.time() - giga_start, giga_stats, True)
