import pygame

from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    RIGHT_PANEL_WIDTH
)


# =========================================================
# PANEL
# =========================================================

PANEL_X = SCREEN_WIDTH - RIGHT_PANEL_WIDTH


# =========================================================
# DRAW PANEL
# =========================================================

def draw_frame_panel(
    screen,
    frames,
    current_frame_index,
    scroll_offset
):

    frame_rects = []

    # =====================================================
    # PANEL BACKGROUND
    # =====================================================

    pygame.draw.rect(
        screen,
        (24, 24, 28),
        (
            PANEL_X,
            0,
            RIGHT_PANEL_WIDTH,
            SCREEN_HEIGHT
        )
    )

    # =====================================================
    # TITLE
    # =====================================================

    font = pygame.font.SysFont(
        "arial",
        26,
        bold=True
    )

    title = font.render(
        "TIMELINE",
        True,
        (240, 240, 240)
    )

    screen.blit(
        title,
        (PANEL_X + 35, 30)
    )

    # =====================================================
    # FRAMES
    # =====================================================

    y = 90 - scroll_offset

    for i in range(len(frames)):

        rect = pygame.Rect(
            PANEL_X + 25,
            y,
            RIGHT_PANEL_WIDTH - 50,
            70
        )

        # Active frame glow
        if i == current_frame_index:

            pygame.draw.rect(
                screen,
                (90, 200, 255),
                rect,
                border_radius=16
            )

            inner_color = (42, 42, 52)

        else:

            inner_color = (34, 34, 40)

        # Card
        pygame.draw.rect(
            screen,
            inner_color,
            rect,
            border_radius=16
        )

        # Border
        pygame.draw.rect(
            screen,
            (80, 80, 90),
            rect,
            2,
            border_radius=16
        )

        # Text
        text_font = pygame.font.SysFont(
            "arial",
            22,
            bold=True
        )

        text = text_font.render(
            f"Frame {i + 1}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (rect.x + 22, rect.y + 22)
        )

        frame_rects.append(rect)

        y += 85

    return frame_rects