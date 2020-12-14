import random as rnd
import solids
import monkey
import bullet



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
        self.bullets = []
        self.current_floor = 0
        self.banana = None
        self.lost = False
        self.won = False
        self.end_game_time = 0
        self.last_bullet_time = 0

        #TODO: Remove fill polygon debugging
        self.fillPolygon = True
        self.showAxis = False

    def createMonkey(self):
        self.monkey = monkey.Monkey(3.5, 1.5, 0.0)
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

                elif self.forwrdKeyOn or self.backwrdKeyOn:
                    if self.monkey.y < platform.y + platform.depth < self.monkey.y + self.monkey.depth:
                        self.monkey.y = platform.y + platform.depth
                        return
                    elif self.monkey.y < platform.y < self.monkey.y + self.monkey.depth:
                        self.monkey.y = platform.y - self.monkey.depth
                        return
            else:
                if self.monkey.is_falling is False and self.monkey.is_jumping is False:
                    self.monkey.start_fall()

        for fake_platform in self.fake_platform_list:
            if self.monkey.collidesWith(fake_platform):
                fake_platform.blinking = True
                self.fake_platform_list.remove(fake_platform)

        for a_bullet in self.bullets:
            if self.monkey.collidesWith(a_bullet):
                a_bullet.collided = True

        self.monkey.move_x(self.leftKeyOn, self.rightKeyOn)
        self.monkey.move_y(self.forwrdKeyOn, self.backwrdKeyOn)
        self.monkey.move_z()

        if self.monkey.z < 0:
            self.monkey.z = 0
            self.monkey.is_jumping = False
            self.monkey.is_falling = False
            return
        elif self.monkey.x < 0.0:
            self.monkey.x = 0.0
            return
        elif self.monkey.x > 6.5:
            self.monkey.x = 6.5
            return
        elif self.monkey.y < 0.0:
            self.monkey.y = 0.0
            return
        elif self.monkey.y > 3.9:
            self.monkey.y = 3.9
            return

    def add_platform(self, x, y, z):
        self.platform_list.append(solids.Platform(x+1, y, z+1))

    def add_fake_platform(self, x, y, z):
        self.fake_platform_list.append(solids.FakePlatform(x+1, y, z+1))

    def check_bullets(self, time):
        if len(self.bullets) < 4 and time - self.last_bullet_time > 1.0:
            direction = rnd.randrange(0, 2)
            self.bullets.append(bullet.Bullet(rnd.randrange(1, 6) + 0.4,
                                              4.0*direction,
                                              rnd.randrange(0, 3) + 0.3,
                                              direction))
            self.last_bullet_time = time

        for a_bullet in self.bullets:
            a_bullet.move_bullet()
            if a_bullet.collided or a_bullet.y > 4.0 or a_bullet.y < -0.4:
                self.bullets.remove(a_bullet)


    def createBanana(self):
        self.banana = solids.Banana(self.platform_list[len(self.platform_list) - 1].x +
                                    self.platform_list[len(self.platform_list) - 1].width*0.5,
                                    self.platform_list[len(self.platform_list) - 1].y +
                                    self.platform_list[len(self.platform_list) - 1].depth*0.5,
                                    self.platform_list[len(self.platform_list) - 1].z + 0.6)

        self.banana.x += self.banana.width*0.5
        self.banana.y += self.banana.depth*0.5
