"""
The template of the script for the machine learning process in game pingpong
"""
import random
import math


class MLPlay:
    def __init__(self, side):
        """
        Constructor
        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.last_y = 0
        self.predict_X_1P = 0
        self.predict_Y_1P = 0
        self.predict_X_2P = 0
        self.predict_Y_2P = 0

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """

        if scene_info["status"] != "GAME_ALIVE":

            print(scene_info["ball_speed"][1])
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
            command = "NONE"
            m = scene_info["ball_speed"][1] / scene_info["ball_speed"][0]  # left is 1 right is -1
            if scene_info["ball_speed"][1] > 0:  # Down
                self.predict_Y_1P = 415 - scene_info["ball"][1]
                self.predict_X_1P = scene_info["ball"][0] + self.predict_Y_1P * m
                if (self.predict_X_1P//195) % 2 == 1:
                    self.predict_X_1P = 195 - self.predict_X_1P % 195
                else:
                    self.predict_X_1P = self.predict_X_1P % 195

                self.predict_X_2P = self.predict_X_1P + 335 * m

                if (self.predict_X_2P//195) % 2 == 1:
                    self.predict_X_2P = 195 - self.predict_X_2P % 195
                else:
                    self.predict_X_2P = self.predict_X_2P % 195
            else:
                self.predict_Y_2P = scene_info["ball"][1] - 80
                self.predict_X_2P = scene_info["ball"][0] - self.predict_Y_2P * m
                if (self.predict_X_2P//195) % 2 == 1:
                    self.predict_X_2P = 195 - self.predict_X_2P % 195
                else:
                    self.predict_X_2P = self.predict_X_2P % 195

                self.predict_X_1P = self.predict_X_2P - 335 * m

                if (self.predict_X_1P // 195) % 2 == 1:
                    self.predict_X_1P = 195 - self.predict_X_1P % 195
                else:
                    self.predict_X_1P = self.predict_X_1P % 195

            self.last_y = scene_info["ball"][1]
            if self.side == "1P":
                if scene_info["ball"][1] > 410:
                    return "NONE"
                if scene_info["platform_1P"][0] + 25 < self.predict_X_1P:
                    return "MOVE_RIGHT"
                elif scene_info["platform_1P"][0] + 15 > self.predict_X_1P:
                    return "MOVE_LEFT"
                else:
                    return "NONE"

            if self.side == "2P":
                if scene_info["ball"][1] < 90:
                    return "NONE"
                if scene_info["platform_2P"][0] + 25 < self.predict_X_2P:
                    return "MOVE_RIGHT"
                elif scene_info["platform_2P"][0] + 15 > self.predict_X_2P:
                    return "MOVE_LEFT"
                else:
                    return "NONE"
            return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
