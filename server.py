from urllib.request import proxy_bypass_registry

from flask import Flask, Blueprint, jsonify, request

app = Flask(__name__)
player_1 = [0, 420, 1000]
player_2 = [100, 450, 1000]
bullets_from_player_1 = []
blueprint = Blueprint(
    'players',
    __name__,
    template_folder='templates'
)


@blueprint.route('/player1')
def return_coord_player1():
    return jsonify(
        {
            'x': player_1[0],
            'y': player_1[1]
        }
    )


@blueprint.route('/player1', methods=['POST'])
def get_coord_player_1():
    global player_1
    player_1 = [request.json['x'], request.json['y']]
    return jsonify({"Status": 'OK'})


@blueprint.route('/player2')
def return_coord_player_2():
    return jsonify(
        {
            'x': player_2[0],
            'y': player_2[1]
        }
    )


@blueprint.route('/player2', methods=['POST'])
def get_coord_player_2():
    global player_2
    player_2 = [request.json['x'], request.json['y']]
    return jsonify({'Status': 'OK'})


@blueprint.route('/bullets_from_player_1', methods=['POST'])
def bullets_player_1():
    global bullets_from_player_1
    print(request.json)
    return jsonify({'Status': 'OK'})



app.register_blueprint(blueprint)


def main():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
