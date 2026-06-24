from flask import Flask, Blueprint, jsonify, request

app = Flask(__name__)
player_1 = [0, 0]
player_2 = [0, 0]
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
    print(player_1)
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


app.register_blueprint(blueprint)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
