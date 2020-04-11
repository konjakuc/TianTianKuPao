import random
import pygame

# 设置屏幕
SCREEN_RECT = pygame.Rect(0, 0, 1280, 720)
# 设置刷新帧率
FPS = 60
# 设置生成障碍物的事件
CREAT_OBSTACLE = pygame.USEREVENT
# 设置生成金币的事件
CREAT_FRUITS = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """游戏精灵"""

    def __init__(self, imageName, speed_x=-15):
        super().__init__()

        self.image = pygame.image.load(imageName)
        self.rect = self.image.get_rect()
        self.speed_x = speed_x

    def update(self):
        self.rect.x += self.speed_x


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        # 1. 调用父类方法实现精灵的创建(image/rect/speed_x)
        super().__init__("resources/images/background.jpg")

        # 2. 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.x = SCREEN_RECT.right

    def update(self):

        # 1. 调用父类的update方法
        super().update()
        # 2. 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的右侧
        if self.rect.right <= 0:
            self.rect.x = SCREEN_RECT.right


class Role(GameSprite):
    """角色精灵"""

    def __init__(self):

        self.i = 0  # (self.i // 2)是人物动作的图片的下标
        super().__init__("resources/images/role.png", 10)

        self.com_image = self.image  # 加载的完整的人物图片
        self.comImg_width = self.com_image.get_width()
        self.comImg_height = self.com_image.get_height()

        self.rect = pygame.Rect(-110, 435, 110, 110)  # 人物的矩形区域

        self.speed_y = 0
        self.isJumping = False
        self.num_jumped = 0  # 记录在空中跳的次数

        self.distance = 0  # 距离分
        self.bonus = 0  # 奖励分
        self.totalScore = 0  # 总分

    def update(self):

        # 人物从左侧出现, x > 200 时不再向前移动
        self.rect.x += self.speed_x
        if self.rect.x >= 200:
            self.rect.x = 200
            self.distance += 1

        # 如果正在跳 保持动作不变(在空中跑的动作很滑稽)
        if self.isJumping:
            self.i = 6
            # 人物下落时 换一个动作
            if self.speed_y >= 0:
                self.i = 22

            self.jump()  # 上面是调整动作，这个主要调整人物在y轴的位置

        # 提取人物每个动作的图片 surface.subsurface(x, y, width, height)
        self.image = self.com_image.subsurface(
            (self.comImg_width / 12) * (self.i // 2), 0, (self.comImg_width / 12), self.comImg_height
        )

        # 循环12个人物动作 实现人物跑的动画效果
        self.i += 1
        if self.i == 24:
            self.i = 0

        self.totalScore = self.distance + self.bonus

    def jump(self):

        self.speed_y += 0.98  # (设成1落地太快)
        self.rect.y += self.speed_y
        if self.rect.y >= 435:
            self.rect.y = 435
            self.isJumping = False
            self.num_jumped = 0


class Obstacle(GameSprite):
    """障碍物精灵"""

    def __init__(self, imageName, y=0, speed_x=-15):
        super().__init__(imageName, speed_x)
        self.rect.x = random.choice([SCREEN_RECT.right + SCREEN_RECT.width / 2, 2 * SCREEN_RECT.width])
        self.rect.y = y
        self.alive = True  # 注意不是精灵的alive()方法，只是自己定义的一个标识符

    def update(self):
        super().update()
        # 如果图片移出屏幕 使用kill方法将自动调用__del__删除这个障碍物
        if self.rect.right <= 0:
            self.kill()


class Fruits(GameSprite):
    """食物精灵"""

    def __init__(self):
        super().__init__("resources/images/fruits.png")
        self.com_image = self.image  # 加载的完整的金币图片
        self.comImg_width = self.com_image.get_width()
        self.comImg_height = self.com_image.get_height()

        self.index = random.randint(0, 2)  # 单个金币的下标
        self.image = self.com_image.subsurface(
            (self.comImg_width / 3) * self.index, 0, (self.comImg_width / 3), self.comImg_height
        )
        self.rect.x = SCREEN_RECT.right + SCREEN_RECT.right / 4
        self.rect.y = random.choice([450, 350, 250])

    def update(self):
        super().update()
        # 如果图片移出屏幕 使用kill方法将自动调用__del__删除这个金币
        if self.rect.right <= 0:
            self.kill()
