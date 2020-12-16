"""
Pablo Sanchez.

Monkey movement and animation definitions.

"""
from OpenGL.GL import *

import include.basic_shapes as bs

import solids


class Bullet(solids.HitBox):
    def __init__(self, x, y, z, direction):
        super().__init__(x, y, z, 0.1, 0.3, 0.1)
        self.speed = 0.02 * (1.0 - direction * 2)
        self.collided = False

    # TODO: Remove view class from model code
    def hitboxShape(self, texture):
        # Defining the location and texture coordinates of each vertex  of the shape
        vertices = [
            # Z+
            0.0, 0.0, self.height, 0.0, 1.0,
            self.width, 0.0, self.height, 1.0, 1.0,
            self.width, self.depth*0.5, self.height, 1.0, 0.0,
            0.0, self.depth*0.5, self.height, 0.0, 0.0,

            # Z-
            0.0, 0.0, 0.0, 0.0, 1.0,
            self.width, 0.0, 0.0, 1.0, 1.0,
            self.width, self.depth*0.5, 0.0, 1.0, 0.0,
            0.0, self.depth*0.5, 0.0, 0.0, 0.0,

            # X+
            self.width, 0.0, 0.0, 0.0, 1.0,
            self.width, self.depth*0.5, 0.0, 1.0, 1.0,
            self.width, self.depth*0.5, self.height, 1.0, 0.0,
            self.width, 0.0, self.height, 0.0, 0.0,

            # X-
            0.0, 0.0, 0.0, 0.0, 1.0,
            0.0, self.depth*0.5, 0.0, 1.0, 1.0,
            0.0, self.depth*0.5, self.height, 1.0, 0.0,
            0.0, 0.0, self.height, 0.0, 0.0,

            # Y+
            0.0, self.depth*0.5, 0.0, 0.0, 1.0,
            self.width, self.depth*0.5, 0.0, 1.0, 1.0,
            self.width, self.depth*0.5, self.height, 1.0, 0.0,
            0.0, self.depth*0.5, self.height, 0.0, 0.0,

            # Y-
            0.0, 0.0, 0.0, 0.0, 1.0,
            self.width, 0.0, 0.0, 1.0, 1.0,
            self.width, 0.0, self.height, 1.0, 0.0,
            0.0, 0.0, self.height, 0.0, 0.0,

            self.width * 0.5, self.depth * 1.5, self.height * 0.5, 1.0, 1.0  # Y+ Bullet point
        ]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = [
            0, 1, 2, 2, 3, 0,  # Z+
            7, 6, 5, 5, 4, 7,  # Z-
            8, 9, 10, 10, 11, 8,  # X+
            15, 14, 13, 13, 12, 15,  # X-
            19, 18, 24, 18, 17, 24,  # Y+ Bullet point
            17, 16, 24, 16, 19, 24,  # Y+ Bullet point
            20, 21, 22, 22, 23, 20]  # Y-

        return bs.Shape(vertices, indices, texture)

    def move_bullet(self):
        self.y += self.speed
