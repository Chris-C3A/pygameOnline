#!/usr/bin/env python3
import pygame
import sys
import os
# from src.player import Player
# from src.bullet import Bullet
from src.network import Network

WIDTH, HEIGHT = 1200, 900
FPS = 120

pygame.init()

screen = (WIDTH, HEIGHT)
pygame.display.set_caption('Tanks!')
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (360, 100)

clock = pygame.time.Clock()
win = pygame.display.set_mode(screen)

x, y, scale = WIDTH / 2, HEIGHT / 2, 8

bg = pygame.image.load("resources/background.jpg")
tank_img = pygame.transform.scale(pygame.image.load(
    os.path.join("resources", "tank.png")),
    (500 // scale, 637 // scale)
)
gun_img = pygame.transform.scale(pygame.image.load(
    os.path.join("resources", "gun.png")),
    (285 // scale, 560 // scale)
)


def redraw_game_window(idx):
    global players
    # draw background image
    win.blit(bg, (0, 0))

    for player in players.values():
        for bullet in player.bullets:
            bullet.draw(win)

        player.update_pivot()

        rotated_img, rect = rotate_image(tank_img, player.angle, player.pivot, player.offset)
        player.draw(win, rotated_img, rect)

        rotated_img, rect = rotate_image(gun_img, player.turret.angle, player.pivot, player.turret.offset)
        player.turret.draw(win, rotated_img, rect)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Primmary Ammo: " + str(players[idx].turret.primary_ammo), True, (0, 0, 0))
    win.blit(text, (50, 100))

    # send request to update server
    n.send({"server": "update"})

    pygame.display.update()


def event_handling():
    global bullets
    global n

    mouse_x, mouse_y = pygame.mouse.get_pos()
    n.send({"mouse":{"x": mouse_x, "y": mouse_y}})

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            n.send({"key": "space"})

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        n.send({"key": "a"})
    elif keys[pygame.K_d]:
        n.send({"key": "d"})

    if keys[pygame.K_w]:
        n.send({"key": "w"})
    elif keys[pygame.K_s]:
        n.send({"key": "s"})


def rotate_image(surface, angle, pivot, offset):
    """
    Rotate the surface around the pivot point
    :param surface: pygame.Surface
    :param angle: float
    :param pivot: list
    :param offset: pygame.math.Vector2
    :return: IMG, rect
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.`


n = Network()
def main():
    global players
    global n
    idx = n.get_idx()["idx"]
    if idx is None:
        print("error connecting")
        exit(1)

    while True:
        clock.tick(FPS)
        players = n.send({"get": "players"})
        print(players)

        if players[idx].health <= 0:
            print("YOU DIED")
            n.disconnect()
            exit(0)

        event_handling()
        redraw_game_window(idx)


if __name__ == "__main__":
    main()
