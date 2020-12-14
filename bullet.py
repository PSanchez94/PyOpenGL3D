"""
Pablo Sanchez.

Monkey movement and animation definitions.

"""
import include.easy_shaders as es

import solids


class Bullet(solids.HitBox):
    def __init__(self, x, y, z, direction):
        super().__init__(x, y, z, 0.1, 0.3, 0.1)
        self.speed = 0.02 * (1.0 - direction*2)
        self.collided = False

    def move_bullet(self):
        self.y += self.speed

    def createShape(self):
        self.hitbox_shape = es.toGPUShape(self.hitboxShape(0.3, 0.1, 0.4))

    def collidesWith(self, hitbox):
        return super().collidesWith(hitbox)
