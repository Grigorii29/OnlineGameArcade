import arcade
from Classes.CONSTANTES import *


class GreenTank(arcade.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.texture = arcade.load_texture('Files/Green tank/Tank0.png')
        self.center_x = x
        self.center_y = y
        self.scale = TANK_SKALE
        self.hp = 100

    # def on_update(self, dt):
    #     self.center_x += self.change_x * dt
    #     self.upd()

    def on_update(self, dt):
        self.center_x += self.change_x * dt

    def revival(self):  # Функция оживления
        self.center_x = 100
        self.center_y = 420
        self.hp = 100
        self.texture = arcade.load_texture('Files/Green tank/Tank0.png')
        if self.game.cl == 'client1':
            self.game.count_shells = {
                'Rockets': 10,
                'Bullet': 30
            }


class GrayTank(arcade.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.texture = arcade.load_texture('Files/Gray tank/Tank0.png')
        self.center_x = x
        self.center_y = y
        self.scale_x = -TANK_SKALE
        self.scale_y = TANK_SKALE
        self.hp = 100

    def on_update(self, dt):
        self.center_x += self.change_x * dt

    def revival(self):  # Функция оживления
        self.center_x = 8200
        self.center_y = 420
        self.hp = 100
        self.texture = arcade.load_texture('Files/Gray tank/Tank0.png')
        if self.game.cl == 'client2':
            self.game.count_shells = {
                'Rockets': 10,
                'Bullet': 30
            }
