import pyautogui
import win32api, win32con
from time import sleep, time
from numpy import random, array
from threading import Thread

class App:
    def __init__(self, gui, resolution, fleet, findCooldown, forceRepair):

        self.gui = gui
        self.resolution = resolution
        self.fleet = fleet
        self.findCooldown = findCooldown
        self.forceRepair = forceRepair

        self.isRunning = True

        match self.resolution:
            case '1920x1080':
                self.pos = {'repair': [(955, 924)],
                            'blitz': [(1436, 187)],
                            }
                self.images = {'attack': 'resources/1920x1080/attack.png',
                               'repair': 'resources/1920x1080/freeRepair.png',
                               'inBattle': 'resources/1920x1080/inBattle.png',
                               'alert': 'resources/1920x1080/alert.png',
                               'blitz': 'resources/1920x1080/blitzAlert.png',
                               'game': 'resources/1920x1080/game.png',
                               'find': 'resources/1920x1080/findButton.png',
                               'join': 'resources/1920x1080/join.png'
                               }

            case '2560x1440':
                self.pos = {'repair': [(955, 924)],
                            'blitz': [(1915, 240)],
                            }

                self.images = {'attack': 'resources/2560x1440/attack.png',
                               'repair': 'resources/2560x1440/freeRepair.png',
                               'inBattle': 'resources/2560x1440/inBattle.png',
                               'alert': 'resources/2560x1440/alert.png',
                               'blitz': 'resources/2560x1440/blitzAlert.png',
                               'game': 'resources/2560x1440/game.png',
                               'find': 'resources/2560x1440/findButton.png',
                               'join': 'resources/2560x1440/join.png'
                               }

        self.mainThread = Thread(target=self.run)
        self.mainThread.start()


    def run(self):

        self.gui.status = 'Online'
        self.gui.time = time()
        self.gui.refresh()

        if self.locate(self.images['game']) and self.locate(self.images['find']):
            find = self.locate(self.images['find'])
            self.gui.writeLogFile('Script has started!')
        else:
            self.gui.writeLogFile('Couldnt find game on screen!')
            self.exit()


        while self.isRunning: #main loop

            inbattle = self.locate(self.images['inBattle'])

            if inbattle == None:
                inbattle = []


            if len(self.fleet) != len(inbattle):

                self.checkForEvents()

                for number in self.fleet:
                    if self.locate(self.images['game']) != None:

                        self.selectFleet(number)

                        sleep(self.random_value(0.4, 0.8))

                        skip = self.locate(self.images['join'])

                        if skip == None:

                            self.freeRepair()

                            self.gui.status = 'Seeking target...'
                            self.click(find)

                            sleep(self.random_value(0.4, 0.8))

                            attack = self.locate(self.images['attack'])
                            if attack != None:
                                self.gui.status = 'Fleet is attacking...'
                                self.click(attack)
                            sleep(self.random_value(0.4, 0.8))

                    else:
                        self.gui.status = 'Online'

            else:
                self.gui.status = 'In battle.'

            #check cooldown
            sleep(self.findCooldown/2)


    def selectFleet(self, fleet):
        pyautogui.keyDown(fleet)
        sleep(self.random_value(0.1, 0.3))
        pyautogui.keyUp(fleet)
        sleep(self.random_value(0.1, 0.3))

    def checkForEvents(self):

        alert = self.locate(self.images['alert'])
        blitz = self.locate(self.images['blitz'])

        if alert != None:
            self.click(alert)

        if blitz != None:
            self.click(self.pos['blitz'])

    def freeRepair(self):

        repair = self.locate(self.images['repair'], True, 0.9)
        if repair != None:
            self.gui.status = 'Fleet repaired.'
            self.click(repair)
        elif self.forceRepair:
            self.click(self.pos['repair'])

        sleep(self.random_value(0.3, 0.5))

    def locate(self, img, grays=True, conf=0.75):

        located = []
        threshold = 15
        for box in pyautogui.locateAllOnScreen(img, grayscale=grays, confidence=conf):

            passed = True

            if len(located) == 0:

                located.append(box)

            else:

                for loc in located:

                    leftDiff = abs(box.left - loc.left)
                    topDiff = abs(box.top - loc.top)

                    if topDiff > threshold:
                        passed = True

                    else:
                        passed = False
                        break

                if passed:
                    located.append(box)

        else:
            pass

        if len(located) == 0:
            return None
        else:
            final = []
            for loc in located:
                pos = pyautogui.center(loc)
                final.append((pos[0], pos[1]))

            return final

    def click(self, tuple):

        baseX = tuple[0][0]
        baseY = tuple[0][1]

        pos = random.randint(baseX-10, baseX+10), random.randint(baseY-10, baseY+10)

        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        sleep(self.random_value(0.2, 0.4))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def random_value(self, x, y):
        result = random.uniform(x, y)
        return result


    def exit(self):
        self.gui.status = 'Offline'
        self.isRunning = False
        self.gui.isRunning = False