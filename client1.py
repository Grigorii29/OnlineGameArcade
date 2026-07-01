import requests
import arcade

from Classes.CONSTANTES import *
from Classes.Tanks import GreenTank

with open('Screen size.txt') as f:
    SCREEN_WIDTH, SCREEN_HEIGHT = [int(line) for line in f]

class Client1(arcade.View):
    def __init__(self):
        super().__init__()
        self.pl1_x = 100
        self.pl1_y = 420
        self.pl2_x = 0
        self.pl2_y = 0
        arcade.schedule(self.get_coord, UPDATE_TIME)
        arcade.schedule(self.post_coord, UPDATE_TIME)
        self.player_1 = GreenTank(self.pl1_x, self.pl1_y, self)
        self.players_list = arcade.SpriteList()
        self.players_list.append(self.player_1)
        self.map_setup()


    def get_coord(self, delta_t):  # Клиент 1, поэтому принимаю координаты второго, отправляю свои
        try:
            response = requests.get(server_address + '/player2').json()
            self.pl2_x = response['x']
            self.pl2_y = response['y']
        except Exception:
            pass

    def post_coord(self, delta_t):
        try:
            response = requests.post(server_address + '/player1', json={
                'x': self.pl1_x,
                'y': self.pl1_y
            })
        except Exception:
            pass

    def on_draw(self):
        self.clear()
        self.land_list.draw()
        self.details_list.draw()
        self.players_list.draw()
        arcade.draw_circle_filled(self.pl2_x, self.pl2_y, 20, arcade.color.SKY_BLUE)

    def on_update(self, delta_t):
        self.engine.update()
        self.player_1.change_y -= 1
        self.players_list.update(delta_t)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_1.change_x = -2
        elif key == arcade.key.RIGHT:
            self.player_1.change_x = 2
        # if key == arcade.key.UP:
        #     self.player_1.change_y = 10

    def map_setup(self):
        tile_map = arcade.load_tilemap('Files/map_for_tanks.tmx', scaling=1)
        self.collision_list = tile_map.sprite_lists['collision']
        self.details_list = tile_map.sprite_lists['details']
        self.land_list = tile_map.sprite_lists['Land']
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.engine = arcade.PhysicsEngineSimple(self.player_1, self.collision_list)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    client = Client1()
    window.show_view(client)
    arcade.run()


if __name__ == '__main__':
    main()
