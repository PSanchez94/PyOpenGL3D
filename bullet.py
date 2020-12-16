"""
Pablo Sanchez.

Monkey movement and animation definitions.

"""
from OpenGL.GL import *

import include.easy_shaders as es

import solids


class Bullet(solids.HitBox):
    def __init__(self, x, y, z, direction):
        super().__init__(x, y, z, 0.1, 0.3, 0.1)
        self.speed = 0.02 * (1.0 - direction*2)
        self.collided = False

    def move_bullet(self):
        self.y += self.speed
