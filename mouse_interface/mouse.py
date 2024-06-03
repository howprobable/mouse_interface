from typing import Union, Optional
import pyautogui
import math
from py_helpers import Point
from py_helpers import Rectangle

import numpy as np


class mouseIF:
    ### standards
    def __init__(
        self,
    ):
        self.offset = Point(0, 0)
        self.window = None

    def __del__(self):
        pass

    ###public
    def set_offset(self, offset: Point):
        self.offset: Point = offset

    def set_window(self, window: Rectangle):
        self.window: Rectangle = window

    def go_to_delta(self, d: Point, speed: int = 1000) -> None:
        self.go_to(pos=self.get_position() + d, speed=speed)

    def go_to(self, pos: Point, speed: int = 1000) -> None:
        if self.window:
            pos = self.window.getEdgeIfOutside(p=pos)

        start_pos = pyautogui.position()
        distance = math.sqrt(
            (self.offset.x + pos.x - start_pos.x) ** 2
            + (self.offset.y + pos.y - start_pos.y) ** 2
        )
        duration = distance / speed

        pyautogui.moveTo(
            x=self.offset.x + pos.x, y=self.offset.y + pos.y, duration=duration
        )

    def click(self, pos: Optional[Point], speed: int = 1000) -> None:
        if pos:
            self.go_to(
                pos=pos,
                speed=speed,
            )

        pyautogui.click()

    def get_position(
        self,
    ) -> Point:
        pos = pyautogui.position()

        return Point(x=pos.x - self.offset.x, y=pos.y - self.offset.y)

    ###private


def human_like_mouse_move(end: Point, duration: int = 2):
    start_pos = pyautogui.position()
    start = Point(x=start_pos.x, y=start_pos.y)

    # Generate time steps
    t: np.ndarray = np.linspace(0, 1, num=100)

    # Generate random control points for Bezier curve
    control_points: np.ndarray = np.array(
        [
            start,
            start + (end + (start * (-1))) * np.random.rand(),
            end + (end + (start * (-1))) * (-1) * np.random.rand(),
            end,
        ]
    )

    # Calculate the Bezier curve points
    bezier_curve = (
        (1 - t) ** 3 * control_points[0]
        + 3 * (1 - t) ** 2 * t * control_points[1]
        + 3 * (1 - t) * t**2 * control_points[2]
        + t**3 * control_points[3]
    )

    # Move mouse
    for point in bezier_curve:
        pyautogui.moveTo(point[0], point[1], duration=duration / len(bezier_curve))


if __name__ == "__main__":
    human_like_mouse_move(end=Point(2, 2))
