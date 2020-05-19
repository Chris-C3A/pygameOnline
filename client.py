#!/usr/bin/env python3
import pygame
import sys
import os
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

bullets = []
players = []


def redraw_game_window(main_player):
    global players

    # draw background image
    win.blit(bg, (0, 0))

    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Primmary Ammo: " + str(main_player.turret.primary_ammo), True, (0, 0, 0))
    win.blit(text, (50, 100))

    pygame.display.update()


def event_handling(player):
    global bullets
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.update_pivot()
    player.turret.rotate(mouse_x, mouse_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.turret.primary_ammo > 0:
            player.fire()
            player.turret.primary_ammo -= 1

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.rotate(direction=-1)
    elif keys[pygame.K_d]:
        player.rotate(direction=1)

    if keys[pygame.K_w]:
        player.move(direction=-1)
    elif keys[pygame.K_s]:
        player.move(direction=0.7)


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
    global n
    global players

    main_player = n.getPlayerObject()

    if not main_player:
        print("error connecting")
        exit(1)

    while True:
        clock.tick(FPS)
        # TODO how to send data lol
        players = n.send(['1', main_player])

        if main_player.health <= 0:
            print("YOU DIED")
            n.disconnect()
            exit(0)

        event_handling(main_player)
        redraw_game_window(main_player)


if __name__ == "__main__":
    main()
