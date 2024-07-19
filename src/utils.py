# -*- coding:utf-8 -*-
# This file holds useful functions.
# It shouldn't import any other local files, to avoid circular imports.

# Standard library imports.
from typing import Hashable, Callable, Sequence, Optional, Iterable
from pathlib import Path  # This module allows object-oriented filesystem interaction.
import random  # Random number generation.

# Third-party library imports.
import pygame as pg

# Local library imports.
from colors import *


# Create the missing image Surface.
# DO NOT `convert()` it, that will be handled by the `load_image()` function.
# This is the classic black-and-magenta checkerboard image.
# By default, `pg.Surface` returns a black image.
MISSING_IMAGE = pg.Surface((32, 32))
MISSING_IMAGE.fill(MAGENTA, (0, 0, 16, 16))
MISSING_IMAGE.fill(MAGENTA, (16, 16, 32, 32))


def load_image(file: Path, convert: bool = True, alpha: bool = False) -> pg.Surface:
    """Load an image from the given file and optionally convert it to the display pixel format.

    The only reason you'd want to avoid conversion is loading images before the display is initialized
    with ``pygame.display.set_mode()``. Loading window icons is a good example of this.
    This function does not support ``convert_alpha()``, which could be added later if needed.
    """
    try:
        # Load the image from the file and return it as a Surface.
        # Convert it according to the given parameters.
        if convert:
            if alpha:
                return pg.image.load(file).convert_alpha()
            return pg.image.load(file).convert()
        return pg.image.load(file)
    except FileNotFoundError:
        # Return the missing image Surface instead.
        # Don't bother with converting alpha, because MISSING_IMAGE has no transparency.
        if convert:
            return MISSING_IMAGE.convert()
        return MISSING_IMAGE


def make_circle_image(radius: int, color: Sequence[int]) -> pg.Surface:
    """Create and return an image with a colored circle and a color key of BLACK.

    The surface size is ``(radius*2,radius*2)``.
    """
    image = pg.Surface((radius * 2, radius * 2))
    pg.draw.circle(image, color, (radius, radius), radius)  # noqa
    # Tell pygame to make BLACK pixels transparent when drawing to another surface.
    image.set_colorkey(BLACK)
    return image


class Timer:
    """A utility class for checking when certain time periods have passed."""
    def __init__(self, interval: float = 0, start: int = 0):
        """The interval is the length of time in milliseconds.

        An optional start value gives the timer a starting point in milliseconds.
        """
        self.interval = interval
        self.last_tick = start

    def tick(self, interval: Optional[float] = None) -> bool:
        """Return a bool indicating if the time period specified by ``interval`` has passed.

        If no interval is given to ``tick``, it uses the interval passed into the class constructor.
        """
        if pg.time.get_ticks() - self.last_tick >= (self.interval if interval is None else interval):
            self.last_tick = pg.time.get_ticks()
            return True
        return False


# These are for high-performance particle systems.
class ImageCache:
    """Utility class for caching images from certain data for fast access."""
    def __init__(self, make_image_func: Callable[[Hashable], pg.Surface]):
        self.cache: dict[Hashable, pg.Surface] = {}
        self.make_image = make_image_func

    def __len__(self) -> int:
        return len(self.cache)

    @property
    def size(self) -> int:
        return len(self)

    def clear_cache(self):
        self.cache: dict[Hashable, pg.Surface] = {}

    def get_image(self, item: Hashable) -> pg.Surface:
        """If the requested image exists, return it. Otherwise, create, cache, and return the image."""
        if item not in self.cache:
            self.cache[item] = self.make_image(item)
        return self.cache[item]


class Particle:
    """The base particle class. Should be overwritten with custom behavior."""
    def update(self, dt: float, *args, **kwargs) -> bool:
        """Return False when particle should be removed."""
        return True

    def draw_pos(self, image: pg.Surface) -> Sequence[float]:
        """Given the particle image, return the position the image should be blit at."""
        raise NotImplementedError

    def cache_lookup(self) -> Hashable:
        """The item to be passed to the ``ImageCache.make_image`` function."""
        return 1


class SmokeParticle(Particle):
    """The extinguisher smoke particles that appear when the player is thrusting."""
    def __init__(self, pos: Sequence[float], vel: Sequence[float], radius: int):
        self.pos = pg.Vector2(pos)  # noqa
        self.vel = pg.Vector2(vel)  # noqa
        self.radius = radius
        self.life_time = random.randint(1500, 2000)
        self.start_time = pg.time.get_ticks()

    def update(self, dt: float, *args, **kwargs) -> bool:
        # Delete the particles when their lifetime expires.
        if pg.time.get_ticks() - self.start_time >= self.life_time:
            return False
        self.pos += self.vel * dt
        return True

    def draw_pos(self, image: pg.Surface) -> Sequence[float]:
        # Center the image on the particle's position.
        return self.pos - (self.radius, self.radius)

    def cache_lookup(self) -> Hashable:
        # The radius is the only difference between these particles.
        return self.radius


class PortalParticle(Particle):
    """The portal dust particle, sucked towards the center of the wormhole."""
    def __init__(self, pos: Sequence[float], target: Sequence[float], speed: int = 20):
        self.pos = pg.Vector2(pos)  # noqa
        self.target_pos = pg.Vector2(target)  # noqa
        self.target_vector = pg.Vector2(target - self.pos)  # noqa
        self.target_vector.scale_to_length(speed)

    def update(self, dt: float, *args, **kwargs) -> bool:
        # Go towards the target, deleting if too close.
        self.pos += self.target_vector * dt
        return self.pos.distance_squared_to(self.target_pos) > 20

    def draw_pos(self, image: pg.Surface) -> Sequence[float]:
        # Center the image on the particle position.
        return self.pos - image.get_size()

    def cache_lookup(self) -> Hashable:
        # All dust particles are the same.
        return 1


class ParticleGroup:
    """The container class that holds, updates, and draws particles."""
    def __init__(self, image_cache: ImageCache, blend: int = pg.BLENDMODE_NONE,
                 particles: Optional[list[Particle]] = None):
        self.particles: list[Particle] = particles if particles is not None else []
        self.image_cache = image_cache
        self.blend = blend

    def __len__(self):
        return len(self.particles)

    def add(self, particles: Particle | Iterable[Particle]):
        """Add a particle or a sequence of particles to the ParticleGroup."""
        if isinstance(particles, Particle):
            self.particles.append(particles)
        else:
            self.particles.extend(particles)

    def update(self, dt: float, *args, **kwargs):
        """Update all the particles, deleting them when they expire."""
        self.particles = [p for p in self.particles if p.update(dt, *args, **kwargs)]

    def _get_draw_tuple(self, p: Particle, camera: pg.Vector2) -> tuple[pg.Surface, Sequence[float]]:
        """Internal method to get the (image, blit_pos) for each particle."""
        image = self.image_cache.get_image(p.cache_lookup())
        return image, p.draw_pos(image) + camera

    def draw(self, screen: pg.Surface, camera: pg.Vector2, blend: int = pg.BLENDMODE_NONE):
        """Blit all particles on the screen with a certain blend mode."""
        screen.fblits([self._get_draw_tuple(p, camera) for p in self.particles], blend if blend else self.blend)  # noqa
