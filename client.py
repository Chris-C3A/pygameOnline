#!/usr/bin/env python3
import pygame
import sys
from pygame.locals import *
import os
# from src.player import Player
from src.bullet import Bullet
from src.network import Network

WIDTH, HEIGHT = 1200, 900
FPS = 120

# TODO
# map generation?
# walls n shit

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

# player = Player(x, y, scale)

bullets = []


def redraw_game_window(main_player, players):
    # draw background image
    win.blit(bg, (0, 0))

    for bullet in bullets:
        bullet.draw(win)
        if bullet.x > screen[0] or bullet.x < 0:
            bullets.pop(bullets.index(bullet))

    for i in range(30):
        pygame.draw.rect(win, (0, 255, 0), (WIDTH / 2, i * 30, 30, 30))

    for player in players:
        player.update_pivot()

        rotated_img, rect = rotate_image(tank_img, player.angle, player.pivot, player.offset)
        player.draw(win, rotated_img, rect)

        rotated_img, rect = rotate_image(gun_img, player.turret.angle, player.pivot, player.turret.offset)
        player.turret.draw(win, rotated_img, rect)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Primmary Ammo: " + str(main_player.turret.primary_ammo), True, (0, 0, 0))
    win.blit(text, (50, 100))

    pygame.display.update()


def event_handling(player, n):
    global bullets
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.update_pivot()
    player.turret.rotate(mouse_x, mouse_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.turret.primary_ammo > 0:
            # send code to server that indicates that this player fired a bullet
            bullets = n.send("0")
            # n.send(bullets)
            # bullets = n.send(player)
            # bullets.append(Bullet(player.pivot, player.turret.angle))
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
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.`


def main():
    n = Network()
    main_player = n.getPlayerObject()
    while True:
        clock.tick(FPS)
        players = n.send(main_player)

        event_handling(main_player, n)
        redraw_game_window(main_player, players)



if __name__ == "__main__":
    main()
