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
import math  # C-style math functions.
import functools  # Don't worry about this import. It's advanced.

# Third-party library imports.
# I am abbreviating `pygame` here to `pg` because it will be used a lot.
# Generally, using full names is preferred, but I know what I am doing.
import pygame as pg

# Local library imports.
from colors import *
import utils
import sprites
import level
import webbrowser

# Constants.
FPS = 0  # Set to 0 for unbounded frame-rate. Setting this to 60 will limit the game to 60 fps.
SCREEN_SIZE = pg.Vector2(800, 600)  # This is a Vector2 to enable easy mathematical operations later.

APPLICATION_DIRECTORY = Path(__file__, "../..").resolve()  # This is the top level folder of the project.
IMAGE_DIRECTORY = APPLICATION_DIRECTORY / "images"  # The path to the folder of images.
SOUND_DIRECTORY = APPLICATION_DIRECTORY / "sounds"  # The path to the folder of sounds and music.
FONT_PATH = APPLICATION_DIRECTORY / "kenney_font.ttf"  # The path to the font file.

ASTEROID_IMAGE_FILENAMES = (  # The file names of the asteroid images.
    "Asteroid_60.png",
    "Asteroid_100.png",
    "Asteroid_140.png",
    "Asteroid_160.png",
)
BACKGROUND_IMAGE_FILENAME = "Level Design/Background.png"

FUEL_LEVEL_TEXT_POS = pg.Vector2(32, 50)
FUEL_LEVEL_IMAGE_POS = pg.Vector2(10, 25)

# Helpful application functions.
def terminate() -> None:
    """Terminate the application safely.

    This is where you would save the game or generally ensure clean termination.
    """
    # Quit pygame to close the window and free system resources.
    pg.quit()
    # Terminate python execution.
    sys.exit()


def main(levelnum) -> None:
    """This is the main application code."""
    # Pygame must be initialized before anything can be done with it.
    pg.init()
    pg.mixer.init()

    #Set game clock and start time
    timer = 60
    game_clock = utils.Timer(1000)
    
    # Load in the sounds and music.
    hit_sound = pg.mixer.Sound(SOUND_DIRECTORY / "mixkit-boxer-getting-hit-2055.wav")
    fire_extinguisher_sound = pg.mixer.Sound(SOUND_DIRECTORY / "fire-extinguisher-sound-effect.wav")

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
    debug_font = pg.Font(None, 24)
    # Create a nice font.
    kenney_font = pg.Font(FONT_PATH, 18)
    # Create the game bounds (width and height).
    game_size = pg.Vector2(1600, 1200)
    # Get the background image.
    background_image = utils.load_image(IMAGE_DIRECTORY / BACKGROUND_IMAGE_FILENAME)

    # Create the player object.
    # Center it in the middle of the screen.
    player = sprites.Player(SCREEN_SIZE // 2, utils.load_image(IMAGE_DIRECTORY / "astro.png", alpha=True))
    player_angle_vector = pg.Vector2()  # Used for vector math to draw the player angle debug line.

    # This variable helps track the movement events to swap between mouse and keyboard.
    # Moving the mouse sets this to False, and pressing movement keys sets this to True.
    # That way the player angle follows the mouse even when it is stationary until movement keys are pressed.
    # When movement keys are pressed, the player ignores the mouse position until it moves.
    using_keyboard = False

    # Create and place the obstacles depending on the level.
    if levelnum == 1:
        obstacles = level.SetLevelOneObstacles(IMAGE_DIRECTORY,ASTEROID_IMAGE_FILENAMES)
        items = level.SetLevelOneItems(IMAGE_DIRECTORY)
    if levelnum == 2:
        obstacles = level.SetLevelTwoObstacles(IMAGE_DIRECTORY,ASTEROID_IMAGE_FILENAMES)
        items = level.SetLevelTwoItems(IMAGE_DIRECTORY)


    # I'm creating a ParticleGroup here.
    # Don't worry if you don't understand, I'll handle all the particle code.
    make_smoke_circle_image = functools.partial(utils.make_circle_image, color=SMOKE)
    smoke_particles = utils.ParticleGroup(utils.ImageCache(make_smoke_circle_image), pg.BLEND_ADD)
    portal_dust_image = utils.load_image(IMAGE_DIRECTORY / "Portal Dust.png", alpha=True)
    portal_particles = utils.ParticleGroup(utils.ImageCache(lambda _: portal_dust_image))

    portal_dust_spawn_timer = utils.Timer(100)

    # Starting tank level.
    tank_level = sprites.TANK_MAX

    # The tank image.
    tank_image = utils.load_image(IMAGE_DIRECTORY / "tank_bar2.png", alpha=True)
    tank_fill_image = utils.load_image(IMAGE_DIRECTORY / "tank_fill.png", alpha=True)
    tank_fill_bg_image = pg.mask.from_surface(tank_fill_image).to_surface(setcolor=TANK_BG_COLOR,
                                                                          unsetcolor=TRANS_BLACK).convert_alpha()

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

                if event.key in (pg.K_UP, pg.K_w):
                    # The user wants to use the extinguisher.
                    player.pushing = True
                    fire_extinguisher_sound.play()

            if event.type == pg.KEYUP:
                if event.key in (pg.K_UP, pg.K_w):
                    # The user wants to stop using the extinguisher.
                    player.pushing = False
                    fire_extinguisher_sound.stop()

            if event.type == pg.MOUSEMOTION:
                # User wants to use the mouse to move the player.
                using_keyboard = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Button 1 is the left mouse button.
                    # The user wants to use the extinguisher.
                    player.pushing = True
                    fire_extinguisher_sound.play()

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Button 1 is the left mouse button.
                    # The user wants to stop using the extinguisher.
                    player.pushing = False
                    fire_extinguisher_sound.stop()

        # This is another way of handling events.
        # Choosing this method over the other depends on your use case.
        # It is perfect for detecting whether a key is currently being held down,
        # but it can miss multiple small presses between frames.
        # We plan on the frame-rate being as high as possible, so this code saves us some state variables
        # that we would otherwise have to use with the event queue.
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # The user wants to rotate the player angle counterclockwise.
            player.rotate(-sprites.PLAYER_ROTATE_SPEED * dt, obstacles)
            # User wants to use the keyboard controls, not the mouse.
            using_keyboard = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            # The user wants to rotate the player angle clockwise.
            player.rotate(sprites.PLAYER_ROTATE_SPEED * dt, obstacles)
            # User wants to use the keyboard controls, not the mouse.
            using_keyboard = True

        # Use the mouse to move the player angle.
        if not using_keyboard:
            # Get the desired angle.
            # This is based on the screen center, not on the player position within the screen.
            desired_angle = pg.Vector2().angle_to(pg.mouse.get_pos() - (SCREEN_SIZE // 2)) % 360
            dist = desired_angle - player.angle  # One of the two modulo distances.
            abs_dist = math.fabs(dist)  # Precalculate this value for later equations.
            # If the shortest modulo distance is too small, don't rotate. This reduces jitter.
            if min(abs_dist, 360 - abs_dist) > 1:  # If the mouse angle is further than <amount> degrees.
                # Find the direction the player needs to rotate in to get to the mouse in the shortest distance.
                direction = math.copysign(1, dist) if abs_dist < 360 - abs_dist else -math.copysign(1, dist)
                player.rotate(sprites.PLAYER_ROTATE_SPEED * dt * direction, obstacles)

        # Update everything.

        #update timer
        if game_clock.tick():
            timer -= 1
            if timer < 0:
                terminate()

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

        # Update the player, playing hit sound if needed.
        if player.update(dt, game_size, obstacles):
            hit_sound.play()

        # Test for item collision.
        for item in items[:]:  # Loop over a copy of the list because we will be removing items.
            # Using squared distance is faster.
            if item.pos.distance_squared_to(player.pos) < sprites.PLAYER_PICKUP_RANGE ** 2 and not isinstance(item, sprites.Teleporter):
                items.remove(item)  # De-spawn the item.
                # Activate item effects.
                if item.type is sprites.ItemType.FUEL:
                    tank_level = sprites.TANK_MAX

                if item.type is sprites.ItemType.EXIT:
                    terminate()

        # Update the obstacles.
        for obstacle in obstacles:
            obstacle.update(dt)

        # Update the items.
        for item in items:
            item.update(dt)

        # Check for player interaction with teleporters
        for item in items:
            if isinstance(item, sprites.Teleporter):
                if player.rect.colliderect(item.rect):
                    item.interact(player)


        # Spawn portal dust.
        if portal_dust_spawn_timer.tick():
            for item in items:
                if item.type is sprites.ItemType.EXIT:
                    spawn_pos = pg.Vector2()
                    spawn_pos.from_polar((random.randint(50, 100), random.randrange(360)))
                    portal_particles.add(utils.PortalParticle(item.pos + spawn_pos, item.pos))

        # Update the particles.
        smoke_particles.update(dt)
        portal_particles.update(dt)

        # Update the camera.
        camera = pg.Vector2(SCREEN_SIZE) // 2 - player.pos

        # Draw everything to the screen.

        # Clear the screen completely by pasting the background image.
        screen.blit(background_image, (0, 0))

        # Draw the obstacles.
        # There are faster and more efficient ways to create and draw the obstacle images,
        # but I'm going the simple route for clarity.
        for obstacle in obstacles:
            obstacle.draw(screen, camera)
            # Draw the collision circles.
            if debug:
                # pg.draw.circle(screen, CYAN, obstacle.pos + camera, obstacle.radius, 1)
                screen.blit(obstacle.mask_image, obstacle.mask_rect.topleft + camera)

        # Draw each of the items.
        for item in items:
            item.draw(screen, camera)

        # Draw the player.
        player.draw(screen, camera)
        # Draw the hit box and player angle.
        if debug:
            # pg.draw.circle(screen, CYAN, player.pos + camera, player.radius, 1)
            screen.blit(player.mask_image, player.rect.topleft + camera)
            pg.draw.circle(screen, RED, player.pos + camera, sprites.PLAYER_PICKUP_RANGE, 1)
            player_angle_vector.from_polar((30, player.angle))
            pg.draw.line(screen, RED, player.pos + camera, player.pos + player_angle_vector + camera, 3)

        # Draw the particles.
        smoke_particles.draw(screen, camera)
        portal_particles.draw(screen, camera)

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
        tank_text_surf = kenney_font.render(tank_text, True, RED)
        screen.blit(tank_text_surf, FUEL_LEVEL_TEXT_POS)

        timer_surf = debug_font.render(f"Time:{timer} ",True, WHITE, BLACK)
        screen.blit(timer_surf,(700,45))

        # Show the fps.
        if debug:
            # Read the documentation to see how to render text.
            # The `font.render` method returns a `pygame.Surface` object, which is like an image.
            fps_surf = debug_font.render(f"FPS: {fps:.2f}", True, WHITE, BLACK)
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
