import random
from uuid import uuid4


class Planet:
    def __init__(self, planet_type, temperature, gravity, atmosphere, resources):
        self.planet_type = planet_type
        self.temperature = temperature
        self.gravity = gravity
        self.atmosphere = atmosphere
        self.resources = resources
        self.can_mine = True
        self.position = (0, 0)
        self.id = str(uuid4())
        self.aliens = 0
        self.star_system = None

    def set_star_system(self, star_system):
        self.star_system = star_system

    def set_position(self, position):
        self.position = position

    def can_be_mined(self):
        if self.star_system and not self.star_system.can_be_mined():
            return False

        return self.can_mine

    def mine(self):
        self.can_mine = False
        if self.star_system:
            self.star_system.mine()

    def to_dict(self):
        return self.__dict__

    def get_random_resource(self, exclude=None):
        if exclude is None:
            exclude = []

        possible_resources = list(self.resources.keys())

        if exclude in possible_resources:
            possible_resources.remove(exclude)

        if len(possible_resources) == 0:
            return None

        return random.choice(possible_resources)

    def populate_with_alians(self):
        self.aliens = random.randint(100, 1000)

    def get_info(self):
        planet_info = {
            'id': self.id,
            'planet_type': self.planet_type,
            'temperature': self.temperature,
            'gravity': self.gravity,
            'atmosphere': self.atmosphere,
            'resources': self.resources,
            'can_be_mined': self.can_be_mined()
        }

        if self.aliens > 0:
            planet_info['aliens'] = self.aliens

        return planet_info


def generate_resources(chances, ranges):
    resources = {}
    for resource, (chance, range_) in zip(['Dark Matter', 'Scrap', 'Energy Crystals', 'Rare Earth Elements', 'Plasma'],
                                          zip(chances, ranges)):
        if random.random() < chance:
            resources[resource] = random.randint(*range_)
    return resources


def generate_planet(planet_type):
    if planet_type == 'Terrestrial':
        return Planet(
            planet_type,
            random.randint(-50, 50),
            random.uniform(0.7, 1.5),
            random.choice(['Nitrogen-Oxygen', 'Carbon Dioxide', 'Methane']),
            generate_resources([0.1, 0.7, 0.2, 0.8, 0.5],
                               [(100, 500), (500, 1000), (100, 200), (500, 1500), (400, 800)])
        )
    elif planet_type == 'Gas Giant':
        return Planet(
            planet_type,
            random.randint(-150, -50),
            random.uniform(2.5, 4.0),
            random.choice(['Hydrogen-Helium', 'Methane']),
            generate_resources([0.8, 0.1, 0.4, 0.2, 0.7],
                               [(1000, 2000), (200, 400), (400, 800), (200, 400), (800, 1600)])
        )
    elif planet_type == 'Ice Giant':
        return Planet(
            planet_type,
            random.randint(-200, -100),
            random.uniform(0.8, 1.2),
            random.choice(['Methane', 'Nitrogen-Oxygen']),
            generate_resources([0.5, 0.2, 0.7, 0.5, 0.3],
                               [(500, 1000), (300, 600), (600, 1200), (400, 800), (300, 600)])
        )
    elif planet_type == 'Asteroid Field':
        return Planet(
            planet_type,
            random.randint(-200, 200),
            0,
            'No Atmosphere',
            generate_resources([0.1, 0.9, 0.4, 0.1, 0.1],
                               [(200, 400), (1000, 2000), (400, 800), (200, 400), (200, 400)])
        )
    elif planet_type == 'Moon':
        return Planet(
            planet_type,
            random.randint(-150, 100),
            random.uniform(0.1, 1.0),
            random.choice(['No Atmosphere', 'Nitrogen-Oxygen', 'Carbon Dioxide', 'Methane']),
            generate_resources([0.1, 0.5, 0.2, 0.7, 0.3],
                               [(100, 500), (500, 1000), (200, 400), (700, 1400), (300, 600)])
        )
    elif planet_type == 'Dwarf Planet':
        return Planet(
            planet_type,
            random.randint(-200, 50),
            random.uniform(0.2, 0.8),
            random.choice(['No Atmosphere', 'Nitrogen-Oxygen', 'Carbon Dioxide', 'Methane']),
            generate_resources([0.3, 0.7, 0.2, 0.6, 0.2],
                               [(300, 600), (700, 1400), (200, 400), (600, 1200), (200, 400)])
        )
