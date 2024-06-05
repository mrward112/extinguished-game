#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Do not mess with the above comments. They are important.
# If you know what PEP-8 is, follow it. Otherwise, ignore this comment.
# Try to use type hints as much as possible, as it allows others to read your code easier.
# If you have questions about a pygame function, check out the docs: https://pyga.me/docs/

# Standard library imports.
import sys  # This module provides information about the system and enables us to terminate the program.
from pathlib import Path  # This module allows object-oriented filesystem interaction.
import random  # Random number generation.
import functools  # Don't worry about this import. It's advanced.

# Third-party library imports.
# I am abbreviating `pygame` here to `pg` because it will be used a lot.
# Generally, using full names is preferred, but I know what I am doing.
import pygame as pg

# Local library imports.
from colors import *
import utils
import sprites


# Constants.
FPS = 0  # Set to 0 for unbounded frame-rate. Setting this to 60 will limit the game to 60 fps.
SCREEN_SIZE = pg.Vector2(800, 600)  # This is a Vector2 to enable easy mathematical operations later.
APPLICATION_DIRECTORY = Path(__file__, "../..").resolve()  # This is the top level folder of the project.
IMAGE_DIRECTORY = APPLICATION_DIRECTORY / "images"  # The path to the folder of images.
ASTEROID_IMAGE_FILENAMES = (  # The file names of the asteroid images.
    "Asteroid_60.png",
    "Asteroid_100.png",
    "Asteroid_140.png",
    "Asteroid_160.png",
)
BACKGROUND_IMAGE_FILENAME = "Level Design/Background.png"

FUEL_LEVEL_TEXT_POS = pg.Vector2(32, 50)
FUEL_LEVEL_IMAGE_POS = pg.Vector2(10, 25)
FUEL_LEVEL_BAR_POS = FUEL_LEVEL_IMAGE_POS + (20, 15)


# Draw extinguisher tank function.
def draw_tank_bar(tank_level, screen):
    """ Draw the tank level bar on the screen. """
    bar_width = 200
    bar_height = 30
    bar_x = 10
    bar_y = 30

    # Draw the background of the bar (empty part)
    pg.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))

    # Calculate the width of the filled part based on the tank level
    fill_width = (tank_level / 100) * bar_width

    # Draw the filled part of the bar
    pg.draw.rect(screen, GREEN, (bar_x, bar_y, fill_width, bar_height))


# Helpful application functions.
def terminate() -> None:
    """Terminate the application safely.

    This is where you would save the game or generally ensure clean termination.
    """
    # Quit pygame to close the window and free system resources.
    pg.quit()
    # Terminate python execution.
    sys.exit()


def main() -> None:
    """This is the main application code."""
    # Pygame must be initialized before anything can be done with it.
    pg.init()

    # Set the title of the window.
    # Should be called before creating the screen for best system compatibility.
    pg.display.set_caption("Extinguished")
    # Load in the icon for the window.
    # Find the file by searching from the application directory Path object.
    # Don't convert it or the application will crash (because display is not initialized).
    # I chose a large icon because macOS uses large system icons on the dock (taskbar).
    icon_image = utils.load_image(IMAGE_DIRECTORY / "icon.png", False)
    # Set the icon of the window.
    # Should be called before creating the screen for best system compatibility.
    pg.display.set_icon(icon_image)

    # Create the main window.
    # Don't worry about the other arguments to this function.
    screen = pg.display.set_mode(SCREEN_SIZE)
    # Create the Clock object, which will keep track of frame-rate and delta-time.
    clock = pg.time.Clock()
    # Debug variable.
    debug = True
    # Create a font using pygame-ce's default font.
    # We can add in a nicer font later, this one is for testing.
    font = pg.Font(None, 24)
    # Create the game bounds (width and height).
    game_size = pg.Vector2(1600, 1200)
    # Get the background image.
    background_image = utils.load_image(IMAGE_DIRECTORY / BACKGROUND_IMAGE_FILENAME)

    # Create the player object.
    # Center it in the middle of the screen.
    player = sprites.Player(SCREEN_SIZE // 2, utils.load_image(IMAGE_DIRECTORY / "astro.png", alpha=True))

    # Load in the asteroid images.
    asteroid_images = {name: utils.load_image(IMAGE_DIRECTORY / name, alpha=True) for name in ASTEROID_IMAGE_FILENAMES}

    # Create and place the obstacles for level 1.
    obstacles = [sprites.Obstacle((300,250), utils.load_image(IMAGE_DIRECTORY / "Asteroid_60.png", alpha=True)),
                 sprites.Obstacle((600,450), utils.load_image(IMAGE_DIRECTORY / "Asteroid_140.png", alpha=True)),
                 sprites.Obstacle((250,900), utils.load_image(IMAGE_DIRECTORY / "Asteroid_60.png", alpha=True)),
                 sprites.Obstacle((750,550), utils.load_image(IMAGE_DIRECTORY / "Asteroid_100.png", alpha=True)),
                 sprites.Obstacle((850,1050), utils.load_image(IMAGE_DIRECTORY / "Asteroid_100.png", alpha=True)),
                 sprites.Obstacle((1400,900), utils.load_image(IMAGE_DIRECTORY / "Asteroid_160.png", alpha=True)),
                 sprites.Obstacle((1500,650), utils.load_image(IMAGE_DIRECTORY / "Asteroid_60.png", alpha=True)),
                 sprites.Obstacle((1500,1050), utils.load_image(IMAGE_DIRECTORY / "Asteroid_100.png", alpha=True)),]

    # I'm creating a ParticleGroup here.
    # Don't worry if you don't understand, I'll handle all the particle code.
    make_smoke_circle_image = functools.partial(utils.make_circle_image, color=SMOKE)
    smoke_particles = utils.ParticleGroup(utils.ImageCache(make_smoke_circle_image), pg.BLEND_ADD)

    # Starting tank level.
    tank_level = sprites.TANK_MAX

    # The tank image.
    tank_image = utils.load_image(IMAGE_DIRECTORY / "tank_bar2.png", alpha=True)
    tank_fill_image = utils.load_image(IMAGE_DIRECTORY / "tank_fill.png", alpha=True)
    tank_fill_bg_image = pg.mask.from_surface(tank_fill_image).to_surface(setcolor=TANK_BG_COLOR,
                                                                          unsetcolor=(0, 0, 0, 0)).convert_alpha()

    # Enter the game loop.
    while True:
        # Get the delta-time and fps.
        # I am abbreviating delta-time here to `dt` because it will be used often.
        # `dt` is the number of seconds that passed since last frame.
        # `clock.tick(FPS)` returns the elapsed milliseconds, so we divide by 1000.0 to get the seconds.
        # This makes the velocities of our objects easier to reason with.
        dt = clock.tick(FPS) / 1000.0
        fps = clock.get_fps()  # This is the average frames-per-second over the last ten frames.
        # Handle events.
        # Pygame provides a queue of events that occurred last frame that we can iterate over.
        for event in pg.event.get():

            # `QUIT` is sent when the user hits the X button to close the window.
            if event.type == pg.QUIT:
                terminate()

            if event.type == pg.KEYDOWN:
                # Toggle debug mode.
                if event.key == pg.K_F3:
                    debug = not debug

                if event.key == pg.K_ESCAPE:
                    # The ESCAPE key should bring up a pause menu or something, but we don't have one.
                    # For the time being, we'll just terminate the application.
                    terminate()
                    # Show the pause menu.
                    pass

                if event.key in (pg.K_UP, pg.K_w):
                    # The user wants to use the extinguisher.
                    player.pushing = True

            if event.type == pg.KEYUP:
                if event.key in (pg.K_UP, pg.K_w):
                    # The user wants to stop using the extinguisher.
                    player.pushing = False

            # When the mouse moves, change the player angle.
            # This causes the angle to snap to the mouse, making it a better option than keyboard.
            # I can change this later to move the angle towards the mouse angle at the same speed as the keyboard.
            # This is based on the screen center, not the player position within the screen.
            if event.type == pg.MOUSEMOTION:
                player.angle = pg.Vector2(0, 0).angle_to(pg.Vector2(pg.mouse.get_pos()) - SCREEN_SIZE // 2)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Button 1 is the left mouse button.
                    # The user wants to use the extinguisher.
                    player.pushing = True

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Button 1 is the left mouse button.
                    # The user wants to stop using the extinguisher.
                    player.pushing = False

        # This is another way of handling events.
        # Choosing this method over the other depends on your use case.
        # It is perfect for detecting whether a key is currently being held down,
        # but it can miss multiple small presses between frames.
        # We plan on the frame-rate being as high as possible, so this code saves us some state variables
        # that we would otherwise have to use with the event queue.
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # The user wants to rotate the player angle counterclockwise.
            player.angle -= sprites.PLAYER_ROTATE_SPEED * dt
            # Keep the player angle in the range of [0, 359].
            player.angle %= 360
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            # The user wants to rotate the player angle clockwise.
            player.angle += sprites.PLAYER_ROTATE_SPEED * dt
            # Keep the player angle in the range of [0, 359].
            player.angle %= 360

        # If the mouse is being held down, the angle should follow the mouse.
        # This causes the angle to snap to the mouse, making it a better option than keyboard.
        # I can change this later to move the angle towards the mouse angle at the same speed as the keyboard.
        # This is based on the screen center, not the player position within the screen.
        if pg.mouse.get_pressed()[0]:
            player.angle = pg.Vector2(0, 0).angle_to(pg.Vector2(pg.mouse.get_pos()) - SCREEN_SIZE // 2)

        # Update everything.

        # Update the tank.
        if player.pushing:
            tank_level -= sprites.TANK_DECREASE * dt
            if tank_level <= 0:
                tank_level = 0
                player.pushing = False

        # Add smoke particles if extinguisher is active.
        if player.pushing:
            vel_vector = pg.Vector2()
            vel_vector.from_polar((random.randint(150, 200), (player.angle + random.randint(-20, 20) % 360)))
            smoke_particles.add(utils.SmokeParticle(player.pos, vel_vector + player.vel, random.randint(3, 5)))

        # Update the player.
        player.update(dt, game_size, obstacles)

        # Update the obstacles.
        for obstacle in obstacles:
            obstacle.update(dt)

        # Update the particles.
        smoke_particles.update(dt)

        # Update the camera.
        camera = pg.Vector2(SCREEN_SIZE) // 2 - player.pos

        # Draw everything to the screen.
        screen.blit(background_image, (0, 0))  # Clear the screen completely by pasting the background image.

        # Draw the obstacles.
        # There are faster and more efficient ways to create and draw the obstacle images,
        # but I'm going the simple route for clarity.
        for obstacle in obstacles:
            obstacle.draw(screen, camera)
            # Draw the collision circles.
            if debug:
                pg.draw.circle(screen, CYAN, obstacle.pos + camera, obstacle.radius, 1)

        # Draw the player.
        player.draw(screen, camera)
        # Draw the hit box and player angle.
        if debug:
            pg.draw.circle(screen, CYAN, player.pos + camera, player.radius, 1)
            player_angle_offset = pg.Vector2()
            player_angle_offset.from_polar((30, player.angle))
            pg.draw.line(screen, RED, player.pos + camera, player.pos + player_angle_offset + camera, 3)

        # Draw the particles.
        smoke_particles.draw(screen, camera)

        # The game boundaries.
        pg.draw.rect(screen, GAME_BORDER, (*camera, *game_size), 10)

        # Draw the tank bar.
        # draw_tank_bar(tank_level, screen)
        # Render the image tank bar.
        screen.blit(tank_fill_bg_image, FUEL_LEVEL_IMAGE_POS)
        bar_width = tank_image.get_width() * (tank_level / sprites.TANK_MAX)
        screen.blit(tank_fill_image.subsurface(0, 0, bar_width, tank_fill_image.get_height()), FUEL_LEVEL_IMAGE_POS)
        screen.blit(tank_image, FUEL_LEVEL_IMAGE_POS)
        # Display tank level as text.
        if tank_level == sprites.TANK_MAX:
            tank_text = "Tank: FULL"
        elif tank_level <= 0:
            tank_text = "Tank: EMPTY"
        else:
            tank_text = f"Tank: {int(tank_level)}/{sprites.TANK_MAX}"
        tank_text_surf = font.render(tank_text, True, RED)
        screen.blit(tank_text_surf, FUEL_LEVEL_TEXT_POS)

        # Show the fps.
        if debug:
            # Read the documentation to see how to render text.
            # The `font.render` method returns a `pygame.Surface` object, which is like an image.
            fps_surf = font.render(f"FPS: {fps:.2f}", True, WHITE, BLACK)
            # The `blit` method takes a Surface and a position and pastes the Surface at that position.
            # There are other arguments, but you can ignore those for now.
            # Here we have an example of why SCREEN_SIZE is a Vector2. Easy mathematical operations.
            # This will paste `fps_surf` in the bottom-left corner of the screen.
            # Remember that the origin is the upper-left and SCREEN_SIZE.y is the height of the screen.
            # If we blit just to (0, SCREEN_SIZE.y) the image would be off the bottom of the screen because the
            # image is pasted from its upper-left corner. We shift the image up (by subtracting from the y) by its
            # height, so it is visible.
            screen.blit(fps_surf, (0, SCREEN_SIZE.y - fps_surf.get_height()))

        # Show the screen.
        # Nothing we just drew is visible yet, so we flip the surface buffers to update the screen.
        pg.display.flip()

        # That was one frame. Now we go back up to the top and handle events for the next frame!


# This name-main idiom ensures that only the code contained in the
# `main` function will run when this module is imported.
if __name__ == "__main__":
    main()
