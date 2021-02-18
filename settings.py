import pygame


class Settings:
    """存储游戏的所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置--背景长，宽和背景图片
        # self.size = (1200, 700)  # 设置屏幕大小,这个是小窗口
        # self.screen = pygame.display.set_mode(self.size)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background = pygame.image.load('images/background.jpg')
        # 飞船速度设置
        self.ship_speed = 1.5
        self.ship_limit = 3
        # 子弹速度设置
        self.bullet_speed = 1.5
        # 子弹上限设置，屏幕上最多有10颗子弹
        self.bullets_allowed = 15
        # 外星人速度
        self.alien_speed = 10
        self.fleet_drop_speed = 20
        # fleet_direction 为1表示向右移动，-1表示向左移动
        self.fleet_direction = 1

    def build_screen(self):
        self.screen.blit(pygame.transform.scale(self.background,
                                                (self.screen.get_rect().width, self.screen.get_rect().height)),
                         (0, 0))  # 伸缩背景
