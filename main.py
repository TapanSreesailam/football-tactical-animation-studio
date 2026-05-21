import pygame
import math
import imageio
import numpy as np

from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    RIGHT_PANEL_WIDTH
)

from ui.pitch import (
    draw_pitch,
    goal_wobble,
    PITCH_X,
    PITCH_Y,
    PITCH_WIDTH,
    PITCH_HEIGHT,
    GOAL_WIDTH
)

from ui.frame_panel import draw_frame_panel

from core.player import Player
from core.ball import Ball
from core.frame import Frame


# =========================================================
# INIT
# =========================================================

pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "Football Tactical Animation Studio"
)

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    "arial",
    24
)

menu_font = pygame.font.SysFont(
    "arial",
    20
)


# =========================================================
# PITCH CENTER
# =========================================================

CENTER_X = PITCH_X + PITCH_WIDTH // 2


# =========================================================
# PLAYERS
# =========================================================

players = [

    Player(CENTER_X, 760, "GK", 1),

    Player(CENTER_X - 160, 610, "LCB", 2),
    Player(CENTER_X + 160, 610, "RCB", 3),

    Player(CENTER_X - 250, 420, "LM", 4),
    Player(CENTER_X, 500, "CM", 5),
    Player(CENTER_X + 250, 420, "RM", 6),

    Player(CENTER_X, 190, "ST", 7),
]


# =========================================================
# BALL
# =========================================================

ball = Ball(
    players[4].x,
    players[4].y - 22
)


# =========================================================
# FRAME SYSTEM
# =========================================================

frames = []

current_frame_index = 0

scroll_offset = 0


# =========================================================
# PLAYBACK
# =========================================================

playing = False

exporting_video = False

animation_progress = 0

animation_speed = 0.014


# =========================================================
# LOFT MODE
# =========================================================

loft_mode = False


# =========================================================
# CONTEXT MENU
# =========================================================

show_context_menu = False

context_menu_x = 0
context_menu_y = 0

context_frame_index = None


# =========================================================
# SAVE FRAME
# =========================================================

def save_current_frame():

    player_positions = []

    for player in players:

        player_positions.append(
            (player.x, player.y)
        )

    return Frame(
        player_positions,
        (ball.x, ball.y),
        loft_mode
    )


# =========================================================
# LOAD FRAME
# =========================================================

def load_frame(frame):

    for i, player in enumerate(players):

        player.x = frame.player_positions[i][0]
        player.y = frame.player_positions[i][1]

    ball.x = frame.ball_position[0]
    ball.y = frame.ball_position[1]


# =========================================================
# INITIAL FRAME
# =========================================================

frames.append(
    save_current_frame()
)

selected_player = players[4]


# =========================================================
# EASING
# =========================================================

def ease_in_out(t):

    return t * t * (3 - 2 * t)


# =========================================================
# LERP
# =========================================================

def lerp(a, b, t):

    return a + (b - a) * t


# =========================================================
# EXPORT VIDEO
# =========================================================

def export_video():

    writer = imageio.get_writer(
        "football_tactics_export.mp4",
        fps=60
    )

    temp_progress = 0

    temp_frame_index = 0

    while temp_frame_index < len(frames) - 1:

        start_frame = frames[temp_frame_index]
        end_frame = frames[temp_frame_index + 1]

        temp_progress += animation_speed

        t = ease_in_out(temp_progress)

        # PLAYERS
        for i, player in enumerate(players):

            start_x = start_frame.player_positions[i][0]
            start_y = start_frame.player_positions[i][1]

            end_x = end_frame.player_positions[i][0]
            end_y = end_frame.player_positions[i][1]

            player.x = lerp(start_x, end_x, t)
            player.y = lerp(start_y, end_y, t)

        # BALL
        ball.x = lerp(
            start_frame.ball_position[0],
            end_frame.ball_position[0],
            t
        )

        ball.y = lerp(
            start_frame.ball_position[1],
            end_frame.ball_position[1],
            t
        )

        # LOFT
        if end_frame.lofted:

            peak_height = 120

            ball.height = (
                math.sin(t * math.pi)
                * peak_height
            )

        else:

            ball.height = 0

        # DRAW
        draw_pitch(screen)

        for player in players:

            player.draw(screen)

        ball.draw(screen)

        draw_frame_panel(
            screen,
            frames,
            temp_frame_index,
            scroll_offset
        )

        pygame.display.flip()

        # CAPTURE
        frame_array = pygame.surfarray.array3d(
            screen
        )

        frame_array = np.transpose(
            frame_array,
            (1, 0, 2)
        )

        writer.append_data(frame_array)

        # NEXT
        if temp_progress >= 1:

            temp_progress = 0

            temp_frame_index += 1

    writer.close()

    print(
        "✅ Exported football_tactics_export.mp4"
    )


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    clock.tick(FPS)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    frame_rects = draw_frame_panel(
        screen,
        frames,
        current_frame_index,
        scroll_offset
    )

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # =================================================
        # KEYBOARD
        # =================================================

        if event.type == pygame.KEYDOWN:

            # PLAYER SWITCH
            if pygame.K_1 <= event.key <= pygame.K_7:

                selected_player = players[
                    event.key - pygame.K_1
                ]

            # EXPORT
            if event.key == pygame.K_e:

                export_video()

            # LOFT
            if event.key == pygame.K_l:

                loft_mode = not loft_mode

            # NEW FRAME
            if event.key == pygame.K_n:

                frames.append(
                    save_current_frame()
                )

                current_frame_index = len(frames) - 1

            # PLAY
            if event.key == pygame.K_SPACE:

                if len(frames) > 1:

                    playing = True

                    animation_progress = 0

            # NEXT FRAME
            if event.key == pygame.K_RIGHT:

                if current_frame_index < len(frames) - 1:

                    current_frame_index += 1

                    load_frame(
                        frames[current_frame_index]
                    )

            # PREVIOUS FRAME
            if event.key == pygame.K_LEFT:

                if current_frame_index > 0:

                    current_frame_index -= 1

                    load_frame(
                        frames[current_frame_index]
                    )

        # =================================================
        # SCROLL
        # =================================================

        if event.type == pygame.MOUSEWHEEL:

            scroll_offset -= event.y * 30

            if scroll_offset < 0:

                scroll_offset = 0

        # =================================================
        # MOUSE DOWN
        # =================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            # RIGHT CLICK
            if event.button == 3:

                for i, rect in enumerate(frame_rects):

                    if rect.collidepoint(mouse_x, mouse_y):

                        show_context_menu = True

                        context_menu_x = mouse_x
                        context_menu_y = mouse_y

                        context_frame_index = i

            # LEFT CLICK
            if event.button == 1:

                # MENU
                if show_context_menu:

                    play_rect = pygame.Rect(
                        context_menu_x,
                        context_menu_y,
                        220,
                        40
                    )

                    delete_rect = pygame.Rect(
                        context_menu_x,
                        context_menu_y + 40,
                        220,
                        40
                    )

                    # PLAY FROM
                    if play_rect.collidepoint(mouse_x, mouse_y):

                        current_frame_index = context_frame_index

                        animation_progress = 0

                        playing = True

                    # DELETE
                    elif delete_rect.collidepoint(mouse_x, mouse_y):

                        if len(frames) > 1:

                            del frames[
                                context_frame_index
                            ]

                            if current_frame_index >= len(frames):

                                current_frame_index = (
                                    len(frames) - 1
                                )

                    show_context_menu = False

                # FRAME SELECT
                for i, rect in enumerate(frame_rects):

                    if rect.collidepoint(mouse_x, mouse_y):

                        current_frame_index = i

                        load_frame(frames[i])

                # PLAYER DRAG
                for player in players:

                    dx = mouse_x - player.x
                    dy = mouse_y - player.y

                    if dx * dx + dy * dy < 20 * 20:

                        player.dragging = True

                        selected_player = player

                # BALL DRAG
                dx = mouse_x - ball.x
                dy = mouse_y - ball.y

                if dx * dx + dy * dy < 15 * 15:

                    ball.dragging = True

        # =================================================
        # MOUSE UP
        # =================================================

        if event.type == pygame.MOUSEBUTTONUP:

            for player in players:

                player.dragging = False

            ball.dragging = False

    # =====================================================
    # PLAYER DRAGGING
    # =====================================================

    for player in players:

        if player.dragging:

            player.x = mouse_x
            player.y = mouse_y

    # =====================================================
    # BALL DRAGGING
    # =====================================================

    if ball.dragging:

        ball.x = mouse_x
        ball.y = mouse_y

    # =====================================================
    # PLAYBACK
    # =====================================================

    if playing:

        if current_frame_index < len(frames) - 1:

            start_frame = frames[current_frame_index]
            end_frame = frames[current_frame_index + 1]

            animation_progress += animation_speed

            t = ease_in_out(
                animation_progress
            )

            # PLAYERS
            for i, player in enumerate(players):

                start_x = start_frame.player_positions[i][0]
                start_y = start_frame.player_positions[i][1]

                end_x = end_frame.player_positions[i][0]
                end_y = end_frame.player_positions[i][1]

                player.x = lerp(start_x, end_x, t)
                player.y = lerp(start_y, end_y, t)

            # BALL
            ball.x = lerp(
                start_frame.ball_position[0],
                end_frame.ball_position[0],
                t
            )

            ball.y = lerp(
                start_frame.ball_position[1],
                end_frame.ball_position[1],
                t
            )

            # GOAL DETECTION
            goal_left = (
                PITCH_X
                + (PITCH_WIDTH - GOAL_WIDTH) // 2
            )

            goal_right = (
                goal_left + GOAL_WIDTH
            )

            # TOP GOAL
            if (
                goal_left <= ball.x <= goal_right
                and ball.y <= PITCH_Y
            ):

                import ui.pitch as pitch_module

                pitch_module.goal_wobble = 12

            # BOTTOM GOAL
            if (
                goal_left <= ball.x <= goal_right
                and ball.y >= PITCH_Y + PITCH_HEIGHT
            ):

                import ui.pitch as pitch_module

                pitch_module.goal_wobble = 12

            # LOFT
            if end_frame.lofted:

                peak_height = 120

                ball.height = (
                    math.sin(t * math.pi)
                    * peak_height
                )

            else:

                ball.height = 0

            # NEXT
            if animation_progress >= 1:

                animation_progress = 0

                current_frame_index += 1

        else:

            playing = False

    # =====================================================
    # DRAW
    # =====================================================

    draw_pitch(screen)

    # PLAYERS
    for player in players:

        player.draw(
            screen,
            selected=(player == selected_player)
        )

    # BALL
    ball.draw(screen)

    # TIMELINE
    draw_frame_panel(
        screen,
        frames,
        current_frame_index,
        scroll_offset
    )

    # LOFT STATUS
    loft_text = (
        "LOFT: ON"
        if loft_mode
        else "LOFT: OFF"
    )

    loft_surface = font.render(
        loft_text,
        True,
        (255, 255, 255)
    )

    screen.blit(
        loft_surface,
        (40, 30)
    )

    # CONTEXT MENU
    if show_context_menu:

        pygame.draw.rect(
            screen,
            (35, 35, 35),
            (
                context_menu_x,
                context_menu_y,
                220,
                80
            ),
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            (70, 70, 70),
            (
                context_menu_x,
                context_menu_y,
                220,
                80
            ),
            2,
            border_radius=8
        )

        play_text = menu_font.render(
            "▶ Play From This Frame",
            True,
            (255, 255, 255)
        )

        delete_text = menu_font.render(
            "🗑 Delete This Frame",
            True,
            (255, 120, 120)
        )

        screen.blit(
            play_text,
            (
                context_menu_x + 15,
                context_menu_y + 10
            )
        )

        screen.blit(
            delete_text,
            (
                context_menu_x + 15,
                context_menu_y + 50
            )
        )

    pygame.display.flip()

pygame.quit()