# -*- coding:utf-8 -*-
# This file holds various game objects like the player, obstacles, and items.

# Standard library imports.
from typing import Sequence

# Third-party library imports.
import pygame as pg

# Local library imports.
from colors import *
import utils


# Constants
PLAYER_ROTATE_SPEED = 300  # The speed the keyboard can rotate the player angle.
PLAYER_PUSH_ACC = 300  # The acceleration that is applied to the player when the extinguisher is active.


class Player:
    def __init__(self, pos: Sequence[float], image: pg.Surface):
        # I'm not using type hints for some variables here because their type is obvious.
        self.pos = pg.Vector2(pos)  # The position of the player, in pixels.
        self.vel = pg.Vector2(0, 0)  # The velocity of the player.
        self.acc = pg.Vector2(0, 0)  # The acceleration of the player.
        self.angle: float = 0.0  # The angle of the fire extinguisher, in degrees.
        self.pushing: bool = False  # Whether the extinguisher is active and pushing.
        self.radius: int = 20  # The radius used for circular collision code in pixels.
        # We don't have a player image yet, so I will use a placeholder.
        # self.image = utils.make_circle_image(self.radius, GREEN)
        self.image = image
        

        # Load the player image and mask.
        self.mask = pg.mask.from_surface(self.image)
        
        #centers the mask on the middle of the image
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt: float, screen_size: pg.Vector2, obstacles: list["Obstacle"]):
        """Update the player.

        This function handles movement, collision detection, etc.
        """
        # Update the acceleration if the extinguisher is active.
        if self.pushing:
            self.acc.from_polar((-PLAYER_PUSH_ACC, self.angle))
        else:
            self.acc = pg.Vector2(0, 0)
        # Update the velocity and position based on acceleration and delta-time.
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        # Collision detection with the screen boundaries.
        # We won't need this when we have a working camera.
        # The player bounces off the screen edges.
        if self.pos.x - self.radius < 0:
            self.vel.x *= -1
            self.pos.x = self.radius
        if self.pos.x + self.radius > screen_size.x:
            self.vel.x *= -1
            self.pos.x = screen_size.x - self.radius
        if self.pos.y - self.radius < 0:
            self.vel.y *= -1
            self.pos.y = self.radius
        if self.pos.y + self.radius > screen_size.y:
            self.vel.y *= -1
            self.pos.y = screen_size.y - self.radius

        # Update the player's rect position.
        self.rect = self.image.get_rect(center=self.pos)

        # Collision detection with obstacles.
        if self.rect.colliderect(obstacles[0].rect):
            self.vel *= -1

    def draw(self, screen: pg.Surface):
        """Draw the player to the screen.

        The position adjustment by radius is because images are drawn from the top-left corner.
        """

        # Draw the player image and mask.
        screen.blit(self.image, self.pos - (self.radius, self.radius))
        screen.blit(self.mask.to_surface(), (0, 0))

        # Draw the hitbox.
        pg.draw.rect(screen, RED, self.rect, 1)


class Obstacle:
    def __init__(self, pos: Sequence[float], radius: int):
        self.pos = pg.Vector2(pos)
        self.radius: int = radius
        self.image = utils.make_circle_image(radius, YELLOW)

        # center the rect on the position
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt: float):
        """Update obstacles.

        This function is blank right now.
        """
        pass

    def draw(self, screen: pg.Surface):
        """Draw the obstacle to the screen.

        The position adjustment by radius is because images are drawn from the top-left corner.
        """
        screen.blit(self.image, self.pos - (self.radius, self.radius))

        # Draw the hitbox.
        pg.draw.rect(screen, RED, self.rect, 1)
