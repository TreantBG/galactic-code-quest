from src.galaxy.galaxy import Galaxy
from src.ship.ship import Ship

if __name__ == '__main__':
    player = Ship()

    galaxy = Galaxy(100, 100)
    galaxy.generate()

    # scanned_systems = galaxy.get_cells_in_range(player.position[0], player.position[1], player.scanner.value)
    # # print(scanned_systems)
    #
    # print(player.scan(scanned_systems))