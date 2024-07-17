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
    teleporter_image = utils.load_image(IMAGE_DIRECTORY / "Teleporter.png", alpha=True)
    
    # create teleporters
    teleporters = {
        'A': sprites.Teleporter((900, 1070), teleporter_image, 'A'),
        'B': sprites.Teleporter((1400, 1000), teleporter_image, 'B'),
        # 'C': sprites.Teleporter((1100, 700), teleporter_image, 'C'),
        # 'D': sprites.Teleporter((500, 200), teleporter_image, 'D')
    }  

    # links teleporters
    teleporters['A'].link(teleporters['B'])  
    teleporters['B'].link(teleporters['A'])
    # teleporters['C'].link(teleporters['D'])
    # teleporters['D'].link(teleporters['C'])

    
    items = [
        sprites.Item((750, 1050), fuel_item_image),
        sprites.Item((1450,300),exit_image,sprites.ItemType.EXIT),
        *teleporters.values()
        # sprites.Item((900, 1070),teleporter_image, sprites.ItemType.Teleporter),
        # sprites.Item((1400, 1000),teleporter_image, sprites.ItemType.Teleporter)
    ]

    return items

