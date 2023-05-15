import json
import math
import random

from src.galaxy.star_system import generate_star_system


class Galaxy:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(height)] for _ in range(width)]

    def generate(self):
        star_systems = 0
        planets = 0
        alians = 0

        for i in range(self.width):
            for j in range(self.height):
                if random.random() < 0.15:  # 20% chance for a star system to exist in a grid cell
                    star_system = generate_star_system()
                    star_system.set_position((i, j))
                    self.grid[i][j] = star_system

                    star_systems += 1
                    planets += len(star_system.planets)

                    if random.random() < 0.05:
                        star_system.populate_with_alians()
                        alians += 1

        print(f'Generated {star_systems} star systems with {planets} planets and {alians} alians')

    def get_cells_in_range(self, x, y, range_):
        cells = []
        for i in range(x - range_, x + range_ + 1):
            for j in range(y - range_, y + range_ + 1):
                star_system = self.grid[i][j]
                if star_system:
                    distance = math.dist((x, y), star_system.position)
                    if distance <= range_:
                        cells.append(star_system)
        return cells

    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'grid': [[cell.to_dict() if cell is not None else None for cell in row] for row in self.grid]
        }

    def toJSON(self):
        return json.dumps(self.to_dict(), indent=4)


if __name__ == '__main__':
    galaxy = Galaxy(10, 10)
    galaxy.generate()
    # print(galaxy.toJSON())

    for cell in galaxy.get_cells_in_range(0, 0, 5):
        if cell:
            print(cell.position, cell.star_type)
