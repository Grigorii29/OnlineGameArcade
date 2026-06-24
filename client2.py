import requests
import arcade

with open('Screen size.txt') as f:
    SCREEN_WIDTH, SCREEN_HEIGHT = [int(line) for line in f]
TITLE = 'Онлайн игра'
server_address = 'http://127.0.0.1:8080'
UPDATE_TIME = 0.05


class Client2(arcade.View):
    def __init__(self):
        super().__init__()
        # arcade.draw_circle_filled(100, 100, 50, arcade.color.SKY_BLUE)
        self.pl1_x = 0
        self.pl1_y = 0
        self.pl2_x = 0
        self.pl2_y = 0
        arcade.schedule(self.get_coord, UPDATE_TIME)  # автопроверка координат первого игрока
        arcade.schedule(self.post_coord, UPDATE_TIME)  # автоотправка координат

    def get_coord(self, delta_t):
        try:
            response = requests.get(server_address + '/player1').json()
            self.pl1_x = response['x']
            self.pl1_y = response['y']
            # print(self.pl1_x, self.pl1_y)
            print(self.pl1_y)
        except Exception:
            pass

    def post_coord(self, delta_t):
        try:
            response = requests.post(server_address + '/player2', json={
                'x': self.pl2_x,
                'y': self.pl2_y
            })
        except Exception:
            pass

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(self.pl1_x, self.pl1_y, 20, arcade.color.SKY_BLUE)
        arcade.draw_circle_filled(self.pl2_x, self.pl2_y, 15, arcade.color.GREEN)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    client = Client2()
    window.show_view(client)
    arcade.run()


if __name__ == '__main__':
    main()
