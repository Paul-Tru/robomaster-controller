import cv2

import vars

class PersonInfo:

    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)


def on_detect_person(person_info):
    number = len(person_info)
    vars.persons.clear()
    print(f"Detected {number} person(s).")  # Debug: Show how many persons are detected
    for i in range(0, number):
        x, y, w, h = person_info[i]
        vars.persons.append(PersonInfo(x, y, w, h))
