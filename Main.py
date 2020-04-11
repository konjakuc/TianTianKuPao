import os
import pygame
from Sprite import *


class KuPaoGame(object):
    """酷跑主游戏"""

    isFirstInit = True  # 是否第一次初始化
    maxScore = 0  # 最高分

    def __init__(self):

        pygame.init()

        self.isPlaying = False  # 是否正在游戏
        self.game_over = False  # 是否游戏结束

        # 创建游戏的窗口
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 30)  # 窗口位置
        pygame.display.set_caption("天天酷跑")  # 窗口标题
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)  # 窗口尺寸

        self.__loadResources()  # 加载资源
        self.__create_sprites()  # 创建精灵和精灵组

        # 创建游戏的时钟 用来设置最大帧率
        self.clock = pygame.time.Clock()

        # 事件监听里用来延时展示某个界面或事件的时间戳
        self.tick1 = self.tick2 = self.tick3 = self.tick4 = 0

        # 设置生成障碍物的定时器   1.6 s (1600毫秒)
        pygame.time.set_timer(CREAT_OBSTACLE, 1600)
        # 设置生成金币的定时器
        pygame.time.set_timer(CREAT_FRUITS, 1600)

    # 加载资源文件
    def __loadResources(self):

        self.interface_start = pygame.image.load("resources/images/start.jpg")  # 开始界面图片
        self.interface_score = pygame.image.load("resources/images/score.jpg")  # 结算分数图片
        self.interface_txgame = pygame.image.load("resources/images/tencentgame.jpg")  # tencentgame图片
        self.interface_TiMi = pygame.image.load("resources/images/TiMi.jpg")  # TiMi图片

        self.font1 = pygame.font.SysFont("freesansbold", 80)
        # self.font1 = pygame.font.Font("resources/freesansbold.ttf", 80)
        self.font2 = pygame.font.SysFont("simhei", 30)

        self.sound_jump = pygame.mixer.Sound("resources/jump.wav")  # 角色跳的音效
        self.sound_getStar = pygame.mixer.Sound("resources/get_star.wav")  # 吃到星星和金币
        self.sound_alert = pygame.mixer.Sound("resources/alert.wav")  # 火焰警报音效
        self.sound_dead = pygame.mixer.Sound("resources/dead.wav")  # 角色死亡音效
        self.sound_gmov = pygame.mixer.Sound("resources/game_over.wav")  # gameover音效
        self.sound_TiMi = pygame.mixer.Sound("resources/timi.wav")
        self.bgmusic1 = pygame.mixer.music.load("resources/bgmusic1.mp3")  # 背景音乐1
        self.bgmusic2 = pygame.mixer.Sound("resources/bgmusic2.wav")  # 背景音乐2

    # 创建精灵和精灵组
    def __create_sprites(self):

        # 创建背景精灵和精灵组
        background1 = Background()
        background2 = Background(True)
        self.bg_group = pygame.sprite.Group(background1, background2)

        # 创建角色精灵和精灵组
        self.role = Role()
        self.role_group = pygame.sprite.Group(self.role)

        # 创建障碍物精灵组
        self.obstacle_group = pygame.sprite.Group()

        # 创建食物精灵组
        self.fruits_group = pygame.sprite.Group()

    # 选择生成哪种障碍物
    def __choice_obstacle(self):

        dingzi = Obstacle("resources/images/dingzi.png", 462)
        gaoguai = Obstacle("resources/images/gaoguai.png", 417)
        sdg = Obstacle("resources/images/sdg.png", 110)
        self.flame = Obstacle("resources/images/flame.png", 215, -17)

        self.ran_obstacle = random.choice([self.flame, dingzi, gaoguai, [sdg, gaoguai], [sdg, dingzi]])

        return self.ran_obstacle

    # 事件监听
    def __event_handler(self):

        for event in pygame.event.get():

            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # 第一次初始化需要加载tencentgame,TiMi图片及TiMi音效
            elif self.isFirstInit:

                tick = pygame.time.get_ticks()
                if tick <= 3000:
                    self.screen.blit(self.interface_txgame, (0, 0))
                elif tick <= 6000:
                    self.screen.blit(self.interface_TiMi, (0, 0))
                    self.num_sd_TiMi = self.sound_TiMi.get_num_channels()
                    # 音效只加载一次
                    if self.num_sd_TiMi < 1:
                        self.sound_TiMi.play()
                # 第一次加载完成，绘制准备开始界面，并改变isFirstInit标识符
                else:
                    self.screen.blit(self.interface_start, (0, 0))
                    self.isFirstInit = False

            # 判断是否游戏结束，绘制得分界面
            elif self.game_over:

                self.num_sd_gmov = self.sound_gmov.get_num_channels()
                if self.num_sd_gmov < 1:
                    self.sound_gmov.play()
                    self.tick1 = pygame.time.get_ticks()

                self.tick2 = pygame.time.get_ticks()

                # 音效开始播放一秒后展示得分界面
                if self.tick2 - self.tick1 >= 1000:

                    self.__showScore()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.sound_gmov.stop()

                        # 更新历史最高分
                        if self.role.totalScore > self.maxScore:
                            KuPaoGame.maxScore = self.role.totalScore

                        self.__init__()
                        self.screen.blit(self.interface_start, (0, 0))

            # 游戏初始界面，准备开始游戏
            elif not self.isPlaying:

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1, 2.0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    pygame.mixer.music.pause()
                    self.tick3 = pygame.time.get_ticks()

                self.tick4 = pygame.time.get_ticks()

                if self.tick3 != 0 and self.tick4 - self.tick3 >= 500:
                    self.isPlaying = True

            # 判断是否正在游戏
            if self.isPlaying:

                if not pygame.mixer.get_busy():
                    self.bgmusic2.play()

                if event.type == pygame.KEYDOWN:
                    # 判断是否跳跃
                    if event.key == pygame.K_SPACE and self.role.num_jumped <= 2:
                        self.sound_jump.play()  # 跳到音效
                        self.role.speed_y = -15  # y轴初始速度
                        self.role.num_jumped += 1  # 在空中跳的次数
                        self.role.isJumping = True  # 跳的状态

                # 判断是否要生成障碍物
                if event.type == CREAT_OBSTACLE:
                    self.obstacle = self.__choice_obstacle()

                    # 如果障碍物是火焰，播放火焰警报声
                    if self.obstacle == self.flame:
                        self.sound_alert.play()

                    self.obstacle_group.add(self.obstacle)

                # 判断是否要生成金币
                if event.type == CREAT_FRUITS:
                    self.fruit = Fruits()
                    self.fruits_group.add(self.fruit)

    # 碰撞检测
    def __check_collide(self):

        # 判断是否撞到障碍物
        obstacles = pygame.sprite.spritecollide(self.role, self.obstacle_group, False)
        if len(obstacles) > 0:
            self.role.kill()
            self.sound_dead.play()  # 角色死了的音效
            self.bgmusic2.stop()  # 停止播放背景音乐

            print("Game over !")
            self.isPlaying = False
            self.game_over = True
            return

        # 判断是否躲过障碍物
        for i in self.obstacle_group:
            if i.alive and i.rect.right <= self.role.rect.x:
                print("躲过一个障碍物 奖励分+5")
                self.role.bonus += 5
                i.alive = False  # 改变标识符，角色躲过后不需要判断它

        # 判断是否吃到金币
        fruits = pygame.sprite.spritecollide(self.role, self.fruits_group, True)
        if len(fruits) > 0:
            for i in fruits:
                if i.index == 0:
                    print("吃到星星 奖励分+10")
                    self.sound_getStar.play()
                    self.role.bonus += 10
                elif i.index == 1:
                    print("吃到实心金币 奖励分+7")
                    self.sound_getStar.play()
                    self.role.bonus += 7
                else:
                    print("吃到空心金币 奖励分+3")
                    self.sound_getStar.play()
                    self.role.bonus += 3

    # 更新并绘制精灵组
    def __update_sprites(self):

        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.role_group.update()
        self.role_group.draw(self.screen)

        self.obstacle_group.update()
        self.obstacle_group.draw(self.screen)

        self.fruits_group.update()
        self.fruits_group.draw(self.screen)

    # 更新显示分数
    def __update_score(self):

        self.distance_Surface = self.font2.render("距离分：" + str(self.role.distance), True, (0, 0, 139))
        self.distance_Rect = self.distance_Surface.get_rect()
        self.distance_Rect.x, self.distance_Rect.y = (30, 10)

        self.bonus_Surface = self.font2.render("奖励分：" + str(self.role.bonus), True, (0, 0, 139))
        self.bonus_Rect = self.bonus_Surface.get_rect()
        self.bonus_Rect.x, self.bonus_Rect.y = (300, 10)

        self.screen.blit(self.distance_Surface, self.distance_Rect)
        self.screen.blit(self.bonus_Surface, self.bonus_Rect)

    # 展示得分界面
    def __showScore(self):

        if self.role.totalScore > self.maxScore:
            self.maxScore_Surface = self.font2.render("新纪录！！", True, (139, 0, 0))
        else:
            self.maxScore_Surface = self.font2.render("历史最高：" + str(self.maxScore), True, (0, 0, 139))
        self.maxScore_Rect = self.maxScore_Surface.get_rect()

        self.totalScore_Surface = self.font1.render(str(self.role.totalScore), True, (139, 0, 0))
        self.totalScore_Rect = self.totalScore_Surface.get_rect()

        self.totalScore_Rect.center = (420, 330)
        self.maxScore_Rect.center = (420, 270)
        self.distance_Rect.x, self.distance_Rect.y = (300, 400)
        self.bonus_Rect.x, self.bonus_Rect.y = (300, 470)

        self.screen.blit(self.interface_score, (0, 0))  # 分数界面
        self.screen.blit(self.totalScore_Surface, self.totalScore_Rect)
        self.screen.blit(self.maxScore_Surface, self.maxScore_Rect)
        self.screen.blit(self.distance_Surface, self.distance_Rect)
        self.screen.blit(self.bonus_Surface, self.bonus_Rect)

    # 开始游戏
    def start_game(self):

        # 游戏循环  一帧一循环(动画效果)
        while True:
            # 1. 设置帧率：每秒最大刷新60次
            self.clock.tick(FPS)
            # 2. 事件监听
            self.__event_handler()
            if self.isPlaying:
                # 3. 碰撞检测
                self.__check_collide()
            if self.isPlaying:
                # 4. 更新/绘制精灵组
                self.__update_sprites()
                # 5. 更新分数
                self.__update_score()
            # 6. 更新显示
            pygame.display.update()


if __name__ == '__main__':
    # 创建游戏对象
    game = KuPaoGame()

    # 启动游戏
    game.start_game()
