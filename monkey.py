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
    def __init__(self, x, y):
        super().__init__(x, y, 0.3, 0.5)
        self.x_speed = 0.05
        self.jump_vel = 0.0
        self.gravity = -0.01
        self.is_jumping = False
        self.is_falling = False
        self.jump_start_time = 0
        self.jump_fall_time = 0
        self.collision = True
        self.has_banana = False

    def move_x(self, left, right):
        self.x += self.x_speed * (right - left)

    def move_y(self):
        if self.is_jumping or self.is_falling:
            self.y += self.jump_vel
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

    def createMonkey(self):
        # TODO: How to animate. Change texture per time?
        # monkey_texture= es.toGPUShape(bs.createTextureQuad("textures/wheel.png", 1, 1), GL_REPEAT, GL_NEAREST)

        monkey_texture = sg.SceneGraphNode("Monkey Texture")
        monkey_texture.transform = tr.translate(self.x, self.y - self.height, 0)
        return monkey_texture

    def collidesWith(self, hitbox):
        if self.collision:
            if self.y + self.height > hitbox.y and self.y < hitbox.y + hitbox.height:
                if self.x < hitbox.x + hitbox.width and self.x + self.width > hitbox.x:
                    return True
