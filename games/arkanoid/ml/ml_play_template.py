"""
The template of the main script of the machine learning process
"""
import random


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.last_x = 0
        self.last_y = 0
        self.predict_X = 0
        self.predict_Y = 0

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
            command = "NONE"
            mx = scene_info["ball"][0] - self.last_x  # mx > 0 RIGHT
            my = scene_info["ball"][1] - self.last_y  # my > 0 DOWN
            m = my / mx
            if mx > 0 and my > 0 :  # RIGHT_DOWN
                self.predict_Y = 400 - scene_info["ball"][1]
                self.predict_X = scene_info["ball"][0] + self.predict_Y / m
                self.predict_X = int(self.predict_X)
                xxx = self.predict_X // 200
                if xxx % 2 == 1:
                    self.predict_X = 200 - self.predict_X % 200
                else:
                    self.predict_X = self.predict_X % 200
                self.predict_X = self.predict_X + random.randint(-5, 5)
                if scene_info["platform"][0] < (self.predict_X - 20) and my > 0:
                    command = "MOVE_RIGHT"
                elif scene_info["platform"][0] > (self.predict_X - 20) and my > 0:
                    command = "MOVE_LEFT"
                else:
                    command = "NONE"
            c
            else:
                command = "NONE"
                ##     ## mx > 0 and my < 0:  # RIGHT_UP
                ## if scene_info["ball"][1] > 200:
                ##     command = "MOVE_RIGHT"
                ## elif scene_info["platform"][0] > 80:
                ##     command = "MOVE_LEFT"
                ## elif scene_info["platform"][0] < 80:
                ##     command = "MOVE_RIGHT"
                ## else:
                ##     command = "NONE"
                ## elif mx < 0 and my < 0:  # LEFT_UP
                ##     if scene_info["ball"][1] > 200:
                ##         command = "MOVE_LEFT"
                ##     elif scene_info["platform"][0] > 80:
                ##         command = "MOVE_LEFT"
                ##     elif scene_info["platform"][0] < 80:
                ##         command = "MOVE_RIGHT"
                ##     else:
                ##         command = "NONE"

            if scene_info["platform"][1] - scene_info["ball"][1] < 10:
                command = "NONE"
            if scene_info["ball"][1] < 160:
                command = "NONE"
            self.last_x = scene_info["ball"][0]
            self.last_y = scene_info["ball"][1]

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
