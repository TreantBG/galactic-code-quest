from src.galaxy.galaxy import Galaxy
from src.ship.ship import Ship

if __name__ == '__main__':
    # Define the size of the universe
    def get_next_position(position, direction, steps, boundaries):
        x, y = position
        max_x, max_y = boundaries

        if direction == 'up':
            return (x, min(y + steps, max_y))
        elif direction == 'right':
            return (min(x + steps, max_x), y)
        elif direction == 'down':
            return (x, max(y - steps, 0))
        elif direction == 'left':
            return (max(x - steps, 0), y)


    def get_next_spiral_checkpoint():
        global current_position
        global direction
        global steps
        global turn_counter

        next_position = get_next_position(current_position, direction, steps, (1000, 1000))

        turn_counter += 1
        if turn_counter == 2:
            turn_counter = 0
            steps += 1

        directions = ['up', 'right', 'down', 'left']
        direction = directions[(directions.index(direction) + 1) % 4]

        current_position = next_position

        return next_position


    # Initialize global variables
    current_position = (500, 500)  # Starting position
    direction = 'up'  # Initial direction
    steps = 5  # Number of steps in current direction
    turn_counter = 0  # Count turns to know when to increase steps

    # Test the function
    for i in range(10):
        print(get_next_spiral_checkpoint())
    # player = Ship()
    #
    # galaxy = Galaxy(100, 100)
    # galaxy.generate()

    # scanned_systems = galaxy.get_cells_in_range(player.position[0], player.position[1], player.scanner.value)
    # # print(scanned_systems)
    #
    # print(player.scan(scanned_systems))