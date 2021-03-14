"""
The template of the main script of the machine learning process
"""


def count(self, point):
    if point > 200:
        return 400 - point
    elif point < 0:
        return (-1) * point
    else:
        return point


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_LEFT"

        else:
            x = scene_info["ball"][0]
            y = 400 - scene_info["ball"][1]
            point1 = x + y
            point2 = x - y
            if point1 > 200:
                point1 = 400 - point1
            elif point1 < 0:
                point1 = (-1) * point1

            if point2 > 200:
                point2 = 400 - point2
            elif point2 < 0:
                point2 = (-1) * point2

            mx = scene_info["platform"][0] - scene_info["ball"][0]
            my = scene_info["platform"][1] - scene_info["ball"][1]
            if mx == 0:
                m = 0
            else:
                m = my / mx

            if (m < 10) and (m > -10):
                if scene_info["ball"][0] > scene_info["platform"][0]:
                    if point1 > scene_info["ball"][0]:
                        command = "MOVE_RIGHT"
                    else:
                        command = "MOVE_LEFT"
                else:
                    if point2 > scene_info["ball"][0]:
                        command = "MOVE_RIGHT"
                    else:
                        command = "MOVE_LEFT"
            else:
                print(m)
                command = ""
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
