import requests

import arcade

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
TITLE = 'Онлайн игра'
server_adress = 'http://127.0.0.1:8080'


class Client2(arcade.View):
    def __init__(self):
        super().__init__()
        # arcade.draw_circle_filled(100, 100, 50, arcade.color.SKY_BLUE)
        self.pl1_x = 0
        self.pl1_y = 0
        print('qweqweqwe')
        arcade.schedule(self.get_coords, 0.05)  # автопроверка координат первого игрока
        print('wqeqweqw')

    def get_coords(self, tm):
        response = requests.get(server_adress + '/player1').json()
        self.pl1_x = response['x']
        self.pl1_y = response['y']
        print(self.pl1_x, self.pl1_y)

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(self.pl1_x, self.pl1_y, 20, arcade.color.SKY_BLUE)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    client_2 = Client2()
    window.show_view(client_2)
    arcade.run()


if __name__ == '__main__':
    main()
