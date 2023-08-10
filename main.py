import random

import pyautogui
import win32api, win32con
import time
import numpy as np
import sys, os
from tkinter import *
from threading import *
from pynput import keyboard

class App:
    def __init__(self, gui, fleet, forceRepair, findCooldown):

        self.gui = gui

        self.inBattle = False
        self.fleet = fleet
        self.forceRepair = forceRepair
        self.findCooldown = findCooldown
        self.status = 'Offline'
        self.count = 0

        self.isRunning = True

        self.mainThread = Thread(target=self.run)
        self.mainThread.start()

        self.updateThread = Thread(target=self.update)
        self.updateThread.start()


        #TODO make monitor

        # self.obsThread = Thread(target=self.monitor)
        # self.obsThread.start()


    def run(self):

        if self.locate('resources/findButton.png'):

            self.selectFleet()
            self.freeRepair()

            while self.isRunning:
                #pyautogui.displayMousePosition()

                self.checkForEvents()

                if not self.locate('resources/fleet.png') and not self.locate('resources/inBattle.png'):
                    self.selectFleet()
                    self.freeRepair()

                if self.locate('resources/findButton.png') and not self.locate('resources/inBattle.png'):
                    self.click(1654, 88)
                    self.status = 'Seeking target...'
                    time.sleep(self.random(1.0, 1.4))

                if self.locate('resources/attack.png') and not self.locate('resources/inBattle.png'):
                    self.click(817, 1010)
                    self.status = 'Fleet is attacking...'
                    time.sleep(self.random(self.findCooldown+0.1, self.findCooldown+0.5))

                if self.locate('resources/inBattle.png'):
                    self.status = 'In battle.'



                time.sleep(self.random(0.3, 0.6))

        else:
            self.isRunning = False

    def monitor(self):

        cnt = 0

        while self.isRunning:

            cnt = time.time()

            if self.locate('resources/alert.png') != None:
                self.visuals['alert'] = self.locate('resources/alert.png')
            else:
                self.visuals['alert'] = False

            if self.locate('resources/findButton.png') != None:
                self.visuals['find'] = self.locate('resources/findButton.png')
            else:
                self.visuals['find'] = False

            if self.locate('resources/inBattle.png') != None:
                self.visuals['join'] = self.locate('resources/inBattle.png')
            else:
                self.visuals['join'] = False

            if self.locate('resources/attack.png') != None:
                self.visuals['attack'] = self.locate('resources/attack.png')
            else:
                self.visuals['attack'] = False

            if self.locate('resources/freeRepair.png') != None:
                self.visuals['repair'] = self.locate('resources/freeRepair.png')
            else:
                self.visuals['repair'] = False

            new = time.time() - cnt


            print(self.visuals)
            print(new)

        print('monitor stopped')
        self.exit()

    def update(self):

        bSeconds = time.time()

        while self.isRunning:

            #TODO get this fucking thing to match case

            if self.status == 'Offline':
                self.gui.updateLabel.configure(text=self.status, fg='red')
            if self.status == 'Seeking target...':
                self.gui.updateLabel.configure(text=self.status, fg='orange')
            if self.status == 'Fleet is attacking...':
                self.gui.updateLabel.configure(text=self.status, fg='orange')
            if self.status == 'Fleet repaired. (for free)':
                self.gui.updateLabel.configure(text=self.status, fg='yellow')
            if self.status == 'In battle.':
                self.gui.updateLabel.configure(text=self.status, fg='#de4d30')

            nSeconds = time.time() - bSeconds
            nSeconds = round(nSeconds)

            mm, ss = divmod(nSeconds, 60)
            hh, mm = divmod(mm, 60)

            self.gui.timeLabel.configure(text=f'{hh}:{mm}:{ss}')


        self.status = 'Offline'
        self.gui.updateLabel.configure(text=self.status, fg='red')


    def selectFleet(self):
        pyautogui.keyDown(self.fleet)
        time.sleep(self.random(0.1, 0.3))
        pyautogui.keyUp(self.fleet)
        time.sleep(self.random(0.1, 0.3))

    def checkForEvents(self):

        if self.locate('resources/alert.png') != None:
            self.click(960, 666)
            self.status = 'Fleet not found.'

        if self.locate('resources/blitzAlert.png') != None:
            self.click(1436, 187)
            self.status = 'Blitz skipped.'

    def freeRepair(self):
        if self.locate('resources/freeRepair.png', True, 0.9) != None:
            self.status = 'Fleet repaired. (for free)'
            self.click(955, 924)

        time.sleep(self.random(0.2, 0.4))

    def getStatus(self):
        return self.status

    def locate(self, img, grays=True, conf=0.8):
        return pyautogui.locateOnScreen(img, grayscale=grays, confidence=conf)


    def click(self, x, y):

        pos = random.randint(x-10, x+10), random.randint(y-10, y+10)

        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(self.random(0.2, 0.4))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def random(self, x, y):
        result = np.random.uniform(x, y)
        return result


    def exit(self):
        print('SHUTTING DOWN')

        self.status = 'Offline'
        time.sleep(1)
        self.isRunning = False

