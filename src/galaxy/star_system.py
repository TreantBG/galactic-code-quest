import random

from src.galaxy.planet import generate_planet


class StarSystem:
    def __init__(self, star_type, planets):
        self.star_type = star_type
        self.planets = planets
        self.position = (0, 0)  # start at the origin

    def to_dict(self):
        return {
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

    planets = []
    for _ in range(random.randint(*planet_counts[star_type])):
        planets.append(generate_planet(random.choice(planet_types)))

    return StarSystem(star_type, planets)
