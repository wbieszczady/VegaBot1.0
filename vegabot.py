import tkinter
import customtkinter
from instructions import App
from tkinter import *
from threading import Thread
from keyboard import add_hotkey
from time import sleep, time

class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.RESOLUTIONS = ['1920x1080', '2560x1440']
        self.STYLES = ['Light', 'Dark']

        self.REPAIR = ['True', 'False']

        # window init
        self.geometry('700x800')
        self.resizable(False, False)
        self.title('VegaBot v1.2')
        self.iconbitmap('resources/appIcon.ico')

        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("green")

        #variables
        self.resolution = StringVar(self)
        self.resolution.set(self.RESOLUTIONS[0])

        self.style = StringVar(self)
        self.style.set(self.STYLES[1])

        self.repair = StringVar(self)
        self.repair.set(self.REPAIR[1])

        #widgets init
        self.font = 'Verdana'
        self.labels = []
        self.frames = []
        self.menus = []
        self.sliders = []
        self.switches = []
        self.boxes = []

        self.place()

        #controls
        self.isRunning = False
        self.time = time()
        self.status = 'Offline'

    def refresh(self):


        nSeconds = time() - self.time
        nSeconds = round(nSeconds)

        mm, ss = divmod(nSeconds, 60)
        hh, mm = divmod(mm, 60)

        self.labels[7].configure(text=f'{hh}h {mm}m {ss}s')

        #status
        match self.status:
            case 'Offline':
                self.labels[6].configure(text=self.status, text_color='red')
            case 'Seeking target...':
                self.labels[6].configure(text=self.status, text_color='orange')
            case 'Fleet is attacking...':
                self.labels[6].configure(text=self.status, text_color='orange')
            case 'Fleet repaired. (for free)':
                self.labels[6].configure(text=self.status, text_color='yellow')
            case 'In battle.':
                self.labels[6].configure(text=self.status, text_color='#de4d30')
            case 'Online':
                self.labels[6].configure(text=self.status, text_color='#0ed145')

        if self.isRunning:
            self.after(1000, lambda: self.refresh())
        else:
            self.status = 'Offline'
            self.labels[6].configure(text=self.status, text_color='red')

    def place(self):

        self.createFrame(20, 20, 660, 135) # General settings
        self.createLabel(self.frames[0], 260, 10, 'General settings', 18)
        self.createMenu(self.frames[0], 170, 60, 150, 35, 18, self.resolution, *self.RESOLUTIONS)
        self.createButton(self.frames[0], 350, 60, 150, 35, 'Toggle mode', 18)


        self.createFrame(20, 165, 660, 325)  #Commons settings
        self.createLabel(self.frames[1], 155, 10, 'Common settings', 18)

        self.createLabel(self.frames[1], 20, 60, 'Finding cooldown', 18)
        self.createSlider(self.frames[1], 200, 67)

        self.createLabel(self.frames[1], 20, 100, 'Force repair', 18)
        self.createSwitch(self.frames[1], 160, 105)

        self.createSubFrame(self.frames[1], 450, 0, 210, 325)

        self.createLabel(self.frames[2], 80, 10, 'Fleet', 18)

        self.createCheckbox(self.frames[2], '1', 55, 50)
        self.createCheckbox(self.frames[2], '2', 55, 85)
        self.createCheckbox(self.frames[2], '3', 55, 120)
        self.createCheckbox(self.frames[2], '4', 55, 155)
        self.createCheckbox(self.frames[2], '5', 55, 190)
        self.createCheckbox(self.frames[2], '6', 55, 225)
        self.createCheckbox(self.frames[2], '7', 55, 260)


        self.createFrame(20, 500, 660, 280) # Footer

        self.createLabel(self.frames[3], 300, 10, 'Status', 18)
        self.createLabel(self.frames[3], 20, 60, 'Offline', 18)
        self.labels[6].configure(text_color='red')

        self.createLabel(self.frames[3], 20, 90, '0h 0m 0s', 18)

    def submit(self):

        self.fleet = []

        for box in self.boxes:
            if box.get() != False:
                self.fleet.append(box.get())

        if not self.isRunning and len(self.fleet) > 0:

            var1 = self.resolution.get()
            var2 = self.fleet
            var3 = self.sliders[0].get()
            var4 = self.switches[0].get()

            self.isRunning = True
            self.app = App(self, var1, var2, var3, var4)

    def changeStyle(self):
        if self.style.get() == 'Dark':
            customtkinter.set_appearance_mode("Light")
            self.style.set(self.STYLES[0])
        else:
            customtkinter.set_appearance_mode("Dark")
            self.style.set(self.STYLES[1])

    def createLabel(self, master, x, y, text, fontsize):
        object = customtkinter.CTkLabel(master=master, text=text, font=(self.font, fontsize))
        object.place(x=x, y=y)
        self.labels.append(object)
    def createFrame(self, x, y, w, h):
        object = customtkinter.CTkFrame(master=self, width=w, height=h, corner_radius=10)
        object.place(x=x, y=y)
        self.frames.append(object)
    def createSubFrame(self, master, x, y, w, h):
        object = customtkinter.CTkFrame(master=master, width=w, height=h, corner_radius=0)
        object.place(x=x, y=y)
        self.frames.append(object)
    def createMenu(self, master, x, y, w, h, fontsize, variable, *variableOptions):
        object = customtkinter.CTkOptionMenu(master=master, variable=variable, values=variableOptions,width=w, height=h, corner_radius=0, dropdown_font=(self.font, fontsize), font=(self.font, fontsize))
        object.place(x=x, y=y)
        self.menus.append(object)
    def createButton(self, master, x, y, w, h, text, fontsize):
        object = customtkinter.CTkButton(master=master, width=w, height=h, text=text, corner_radius=0, font=(self.font, fontsize), command=lambda: self.changeStyle())
        object.place(x=x, y=y)

    def createSlider(self, master, x, y):
        object = customtkinter.CTkSlider(master=master, from_=1, to=11, orientation='horizontal', number_of_steps=10)
        object.place(x=x, y=y)
        self.sliders.append(object)
    def createSwitch(self, master, x, y):
        object = customtkinter.CTkSwitch(master=master, onvalue=True, offvalue=False, text='')
        object.place(x=x, y=y)
        self.switches.append(object)
    def createCheckbox(self, master, value, x, y):
        object = customtkinter.CTkCheckBox(master=master, onvalue=value, offvalue=False, text=value, font=(self.font, 18), checkbox_width=100)
        object.place(x=x, y=y)
        self.boxes.append(object)

    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        add_hotkey('backspace', lambda: self.stop())
        add_hotkey('space', lambda: self.submit())
        self.mainloop()

    def stop(self):
        if self.isRunning:
            self.app.exit()
            self.isRunning = False

    def onClose(self):
        self.stop()
        self.destroy()

if __name__ == '__main__':
    gui = Gui()
    gui.run()