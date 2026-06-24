from ftplib import all_errors

import requests
import arcade

with open('Screen size.txt') as f:
    SCREEN_WIDTH, SCREEN_HEIGHT = [int(line) for line in f]

TITLE = 'Online Game player1'
server_address = 'http://192.168.0.106:8080'
UPDATE_TIME = 0.05
TANK_SKALE = 0.8


class GreenTank(arcade.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.texture = arcade.load_texture('Files/Green tank/Tank0.png')
        self.center_x = x
        self.center_y = y
        self.scale = TANK_SKALE

class Client1(arcade.View):
    def __init__(self):
        super().__init__()
        self.pl1_x = 0
        self.pl1_y = 0
        self.pl2_x = 0
        self.pl2_y = 0
        arcade.schedule(self.get_coord, UPDATE_TIME)
        arcade.schedule(self.post_coord, UPDATE_TIME)
        self.player_1 = GreenTank(self.pl1_x, self.pl1_y, self)
        self.all_sprites_to_draw = arcade.SpriteList()
        self.all_sprites_to_draw.append(self.player_1)
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
        self.collision_list.draw()
        self.all_sprites_to_draw.draw()
        # arcade.draw_circle_filled(self.pl1_x, self.pl1_y, 20, arcade.color.SKY_BLUE)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.pl1_y += 2
        elif key == arcade.key.DOWN:
            self.pl1_y -= 2
        elif key == arcade.key.LEFT:
            self.pl1_x -= 2
        elif key == arcade.key.RIGHT:
            self.pl1_x += 2

    def map_setup(self):
        tile_map = arcade.load_tilemap('Files/map_for_tanks.tmx', scaling=1)
        self.collision_list = tile_map.sprite_lists['collision']


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    client = Client1()
    window.show_view(client)
    arcade.run()


if __name__ == '__main__':
    main()
