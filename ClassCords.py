import pyautogui as pg


class ClassCords:

    def return_cords():
        x,y = pg.position()
        return x,y
