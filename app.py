import os

from src.galaxy.galaxy import Galaxy
from src.ship.ship import Ship

from flask import Flask, jsonify, request

app = Flask(__name__)

grid_size = int(os.environ.get('GRID_SIZE', 30))
star_system_chance = float(os.environ.get('STAR_SYSTEM_CHANCE', 0.15))
aliens_chance = float(os.environ.get('ALIENS_CHANCE', 0.1))

galaxy = Galaxy(grid_size, star_system_chance, aliens_chance)
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
        'message': 'Mining failed, planet not found.'
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
    return jsonify(player.upgrade(part_name))


if __name__ == '__main__':
    app.run()
