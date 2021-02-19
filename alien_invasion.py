import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()  # 这个不用是因为我在settings里设置了screen，就是原始的屏幕
        self.screen = self.settings.screen  # 这边必须要先定义screen，不然ship的__init__用不了
        pygame.display.set_caption("Alien Invasion")
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 创建存储游戏统计信息的实例，并创建记分牌
        self.score_board = Scoreboard(self, '')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, 'Play')

        self._create_fleet()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:  # 当活动处于活动状态时
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """单击Play按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            # 重置游戏统计信息
            self.stats.game_active = True
            self.stats.reset_stats()  # 重置飞船数量和分数
            self.score_board.prep_score("Current score:")  # 重置显示分数
            self.score_board.prep_level("Current level:")  # 重置当前等级
            self.score_board.prep_ships()  # 重置飞船
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)  # 开始游戏就隐藏鼠标

    def _check_key_down_event(self, event):
        """响应按下按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_key_up_event(self, event):
        """响应松开按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组"""
        if len(self.bullets) < self.settings.bullets_allowed:  # 屏幕上的子弹少于限额才能发射子弹
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """更新屏幕上的图集，并切换到新的屏幕"""
        self.settings.build_screen()  # 每次循环都重绘屏幕
        self.ship.blit_me()  # 放置飞船
        for bullet in self.bullets.sprites():  # 绘制子弹
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # 放置外星人
        # 显示得分
        self.score_board.show_score()

        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 让绘制的屏幕可见
        pygame.display.flip()

    def _update_bullets(self):
        """更新子弹位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检测是否有子弹击中了外星人，是，则删除子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 击中得分
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.score_board.prep_score("Current score:")  # 更新分数
            self.score_board.check_high_score()  # 更新最高分
        # 如果现在屏幕上的外星人被消灭完
        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # 提高等级并显示
            self.stats.level += 1
            self.score_board.prep_level("Current level:")

    def _update_aliens(self):
        """更新外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检测到达外星人底部
        self._check_aliens_bottom()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可以容纳多少个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen.get_rect().width - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)  # 间距为外星人的宽度
        # 计算屏幕可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen.get_rect().height - 3 * alien_height - ship_height
        number_rows = available_space_y // (2 * alien_height)
        # 创建一群外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人，并将其放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时，采取措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """飞船被撞到"""
        if self.stats.ships_left > 0:
            # 将飞船数减一并更新记分牌
            self.stats.ships_left -= 1
            self.score_board.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()  # 让飞船居中
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检测到外星人到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


if __name__ == '__main__':
    # 创建实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
