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
ROUND_DURATION = 30.0


class GameEngine:
    def __init__(self):
        self._spawn_count = 0
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self._last_update_time = pygame.time.get_ticks()
        self.round_start_time = self._last_update_time
        self.round_active = True
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

        return Target(x, y, radius=TARGET_RADIUS, vx=vx, vy=vy)

    def restart(self):
        """Reset the game state and start a new 30-second round."""
        self._spawn_count = 0
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]

        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo_multiplier = 1

        now = pygame.time.get_ticks()
        self.round_start_time = now
        self._last_update_time = now
        self.round_active = True

    def _time_remaining(self):
        """Return the remaining round time in seconds, clamped at zero."""
        elapsed = (pygame.time.get_ticks() - self.round_start_time) / 1000.0
        return max(0.0, ROUND_DURATION - elapsed)

    def handle_click(self, pos):
        # Do not allow shots once the round has ended or time has reached zero.
        if not self.round_active:
            return

        if self._time_remaining() <= 0.0:
            self.round_active = False
            return

        target = check_hit(self.targets, pos)

        if target is not None:
            self.hits += 1
            self.score += POINTS_PER_HIT * self.combo_multiplier
            self.combo_multiplier += 1
            self.targets.remove(target)
            self.targets.append(self._random_target())

        else:
            self.misses += 1
            self.combo_multiplier = 1

    def update(self):
        if not self.round_active:
            return

        now = pygame.time.get_ticks()

        # End the round as soon as 30 seconds have elapsed.
        if now - self.round_start_time >= ROUND_DURATION * 1000:
            self.round_active = False
            self._last_update_time = now
            return

        dt = (now - self._last_update_time) / 1000.0
        self._last_update_time = now

        for target in self.targets:
            target.update(dt, WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.targets)

        if self.round_active:
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
            renderer.draw_text(
                surface,
                font,
                f"Time: {self._time_remaining():.1f}",
                (10, 62),
            )
        else:
            renderer.draw_text(
                surface,
                font,
                f"Final Score: {self.score}",
                (10, 10),
            )
            renderer.draw_banner(
                surface,
                font,
                f"Time's up!  Final Score: {self.score}",
            )
            renderer.draw_text(
                surface,
                font,
                "Press R to restart",
                (10, 36),
            )