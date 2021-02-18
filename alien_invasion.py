import pygame
import sys
from settings import Settings
from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()  # 这个不用是因为我在settings里设置了screen，就是原始的屏幕
        self.screen = self.settings.screen  # 这边必须要先定义screen，不然ship的__init__用不了
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # 这是可以全局游戏的设置，但是我的背景图片不能
        # 全覆盖，而且出现了BUG，不能用
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """监视键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # 退出游戏
            elif event.type == pygame.KEYDOWN:  # 按下按键
                self._check_key_down_event(event)
            elif event.type == pygame.KEYUP:  # 松开按键
                self._check_key_up_event(event)

    def _check_key_down_event(self, event):
        """响应按下按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_key_up_event(self, event):
        """响应松开按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """更新屏幕上的图集，并切换到新的屏幕"""
        self.settings.build_screen()  # 每次循环都重绘屏幕
        self.ship.blit_me()  # 放置飞船
        # 让绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
