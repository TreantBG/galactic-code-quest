import requests as requests


def into():
    response = requests.get("http://localhost:5000/info")
    return response.json()


def scan():
    response = requests.get("http://localhost:5000/scan")
    return response.json()


def travel(position):
    print("travel to", position)
    response = requests.post("http://localhost:5000/travel", json={"x": position[0], "y": position[1]})
    return response.json()


def mine(planet_id, resource1=None, resource2=None):
    response = requests.post("http://localhost:5000/mine",
                             json={"planet_id": planet_id, "resource1": resource1, "resource2": resource2})
    return response.json()


if __name__ == '__main__':
    scan = scan()
    info = into()

    ship_position = info["position"]

    for system in scan:
        # if "celestial_bodies" in system:
        #     travel_result = travel(system["position"])
        #     print(travel_result)
        #     break
        if system["position"] == ship_position:
            for planet in system["celestial_bodies"]:
                mine_result = mine(planet["id"])
                print(mine_result)
