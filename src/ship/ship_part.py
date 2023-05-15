from src.galaxy.resources import index_to_resource


class ShipPart:
    def __init__(self, base_value, upgrade_value, base_cost, upgrade_cost):
        self.level = 1
        self.value = base_value
        self.upgrade_value = upgrade_value
        self.cost = base_cost
        self.upgrade_cost = upgrade_cost

    def upgrade(self, cargo_hold):
        if all([a >= b for a, b in zip(cargo_hold.resources, self.cost)]):
            self.level += 1
            self.value += self.upgrade_value
            # ['Dark Matter', 'Scrap', 'Energy Crystals', 'Rare Earth Elements', 'Plasma']
            cargo_hold.resources = [a - b for a, b in zip(cargo_hold.resources, self.cost)]
            self.cost = [self.level * cost for cost in self.upgrade_cost]
            return {
                "success": True,
                "message": "Part successfully upgraded",
                "resources": cargo_hold.resources
            }

        missing_resources_result = {}
        missing_resources = [a - b for a, b in zip(cargo_hold.resources, self.cost)]
        for i in range(5):
            if missing_resources[i] < 0:
                missing_resources_result[index_to_resource(i)] = missing_resources[i]

        return {
            "success": False,
            "message": "Not enough resources",
            "missing_resources": missing_resources_result
        }

    def get_next_upgrade_cost(self):
        return [self.level * cost for cost in self.upgrade_cost]

    def get_info(self):
        return {
            "level": self.level,
            "value": self.value,
            "cost": self.cost,
            "upgrade_cost": self.get_next_upgrade_cost()
        }


class FuelTank(ShipPart):
    def __init__(self):
        super().__init__(200, 20, [0, 500, 0, 0, 0], [0, 100, 0, 50, 0])


class PlasmaInjector(ShipPart):
    def __init__(self):
        super().__init__(5, -0.1, [0, 300, 50, 0, 0], [0, 100, 50, 0, 50])


class Scanner(ShipPart):
    def __init__(self):
        super().__init__(4, 1, [0, 400, 50, 0, 0], [0, 100, 50, 10, 0])


class WarpDrive(ShipPart):
    def __init__(self):
        super().__init__(6, 1, [0, 500, 100, 0, 0], [0, 150, 75, 40, 10])


class CargoHold(ShipPart):
    def __init__(self):
        super().__init__(1000, 200, [0, 700, 0, 0, 0], [0, 150, 0, 20, 0])
