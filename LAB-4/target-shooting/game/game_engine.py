"""
GameEngine: owns the targets and handles player clicks.

Starter version: a few static targets that respawn elsewhere when
clicked (correctly or not, depending on the hit-detection bug) - no
movement, no score/combo, no timer yet. That's Tasks 2-4.
"""

import random

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28


class GameEngine:
    def __init__(self):
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0

    def _random_target(self):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)
        return Target(x, y, radius=TARGET_RADIUS)

    def handle_click(self, pos):
        target = check_hit(self.targets, pos)
        if target is not None:
            self.hits += 1
            self.targets.remove(target)
            self.targets.append(self._random_target())
        else:
            self.misses += 1

    def update(self):
        pass

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.targets)
        renderer.draw_text(surface, font, f"Hits: {self.hits}  Misses: {self.misses}", (10, 10))
