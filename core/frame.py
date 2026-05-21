# =========================================================
# FRAME
# =========================================================

class Frame:

    def __init__(
        self,
        player_positions,
        ball_position,
        lofted=False
    ):

        self.player_positions = player_positions

        self.ball_position = ball_position

        # Loft setting for THIS frame
        self.lofted = lofted