from pathlib import Path
import sprites
import utils

def SetLevelOneObstacles(IMAGE_DIRECTORY,ASTEROID_IMAGE_FILENAMES):
    asteroid_images = {name: utils.load_image(IMAGE_DIRECTORY / name, alpha=True)
                       for name in ASTEROID_IMAGE_FILENAMES}

    level_one_obstacles = [sprites.Obstacle((300, 250), asteroid_images["Asteroid_60.png"]),
                 sprites.Obstacle((600, 450), asteroid_images["Asteroid_140.png"]),
                 sprites.Obstacle((250, 900), asteroid_images["Asteroid_60.png"]),
                 sprites.Obstacle((750, 550), asteroid_images["Asteroid_100.png"]),
                 sprites.Obstacle((850, 1050), asteroid_images["Asteroid_100.png"]),
                 sprites.Obstacle((1400, 900), asteroid_images["Asteroid_160.png"]),
                 sprites.Obstacle((1500, 650), asteroid_images["Asteroid_60.png"]),
                 sprites.Obstacle((1500, 1050), asteroid_images["Asteroid_100.png"]),
                 ]

    return level_one_obstacles


# Create and place the items for level 1.
# Reduce image loading by only loading the image once.
def SetLevelOneItems(IMAGE_DIRECTORY):
    fuel_item_image = utils.load_image(IMAGE_DIRECTORY / "Fire_ex.png", alpha=True)
    exit_image = utils.load_image(IMAGE_DIRECTORY/ "Portal.png", alpha=True)

    level_one_items = [
        sprites.Item((750, 1050), fuel_item_image),
        sprites.Item((1450,300),exit_image,sprites.ItemType.EXIT)
    ]
    
    return level_one_items