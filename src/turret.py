import pygame
import os
import math


class Turret(object):
    def __init__(self, player):
        """
        init turret object
        :param player: Player
        """
        self.player = player
        self.x = player.x
        self.y = player.y
        self.w = 285 // self.player.scale
        self.h = 560 // self.player.scale

        self.offset = pygame.math.Vector2(x=0, y=-25)
        self.angle = 0

        self.primary_ammo = 500  # amount of bullets player has left
        self.secondary_ammo = 5  # amount of rockets player has left

        # self.gun_img = pygame.transform.scale(pygame.image.load(os.path.join("resources", "gun.png")), (self.w, self.h))

    def draw(self, win, rotated_image, rect):
        """
        draw turret sprite onto the screen
        :param win: Window
        :param rotated_image img
        :param rect (x, y)
        :return: None
        """
        # rotated_image, rect = self.player.rotate_image(self.gun_img, self.angle, self.player.pivot, self.offset)
        self.x, self.y = rect.x, rect.y
        win.blit(rotated_image, (self.x, self.y))

    def rotate(self, mouse_x, mouse_y):
        """
        rotates the turret relative to the mouse position
        :param mouse_x: int
        :param mouse_y: int
        :return:
        """
        try:
            tan_angle = (self.player.pivot[0] - mouse_x) / (self.player.pivot[1] - mouse_y)
            a = math.degrees(math.atan(tan_angle)) * - 1

            if mouse_y > self.player.pivot[1]:
                a += 180
            self.angle = a
        except Exception as e:
            print(e)
