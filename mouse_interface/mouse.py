from typing import  Optional
import pyautogui
import subprocess
from py_helpers import Point
from py_helpers import Rectangle

import numpy as np

import time

pyautogui.MINIMUM_DURATION = 0.001
pyautogui.MINIMUM_SLEEP = 0.001
pyautogui.PAUSE = 0.001


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

    def go_to_delta(self, d: Point, duration: float = 1.0, natural: bool = True) -> None:
        self.go_to(pos=self.get_position() + d, duration=duration, natural=natural)

    def go_to(self, pos: Point, duration: float = 1.0, natural: bool = True) -> None:
        if self.window:
            pos : Point = self.window.getEdgeIfOutside(p=pos)

        if natural:
            self.human_like_mouse_move(pos=pos, duration=duration)
        else:
            pyautogui.moveTo(
                x=self.offset.x + pos.x, y=self.offset.y + pos.y, duration=duration
            )

    def click(self, pos: Optional[Point], duration: float = 1.0, natural:bool = True) -> None:
        if pos:
            self.go_to(
                pos=pos,
                duration=duration,
                natural=natural
            )

        pyautogui.click()

    def get_position(
        self,
    ) -> Point:
        pos = pyautogui.position()

        return Point(x=pos.x - self.offset.x, y=pos.y - self.offset.y)

    def human_like_mouse_move(self, pos: Point, duration: float = 1.0):
        start_pos = pyautogui.position()
        start = Point(x=start_pos.x, y=start_pos.y)
        t: np.ndarray = np.linspace(0, 1, num=25)

        control_points: np.ndarray = np.array(
            [
                start,
                start + (pos + (start * (-1))) * np.random.rand(),
                pos + (pos + (start * (-1))) * (-1) * np.random.rand(),
                pos,
            ]
        )
        bezier_curve = (
            (1 - t) ** 3 * control_points[0]
            + 3 * (1 - t) ** 2 * t * control_points[1]
            + 3 * (1 - t) * t**2 * control_points[2]
            + t**3 * control_points[3]
        )

        start_time = time.time() 
        for point, i in zip(bezier_curve, range(len(bezier_curve))):
            pyautogui.moveTo(point[0], point[1])
            now = time.time()

            wait_to = start_time + i*(duration/len(bezier_curve))
            if now < wait_to: 
                pyautogui.sleep(wait_to - now)

    def reset_mouse_size(self): 
        self.set_mouse_size(32)
            
    def set_mouse_size(self, size: int):
        ps: str = f"""
$CSharpSig = @'
[DllImport("user32.dll", EntryPoint = "SystemParametersInfo")]
public static extern bool SystemParametersInfo(
                  uint uiAction,
                  uint uiParam,
                  uint pvParam,
                  uint fWinIni);
'@
$CursorRefresh = Add-Type -MemberDefinition $CSharpSig -Name WinAPICall -Namespace SystemParamInfo -PassThru
$CursorRefresh::SystemParametersInfo(0x0057,0,$null,0);
$CursorRefresh::SystemParametersInfo(0x2029, 0, {size}, 0x01);
"""
        subprocess.run(["powershell", "-Command", ps], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ###private

if __name__ == "__main__":
    mouseIF = mouseIF()

    pos = mouseIF.get_position()

    print("Making mouse bigger...")
    mouseIF.set_mouse_size(128)

    time.sleep(1)
    
    print("Moving mouse to 100, 100...")
    mouseIF.go_to(pos=Point(100, 100), duration=1.0)

    time.sleep(1)
    
    print("Going back to original position...")
    mouseIF.go_to(pos=pos, duration=1.0)

    time.sleep(1)

    print("Making mouse smaller...")
    mouseIF.set_mouse_size(32)

