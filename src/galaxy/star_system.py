import random

from src.galaxy.planet import generate_planet


class StarSystem:
    def __init__(self, star_type):
        self.star_type = star_type
        self.planets = []
        self.position = (0, 0)  # start at the origin
        self.total_planet_mines = 2

    def can_be_mined(self):
        return self.total_planet_mines > 0

    def mine(self):
        self.total_planet_mines -= 1

    def add_planet(self, planet):
        self.planets.append(planet)
        planet.set_star_system(self)

    def to_dict(self):
        return {
            'can_be_mined': self.can_be_mined(),
            'star_type': self.star_type,
            'planets': [planet.to_dict() for planet in self.planets]
        }

    def set_position(self, position):
        self.position = position

        for planet in self.planets:
            planet.set_position(position)

    def populate_with_alians(self):
        random.choice(self.planets).populate_with_alians()


def generate_star_system():
    star_type = random.choice(['Red Dwarf', 'Yellow Dwarf', 'Blue Giant'])
    planet_counts = {'Red Dwarf': (2, 6), 'Yellow Dwarf': (4, 8), 'Blue Giant': (6, 10)}
    planet_types = ['Terrestrial', 'Gas Giant', 'Ice Giant', 'Asteroid Field', 'Moon', 'Dwarf Planet']

    star_system = StarSystem(star_type)

    for _ in range(random.randint(*planet_counts[star_type])):
        star_system.add_planet(generate_planet(random.choice(planet_types)))

    return star_system
