# -*- coding:utf-8 -*-
# This file holds various game objects like the player, obstacles, and items.
# Standard library imports.
import random
import math
from typing import Sequence
from enum import Enum, auto

# Third-party library imports.
import pygame as pg

# Local library imports.
from colors import *
import utils

# Constants
PLAYER_ROTATE_SPEED = 300  # The speed the keyboard can rotate the player angle.
PLAYER_PUSH_ACC = 300  # The acceleration that is applied to the player when the extinguisher is active.
PLAYER_CIRCLE_RADIUS = 30  # The radius of the collision circle for the player.
PLAYER_PICKUP_RANGE = 40  # The radius which will collide with item objects.

TANK_DECREASE = 5  # The speed the tank should decrease at per second.
TANK_MAX = 100  # The maximum value of the tank.
PORTAL_ROTATE_SPEED = 100  # The speed the portal rotates at.

MAX_ASTEROID_ROT_SPEED = 20  # The maximum speed an asteroid can rotate at.
ASTEROID_BOUNCE = 0.8  # The percentage of speed to keep when bouncing off an asteroid.


# Item type enumeration.
# To add new item types just add in another variable with a value of auto().
# ``variable is ItemType.Thing``
# to test if variable is a Thing.
class ItemType(Enum):
    FUEL = auto()
    EXIT = auto()


class Player:
    def __init__(self, pos: Sequence[float], image: pg.Surface):
        # I'm not using type hints for some variables here because their type is obvious.
        self.pos = pg.Vector2(pos)  # noqa The position of the player, in pixels.
        self.vel = pg.Vector2(0, 0)  # The velocity of the player.
        self.acc = pg.Vector2(0, 0)  # The acceleration of the player.
        self.angle = 0.0  # The angle of the fire extinguisher, in degrees.
        self.pushing = False  # Whether the extinguisher is active and pushing.
        self.radius = PLAYER_CIRCLE_RADIUS  # The radius of the collision circle.
        self.base_image = image  # Store a copy of the original image to avoid rotation corruption.
        self.image = pg.transform.rotate(self.base_image, -self.angle)  # This image is used for drawing.
        self.rect = self.image.get_rect(center=self.pos)  # This is used only for drawing.

        # Create the player mask.
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface(setcolor=CYAN, unsetcolor=TRANS_BLACK)

    def update(self, dt: float, game_bounds: pg.Vector2, obstacles: list["Obstacle"]) -> bool:
        """Update the player.

        This function handles movement, collision detection, etc.
        It returns a bool indicating a collision with an asteroid.
        """
        # Update the acceleration if the extinguisher is active.
        if self.pushing:
            self.acc.from_polar((-PLAYER_PUSH_ACC, self.angle))
        else:
            self.acc = pg.Vector2(0, 0)
        # Update the velocity and position based on acceleration and delta-time.
        self.vel += self.acc * dt
        self.pos += self.vel * dt

        # Collision detection with the game boundaries.
        # The player bounces off the game edges.
        if self.pos.x - self.radius < 0:
            self.vel.x *= -1
            self.pos.x = self.radius
        if self.pos.x + self.radius > game_bounds.x:
            self.vel.x *= -1
            self.pos.x = game_bounds.x - self.radius
        if self.pos.y - self.radius < 0:
            self.vel.y *= -1
            self.pos.y = self.radius
        if self.pos.y + self.radius > game_bounds.y:
            self.vel.y *= -1
            self.pos.y = game_bounds.y - self.radius

        # Update the image and rect.
        self.image = pg.transform.rotate(self.base_image, -self.angle)
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface(setcolor=CYAN, unsetcolor=TRANS_BLACK)
        self.rect = self.image.get_rect(center=self.pos)

        # Collide with obstacles.
        for obstacle in obstacles:
            if point := self.mask.overlap(obstacle.mask, pg.Vector2(obstacle.mask_rect.topleft) - self.rect.topleft):
                vel_length = self.vel.length() * ASTEROID_BOUNCE
                self.vel = point - obstacle.pos + self.rect.topleft
                self.vel.scale_to_length(vel_length)
                return True  # Indicate a hit sound is to be played.

        # this portion of the code will handle the gravity of the asteroids

        for obstacle in obstacles:
            # the amount of acceleration towards the planet
            accel = 70

            dx = obstacle.pos.x - self.pos.x
            dy = obstacle.pos.y - self.pos.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            direction_x = 0
            direction_y = 0

            if distance != 0 and distance > 80:
                direction_x = dx / distance
                direction_y = dy / distance

            self.pos.x += direction_x * accel * dt
            self.pos.y += direction_y * accel * dt


    def rotate(self, angle: float, obstacles: list["Obstacle"]):
        """Set the player's angle to the given angle, or not if it would collide with an asteroid."""
        test_mask = pg.mask.from_surface(pg.transform.rotate(self.base_image, -angle))
        mask_top_left = test_mask.get_rect(center=self.pos).topleft
        for obstacle in obstacles:
            if test_mask.overlap(obstacle.mask, pg.Vector2(obstacle.mask_rect.topleft) - mask_top_left):
                return
        self.angle += angle
        self.angle %= 360

    def draw(self, screen: pg.Surface, camera: pg.Vector2):
        """Draw the player to the screen."""
        screen.blit(self.image, self.rect.topleft + camera)


class Obstacle:
    def __init__(self, pos: Sequence[float], image: pg.Surface):
        self.pos = pg.Vector2(pos)  # noqa
        self.rot_speed = random.randint(-MAX_ASTEROID_ROT_SPEED, MAX_ASTEROID_ROT_SPEED)
        self.base_image = image
        self.radius = self.base_image.get_width() // 2

        self.angle = random.randrange(360)
        self.image = pg.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)  # Used only for drawing.
        self.mask_image = utils.make_circle_image(image.get_width() // 2, CYAN)
        self.mask = pg.mask.from_surface(self.mask_image)
        self.mask_rect = self.mask.get_rect(center=self.pos)  # For drawing and collision detection.
        # self.mask = pg.mask.from_surface(self.image)
        # self.mask_image = self.mask.to_surface(setcolor=CYAN, unsetcolor=TRANS_BLACK)

    def update(self, dt: float):
        """Update the obstacle.

        Rotate the image, etc.
        """
        self.angle += self.rot_speed * dt
        self.angle %= 360
        self.image = pg.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        # self.mask = pg.mask.from_surface(self.image)
        # self.mask_image = self.mask.to_surface(setcolor=CYAN, unsetcolor=TRANS_BLACK)

    def draw(self, screen: pg.Surface, camera: pg.Vector2):
        """Draw the obstacle to the screen."""
        screen.blit(self.image, self.rect.topleft + camera)


class Item:
    """Basic Item class, just a container with a position, image, and item type."""
    def __init__(self, pos: Sequence[float], image: pg.Surface, item_type: ItemType = ItemType.FUEL):
        self.type = item_type
        self.pos = pg.Vector2(pos)  # noqa
        self.base_image = image
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0
        self.rot_speed = PORTAL_ROTATE_SPEED if random.random() > 0.5 else -PORTAL_ROTATE_SPEED

    def update(self, dt: float):
        """Update the item. Currently only used for rotating the exit portal."""
        # Don't update if not the exit portal.
        if self.type is not ItemType.EXIT:
            return
        # Rotate the image and update the rect.
        self.angle += self.rot_speed * dt
        self.angle %= 360
        self.image = pg.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen: pg.Surface, camera: pg.Vector2):
        """Draw the item to the screen."""
        screen.blit(self.image, self.rect.topleft + camera)
