from typing import Union, Optional
import pyautogui
import math
from py_helpers import Point
from py_helpers import Rectangle


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
