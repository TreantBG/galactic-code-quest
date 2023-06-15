# Galactic Code Quest

Welcome to Galactic Code Quest, an exciting adventure where you can explore the vastness of the galaxy, travel to
distant star systems, and uncover valuable resources. In this game, you will command your own spaceship and embark on
thrilling missions to mine resources, upgrade your ship, and unravel the mysteries of the universe.

# Resources

Throughout your journey, you will encounter various resources that hold immense value. These resources include:

- **Dark Matter**: A mysterious substance that serves as fuel for your spaceship.
- **Scrap**: Salvaged materials that can be used for ship upgrades and repairs.
- **Energy Crystals**: Powerful energy sources that enhance ship performance.
- **Rare Earth Elements**: Precious elements with unique properties, essential for advanced technologies.
- **Plasma**: A highly energized substance used in various scientific and engineering applications.
  
Each resource is vital for your success in the game. Collect them wisely and utilize them strategically to enhance
  your ship's capabilities and survive the challenges that lie ahead.

# Ship Components

Your spaceship consists of several key components, each serving a specific function. These components can be upgraded to
unlock greater potential and withstand the rigors of space travel. The ship components include:

- **Fuel Tank**: Stores Dark Matter, the fuel that powers your ship. Upgrading the fuel tank increases its capacity,
  allowing for longer journeys.
- **Plasma Injector**: Enhances fuel efficiency, enabling your ship to travel greater distances with less Dark Matter
  consumption.
- **Scanner**: Provides valuable information about star systems, such as the number of celestial bodies and basic
  details about their composition.
- **Warp Drive**: Determines the speed at which your ship can traverse the galaxy. Upgrading the Warp Drive increases
  your ship's speed, reducing travel time between star systems.
- **Cargo Hold**: Stores the resources you collect during your missions. Upgrading the Cargo Hold expands its capacity,
  allowing you to carry more valuable resources.
  Upgrade these ship components wisely to maximize your ship's potential and increase your chances of success in the
  vastness of space.

# Functions

In Galactic Code Quest, you have access to several functions that empower you to navigate the galaxy and accomplish your
missions:

- **Info**: Retrieve detailed information about your ship, including its current status, fuel levels, and cargo
  inventory.
- **Travel**: Initiate travel to distant star systems based on your ship's capabilities and fuel reserves.
- **Scan**: Discover and explore star systems within your scanner's range, gathering valuable information about
  celestial bodies and their compositions.
- **Mine**: Engage in resource mining operations on planets, extracting valuable resources to enhance your ship and
  accumulate wealth. Be cautious of the planet's atmosphere, temperature, and gravity, as they can impact mining
  operations.
- **Upgrade**: Enhance your ship's components by investing resources in upgrades. Strengthen your fuel efficiency,
  speed, cargo capacity, and other key attributes to unlock new possibilities.
  Embark on this epic journey through space, utilizing these functions effectively to chart your own path, uncover
  hidden treasures, and become a legendary explorer of the cosmos.

# Special Rules
**Mine**
  - Planet can be mined only once
  - In a system can be mined only 2 planets
  
**Scan**
- Scans are free
- Scans can see limited information about the system depends on the scanner level

# Travel Grid

All positive Numbers are to the right and up.

|         |         |         |
|---------|:-------:|--------:|
| X:0 y:2 | X:1 y:2 | X:2 y:2 |
| X:0 y:1 | X:1 y:1 | X:2 y:1 |
| X:0 y:0 | X:1 y:0 | X:2 y:0 |

Enjoy your adventure in Galactic Code Quest and may the stars shine favorably upon you!

### Access the application at http://localhost:5000/ in your web browser.

Use the provided endpoints to control the ship:

- **/info**: Get ship information.
- **/travel**: Initiate travel to a destination.
    - **X**: The destination X.
    - **Y**: The destination Y.
- **/scan**: Perform a scan of nearby star systems.
- **/mine**: Mine resources from a specific planet.
    - **planet_id**: The planet id to mine.
    - **resource1**: Chose resource to mine or leave black for random. (Dark Matter, Scrap, Energy Crystals, Rare Earth
      Elements, Plasma)
    - **resource2**: Chose resource to mine or leave black for random. (Dark Matter, Scrap, Energy Crystals, Rare Earth
      Elements, Plasma)
- **/upgrade**: Upgrade ship parts.
    - **part_name**: The part to upgrade. (Fuel Tank, Plasma Injector, Scanner, Warp Drive, Cargo Hold)

# Environment Variables

- **GRID_SIZE**: The size of the grid. (Default: 30)

- **STAR_SYSTEM_CHANCE**: The chance of a star system spawning. (Default: 0.15)

- **ALIENS_CHANCE**: The chance of aliens spawning. (Default: 0.1)