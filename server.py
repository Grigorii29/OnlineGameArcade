from flask import Flask, Blueprint, jsonify, request
import sqlite3

app = Flask(__name__)
player_1 = [0, 420, 100]
player_2 = [100, 450, 100]

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
            'y': player_1[1],
            'hp': player_1[2]
        }
    )


@blueprint.route('/player1', methods=['POST'])
def get_coord_player_1():
    global player_1
    player_1 = [request.json['x'], request.json['y'], request.json['hp']]
    return jsonify({"Status": 'OK'})


@blueprint.route('/player2')
def return_coord_player_2():
    return jsonify(
        {
            'x': player_2[0],
            'y': player_2[1],
            'hp': player_2[2]
        }
    )


@blueprint.route('/player2', methods=['POST'])
def get_coord_player_2():
    global player_2
    player_2 = [request.json['x'], request.json['y'], request.json['hp']]
    return jsonify({'Status': 'OK'})


@blueprint.route('/bullets_from_player_1', methods=['POST'])
def get_bullets_from_player_1():
    # global bullets_from_player_1
    con = sqlite3.connect('Files/Bullets.db')
    cur = con.cursor()
    for el in request.json['bullets']:
        # bullets_from_player_1.append(el)
        cur.execute(
            f"""INSERT INTO Bullets_1(center_x, center_y, angle, type, status) 
            VALUES({el[0]}, {el[1]}, {el[2]}, '{el[3]}', 0)""")
    con.commit()
    con.close()
    return jsonify({'Status': 'OK'})


@blueprint.route('/bullets_to_player_1', methods=['GET'])
def post_bullets_to_player_1():
    con = sqlite3.connect('Files/Bullets.db')
    cur = con.cursor()
    bullets_to_send = cur.execute("""SELECT * from Bullets_2 WHERE status = 0""").fetchall()
    cur.execute("""UPDATE Bullets_2 SET status=1 WHERE status=0""")
    con.commit()
    con.close()
    return jsonify({'Bullets': bullets_to_send})


@blueprint.route('/bullets_from_player_2', methods=['POST'])
def get_bullets_from_player_2():
    con = sqlite3.connect('Files/Bullets.db')
    cur = con.cursor()
    for el in request.json['bullets']:
        cur.execute(
            f"""INSERT INTO Bullets_2(center_x, center_y, angle, type, status) 
                VALUES({el[0]}, {el[1]}, {el[2]}, '{el[3]}', 0)""")
    con.commit()
    con.close()
    return jsonify({'Status': 'OK'})


@blueprint.route('/bullets_to_player_2', methods=['GET'])
def post_bullets_to_player_2():
    con = sqlite3.connect('Files/Bullets.db')
    cur = con.cursor()
    bullets_to_send = cur.execute("""SELECT * from Bullets_1 WHERE status = 0""").fetchall()
    cur.execute("""UPDATE Bullets_1 SET status=1 WHERE status=0""")
    con.commit()
    con.close()
    return jsonify({'Bullets': bullets_to_send})


app.register_blueprint(blueprint)


def main():
    con = sqlite3.connect('Files/Bullets.db')
    cur = con.cursor()
    cur.execute('DELETE from Bullets_1')
    cur.execute('DELETE from Bullets_2')
    con.commit()
    con.close()
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
