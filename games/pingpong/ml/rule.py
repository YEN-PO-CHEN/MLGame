"""
The template of the script for the machine learning process in game pingpong
"""
import random
import math


def predict(a):
    b = 195
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
        self.predict_X_1P = 0
        self.predict_Y_1P = 0
        self.predict_X_1P_L = 0
        self.predict_X_2P = 0
        self.predict_X_2P_L = 0
        self.predict_Y_2P = 0

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """

        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            if random.randint(0, 2) == 1:
                return "SERVE_TO_LEFT"
            else:
                return "SERVE_TO_RIGHT"
        else:
            command = "NONE"

            m = scene_info["ball_speed"][0] / scene_info["ball_speed"][1]  # left is 1 right is -1

            if self.side == "1P":
                if scene_info["ball"][1] > 265:  # 下面
                    if scene_info["ball_speed"][1] < 0:  # 往上(反彈)
                        self.predict_Y_1P = scene_info["ball"][1] - 265 + 150
                        self.predict_X_1P = scene_info["ball"][0] - self.predict_Y_1P * m
                        self.predict_X_1P = predict(self.predict_X_1P)
                    else:  # 往下(直接判斷)
                        self.predict_Y_1P = 415 - scene_info["ball"][1]
                        self.predict_X_1P = scene_info["ball"][0] + self.predict_Y_1P * m
                        self.predict_X_1P = predict(self.predict_X_1P)
                else:   # 上面
                    if scene_info["ball_speed"][1] < 0:  # 往上(置中)
                        if scene_info["platform_1P"][0] > 81:
                            return "MOVE_LEFT"
                        elif scene_info["platform_1P"][0] < 79:
                            return "MOVE_RIGHT"
                        else:
                            return "NONE"
                    else:   # 往下(打側板)
                        self.predict_Y_1P = 250 - scene_info["ball"][1]
                        self.predict_X_1P_L = scene_info["ball"][0] + self.predict_Y_1P * m - 165 * m
                        self.predict_X_1P_L = predict(self.predict_X_1P_L)
                        self.predict_Y_1P = 415 - scene_info["ball"][1]
                        self.predict_X_1P = scene_info["ball"][0] + self.predict_Y_1P * m
                        self.predict_X_1P = predict(self.predict_X_1P)
                        self.predict_X_1P = (self.predict_X_1P + self.predict_X_1P_L)//2
                if scene_info["platform_1P"][0] + 22 < self.predict_X_1P:
                    return "MOVE_RIGHT"
                elif scene_info["platform_1P"][0] + 18 > self.predict_X_1P:
                    return "MOVE_LEFT"
                else:
                    return "NONE"
            elif self.side == "2P":
                if scene_info["ball"][1] < 235: # 上面
                    if scene_info["ball_speed"][1] > 0:  # 往下跑
                        self.predict_Y_2P = 235 - scene_info["ball"][1] + 150
                        self.predict_X_2P = scene_info["ball"][0] + self.predict_Y_2P * m
                        self.predict_X_2P = predict(self.predict_X_2P)
                    else:  # 往上跑
                        self.predict_Y_2P = scene_info["ball"][1] - 80
                        self.predict_X_2P = scene_info["ball"][0] - self.predict_Y_2P * m
                        self.predict_X_2P = predict(self.predict_X_2P)
                else:  # 下面
                    if scene_info["ball_speed"][1] > 0:  # 往下跑
                        if scene_info["platform_2P"][0] > 81:
                            return "MOVE_LEFT"
                        elif scene_info["platform_2P"][0] < 79:
                            return "MOVE_RIGHT"
                        else:
                            return "NONE"
                    else:
                        self.predict_Y_2P = scene_info["ball"][1] - 250
                        self.predict_X_2P_L = scene_info["ball"][0] - self.predict_Y_1P * m + 165 * m
                        self.predict_X_2P_L = predict(self.predict_X_2P_L)
                        self.predict_Y_2P = scene_info["ball"][1] - 80
                        self.predict_X_2P = scene_info["ball"][0] - self.predict_Y_2P * m
                        self.predict_X_2P = predict(self.predict_X_2P)
                        self.predict_X_2P = (self.predict_X_2P + self.predict_X_2P_L) // 2
                if scene_info["platform_2P"][0] + 22 < self.predict_X_2P:
                    return "MOVE_RIGHT"
                elif scene_info["platform_2P"][0] + 18 > self.predict_X_2P:
                    return "MOVE_LEFT"
                else:
                    return "NONE"

            return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
