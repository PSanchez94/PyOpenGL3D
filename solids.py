import include.easy_shaders as es
import include.basic_shapes as bs


class HitBox:
    def __init__(self, x, y, z, w, d, h):
        self.x = x
        self.y = y
        self.z = z
        self.width = w
        self.depth = d
        self.height = h
        self.hitbox_shape = None

    def collidesWith(self, hitbox):
        if self.z < hitbox.z + hitbox.height and self.z + self.height > hitbox.z:
            if self.y < hitbox.y + hitbox.depth and self.y + self.depth > hitbox.y:
                if self.x < hitbox.x + hitbox.width and self.x + self.width > hitbox.x:
                    return True

    # TODO: Remove view class from model code
    def hitboxShape(self, texture):

        # Defining the location and texture coordinates of each vertex  of the shape
        vertices = [
            # Z+
            0.0, 0.0, self.height, 0.0, 1.0,
            self.width, 0.0, self.height, 1.0, 1.0,
            self.width, self.depth, self.height, 1.0, 0.0,
            0.0, self.depth, self.height, 0.0, 0.0,

            # Z-
            0.0, 0.0, 0.0, 0.0, 1.0,
            self.width, 0.0, 0.0, 1.0, 1.0,
            self.width, self.depth, 0.0, 1.0, 0.0,
            0.0, self.depth, 0.0, 0.0, 0.0,

            # X+
            self.width, 0.0, 0.0, 0.0, 1.0,
            self.width, self.depth, 0.0, 1.0, 1.0,
            self.width, self.depth, self.height, 1.0, 0.0,
            self.width, 0.0, self.height, 0.0, 0.0,

            # X-
            0.0, 0.0, 0.0, 0.0, 1.0,
            0.0, self.depth, 0.0, 1.0, 1.0,
            0.0, self.depth, self.height, 1.0, 0.0,
            0.0, 0.0, self.height, 0.0, 0.0,

            # Y+
            0.0, self.depth, 0.0, 0.0, 1.0,
            self.width, self.depth, 0.0, 1.0, 1.0,
            self.width, self.depth, self.height, 1.0, 0.0,
            0.0, self.depth, self.height, 0.0, 0.0,

            # Y-
            0.0, 0.0, 0.0, 0.0, 1.0,
            self.width, 0.0, 0.0, 1.0, 1.0,
            self.width, 0.0, self.height, 1.0, 0.0,
            0.0, 0.0, self.height, 0.0, 0.0
            ]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = [
            0, 1, 2, 2, 3, 0,  # Z+
            7, 6, 5, 5, 4, 7,  # Z-
            8, 9, 10, 10, 11, 8,  # X+
            15, 14, 13, 13, 12, 15,  # X-
            19, 18, 17, 17, 16, 19,  # Y+
            20, 21, 22, 22, 23, 20]  # Y-

        return bs.Shape(vertices, indices, texture)

    def createShape(self, gpuShape):
        self.hitbox_shape = gpuShape


class Platform(HitBox):
    def __init__(self, x, y, z):
        super().__init__(x, y, z - 0.1, 1.0, 1.0, 0.13)

    # TODO: Remove view class from model code
    def hitboxShape(self, texture):

        # Defining the location and texture coordinates of each vertex  of the shape
        vertices = [
            # Z+
            0.0, 0.0, self.height, 0.0, 9/10,
            self.width, 0.0, self.height, 1.0, 9/10,
            self.width, self.depth, self.height, 1.0, 0.0,
            0.0, self.depth, self.height, 0.0, 0.0,

            # Z-
            0.0, 0.0, 0.0, 0.0, 9/10,
            self.width, 0.0, 0.0, 1.0, 9/10,
            self.width, self.depth, 0.0, 1.0, 0.0,
            0.0, self.depth, 0.0, 0.0, 0.0,

            # X+
            self.width, 0.0, 0.0, 0.0, 10/10,
            self.width, self.depth, 0.0, 1.0, 10/10,
            self.width, self.depth, self.height, 1.0, 9/10,
            self.width, 0.0, self.height, 0.0, 9/10,

            # X-
            0.0, 0.0, 0.0, 0.0, 10/10,
            0.0, self.depth, 0.0, 1.0, 10/10,
            0.0, self.depth, self.height, 1.0, 9/10,
            0.0, 0.0, self.height, 0.0, 9/10,

            # Y+
            0.0, self.depth, 0.0, 0.0, 10/10,
            self.width, self.depth, 0.0, 1.0, 10/10,
            self.width, self.depth, self.height, 1.0, 9/10,
            0.0, self.depth, self.height, 0.0, 9/10,

            # Y-
            0.0, 0.0, 0.0, 0.0, 10/10,
            self.width, 0.0, 0.0, 1.0, 10/10,
            self.width, 0.0, self.height, 1.0, 9/10,
            0.0, 0.0, self.height, 0.0, 9/10
            ]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = [
            0, 1, 2, 2, 3, 0,  # Z+
            7, 6, 5, 5, 4, 7,  # Z-
            8, 9, 10, 10, 11, 8,  # X+
            15, 14, 13, 13, 12, 15,  # X-
            19, 18, 17, 17, 16, 19,  # Y+
            20, 21, 22, 22, 23, 20]  # Y-

        return bs.Shape(vertices, indices, texture)


class Banana(HitBox):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0.2, 0.2, 0.2)


class FakePlatform(Platform):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.blinking = False
        self.blink_time = 0.0
