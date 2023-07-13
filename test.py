current_position = (500, 500)  # Starting position
direction = 'up'  # Initial direction
steps = 5  # Number of steps in current direction
turn_counter = 0  # Count turns to know when to increase steps
steps_increase = 3  # Increase steps every 2 turns


def set_steps_increase(value):
    global steps_increase
    steps_increase = value


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
    global steps_increase

    next_position = get_next_position(current_position, direction, steps, (1000, 1000))

    turn_counter += 1
    if turn_counter == 2:
        turn_counter = 0
        steps += steps_increase

    directions = ['up', 'right', 'down', 'left']
    direction = directions[(directions.index(direction) + 1) % 4]

    current_position = next_position

    return [current_position[0], current_position[1]]


if __name__ == '__main__':
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
