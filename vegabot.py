import datetime
import customtkinter
from instructions import App
from threading import Thread
from keyboard import add_hotkey
import os
import time

class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.RESOLUTIONS = ['1920x1080', '2560x1440']
        self.STYLES = ['Light', 'Dark']
        self.SIZES = ['Small', 'Big']

        self.REPAIR = ['True', 'False']
        self.DEV = ['True', 'False']


        # window init
        self.geometry('700x800')
        self.resizable(False, False)
        self.title('VegaBot v1.3')
        self.iconbitmap('resources/appIcon.ico')

        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("green")

        #variables
        self.resolution = customtkinter.StringVar(self)
        self.resolution.set(self.RESOLUTIONS[0])

        self.style = customtkinter.StringVar(self)
        self.style.set(self.STYLES[1])

        self.repair = customtkinter.StringVar(self)
        self.repair.set(self.REPAIR[1])

        self.dev = customtkinter.StringVar(self)
        self.dev.set(self.DEV[1])

        self.msize = customtkinter.StringVar(self)
        self.msize.set(self.SIZES[1])

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
        self.time = time.time()
        self.status = 'Offline'

        self.createLogFile()


    def refresh(self):

        nSeconds = time.time() - self.time
        nSeconds = round(nSeconds)

        mm, ss = divmod(nSeconds, 60)
        hh, mm = divmod(mm, 60)

        self.labels[9].configure(text=f'{hh}h {mm}m {ss}s')

        self.timer = f'{hh}h {mm}m {ss}s'

        #status
        match self.status:
            case 'Offline':
                self.labels[8].configure(text=self.status, text_color='red')
            case 'Seeking target...':
                self.labels[8].configure(text=self.status, text_color='orange')
            case 'Fleet is attacking...':
                self.labels[8].configure(text=self.status, text_color='orange')
            case 'Fleet repaired.':
                self.labels[8].configure(text=self.status, text_color='yellow')
            case 'In battle.':
                self.labels[8].configure(text=self.status, text_color='#de4d30')
            case 'Online':
                self.labels[8].configure(text=self.status, text_color='#0ed145')

        if self.isRunning:
            self.after(int(self.sliders[1].get()), lambda: self.refresh())
        else:
            self.status = 'Offline'
            self.labels[8].configure(text=self.status, text_color='red')


    def place(self):

        self.createFrame(20, 20, 660, 135) # General settings
        self.createLabel(self.frames[0], 260, 10, 'General settings', 18)
        self.createMenu(self.frames[0], 95, 60, 150, 35, 18, self.resolution, *self.RESOLUTIONS)
        self.createButton(self.frames[0], 255, 60, 150, 35, 'Toggle mode', 18, lambda: self.changeStyle())
        self.createButton(self.frames[0], 415, 60, 150, 35, 'Toggle size', 18, lambda:self.changeSize())

        self.createFrame(20, 165, 660, 325)  #Commons settings
        self.createLabel(self.frames[1], 155, 10, 'Common settings', 18)

        self.createLabel(self.frames[1], 20, 60, 'Finding cooldown', 18)
        self.createSlider(self.frames[1], 200, 67, 1, 11, 10)
        self.sliders[0].set(7)

        self.createLabel(self.frames[1], 20, 100, 'Refresh cooldown', 18)
        self.createSlider(self.frames[1], 200, 105, 500, 5000, 100)
        self.sliders[1].set(2000)

        self.createLabel(self.frames[1], 20, 180, 'Force repair', 18)
        self.createSwitch(self.frames[1], 160, 184)

        self.createLabel(self.frames[1], 20, 220, 'Debug mode', 18)
        self.createSwitch(self.frames[1], 160, 225, lambda: self.changeDev())

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

        self.createSubFrame(self.frames[3], 0, 0, 200, 280)

        self.createLabel(self.frames[4], 65, 10, 'Status', 18)
        self.createLabel(self.frames[4], 15, 210, 'Offline', 18)
        self.labels[8].configure(text_color='red')

        self.createLabel(self.frames[4], 15, 240, '0h 0m 0s', 18)
        self.createCon(self.frames[3], 210, 0, 420, 270)

        self.createLabel(self.frames[1], 20, 260, 'Remember to turn on AI mode...', 13)


    def createLogFile(self):

        path = './logs'
        self.rowCount = 1

        if not os.path.exists(path):
            os.mkdir(path)
        else:
            pass

        self.logFile = f'logs/{time.strftime("%Y_%m_%d")}-{time.strftime("%H%M%S")}.txt'
        self.writeLogFile('Console is online.')

    def writeLogFile(self, info):

        msg = f'[{time.strftime("%H:%M:%S")}] {info}'


        with open(self.logFile, 'a') as file:

            file.write(f'{msg}\n')

            if self.dev.get() == 'True':
                self.createLabel(self.frames[5], 0, 0, msg, 18, self.rowCount)
                self.rowCount += 1

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

        elif self.isRunning and len(self.fleet) > 0:
            self.writeLogFile('Script is already running!')
        elif not self.isRunning and len(self.fleet) == 0:
            self.writeLogFile('You didnt choose any fleet!')

    def changeStyle(self):
        if self.style.get() == 'Dark':
            customtkinter.set_appearance_mode("Light")
            self.style.set(self.STYLES[0])
        else:
            customtkinter.set_appearance_mode("Dark")
            self.style.set(self.STYLES[1])

    def changeDev(self):

        if self.dev.get() == 'False':
            self.frames[5].place(x=210, y=0)

            self.dev.set(self.DEV[0])
        else:
            self.frames[5].place(x=1000, y=1000)

            self.dev.set(self.DEV[1])

    def changeSize(self):

        if self.msize.get() == 'Big':

            self.geometry('700x700')
            self.frames[3].configure(height=180)
            self.frames[4].configure(height=180)
            self.labels[9].place(y=140)
            self.labels[8].place(y=110)
            self.frames[5].configure(height=0)

            self.msize.set(self.SIZES[0])
        else:

            self.geometry('700x800')
            self.frames[3].configure(height=280)
            self.frames[4].configure(height=280)
            self.labels[9].place(y=240)
            self.labels[8].place(y=210)
            self.frames[5].configure(height=270)

            self.msize.set(self.SIZES[1])

    def createLabel(self, master, x, y, text, fontsize, row=False):
        object = customtkinter.CTkLabel(master=master, text=text, font=(self.font, fontsize), anchor='w')
        self.labels.append(object)

        if row:
            object.grid(sticky='W', row=row, column=0, padx=0)
        else:
            object.place(x=x, y=y)
    def createFrame(self, x, y, w, h):
        object = customtkinter.CTkFrame(master=self, width=w, height=h, corner_radius=10)
        object.place(x=x, y=y)
        self.frames.append(object)
    def createSubFrame(self, master, x, y, w, h, cr=0):
        object = customtkinter.CTkFrame(master=master, width=w, height=h, corner_radius=cr)
        object.place(x=x, y=y)
        self.frames.append(object)
    def createMenu(self, master, x, y, w, h, fontsize, variable, *variableOptions):
        object = customtkinter.CTkOptionMenu(master=master, variable=variable, values=variableOptions,width=w, height=h, corner_radius=0, dropdown_font=(self.font, fontsize), font=(self.font, fontsize))
        object.place(x=x, y=y)
        self.menus.append(object)
    def createButton(self, master, x, y, w, h, text, fontsize, command):
        object = customtkinter.CTkButton(master=master, width=w, height=h, text=text, corner_radius=0, font=(self.font, fontsize), command=command)
        object.place(x=x, y=y)
    def createSlider(self, master, x, y, from_, to, steps):
        object = customtkinter.CTkSlider(master=master, from_=from_, to=to, orientation='horizontal', number_of_steps=steps)
        object.place(x=x, y=y)
        self.sliders.append(object)
    def createSwitch(self, master, x, y, command=None):
        object = customtkinter.CTkSwitch(master=master, onvalue=True, offvalue=False, text='', command=command)
        object.place(x=x, y=y)
        self.switches.append(object)
    def createCheckbox(self, master, value, x, y):
        object = customtkinter.CTkCheckBox(master=master, onvalue=value, offvalue=False, text=value, font=(self.font, 18), checkbox_width=100)
        object.place(x=x, y=y)
        self.boxes.append(object)
    def createCon(self, master, x, y, w, h):
        object = customtkinter.CTkScrollableFrame(master=master, width=w, height=h, label_anchor='e')
        self.frames.append(object)

    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        add_hotkey('backspace', lambda: self.stop())
        add_hotkey('space', lambda: self.submit())
        self.mainloop()

    def stop(self):
        if self.isRunning:
            self.writeLogFile(f'Finished in {self.timer}')
            self.app.exit()
            self.isRunning = False

    def onClose(self):
        self.stop()
        self.destroy()

if __name__ == '__main__':
    gui = Gui()
    gui.run()