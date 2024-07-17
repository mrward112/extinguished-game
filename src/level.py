from pathlib import Path
import sprites
import utils

# The function to create and place obsracles for level 1.
def SetLevelOneObstacles(IMAGE_DIRECTORY,ASTEROID_IMAGE_FILENAMES):
    asteroid_images = {name: utils.load_image(IMAGE_DIRECTORY / name, alpha=True)
                       for name in ASTEROID_IMAGE_FILENAMES}

    obstacles = [sprites.Obstacle((300, 250), asteroid_images["Asteroid_60.png"]),
                 sprites.Obstacle((600, 450), asteroid_images["Asteroid_140.png"]),
                 sprites.Obstacle((250, 900), asteroid_images["Asteroid_60.png"]),
                 sprites.Obstacle((750, 550), asteroid_images["Asteroid_100.png"]),
                 sprites.Obstacle((850, 1050), asteroid_images["Asteroid_100.png"]),
                 sprites.Obstacle((1400, 900), asteroid_images["Asteroid_160.png"]),
                 sprites.Obstacle((1500, 650), asteroid_images["Asteroid_60.png"]),
                 sprites.Obstacle((1500, 1050), asteroid_images["Asteroid_100.png"]),
                 ]

    return obstacles


# The function to create and place the items for level 1.
def SetLevelOneItems(IMAGE_DIRECTORY):
    fuel_item_image = utils.load_image(IMAGE_DIRECTORY / "Fire_ex.png", alpha=True)
    exit_image = utils.load_image(IMAGE_DIRECTORY/ "Portal.png", alpha=True)

    items = [
        sprites.Item((750, 1050), fuel_item_image),
        sprites.Item((1450,300),exit_image,sprites.ItemType.EXIT)
    ]
    
    return items
# The function to create and place obsracles for level 2.
def SetLevelTwoObstacles(IMAGE_DIRECTORY,ASTEROID_IMAGE_FILENAMES):
    asteroid_images = {name: utils.load_image(IMAGE_DIRECTORY / name, alpha=True)
                       for name in ASTEROID_IMAGE_FILENAMES}
    obstacles = [
                sprites.Obstacle((1200, 100), asteroid_images["Asteroid_160.png"]),
                sprites.Obstacle((1150, 250), asteroid_images["Asteroid_160.png"]),
                sprites.Obstacle((1150, 450), asteroid_images["Asteroid_160.png"]),
                sprites.Obstacle((1150, 650), asteroid_images["Asteroid_160.png"]),
                sprites.Obstacle((1150, 850), asteroid_images["Asteroid_160.png"]),
                sprites.Obstacle((1200, 1050), asteroid_images["Asteroid_160.png"]),
                sprites.Obstacle((150, 1050), asteroid_images["Asteroid_100.png"]),
                sprites.Obstacle((135, 900), asteroid_images["Asteroid_140.png"])
                
                ]

    return obstacles

# The function to create and place obsracles for level 2.
def SetLevelTwoItems(IMAGE_DIRECTORY):
    fuel_item_image = utils.load_image(IMAGE_DIRECTORY / "Fire_ex.png", alpha=True)
    exit_image = utils.load_image(IMAGE_DIRECTORY/ "Portal.png", alpha=True)

    items = [
        sprites.Item((750, 1050), fuel_item_image),
        sprites.Item((1450,300),exit_image,sprites.ItemType.EXIT)
    ]
    
    return items

