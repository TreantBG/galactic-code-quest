import requests as requests

base_url = "http://localhost:5002"


def into():
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
    return response.json()


def upgrade(part_name):
    response = requests.post(base_url + "/upgrade", json={"part_name": part_name})
    return response.json()


def resources_to_list(resources):
    order = ['Dark Matter', 'Scrap', 'Energy Crystals', 'Rare Earth Elements', 'Plasma']
    resources_list = [resources.get(resource, 0) for resource in order]
    return resources_list


def get_available_upgrades(info_response):
    available_upgrades = {}
    current_resources = resources_to_list(info_response['resources'])

    for part, details in info_response['parts'].items():
        # checking if the resources are sufficient for the upgrade
        if all(current >= upgrade for current, upgrade in zip(current_resources, details['cost'])):
            available_upgrades[part] = details

    return available_upgrades


if __name__ == '__main__':
    print(travel((495, 500)))

    # upgrade("Cargo Hold")
    #
    # scan = scan()
    # print(scan[2])
    info = into()
    #
    # print(info)
    # ship_parts = info["parts"]
    # ship_position = info["position"]
    ship_resources = info["resources"]
    print(get_available_upgrades(info))
    #
    # print(ship_parts)
    # print(get_my_fuel(info))

    # print("ship_position", ship_position)
    # for system in scan:
    #     if system["position"] == ship_position:
    #         for planet in system["celestial_bodies"]:
    #                 print(planet)
    #                 print()
    #                 print()
    # else:
    #     print(system)
    #     if system["position"] == ship_position:
    #         for planet in system["celestial_bodies"]:
    #             print(planet)
    #             print()
    #             print()
    #     #     travel_result = travel(system["position"])
    #     #     print(travel_result)
    #     #     break
    #     if system["position"] == ship_position:
    #         for planet in system["celestial_bodies"]:
    #             mine_result = mine(planet["id"])
    #             print(mine_result)

    # mine_reuslt = mine("3642e006-6cce-45a8-b90c-578836a63418", "Plasma", "Scrap")
    # print("-----------------------")
    # print(mine_reuslt)
    # print("-----------------------")
    #
    # print()
    # print("-----------------------")
    # print(ship_resources)
    # print()
    # print("-----------------------")
