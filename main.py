import pyautogui
import keyboard
import win32api, win32con
import time
import numpy as np

class App:
    def __init__(self):
        self.inBattle = False
        self.fleet = '1'

    def run(self):

        time.sleep(5)

        while keyboard.is_pressed('p') == False:

            # pyautogui.displayMousePosition()

            # CHOOSING A FLEET
            if not self.inBattle:
                self.selectFleet()
                self.freeRepair()

            # FIND-BUTTON EXISTS
            if pyautogui.pixel(1689, 98)[0] == 0 and self.inBattle == False:
                self.click(1654, 88)
                time.sleep(self.random(1.5, 2.5))

             # ALERT CHECK
            if pyautogui.locateOnScreen('alert.png', grayscale=True, confidence=0.8) != None:
                self.click(960, 666)
                print('FLEET NOT FOUND')

            if pyautogui.locateOnScreen('blitzAlert.png', grayscale=True, confidence=0.8) != None:
                self.click(1436, 187)
                print('BLITZ SKIPPED')

            # ATTACK
            if pyautogui.locateOnScreen('inBattle.png', grayscale=True, confidence=0.8) != None:

                self.inBattle = True
                print('FLEET IN BATTLE...')

            elif pyautogui.pixel(817, 1010)[0] == 232 and self.inBattle == False:

                self.inBattle = True
                self.click(817, 1010)
                print('FLEET IS ATTACKING')
                time.sleep(self.random(10, 20))

            elif not pyautogui.pixel(817, 1010)[0] == 232:
                self.inBattle = False

            time.sleep(0.8)

    def selectFleet(self):
        pyautogui.keyDown(self.fleet)
        time.sleep(self.random(0.1, 0.3))
        pyautogui.keyUp(self.fleet)
        print('FLEET SELECTED')
        time.sleep(self.random(0.1, 0.3))

    def freeRepair(self):
        if pyautogui.locateOnScreen('freeRepair.png', grayscale=True, confidence=0.8) != None:
            print('free repair')
            self.click(955, 924)
        else:
            print('not a free repair, skipping')
        time.sleep(self.random(0.2, 0.4))


    def click(self, x, y):
        pos = x, y
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(self.random(0.2, 0.4))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def random(self, x, y):
        result = np.random.uniform(x, y)
        return result

def initialize():
    app = App()
    app.run()


initialize()
