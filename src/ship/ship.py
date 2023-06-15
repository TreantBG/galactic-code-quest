import math
import random

from src.galaxy.planet import generate_planet
from src.galaxy.resources import index_of_resource
from src.ship.ship_part import FuelTank, PlasmaInjector, Scanner, WarpDrive, CargoHold


class Ship:
    def __init__(self, start_x=0, start_y=0):
        self.fuel_tank = FuelTank()
        self.plasma_injector = PlasmaInjector()
        self.scanner = Scanner()
        self.warp_drive = WarpDrive()
        self.cargo_hold = CargoHold()
        self.position = (start_x, start_y)  # start at the origin
        self.cargo_hold.resources = [100, 200, 200, 200, 200]  # start with each resource

        self.total_collected_alians = 0
        self.total_planets_mined = 0
        self.total_systems_scanned = set()
        self.total_distance_travelled = 0
        self.total_resources_mined = [0, 0, 0, 0, 0]

    def calculate_fuel_cost(self, destination):
        return math.dist(self.position, destination) * self.plasma_injector.value

    def travel(self, destination):
        distance = math.dist(self.position, destination)
        fuel_cost = distance * self.plasma_injector.value

        if self.position == destination:
            return {
                "success": False,
                "message": "Already at destination."
            }
        elif distance > self.warp_drive.value:
            return {
                "success": False,
                "message": "Destination is too far away."
            }
        elif self.cargo_hold.resources[0] < fuel_cost:
            return {
                "success": False,
                "message": "Not enough fuel."
            }
        else:
            self.position = destination
            self.cargo_hold.resources[0] -= distance * self.plasma_injector.value
            self.total_distance_travelled += distance
            return {
                "success": True,
                "message": "Travel successful.",
                "position": self.position,
                "fuel": self.cargo_hold.resources[0],
                "fuel_cost": fuel_cost
            }

    def get_parts_info(self):
        return {
            "Fuel Tank": self.fuel_tank.get_info(),
            "Plasma Injector": self.plasma_injector.get_info(),
            "Scanner": self.scanner.get_info(),
            "Warp Drive": self.warp_drive.get_info(),
            "Cargo Hold": self.cargo_hold.get_info()
        }

    def upgrade(self, part_name):
        if part_name == 'Fuel Tank':
            return self.fuel_tank.upgrade(self.cargo_hold)
        elif part_name == 'Plasma Injector':
            return self.plasma_injector.upgrade(self.cargo_hold)
        elif part_name == 'Scanner':
            return self.scanner.upgrade(self.cargo_hold)
        elif part_name == 'Warp Drive':
            return self.warp_drive.upgrade(self.cargo_hold)
        elif part_name == 'Cargo Hold':
            return self.cargo_hold.upgrade(self.cargo_hold)
        else:
            print("Invalid part name.")
            return {
                "success": False,
                "message": "Invalid part name."
            }

    def calculate_mining_cost(self, planet):
        base_mining_cost = 10
        mining_cost = base_mining_cost

        if planet.gravity > 1.0:
            mining_cost += 2 * (planet.gravity - 1.0)

        if planet.temperature < -100 or planet.temperature > 100:
            mining_cost *= 0.8

        atmosphere_type = planet.atmosphere
        if atmosphere_type == 'Carbon Dioxide':
            mining_cost *= 1.1
        elif atmosphere_type == 'Methane':
            mining_cost *= 0.95
        elif atmosphere_type == 'Hydrogen-Helium':
            mining_cost *= 1.2
        elif atmosphere_type == 'No Atmosphere':
            mining_cost *= 1.05
        elif atmosphere_type == 'Sulfuric Acid':
            mining_cost *= 1.3
        elif atmosphere_type == 'Ammonia':
            mining_cost *= 1.15

        return mining_cost

    def get_resource_space_left(self, resource):
        if resource == "Dark Matter":
            cargo_hold = self.fuel_tank.value
        else:
            cargo_hold = self.cargo_hold.value

        resource_value = self.cargo_hold.resources[index_of_resource(resource)]

        return cargo_hold - resource_value

    def mine(self, planet, resource1=None, resource2=None):
        if not planet.can_be_mined():
            print("Planet or System is already mined out.")
            return {
                "success": False,
                "message": "Planet is already mined out."
            }

        if planet.position != self.position:
            print("Planet is not in range.")
            return {
                "success": False,
                "message": "Planet is not in range."
            }

        # Mining cost calculations
        mining_cost = self.calculate_mining_cost(planet)

        # Mining operation
        if resource1 not in planet.resources or planet.resources[resource1] == 0:
            resource1 = planet.get_random_resource()

        if resource2 not in planet.resources or planet.resources[resource2] == 0:
            resource2 = planet.get_random_resource(resource1)

        if not resource1 and not resource2:
            print("No resources found on planet.")
            return {
                "success": True,
                "message": "No resources found on planet."
            }

        yield1 = random.randint(1, planet.resources[resource1])
        cargo_space_1 = self.cargo_hold.resources[index_of_resource(resource1)]

        if resource2:
            yield2 = random.randint(1, planet.resources[resource2])
            cargo_space_2 = self.cargo_hold.resources[index_of_resource(resource2)]

        if self.cargo_hold.resources[0] > mining_cost:
            planet.mine()
            self.cargo_hold.resources[0] -= mining_cost
            result = {
                "success": True,
                "message": "Mining successful.",
                "cost": mining_cost,
            }

            resource1_cargo_hold_space = self.get_resource_space_left(resource1)
            if cargo_space_1 + yield1 > resource1_cargo_hold_space:
                yield1 = min(planet.resources[resource1], resource1_cargo_hold_space)

            if yield1 > 0:
                planet.resources[resource1] -= yield1
                self.cargo_hold.resources[index_of_resource(resource1)] += yield1
                self.total_resources_mined[index_of_resource(resource1)] += yield1

                result["resource1"] = {
                    "name": resource1,
                    "yield": yield1,
                    "cargo_space": cargo_space_1 + yield1
                }

            if resource2:
                resource2_cargo_hold_space = self.get_resource_space_left(resource2)
                if cargo_space_2 + yield2 > resource2_cargo_hold_space:
                    yield2 = min(planet.resources[resource2], resource2_cargo_hold_space)

                if yield2 > 0:
                    planet.resources[resource2] -= yield2
                    self.cargo_hold.resources[index_of_resource(resource2)] += yield2
                    self.total_resources_mined[index_of_resource(resource2)] += yield2

                    result["resource2"] = {
                        "name": resource2,
                        "yield": yield2,
                        "cargo_space": cargo_space_2 + yield2
                    }

            if planet.aliens > 0:
                self.total_collected_alians += planet.aliens
                result["aliens"] = "Aliens ware collected " + planet.aliens
                print(result["aliens"])

            self.total_planets_mined += 1
            print("Mining operation successful.")
            result["fuel"] = self.cargo_hold.resources[0]
            return result
        else:
            print("Not enough fuel to mine.")
            return {
                "success": False,
                "message": "Not enough fuel to mine."
            }

    def get_cargo_hold_resources(self):
        return {
            'Dark Matter': self.cargo_hold.resources[0],
            'Scrap': self.cargo_hold.resources[1],
            'Energy Crystals': self.cargo_hold.resources[2],
            'Rare Earth Elements': self.cargo_hold.resources[3],
            'Plasma': self.cargo_hold.resources[4]
        }

    def scan(self, scanned_systems):
        max_range = self.scanner.value

        result = []
        for system in scanned_systems:
            self.total_systems_scanned.add(system.position)

            distance = math.dist(self.position, system.position)
            if distance > max_range:
                continue

            if distance >= max_range * 0.75:
                # Only basic information
                system_info = {
                    'star_type': system.star_type,
                    'num_celestial_bodies': len(system.planets),
                }
            elif distance >= max_range * 0.5:
                # Additional details available
                system_info = {
                    'star_type': system.star_type,
                    'num_celestial_bodies': len(system.planets),
                    'celestial_bodies': [
                        {
                            "planet_type": planet.planet_type,
                        }
                        for planet in system.planets]
                }
            else:
                # Full details available
                system_info = {
                    'can_be_mined': system.can_be_mined(),
                    'star_type': system.star_type,
                    'num_celestial_bodies': len(system.planets),
                    'celestial_bodies': [
                        {
                            **planet.get_info(),
                            'mining_cost': self.calculate_mining_cost(planet),
                        }
                        for planet in system.planets
                    ]
                }

            if system_info:
                system_info['position'] = system.position
                system_info['fuel_cost'] = self.calculate_fuel_cost(system.position)
                result.append(system_info)

        return result

    def get_ship_info(self):
        return {
            'position': self.position,
            'resources': self.get_cargo_hold_resources(),
            'parts': self.get_parts_info(),
        }


if __name__ == '__main__':
    # Example usage:
    player = Ship(3, 3)
    planet = generate_planet("Terrestrial")

    planet.set_position((3, 3))
    planet.resources = {
        "Scrap": 2000,
    }
    # print(planet.to_dict())
    # print("mining cost is", player.calculate_mining_cost(planet))

    # print(player.mine(planet))
    # Upgrade the Warp Drive:
    # print(player.total_resources_mined)
    player.cargo_hold.resources = [1000, 970, 1200, 1200, 200]
    # print(player.mine(planet))
    #
    # print(player.travel((-1, 0)))
    print(player.mine(planet))
    # print(planet.resources)
    print("-----------------------------")
    print(player.get_parts_info()['Cargo Hold'])
    print("-----------------------------")
    print(player.upgrade('Cargo Hold'))
    print("-----------------------------")
    print(player.get_parts_info()['Cargo Hold'])
    print("-----------------------------")
    # print(player.upgrade('Warp Drive'))
    # print(player.upgrade('Warp Drive'))
    # print(player.travel((3, 3)))
    # print(player.travel((3, 3)))
    #
    # print(player.get_ship_info())
    # print(player.travel((3, 3)))
    # print(player.get_cargo_hold_resources())
    # print(player.get_parts_info()['Warp Drive'])
