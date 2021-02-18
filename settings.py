import pygame


class Settings:
    """存储游戏的所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置--背景长，宽和背景
        self.size = (1200, 700)  # 设置屏幕大小
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.image.load('images/background.jpg')
        # 飞船设置
        self.ship_speed = 2

    def build_screen(self):
        self.screen.blit(pygame.transform.scale(self.background, self.size), (0, 0))  # 伸缩背景
