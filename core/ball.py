import pygame


# =========================================================
# BALL
# =========================================================

class Ball:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.target_x = x
        self.target_y = y

        self.dragging = False

        self.height = 0

        # Motion trail
        self.trail = []

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        # Faster than players
        speed = 0.28

        self.x += (
            self.target_x - self.x
        ) * speed

        self.y += (
            self.target_y - self.y
        ) * speed

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen):

        # =============================================
        # TRAIL
        # =============================================

        self.trail.append(
            (self.x, self.y - self.height)
        )

        if len(self.trail) > 14:

            self.trail.pop(0)

        for i, pos in enumerate(self.trail):

            alpha = i / len(self.trail)

            radius = int(6 * alpha)

            if radius > 0:

                pygame.draw.circle(
                    screen,
                    (220, 220, 220),
                    (
                        int(pos[0]),
                        int(pos[1])
                    ),
                    radius,
                    1
                )

        # =============================================
        # SHADOW
        # =============================================

        pygame.draw.circle(
            screen,
            (40, 40, 40),
            (
                int(self.x),
                int(self.y)
            ),
            7
        )

        # =============================================
        # BALL HEIGHT
        # =============================================

        draw_y = self.y - self.height

        # Main ball
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                int(self.x),
                int(draw_y)
            ),
            9
        )

        # Center pentagon
        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (
                int(self.x),
                int(draw_y)
            ),
            3
        )

        # Football patches
        offsets = [
            (-4, -2),
            (4, -2),
            (-3, 4),
            (3, 4),
        ]

        for ox, oy in offsets:

            pygame.draw.circle(
                screen,
                (20, 20, 20),
                (
                    int(self.x + ox),
                    int(draw_y + oy)
                ),
                2
            )