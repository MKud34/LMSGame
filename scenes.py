from config import *
from img_load import *


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(level):
    intro_text = ["БАШНЯ", "",
                  f"УРОВЕНЬ {level + 1}",
                  "Правила игры:",
                  "Вы должны добраться до верхнего ",
                  "этажа башни и пройти в открытую дверь",
                  "Управление осуществляется стрелками",
                  "Не забывайте про таймер"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(TARGET_FPS)


def end_screen(timer, stats, ending=False):
    outro_text = ["УРОВЕНЬ ПРОЙДЕН", "",
                  "Ваша статистика:",
                  f"Количество прыжков: {stats['jumps']}",
                  f"Повторов: {stats['fails']}",
                  f"Время прохождения: {round(timer, 2)} секунд"]
    if ending:
        outro_text[0] = "КОНЕЦ"
        outro_text.extend(["", "СПАСИБО ЗА ПРОХОЖДЕНИЕ"])
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in outro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(TARGET_FPS)


def fail_screen(reason):
    outro_text = ["УРОВЕНЬ НЕ ПРОЙДЕН", "",
                  f"Причина: {reason}"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in outro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        outro_rect = string_rendered.get_rect()
        text_coord += 10
        outro_rect.top = text_coord
        outro_rect.x = 10
        text_coord += outro_rect.height
        screen.blit(string_rendered, outro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(TARGET_FPS)


