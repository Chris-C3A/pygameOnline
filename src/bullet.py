import pygame
import math


class Bullet(object):
    def __init__(self, pivot, angle, damage=25):
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

    def draw(self, win):
        """
        draws and updates bullet object
        :param win: Window
        :return: None
        """
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)
        # for i in range(50):
            # pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        # self.x += self.vel * self.facing
        # print(self.angle)
        self.x += self.vel * math.sin(math.radians(self.angle))
        self.y += self.vel * math.cos(math.radians(self.angle)) * -1
