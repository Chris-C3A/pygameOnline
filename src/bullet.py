import pygame
import math


class Bullet(object):
    def __init__(self, player, pivot, angle, damage=25):
        """
        init Bullet object
        :param pivot: (x, y)
        :param angle: float
        :param damage: int
        """
        self.x = pivot[0]
        self.y = pivot[1]
        self.radius = 7
        self.color = (255, 0, 0)
        self.angle = angle
        self.vel = 20
        self.damage = damage

        self.player = player

    def draw(self, win):
        """
        draws and updates bullet object
        :param win: Window
        :return: None
        """
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        """
        movement of bullet
        :return: None
        """
        self.x += self.vel * math.sin(math.radians(self.angle))
        self.y += self.vel * math.cos(math.radians(self.angle)) * -1

    def collide(self, player):
        # print(self.player.idx == player.idx)
        return player.x < self.x < player.x + player.w and player.y < self.y < player.y + player.h
