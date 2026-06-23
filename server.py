from flask import Flask, Blueprint, jsonify

app = Flask(__name__)
player_1 = [100, 100]
player_2 = [100, 100]
blueprint = Blueprint(
    'players',
    __name__,
    template_folder='templates'
)


@blueprint.route('/player1')
def return_1_player():
    js = jsonify(
        {
            'x': player_1[0],
            'y': player_1[1]
        }
    )
    player_1[0] += 1
    return js


app.register_blueprint(blueprint)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
