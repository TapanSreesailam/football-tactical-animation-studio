import pygame

from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    RIGHT_PANEL_WIDTH
)


# =========================================================
# PITCH
# =========================================================

PITCH_WIDTH = 820
PITCH_HEIGHT = 720

usable_width = (
    SCREEN_WIDTH
    - RIGHT_PANEL_WIDTH
)

PITCH_X = (
    usable_width - PITCH_WIDTH
) // 2 + 70

PITCH_Y = 90


# =========================================================
# GOAL SETTINGS
# =========================================================

GOAL_WIDTH = 160
GOAL_DEPTH = 26

goal_wobble = 0


# =========================================================
# DRAW GOAL
# =========================================================

def draw_goal(
    screen,
    x,
    y,
    upside_down=False
):

    global goal_wobble

    wobble_offset = goal_wobble

    post_color = (240, 240, 240)

    net_color = (170, 170, 170)

    # =====================================================
    # POSTS
    # =====================================================

    pygame.draw.line(
        screen,
        post_color,
        (x, y),
        (x, y + GOAL_DEPTH),
        5
    )

    pygame.draw.line(
        screen,
        post_color,
        (x + GOAL_WIDTH, y),
        (x + GOAL_WIDTH, y + GOAL_DEPTH),
        5
    )

    pygame.draw.line(
        screen,
        post_color,
        (x, y),
        (x + GOAL_WIDTH, y),
        5
    )

    # =====================================================
    # NET
    # =====================================================

    spacing = 16

    for i in range(0, GOAL_WIDTH + 1, spacing):

        pygame.draw.line(
            screen,
            net_color,
            (x + i, y),
            (
                x + i,
                y + GOAL_DEPTH + wobble_offset
            ),
            1
        )

    for j in range(0, GOAL_DEPTH + 1, spacing):

        pygame.draw.line(
            screen,
            net_color,
            (x, y + j + wobble_offset),
            (x + GOAL_WIDTH, y + j),
            1
        )


# =========================================================
# DRAW PITCH
# =========================================================

def draw_pitch(screen):

    global goal_wobble

    # =====================================================
    # BACKGROUND
    # =====================================================

    screen.fill((20, 20, 24))

    # =====================================================
    # PITCH
    # =====================================================

    pitch_rect = pygame.Rect(
        PITCH_X,
        PITCH_Y,
        PITCH_WIDTH,
        PITCH_HEIGHT
    )

    pygame.draw.rect(
        screen,
        (34, 139, 34),
        pitch_rect,
        border_radius=8
    )

    # =====================================================
    # STRIPES
    # =====================================================

    stripe_height = 45

    for i in range(18):

        color = (
            (38, 145, 38)
            if i % 2 == 0
            else (32, 128, 32)
        )

        pygame.draw.rect(
            screen,
            color,
            (
                PITCH_X,
                PITCH_Y + i * stripe_height,
                PITCH_WIDTH,
                stripe_height
            )
        )

    line_color = (240, 240, 240)

    # =====================================================
    # OUTER BORDER
    # =====================================================

    pygame.draw.rect(
        screen,
        line_color,
        pitch_rect,
        4,
        border_radius=8
    )

    # =====================================================
    # CENTER LINE
    # =====================================================

    pygame.draw.line(
        screen,
        line_color,
        (
            PITCH_X,
            PITCH_Y + PITCH_HEIGHT // 2
        ),
        (
            PITCH_X + PITCH_WIDTH,
            PITCH_Y + PITCH_HEIGHT // 2
        ),
        4
    )

    # =====================================================
    # CENTER CIRCLE
    # =====================================================

    pygame.draw.circle(
        screen,
        line_color,
        (
            PITCH_X + PITCH_WIDTH // 2,
            PITCH_Y + PITCH_HEIGHT // 2
        ),
        80,
        4
    )

    # =====================================================
    # PENALTY BOXES
    # =====================================================

    box_width = 360
    box_height = 120

    # TOP
    pygame.draw.rect(
        screen,
        line_color,
        (
            PITCH_X + (PITCH_WIDTH - box_width) // 2,
            PITCH_Y,
            box_width,
            box_height
        ),
        4
    )

    # BOTTOM
    pygame.draw.rect(
        screen,
        line_color,
        (
            PITCH_X + (PITCH_WIDTH - box_width) // 2,
            PITCH_Y + PITCH_HEIGHT - box_height,
            box_width,
            box_height
        ),
        4
    )

    # =====================================================
    # GOALS
    # =====================================================

    top_goal_x = (
        PITCH_X
        + (PITCH_WIDTH - GOAL_WIDTH) // 2
    )

    bottom_goal_x = top_goal_x

    # TOP GOAL
    draw_goal(
        screen,
        top_goal_x,
        PITCH_Y - GOAL_DEPTH
    )

    # BOTTOM GOAL
    draw_goal(
        screen,
        bottom_goal_x,
        PITCH_Y + PITCH_HEIGHT
    )

    # =====================================================
    # WOBBLE DECAY
    # =====================================================

    goal_wobble *= 0.82