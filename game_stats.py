class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True  # 表示游戏处于活动状态

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
