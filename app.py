from src.galaxy.galaxy import Galaxy
from src.ship.ship import Ship

from flask import Flask, jsonify, request

app = Flask(__name__)

galaxy = Galaxy(10, 10)
galaxy.generate()

player = Ship()


@app.route('/info', methods=['GET'])
def get_ship_info():
    return jsonify(player.get_ship_info())


@app.route('/travel', methods=['POST'])
def travel():
    data = request.get_json()
    destination = (int(data['x']), int(data['y']))
    return jsonify(player.travel(destination))


@app.route('/scan', methods=['GET'])
def scan():
    scanned_systems = galaxy.get_cells_in_range(player.position[0], player.position[1], player.scanner.value)
    scan_results = player.scan(scanned_systems)
    return jsonify(scan_results)


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    planet_id = data['planet_id']
    resource1 = data['resource1'] if "resource1" in data else None
    resource2 = data['resource2'] if "resource2" in data else None

    if resource1 == "":
        resource1 = None

    if resource2 == "":
        resource2 = None

    scanned_systems = galaxy.get_cells_in_range(player.position[0], player.position[1], player.scanner.value)

    mine_result = {
        'success': False,
        'message': 'Mining failed.'
    }

    for system in scanned_systems:
        for planet in system.planets:
            if planet.id == planet_id:
                mine_result = player.mine(planet, resource1, resource2)

    return jsonify(mine_result)


@app.route('/upgrade', methods=['POST'])
def upgrade():
    data = request.get_json()
    part_name = data['part_name']
    success = player.upgrade(part_name)
    return jsonify({'success': success})


if __name__ == '__main__':
    app.run(debug=True)
