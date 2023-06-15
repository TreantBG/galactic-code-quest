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
            self.cost = [sum(x) for x in zip([cost for cost in self.cost], [cost for cost in self.upgrade_cost])]
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
        super().__init__(200, 20, [20, 500, 50, 50, 50], [0, 300, 50, 150, 35])


class PlasmaInjector(ShipPart):
    def __init__(self):
        super().__init__(5, -0.1, [20, 300, 50, 100, 200], [0, 200, 150, 50, 175])


class Scanner(ShipPart):
    def __init__(self):
        super().__init__(4, 1, [20, 400, 50, 50, 30], [0, 200, 100, 50, 30])


class WarpDrive(ShipPart):
    def __init__(self):
        super().__init__(6, 1, [20, 500, 100, 300, 50], [0, 150, 75, 200, 100])


class CargoHold(ShipPart):
    def __init__(self):
        super().__init__(1000, 200, [20, 800, 0, 200, 0], [0, 300, 150, 150, 50])
