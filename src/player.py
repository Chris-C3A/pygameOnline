import pygame
import os
import math
from src.turret import Turret
from src.bullet import Bullet


class Player:
    def __init__(self, idx, x, y, scale=8):
        """
        init player object
        :param idx: int (player id)
        :param x: int
        :param y: int
        :param scale: int
        """
        self.idx = idx
        self.x = x
        self.y = y
        self.scale = scale
        self.w = 500 // self.scale
        self.h = 637 // self.scale
        self.pivot = [self.x+self.w/2, self.y+self.h/2]
        self.offset = pygame.math.Vector2()

        self.health = 100
        self.vel = 3.5  # speed
        self.turn_speed = 2  # speed of turning around using A / D
        self.angle = 0  # counter clockwise angle of the sprite

        self.turret = Turret(self)
        self.bullets = []
        
    def draw(self, win, rotated_img, rect):
        """
        draws the player's sprites onto the screen
        :param win: Window
        :param rotated_img: img
        :param rect: (x, y)
        :return: None
        """
        win.blit(rotated_img, rect)
        self.hitbox(win)

        self.turret.x, self.turret.y = self.x+15, self.y-22

    def rotate(self, direction):
        """
        rotates the tank
        :param direction: int
        :return: None
        """
        self.angle += self.turn_speed * direction
        if self.angle == 360 or self.angle == -360:
            self.angle = 0

    def move(self, direction):
        """
        Updates player's position based on direction and sin/cos its angle
        :param direction: int
        :return: None
        """
        self.x += self.vel * direction * math.sin(math.radians(self.angle)) * -1
        self.y += self.vel * direction * math.cos(math.radians(self.angle))

    def update_pivot(self):
        self.pivot = [self.x + self.w / 2, self.y + self.h / 2]

    def fire(self):
        self.bullets.append(Bullet(self, self.pivot, self.turret.angle))

    def hitbox(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.w, self.h), 1)
        # alternate hitbox
        # pygame.draw.rect(win, (255, 0, 0), rect, 1)

    def got_hit(self):
        self.health -= 25
