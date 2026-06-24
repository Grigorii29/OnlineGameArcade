from ftplib import all_errors

import requests
import arcade

with open('Screen size.txt') as f:
    SCREEN_WIDTH, SCREEN_HEIGHT = [int(line) for line in f]

TITLE = 'Online Game player1'
server_address = 'http://127.0.0.1:8080'
UPDATE_TIME = 0.05


class Client1(arcade.View):
    def __init__(self):
        super().__init__()
        self.pl1_x = 0
        self.pl1_y = 0
        self.pl2_x = 0
        self.pl2_y = 0
        arcade.schedule(self.get_coord, UPDATE_TIME)
        arcade.schedule(self.post_coord, UPDATE_TIME)

    def get_coord(self, delta_t):  # Клиент 1, поэтому принимаю координаты второго, отправляю свои
        try:
            response = requests.get(server_address + '/player2')
            self.pl1_x = response['x']
            self.pl1_y = response['y']
        except Exception:
            pass

    def post_coord(self, delta_t):
        try:
            response = requests.post(server_address + '/player1', json={
                'x': self.pl1_x,
                'y': self.pl1_y
            })
            print('Данные отправлены')
        except Exception:
            pass

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(self.pl1_x, self.pl1_y, 20, arcade.color.SKY_BLUE)
        arcade.draw_circle_filled(self.pl2_x, self.pl2_y, 15, arcade.color.GREEN)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.pl1_y += 5


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    client = Client1()
    window.show_view(client)
    arcade.run()


if __name__ == '__main__':
    main()
