class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False  # 表示游戏处于非活动状态
        self.high_score = 0  # 最高得分

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
