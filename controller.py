import include.transformations as tr
import include.easy_shaders as es
import include.basic_shapes as bs
import include.scene_graph as sg

import solids
import monkey


class Controller:
    def __init__(self):
        self.leftKeyOn = False
        self.rightKeyOn = False
        self.forwrdKeyOn = False
        self.backwrdKeyOn = False
        self.jumpKeyOn = False
        self.monkey = None
        self.gravity = -0.005
        self.platform_list = []
        self.fake_platform_list = []
        self.current_floor = 0
        self.banana = None
        self.lost = False
        self.won = False
        self.end_game_time = 0

        #TODO: Remove fill polygon debugging
        self.fillPolygon = True
        self.showAxis = True

    def createMonkey(self):
        self.monkey = monkey.Monkey(2.3, 1.0, 0.0)
        self.monkey.gravity = self.gravity

    def moveMonkey(self):
        if self.banana.collidesWith(self.monkey):
            self.monkey.has_banana = True

        for platform in self.platform_list:
            if self.monkey.collidesWith(platform):
                if self.monkey.is_jumping or self.monkey.is_falling:
                    if platform.z < self.monkey.z < platform.z + platform.height < self.monkey.z + self.monkey.height:
                        self.monkey.z = platform.z + platform.height
                        self.monkey.is_jumping = False
                        self.monkey.is_falling = False
                        self.monkey.jump_vel = 0.0
                        return
                    elif self.monkey.z < platform.z < self.monkey.z + self.monkey.height < platform.z + platform.height:
                        self.monkey.z = platform.z - self.monkey.height
                        self.monkey.start_fall()
                        return

                elif self.leftKeyOn or self.rightKeyOn:
                    if self.monkey.x < platform.x + platform.width < self.monkey.x + self.monkey.width:
                        self.monkey.x = platform.x + platform.width
                        return
                    elif self.monkey.x < platform.x < self.monkey.x + self.monkey.width:
                        self.monkey.x = platform.x - self.monkey.width
                        return
            else:
                if self.monkey.is_falling is False and self.monkey.is_jumping is False:
                    self.monkey.start_fall()

        for fake_platform in self.fake_platform_list:
            if self.monkey.collidesWith(fake_platform):
                fake_platform.blinking = True
                self.fake_platform_list.remove(fake_platform)

        self.monkey.move_x(self.leftKeyOn, self.rightKeyOn)
        self.monkey.move_y(self.forwrdKeyOn, self.backwrdKeyOn)
        self.monkey.move_z()

        if self.monkey.z < 0:
            self.monkey.z = 0
            self.monkey.is_jumping = False
            self.monkey.is_falling = False
            return
        elif self.monkey.x < 0.8:
            self.monkey.x = 0.8
            return
        elif self.monkey.x > 3.9:
            self.monkey.x = 3.9
            return
        elif self.monkey.y < 0.8:
            self.monkey.y = 0.8
            return
        elif self.monkey.y > 3.9:
            self.monkey.y = 3.9
            return

    # TODO: Remove view class from model code
    def drawStage(self):
        stage_scene = sg.SceneGraphNode("stage_scene")

        for platform in self.platform_list:
            stage_scene.childs += [platform.drawPlatform()]

        for fake_platform in self.fake_platform_list:
            stage_scene.childs += [fake_platform.drawPlatform()]

        if self.banana is not None:
            stage_scene.childs +=[self.banana.drawPlatform()]

        return stage_scene

    def add_platform(self, x, y, z):
        self.platform_list.append(solids.Platform(x+1, y+1, z+1))

    def add_fake_platform(self, x, y, z):
        self.fake_platform_list.append(solids.FakePlatform(x+1, y+1, z+1))

    def createBanana(self):
        self.banana = solids.Banana(self.platform_list[len(self.platform_list) - 1].x +
                                    self.platform_list[len(self.platform_list) - 1].width*0.5,
                                    self.platform_list[len(self.platform_list) - 1].x +
                                    self.platform_list[len(self.platform_list) - 1].depth*0.5,
                                    self.platform_list[len(self.platform_list) - 1].z + 0.6)

        self.banana.x -= self.banana.width*0.5
        self.banana.y -= self.banana.depth*0.5
