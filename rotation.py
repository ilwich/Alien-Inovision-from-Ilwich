import pygame
from pygame.locals import *


def rotate(img, pos, angle):
    w, h = img.get_size()
    img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
    img2.blit(img, (w - pos[0], h - pos[1]))
    return pygame.transform.rotate(img2, angle)


pygame.init()
screen = pygame.display.set_mode([640, 480])
screen.fill((135, 206, 250))
pygame.display.set_caption("Вращение")
pivot = (100, 200)  # положение центра вращения на экране
angle = 0
clock = pygame.time.Clock()

rect_health_heigth = 5
rect_health_weigth = 60
imagec = pygame.image.load("images/turrel2.bmp")
rect = imagec.copy().get_rect()
center_image = rect.center  # положение центра вращения на изображении



running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((135, 206, 250))
    rect = imagec.copy().get_rect()
    delta_x = rect.width / 2
    delta_y = rect.height / 2
    image = rotate(imagec, center_image, angle)
    rect = image.get_rect()
    rect.center = (pivot[0] + delta_x, pivot[1] + delta_y)
    rect_health = (int(rect.center[0] - rect_health_weigth / 2), int(rect.center[1] - rect_health_heigth / 2),\
                    rect_health_weigth, rect_health_heigth)
    print(rect_health)

    screen.blit(image, rect)


    pygame.draw.line(screen, (0, 0, 0, 0), rect.topleft, rect.topright)
    pygame.draw.line(screen, (0, 0, 0, 0), rect.topright, rect.bottomright)
    pygame.draw.line(screen, (0, 0, 0, 0), rect.bottomright, rect.bottomleft)
    pygame.draw.line(screen, (0, 0, 0, 0), rect.topleft, rect.bottomleft)
    pygame.draw.rect(screen, (25, 25, 25), rect_health)
    angle += 1 % 360

    pygame.display.update()

pygame.quit()