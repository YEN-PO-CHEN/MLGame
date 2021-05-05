"""
The template of the script for the machine learning process in game pingpong
"""
import random
import math


def predict(a, b):
    if (a // b) % 2 == 1:
        return b - a % b
    else:
        return a % b


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
            if random.randint(0, 2) == 1:
                print("SERVE_TO_LEFT")
                return "SERVE_TO_LEFT"
            else:
                print("SERVE_TO_RIGHT")
                return "SERVE_TO_RIGHT"
        else:
            command = "NONE"
            if scene_info["ball_speed"][0] == 0:
                m = 1
            else:
                m = scene_info["ball_speed"][1] / scene_info["ball_speed"][0]  # left is 1 right is -1

            if scene_info["ball_speed"][1] > 0:  # Down
                self.predict_Y_1P = 415 - scene_info["ball"][1]
                self.predict_X_1P = scene_info["ball"][0] + self.predict_Y_1P * m
                self.predict_X_1P = predict(self.predict_X_1P, 195)
                self.predict_X_2P = self.predict_X_1P + 335 * m
                self.predict_X_2P = predict(self.predict_X_2P, 195)
            else:
                self.predict_Y_2P = scene_info["ball"][1] - 80
                self.predict_X_2P = scene_info["ball"][0] - self.predict_Y_2P * m
                self.predict_X_2P = predict(self.predict_X_2P, 195)
                self.predict_X_1P = self.predict_X_2P - 335 * m
                self.predict_X_1P = predict(self.predict_X_1P, 195)
            self.last_y = scene_info["ball"][1]

            if self.side == "1P":
                if scene_info["ball"][1] > 265 and scene_info["ball_speed"][1] < 0:
                    self.predict_Y_1P = scene_info["ball"][1] - 265 + 150
                    self.predict_X_1P = scene_info["ball"][0] - self.predict_Y_1P * m
                    self.predict_X_1P = predict(self.predict_X_1P, 195)
                    # print("1p", self.predict_X_1P,  scene_info["platform_1P"][0], scene_info["ball"][1], scene_info["ball"][0], m)
                # print("1p", scene_info["ball"][1], scene_info["ball"][0], self.predict_X_1P, m)
                if scene_info["platform_1P"][0] + 23 < self.predict_X_1P:
                    return "MOVE_RIGHT"
                elif scene_info["platform_1P"][0] + 17 > self.predict_X_1P:
                    return "MOVE_LEFT"
                else:
                    return "NONE"

            if self.side == "2P":
                if scene_info["ball"][1] < 240 and scene_info["ball_speed"][1] > 0:
                    self.predict_Y_2P = 240 - scene_info["ball"][1] + 150
                    self.predict_X_2P = scene_info["ball"][0] + self.predict_Y_2P * m
                    self.predict_X_2P = predict(self.predict_X_2P, 195)
                    # print("2p", self.predict_X_2P,  scene_info["platform_2P"][0], scene_info["ball"][1], scene_info["ball"][0], m)
                # print("2p", scene_info["ball"][0], self.predict_X_2P)
                if scene_info["platform_2P"][0] + 23 < self.predict_X_2P:
                    return "MOVE_RIGHT"
                elif scene_info["platform_2P"][0] + 17 > self.predict_X_2P:
                    return "MOVE_LEFT"
                else:
                    return "NONE"
            return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
