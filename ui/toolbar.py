import pygame

from config.settings import (
    LEFT_PANEL_WIDTH,
    SCREEN_HEIGHT
)

# =========================================================
# COLORS
# =========================================================

BG = (30, 30, 30)

BUTTON = (52, 52, 52)

ACTIVE = (80, 120, 220)

TEXT = (240, 240, 240)


# =========================================================
# BUTTONS
# =========================================================

buttons = [

    ("DRIBBLE", "DRIBBLE"),
    ("PASS", "PASS"),
    ("THROUGH", "THROUGH"),
    ("CROSS", "CROSS"),
    ("LOFT", "LOFT"),
]


# =========================================================
# DRAW TOOLBAR
# =========================================================

def draw_toolbar(screen, current_mode):

    pygame.draw.rect(
        screen,
        BG,
        (
            0,
            0,
            LEFT_PANEL_WIDTH,
            SCREEN_HEIGHT
        )
    )

    font = pygame.font.SysFont(
        "arial",
        20,
        bold=True
    )

    button_rects = {}

    y = 120

    for text, mode in buttons:

        rect = pygame.Rect(
            20,
            y,
            140,
            48
        )

        color = (
            ACTIVE
            if current_mode == mode
            else BUTTON
        )

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=10
        )

        label = font.render(
            text,
            True,
            TEXT
        )

        label_rect = label.get_rect(
            center=rect.center
        )

        screen.blit(label, label_rect)

        button_rects[mode] = rect

        y += 70

    return button_rects