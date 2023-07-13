import math
import operator
import random

import requests as requests

base_url = "http://localhost:5001"


def info():
    response = requests.get(base_url + "/info")
    return response.json()


def scan():
    response = requests.get(base_url + "/scan")
    return response.json()

def travel(position):
    response = requests.post(base_url + "/travel", json={"x": position[0], "y": position[1]})
    return response.json()


def mine(planet_id, resource1=None, resource2=None):
    response = requests.post(base_url + "/mine",
                             json={"planet_id": planet_id, "resource1": resource1, "resource2": resource2})
    # print(response)
    return response.json()

def statistics():
    response = requests.get(base_url + "/statistics")
    return response.json()

def upgrade(part_name):
    response = requests.post(base_url + "/upgrade", json={"part_name": part_name})
    return response.json()


def resources_to_list(resources):
    order = ['Dark Matter', 'Scrap', 'Energy Crystals', 'Rare Earth Elements', 'Plasma']
    resources_list = [resources.get(resource, 0) for resource in order]
    return resources_list


def get_available_upgrades(info_response):
    if not info_response:
        return {}

    available_upgrades = {}
    current_resources = resources_to_list(info_response['resources'])

    for part, details in info_response['parts'].items():
        # checking if the resources are sufficient for the upgrade
        if all(current >= upgrade for current, upgrade in zip(current_resources, details['cost'])):
            available_upgrades[part] = details

    return list(available_upgrades.keys())


def get_nearest_mineable_system(scanned_systems, fuel):
    if not scanned_systems:
        return None

    # Filter out systems that can't be mined or have no celestial bodies
    mineable_systems = [
        system for system in scanned_systems
        if system.get('can_be_mined', True) and 'celestial_bodies' in system and fuel >= system['fuel_cost']
    ]

    if not mineable_systems:
        return None

    # Get the number of celestial bodies for each system
    for system in mineable_systems:
        system['num_celestial_bodies'] = len(system.get('celestial_bodies'))

    # Sort by fuel cost and then by number of celestial bodies in descending order
    mineable_systems.sort(key=operator.itemgetter('fuel_cost', 'num_celestial_bodies'))

    # Return the nearest system with the most celestial bodies
    return mineable_systems[0]


def get_best_planet(system, priority_resources, ignore_planets_ids=None):
    if not system or not priority_resources:
        return None

    celestial_bodies = [body for body in system.get('celestial_bodies', []) if
                        ignore_planets_ids is None or body['id'] not in ignore_planets_ids]
    celestial_bodies = [body for body in celestial_bodies if body.get('can_be_mined', False)]

    # Get the resources on each celestial body.
    for body in celestial_bodies:
        body_resources = body.get('resources', {})
        body['priority_resources'] = [resource for resource in body_resources if body_resources[resource] > 0]

    # Score the celestial bodies based on the priority of their resources.
    for body in celestial_bodies:
        body['score'] = sum(
            5 - priority_resources.index(resource) if resource in priority_resources else 1 for resource in
            body['priority_resources'])
    # Sort celestial bodies by their score, in descending order.
    celestial_bodies.sort(key=operator.itemgetter('score'), reverse=True)

    if len(celestial_bodies) == 0:
        return

    return {
        'id': celestial_bodies[0]['id'],
        'resources': celestial_bodies[0]['priority_resources'][:2]
    }


def get_best_planets_for_mining(system, priority_resources):
    if not system or not priority_resources:
        return None

    
    first_planet = get_best_planet(system, priority_resources)
    print(first_planet)
    if not first_planet:
        return None
    

    priority_resources = [resource for resource in priority_resources if resource not in first_planet['resources']]
    second_planet = get_best_planet(system, priority_resources, ignore_planets_ids=[first_planet['id']])

    return [first_planet, second_planet]


def mine_best_planets(best_planets):
    if not best_planets:
        return None

    mine_results = []
    for planet in best_planets:
        resource_1 = None
        resource_2 = None
        if planet:
            if 'resources' in planet:
                resource_1 = planet['resources'][0] if len(planet['resources']) > 0 else None
                resource_2 = planet['resources'][1] if len(planet['resources']) > 1 else None

            print("Mining planet: " + str(planet['id']) + " with resources: " + str(resource_1) + " and " + str(resource_2))
            mine_results.append(mine(planet['id'], resource_1, resource_2))

    return mine_results


def scan_current_system(scan_result, position):
    if not scan_result:
        return None

    current_system = None
    for system in scan_result:
        if system['position'] == position:
            current_system = system

    return current_system


def travel_and_scan_current_system(destination):
    travel_result = travel(destination)
    if travel_result['success']:
        for system in scan():
            if system['position'] == destination:
                return system


def find_lacking_resources(ship_info):
    resources = ship_info['resources']
    parts = ship_info['parts']
    cargo_hold_value = parts['Cargo Hold']['value']
    fuel_tank_value = parts['Fuel Tank']['value']

    # Convert the resources dict to a list of tuples, with the amount as a percentage of max capacity
    resources_list = []
    for resource, amount in resources.items():
        max_capacity = fuel_tank_value if resource == 'Dark Matter' else cargo_hold_value
        percentage = (amount / max_capacity) * 100
        resources_list.append((resource, percentage))

    # Sort the list based on the percentage of each resource
    resources_list.sort(key=lambda x: x[1])

    # Now create a list of resource names, sorted by the percentage of each resource
    lacking_resources = [resource for resource, percentage in resources_list]

    return lacking_resources


scan_result = scan()
info_result = info()

ship_parts = info_result["parts"]
ship_position = info_result["position"]
ship_resources = info_result["resources"]
ship_fuel = ship_resources["Dark Matter"]
ship_max_travel_distance = ship_parts["Warp Drive"]["value"]
ship_max_scan_distance = ship_parts["Scanner"]["value"]
ship_max_travel_distance = ship_parts["Warp Drive"]["value"]
ship_max_scan_distance = ship_parts["Scanner"]["value"]

def get_ship_destination_in_direction(direction, ship_info):
    ship_max_travel_distance = ship_info['parts']['Warp Drive']['value'] -1
    diagonal_distance = ship_max_travel_distance / math.sqrt(2)

    # Define the possible moves for each direction
    directions = {
        "N": (0, ship_max_travel_distance),
        "NE": (diagonal_distance, diagonal_distance),
        "E": (ship_max_travel_distance, 0),
        "SE": (diagonal_distance, -diagonal_distance),
        "S": (0, -ship_max_travel_distance),
        "SW": (-diagonal_distance, -diagonal_distance),
        "W": (-ship_max_travel_distance, 0),
        "NW": (-diagonal_distance, diagonal_distance)
    }

    # Get the current position of the ship
    current_position = ship_info['position']

    # Get the move for the specified direction
    move = directions.get(direction)

    if move is None:
        print("Invalid direction!")
        return

    # Calculate the new position
    new_position = (current_position[0] + move[0], current_position[1] + move[1])

    return new_position


def get_random_direction():
    # Define the possible directions
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    # Choose and return a random direction
    return random.choice(directions)


"""
get_available_upgrades(info_response): 
This function returns a list of upgrades that the player can currently afford given the current resources.

get_nearest_mineable_system(scanned_systems, fuel): 
This function selects the nearest mineable system from a list of scanned systems, considering the system's fuel cost and the number of celestial bodies it contains.

get_best_planets_for_mining(system, priority_resources): 
This function returns the top two planets for mining within a given system, considering the priority of different resources.

mine_best_planets(best_planets): 
This function executes the mining operation for the best-selected planets and returns the results.

scan_current_system(scan_result, position): 
This function scans the current system and returns its details.

travel_and_scan_current_system(destination): 
This function executes travel to a destination, scans the system at that location, and returns its details.

find_lacking_resources(ship_info): 
This function determines which resources the player is lacking, considering their current quantities as percentages of maximum capacity. It then returns these resources in ascending order of their percentage amounts.

get_ship_destination_in_direction(direction, ship_max_travel_distance): 
This function calculates the new position of the ship in a given direction based on the maximum travel distance.

get_random_direction(): 
This function randomly selects one direction from eight possible ones: North, North-East, East, South-East, South, South-West, West, and North-West.
"""

#############################


def game_step():
    # Step 1: Get current game information
    scan_result = scan()
    info_result = info()
    get_statistics = statistics()

    # ship_parts = info_result["parts"]
    ship_position = info_result["position"]
    ship_resources = info_result["resources"]
    ship_fuel = ship_resources["Dark Matter"]

    ######### Travel

    
    available_upgrades = get_available_upgrades(info_result)
    if available_upgrades and len(available_upgrades) > 0:
        upgrade("Fuel Tank")
        upgrade("Plasma Injector")
        upgrade(available_upgrades[0])
    lacking_resources = find_lacking_resources(info_result)    
    system_for_mining = get_nearest_mineable_system(scan_result, ship_fuel)
    if system_for_mining and system_for_mining['position'] != ship_position:
        system_for_mining = travel_and_scan_current_system(system_for_mining['position'])
        best_planets = get_best_planets_for_mining(system_for_mining, lacking_resources)
        mine_best_planets(best_planets)
    else:
        random_direction = get_random_direction()  # Possible directions: N, NE, E, SE, S, SW, W, NW
        # print("random_direction", random_direction)
        travel_dest = get_ship_destination_in_direction(random_direction, info_result) # (510, 500)
        response = travel(travel_dest)
        if 'message' in response and response['message'] == 'Not enough fuel.': # Stop the game where there is not enough fuel
            print("Game over: Not enough fuel.")
            print("Statistics:", get_statistics)
            return False
    return True         

def game_loop():
    while True:
        if not game_step():
            break

if __name__ == '__main__':
    game_loop()

##############################
