"""
GameEngine: owns the targets and handles player clicks.

Starter version: a few static targets that respawn elsewhere when
clicked (correctly or not, depending on the hit-detection bug) - no
movement, no score/combo, no timer yet. That's Tasks 2-4.
"""

import random
import pygame

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
POINTS_PER_HIT = 10


class GameEngine:
    def __init__(self):
        self._spawn_count = 0
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self._last_update_time = pygame.time.get_ticks()
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo_multiplier = 1

    def _random_target(self):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)

        # Give targets different movement patterns and speeds.
        pattern = self._spawn_count % 3
        self._spawn_count += 1

        if pattern == 0:
            # Slow horizontal movement.
            vx, vy = 100.0, 0.0
        elif pattern == 1:
            # Faster vertical movement.
            vx, vy = 0.0, 160.0
        else:
            # Faster diagonal movement.
            vx, vy = 130.0, 130.0

        # Randomize initial direction so targets do not all move the same way.
        if vx != 0.0 and random.choice((False, True)):
            vx *= -1

        if vy != 0.0 and random.choice((False, True)):
            vy *= -1

        return Target(
            x,
            y,
            radius=TARGET_RADIUS,
            vx=vx,
            vy=vy,
        )

    def handle_click(self, pos):
        target = check_hit(self.targets, pos)

        if target is not None:
            self.hits += 1

            # Award points using the current combo multiplier.
            self.score += POINTS_PER_HIT * self.combo_multiplier

            # Increase the multiplier for the next consecutive hit.
            self.combo_multiplier += 1

            self.targets.remove(target)
            self.targets.append(self._random_target())

        else:
            self.misses += 1

            # A miss breaks the combo.
            self.combo_multiplier = 1

    def update(self):
        now = pygame.time.get_ticks()
        dt = (now - self._last_update_time) / 1000.0
        self._last_update_time = now

        for target in self.targets:
            target.update(dt, WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.targets)

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}  Combo Multiplier: x{self.combo_multiplier}",
            (10, 10),
        )

        renderer.draw_text(
            surface,
            font,
            f"Hits: {self.hits}  Misses: {self.misses}",
            (10, 36),
        )