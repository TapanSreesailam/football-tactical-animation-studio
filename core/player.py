import pygame


# =========================================================
# PLAYER
# =========================================================

class Player:

    def __init__(self, x, y, role, number):

        self.x = x
        self.y = y

        self.role = role

        self.number = number

        self.dragging = False

        # Motion trail
        self.trail = []

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen, selected=False):

        # =============================================
        # TRAIL
        # =============================================

        self.trail.append((self.x, self.y))

        if len(self.trail) > 8:

            self.trail.pop(0)

        for i, pos in enumerate(self.trail):

            alpha = i / len(self.trail)

            radius = int(12 * alpha)

            if radius > 0:

                pygame.draw.circle(
                    screen,
                    (90, 180, 255),
                    (int(pos[0]), int(pos[1])),
                    radius,
                    1
                )

        # =============================================
        # PLAYER BODY
        # =============================================

        color = (
            (255, 210, 0)
            if selected
            else (70, 140, 255)
        )

        pygame.draw.circle(
            screen,
            color,
            (int(self.x), int(self.y)),
            18
        )

        # =============================================
        # NUMBER
        # =============================================

        font = pygame.font.SysFont(
            "arial",
            18,
            bold=True
        )

        text = font.render(
            str(self.number),
            True,
            (255, 255, 255)
        )

        rect = text.get_rect(
            center=(self.x, self.y)
        )

        screen.blit(text, rect)