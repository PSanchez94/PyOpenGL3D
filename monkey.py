"""
Pablo Sanchez.

Monkey movement and animation definitions.

"""
import include.transformations as tr
import include.easy_shaders as es

# SCENE GRAPH TODO: Is this neccesary?
import include.scene_graph as sg

import solids

jump_start_vel = 0.105


class Monkey(solids.HitBox):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0.3, 0.3, 0.5)
        self.hitpoints = 3
        self.x_speed = 0.05
        self.y_speed = 0.05
        self.jump_vel = 0.0
        self.gravity = -0.01
        self.is_jumping = False
        self.is_falling = False
        self.jump_start_time = 0
        self.jump_fall_time = 0
        self.collision = True
        self.has_banana = False

    def move_x(self, left, right):
        self.x += self.x_speed * (left - right)

    def move_y(self, forwrd, backwrd):
        self.y += self.y_speed * (forwrd - backwrd)

    def move_z(self):
        if self.is_jumping or self.is_falling:
            self.z += self.jump_vel
            self.jump_vel = max(self.jump_vel + self.gravity, -0.105)

    def start_jump(self):
        if self.is_jumping is False:
            self.jump_vel = jump_start_vel
            self.is_jumping = True
            self.is_falling = False

    def start_fall(self):
        self.is_falling = True
        self.jump_vel = 0.0
        self.is_jumping = False

    def createShape(self):
        self.hitbox_shape = es.toGPUShape(self.hitboxShape())

    def collidesWith(self, hitbox):
        if self.collision:
            return super().collidesWith(hitbox)
