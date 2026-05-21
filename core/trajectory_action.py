# =========================================================
# TRAJECTORY ACTION
# =========================================================

class TrajectoryAction:

    def __init__(self, action_type):

        self.action_type = action_type

        self.points = []

    # =====================================================
    # ADD POINT
    # =====================================================

    def add_point(self, pos):

        self.points.append(pos)