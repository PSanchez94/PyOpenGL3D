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
        self.jumpKeyOn = False
        self.monkey = None
        self.gravity = -0.005
        self.platform_list = []
        self.current_floor = 0
        self.banana = None
        self.lost = False
        self.won = False
        self.end_game_time = 0

        #TODO: Remove fill polygon debugging
        self.fillPolygon = False
        self.showAxis = True

    def createMonkey(self):
        self.monkey = monkey.Monkey(2.3, 0.0)
        self.monkey.gravity = self.gravity

    def moveMonkey(self):

        if self.banana.collidesWith(self.monkey):
            self.monkey.has_banana = True

        for platform in self.platform_list:
            if self.monkey.collidesWith(platform):
                if self.monkey.is_jumping or self.monkey.is_falling:
                    if platform.y < self.monkey.y < platform.y + platform.height < self.monkey.y + self.monkey.height:
                        self.monkey.y = platform.y + platform.height
                        self.monkey.is_jumping = False
                        self.monkey.is_falling = False
                        self.monkey.jump_vel = 0.0
                        return
                    elif self.monkey.y < platform.y < self.monkey.y + self.monkey.height < platform.y + platform.height:
                        self.monkey.y = platform.y - self.monkey.height
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

        self.monkey.move_x(self.leftKeyOn, self.rightKeyOn)
        self.monkey.move_y()

        if self.monkey.y < 0:
            self.monkey.y = 0
            self.monkey.is_jumping = False
            self.monkey.is_falling = False
            return
        elif self.monkey.x < 0.8:
            self.monkey.x = 0.8
            return
        elif self.monkey.x > 3.9:
            self.monkey.x = 3.9
            return

    def drawStage(self):
        stage_scene = sg.SceneGraphNode("stage_scene")

        for platform in self.platform_list:
            stage_scene.childs += [platform.drawPlatform()]

        if self.banana is not None:
            stage_scene.childs +=[self.banana.drawPlatform()]

        return stage_scene

    def add_platform(self, x, y):
        self.platform_list.append(solids.Platform(x+1, y+1))

    def createBanana(self):
        self.banana = solids.Banana(self.platform_list[len(self.platform_list) - 1].x +
                                    self.platform_list[len(self.platform_list) - 1].width/2,
                                    self.platform_list[len(self.platform_list) - 1].y + 0.6)

        self.banana.x -= self.banana.width/2
