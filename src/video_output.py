import cv2

class VideoOutput:
    def __init__(self, name: str, frame, x1: int, y1: int, x2: int, y2: int):
        self._name = name
        self._frame = frame
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self.chooseOption()

    def chooseOption(self):
        if self._name == "unknown":
            self._draw_box(self._frame, self._x1, self._y1, self._x2, self._y2, "unknown")
        else:
            self._draw_box(self._frame, self._x1, self._y1, self._x2, self._y2, self._name)

    def _draw_box(self, frame, x1: int, y1: int, x2: int, y2: int, label: str):
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, label, (x1, y2 + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
