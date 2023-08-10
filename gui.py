from main import App
from tkinter import *
from threading import *
import sys
import keyboard
import time

class Gui:
    def __init__(self):

        self.FLEETS = ['1', '2', '3', '4', '5', '6', '7']
        self.REPAIR = ['True', 'False']
        self.COOLDOWNS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

        # window init
        self.root = Tk()
        self.root.geometry('600x800')
        self.root.configure(bg='#353535')
        self.root.resizable(False, False)
        self.root.title('VegaBot v1.0')
        self.root.iconbitmap('resources/appIcon.ico')

        #variables
        self.fleet = StringVar(self.root)
        self.fleet.set(self.FLEETS[0])

        self.repair = StringVar(self.root)
        self.repair.set(self.REPAIR[1])

        self.cooldown = StringVar(self.root)
        self.cooldown.set(self.COOLDOWNS[3])

        #widgets init

        self.fleetLabel = Label(master=self.root, text='Select a fleet', bg='#353535', fg='white', font=('Arial', 18))
        self.fleetEntry = OptionMenu(self.root, self.fleet, *self.FLEETS)

        self.repairLabel = Label(master=self.root, text='Force repair', bg='#353535', fg='white', font=('Arial', 18))
        self.repairEntry = OptionMenu(self.root, self.repair, *self.REPAIR)

        self.cooldownLabel = Label(master=self.root, text='Finding cooldown', bg='#353535', fg='white', font=('Arial', 18))
        self.cooldownEntry = OptionMenu(self.root, self.cooldown, *self.COOLDOWNS)


        self.statusFrame = Frame(master=self.root, bg='#252525', width=560, height=315)
        self.statusLabel = Label(master=self.root, text='Status:', bg='#252525', fg='white', font=('Arial', 25))

        self.updateLabel = Label(master=self.root, text='Offline', bg='#252525', fg='red', font=('Arial', 25))

        self.timeLabel = Label(master=self.root, text=f'00:00:00', bg='#252525', fg='white', font=('Arial', 25))

        #widgets config
        self.fleetEntry.configure(bg='#252525', fg='white', width=8, height=1, font=('Arial', 25))
        self.fleetEntry["menu"].configure(bg='#252525', fg='white')
        self.fleetEntry["highlightthickness"]=0

        self.repairEntry.configure(bg='#252525', fg='white', width=8, height=1, font=('Arial', 25))
        self.repairEntry["menu"].configure(bg='#252525', fg='white')
        self.repairEntry["highlightthickness"] = 0

        self.cooldownEntry.configure(bg='#252525', fg='white', width=8, height=1, font=('Arial', 25))
        self.cooldownEntry["menu"].configure(bg='#252525', fg='white')
        self.cooldownEntry["highlightthickness"] = 0

        #controls
        self.isRunning = False

    def submit(self):

        self.isRunning = True

        self.app = App(self, self.fleet.get(), bool(self.repair.get()), int(self.cooldown.get()))

    def place(self):
        self.fleetLabel.place(x=10, y=35)
        self.fleetEntry.place(x=240, y=30)
        self.repairLabel.place(x=10, y=120)
        self.repairEntry.place(x=240, y=115)
        self.cooldownLabel.place(x=10, y=200)
        self.cooldownEntry.place(x=240, y=195)

        self.statusFrame.place(x=20, y=450)
        self.statusLabel.place(x=40, y=470)
        self.updateLabel.place(x=40, y=530)

        self.timeLabel.place(x=435, y=710)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        keyboard.add_hotkey('p', lambda: self.stop())
        keyboard.add_hotkey('o', lambda: self.submit())
        self.root.mainloop()

    def stop(self):
        if self.isRunning:
            self.app.isRunning = False

    def onClose(self):
        if self.isRunning:
            self.app.isRunning = False
        time.sleep(3)
        self.root.destroy()

if __name__ == '__main__':
    gui = Gui()
    gui.place()
    gui.run()