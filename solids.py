import include.transformations as tr
import include.easy_shaders as es
import include.scene_graph as sg
import include.basic_shapes as bs

from OpenGL.GL import *


class HitBox:
    def __init__(self, x, y, z, w, d, h):
        self.x = x
        self.y = y
        self.z = z
        self.width = w
        self.depth = d
        self.height = h

    def collidesWith(self, hitbox):
        if self.z + self.height > hitbox.z and self.z < hitbox.z + hitbox.height:
            if self.y + self.depth > hitbox.y and self.y < hitbox.y + hitbox.depth:
                if self.x < hitbox.x + hitbox.width and self.x + self.width > hitbox.x:
                    return True

    # TODO: Remove view class from model code
    def hitboxShape(self, r=1.0, g=0.0, b=0.0):

        # Defining the location and colors of each vertex  of the shape
        vertices = [
            #    positions        colors
            0, 0, self.height, r, g, b,
            self.width, 0, self.height, r, g, b,
            self.width, self.depth, self.height, r, g, b,
            0, self.depth, self.height, r, g, b,

            0, 0, 0, r, g, b,
            self.width, 0, 0, r, g, b,
            self.width, self.depth, 0, r, g, b,
            0, self.depth, 0, r, g, b]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = [
            0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            4, 5, 1, 1, 0, 4,
            6, 7, 3, 3, 2, 6,
            5, 6, 2, 2, 1, 5,
            7, 4, 0, 0, 3, 7]

        return bs.Shape(vertices, indices)


class Platform(HitBox):
    def __init__(self, x, y, z):
        super().__init__(x, y, z - 0.1, 1.0, 1.0, 0.13)

    def drawPlatform(self):

        platform = sg.SceneGraphNode("Platform ("
                                     + str(self.x) + ", "
                                     + str(self.y) + ", "
                                     + str(self.z)
                                     + ") Position")
        platform.transform = tr.translate(self.x, self.y, self.z)
        platform.childs += [es.toGPUShape(self.hitboxShape(0.7, 0.3, 0.3), GL_REPEAT, GL_NEAREST)]

        return platform


class Banana(HitBox):
    def __init__(self, x, y, z):
        super().__init__(x, y, z - 0.1, 0.2, 0.2, 0.2)

    # TODO: Remove view class from model code
    def drawPlatform(self):

        platform_scale = sg.SceneGraphNode("Banana Scale")
        platform_scale.childs += [es.toGPUShape(self.hitboxShape(0.7, 0.7, 0.0), GL_REPEAT, GL_NEAREST)]
        platform_position = sg.SceneGraphNode("Banana Position")
        platform_position.transform = tr.translate(self.x, self.y, self.z)
        platform_position.childs += [platform_scale]

        return platform_position


class FakePlatform(Platform):
    def __init__(self, x, y, z):
        super().__init__(x, y, z - 0.1)
        self.blinking = False
