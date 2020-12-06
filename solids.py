import include.transformations as tr
import include.easy_shaders as es
import include.scene_graph as sg
import include.basic_shapes as bs

from OpenGL.GL import *


class HitBox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def collidesWith(self, hitbox):
        if self.y + self.height > hitbox.y and self.y < hitbox.y + hitbox.height:
            if self.x < hitbox.x + hitbox.width and self.x + self.width > hitbox.x:
                return True

    def hitboxShape(self, image_filename):

        r = 1.0
        g = 0.0
        b = 0.0

        # Defining locations and colors for each vertex of the shape
        vertices = [
            #   positions        colors
            0.0, 0.0, 0.0, 0.0, 1.0,
            self.width, 0.0, 0.0, 1.0, 1.0,
            self.width, self.height, 0.0, 1.0, 0.0,
            0.0, self.height, 0.0, 0.0, 0.0]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = [
            0, 1, 2,
            2, 3, 0]

        textureFileName = image_filename

        return bs.Shape(vertices, indices, textureFileName)


class Platform(HitBox):
    def __init__(self, x, y):
        super().__init__(x, y - 0.1, 1.0, 0.13)

    def drawPlatform(self):

        platform = sg.SceneGraphNode("Platform (" + str(self.x) + ", " + str(self.y) + ") Position")
        platform.transform = tr.translate(self.x, self.y, 0)
        platform.childs += [es.toGPUShape(self.hitboxShape("textures/platform.png"), GL_REPEAT, GL_NEAREST)]

        return platform


class Banana(HitBox):
    def __init__(self, x, y):
        super().__init__(x, y - 0.1, 0.2, 0.2)

    def drawPlatform(self):

        platform_scale = sg.SceneGraphNode("Banana Scale")
        platform_scale.childs += [es.toGPUShape(self.hitboxShape("textures/banana.png"), GL_REPEAT, GL_NEAREST)]
        platform_position = sg.SceneGraphNode("Banana Position")
        platform_position.transform = tr.translate(self.x, self.y, 0)
        platform_position.childs += [platform_scale]

        return platform_position
