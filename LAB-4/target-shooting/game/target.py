"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""

import pygame


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70), vx=0.0, vy=0.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy

    def get_bounding_rect(self):
        """A square bounding box around the circle - NOT the same
        shape as the actual circle, and easy to build incorrectly."""
        return pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def update(self, dt, width, height):
        """Move the target and bounce at the playable-area boundaries."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Keep the entire circle inside the play area.
        min_x = self.radius
        max_x = width - self.radius
        min_y = self.radius
        max_y = height - self.radius

        if self.x <= min_x:
            self.x = min_x
            self.vx = abs(self.vx)
        elif self.x >= max_x:
            self.x = max_x
            self.vx = -abs(self.vx)

        if self.y <= min_y:
            self.y = min_y
            self.vy = abs(self.vy)
        elif self.y >= max_y:
            self.y = max_y
            self.vy = -abs(self.vy)
