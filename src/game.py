class Game:
    def __init__(self, idx):
        self.idx = idx
        self.players = []
        self.bullets = []

    def get_players(self):
        return self.players

    def get_bullets(self):
        return self.bullets

    # def collide(self):
    #     for bullet in self.bullets:
    #         for player in self.players:
    #             if self.checkCollision(bullet, player):
    #                 print("[LOG] collision")
    #                 self.bullets.pop(self.bullets.index(bullet))
    #                 self.players[self.players.index(player)].health -= 25
    #
    # @staticmethod
    # def checkCollision(bullet, player):
    #     return player.x < bullet.x < player.x + player.w and \
    #            player.y < bullet.y < player.y + player.h and \
    #            bullet.player.idx != player.idx


