TITLE = 'Online Game player1'
server_address = 'http://127.0.0.1:8080'
UPDATE_TIME = 0.07
TANK_SKALE = 0.8
SPEED_DELTA = 0.1
CAMERA_LERP = 0.15
GRAVITY = 0.5
with open('Screen size.txt') as f:
    SCREEN_WIDTH, SCREEN_HEIGHT = [int(line) for line in f]
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)