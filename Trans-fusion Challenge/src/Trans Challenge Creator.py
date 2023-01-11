import tkinter as tk
from tkinter import Label, Button, Entry, Spinbox, Checkbutton, Canvas, StringVar, IntVar
from tkinter import filedialog


BOX_HEX = "40 62 6f 78 65 73 5b 23 6f 3a 0f 50 6f 6b 65 6d 6f 6e 42 6f 78 08 3a 0d 40 70 6f 6b 65 6d 6f 6e 5b 23"
SYLVEON_HEX = "6f 3b 0e 3a 3b 0f 3a 0c 53 59 4c 56 45 4f 4e 3b 11 69 00 3b 12 30 3b 13 30 3b 14 69 00 3b 15 69 06 3b 16 69 00 3b 17 3b 18 3b 19 69 00 3b 1a 69 00 3b 1b 30 3b 1c 69 00 3b 1d 3a 0e 43 55 54 45 43 48 41 52 4d 3b 1f 3a 0a 48 41 52 44 59 3b 21 30 3b 22 3a 10 44 4e 41 53 50 4c 49 43 45 52 53 3b 23 30 3b 24 5b 07 6f 3b 25 08 3b 0b 3a 0b 54 41 43 4b 4c 45 3b 27 69 00 3b 28 69 28 6f 3b 25 08 3b 0b 3a 0d 54 41 49 4c 57 48 49 50 3b 27 69 00 3b 28 69 23 3b 2b 5b 07 3b 02 1f 04 3b 02 20 04 3b 2c 5b 00 3b 2d 69 00 3b 2e 69 00 3b 2f 69 00 3b 30 69 00 3b 31 69 00 3b 32 69 00 3b 33 69 00 3b 09 30 3b 34 69 4b 3b 35 3b 36 3b 37 69 00 3b 38 7b 0b 3b 39 69 1b 3b 3a 69 00 3b 3b 69 00 3b 3c 69 00 3b 3d 69 00 3b 3e 69 00 3b 3f 7b 00 3b 40 7b 0b 3b 39 69 00 3b 3a 69 00 3b 3b 69 00 3b 3c 69 00 3b 3d 69 00 3b 3e 69 00 3b 41 30 3b 42 30 3b 43 6f 3b 44 09 3b 0b 40 08 3b 09 40 07 3b 1a 69 06 3b 0c 69 07 3b 45 69 00 3b 46 69 53 3b 47 30 3b 48 69 06 3b 49 69 00 3b 4a 69 04 80 13 6e 38 3b 4b 30 3b 4c 30 3b 4d 6c 2b 07 6e 13 7d e6 3b 4e 69 14 3b 4f 69 14 3b 50 69 0d 3b 51 69 0c 3b 52 69 0b 3b 53 69 0c 3b 54 69 0e"
BOX_BYTES = bytes.fromhex(BOX_HEX.replace(" ", ""))
SYLVEON_BYTES = bytes.fromhex(SYLVEON_HEX.replace(" ", ""))

BLUE = "#5bcefa"
PINK = "#f5a9b8"
WHITE = "#ffffff"


class Application:
    validBefore = [b'[#', b'i']
    
    def __init__(self):
        self.data = []
        self.filename = ""

        self.boxDataStartLine = None
        self.boxDataStartCol = None

        self.boxData = None

        self.maxSylveons = 30

        self.padding = 8
        self.widgetH = 32
        self.entryW = self.widgetH*16
        self.createUI()


    def createUI(self):
        self.root = tk.Tk()
        self.root.title("Sylveon Generator")
        self.font = ("Arial", 12)

        self.varFilename = StringVar(self.root)
        self.varNewFile = StringVar(self.root)
        self.varOverwrite = IntVar(self.root, 0)
        self.varSylveonCount = StringVar(self.root, "10")

        self.background = Canvas(self.root)
        
        self.btnOpenFile = Button(self.root, text="Open File", command=self.openFile, font=self.font)
        self.entryFilename = Entry(self.root, state="disabled", textvariable=self.varFilename, font=self.font)

        self.lblSylveonCount = Label(self.root, text="Number of Sylveons: ", bg=PINK, font=self.font)
        self.spinSylveonCount = Spinbox(self.root, from_=1, to=self.maxSylveons, font=self.font, textvariable=self.varSylveonCount)

        self.entryNewFilename = Entry(self.root, state="disabled", textvariable=self.varNewFile, font=self.font)
        self.btnSaveFile = Button(self.root, text="Save to File", command=self.fileToSave, font=self.font)

        self.checkOverwrite = Checkbutton(self.root, text="Overwrite File", variable=self.varOverwrite, bg=WHITE, font=self.font)

        self.lblMadeBy = Label(self.root, text="Made By: @emberthehotlump")

        self.btnRun = Button(self.root, text="Generate Sylveons", font=self.font, state="disabled", command=self.createSylveons)


        rootW = self.padding*3+self.btnOpenFile.winfo_reqwidth()+self.entryW
        
        
        self.background.place(x=-2, y=-2)
        
        section1Y = self.padding
        self.btnOpenFile.place(x=self.padding, y=section1Y, height=self.widgetH)
        self.entryFilename.place(x=self.padding*2+self.btnOpenFile.winfo_reqwidth(), y=section1Y, width=self.entryW, height=self.widgetH)

        section2Y = section1Y + self.widgetH*2
        self.spinSylveonCount.place(x=self.padding*2+self.lblSylveonCount.winfo_reqwidth(), y=section2Y, height=self.widgetH)
        self.lblSylveonCount.place(x=self.padding, y=section2Y+self.widgetH/2-self.lblSylveonCount.winfo_reqheight()/2)

        section3Y = section2Y + round(self.widgetH*2)
        self.checkOverwrite.place(x=self.padding, y=section3Y)
        self.btnSaveFile.place(x=self.padding, y=section3Y+self.widgetH, height=self.widgetH)
        self.entryNewFilename.place(x=self.padding*2+self.btnSaveFile.winfo_reqwidth(), y=section3Y+self.widgetH, width=self.entryW-(self.btnSaveFile.winfo_reqwidth()-self.btnOpenFile.winfo_reqwidth()), height=self.widgetH)

        section4Y = section3Y + self.widgetH*5
        self.btnRun.place(x=rootW-self.btnRun.winfo_reqwidth()-self.padding, y=section4Y, height=self.widgetH)
        self.lblMadeBy.place(x=self.padding, y=section4Y+self.lblMadeBy.winfo_reqheight()/2)

        def isChecked():
            if (self.varOverwrite.get() == 1):
                self.entryNewFilename.place_forget()
                self.btnSaveFile.place_forget()
                self.checkFields()
            else:
                self.btnSaveFile.place(x=self.padding, y=section3Y+self.widgetH, height=self.widgetH)
                self.entryNewFilename.place(x=self.padding*2+self.btnSaveFile.winfo_reqwidth(), y=section3Y+self.widgetH, width=self.entryW-(self.btnSaveFile.winfo_reqwidth()-self.btnOpenFile.winfo_reqwidth()), height=self.widgetH)
        self.checkFields()

        def validateSylveonCount(newVal):
            if (newVal.isdigit() == False):
                return False
            if (int(newVal) > self.maxSylveons or int(newVal) < 1):
                return False
            return True

        self.checkOverwrite.configure(command=isChecked)

        vcmd = (self.root.register(validateSylveonCount), "%P")
        self.spinSylveonCount.configure(validate="key", validatecommand=vcmd)


        
        rootH = section4Y+self.padding+self.widgetH
        self.background.configure(width=rootW, height=rootH)
        self.background.create_rectangle(0, 0, rootW+2, rootH/5+2, fill=BLUE, outline=BLUE)
        self.background.create_rectangle(0, rootH/5, rootW+2, rootH/5*2+2, fill=PINK, outline=PINK)
        self.background.create_rectangle(0, rootH/5*2, rootW+2, rootH/5*3+2, fill=WHITE, outline=WHITE)
        self.background.create_rectangle(0, rootH/5*3, rootW+2, rootH/5*4+2, fill=PINK, outline=PINK)
        self.background.create_rectangle(0, rootH/5*4, rootW+2, rootH+2, fill=BLUE, outline=BLUE)
                                  
        self.root.geometry(f"{rootW}x{rootH}")
        self.root.resizable(width=False, height=False)
        self.root.mainloop()


    def checkFields(self):
        if ((self.varNewFile.get() != "" or self.varOverwrite.get() == 1) and self.varFilename.get() != ""):
            self.btnRun.configure(state="normal")
        else:
            self.btnRun.configure(state="disabled")
            
            
    def fileToSave(self):
        fn = filedialog.asksaveasfilename()
        if (fn == ""):
            return
        
        self.varNewFile.set(fn)
        self.checkFields()


    def openFile(self):
        fn = filedialog.askopenfilename()
        if (fn == ""):
            return
        
        self.filename = fn
        self.readFile()
        self.varFilename.set(self.filename)
        self.checkFields()


    def readFile(self):
        self.data = []
        with open(self.filename, "rb") as f:
            self.data = f.readlines()
            

    def createSylveons(self):
        count = self.varSylveonCount.get()
        count = int(count)

        self.getBoxData()
        for i in range(count):
            self.addToNextEmptySlot()

        self.saveToFile()


    def findBoxDataLocation(self):
        x = 0
        j = -1
        while x < len(self.data):
            j = self.data[x].find(BOX_BYTES)
            if (j != -1):
                break

            x += 1

        self.boxDataStartLine = x
        self.boxDataStartCol = j


    def getBoxData(self):
        self.findBoxDataLocation()
        x = self.boxDataStartLine
        j = self.boxDataStartCol
        
        self.boxData = self.data[x][j+len(BOX_BYTES):]

        for i in range(x+1, len(self.data)):
            self.boxData += self.data[i]
            

    def addToNextEmptySlot(self):
        found = False

        lastPos = 0
        while found == False:
            slotI = self.boxData.find(b'0', lastPos)

            for valid in self.validBefore:
                ln = len(valid)
                if (self.boxData[slotI-ln:slotI] == valid):
                    found = True
                    break

            if (found == False):
                lastPos = slotI+1
            if (lastPos >= len(self.boxData)):
                break

        self.boxData = self.boxData[:slotI] + SYLVEON_BYTES + self.boxData[slotI+1:]


    def combineData(self):
        x = self.boxDataStartLine
        j = self.boxDataStartCol
        
        completed = self.data[0]
        
        for i in range(1, x):
            completed += self.data[i]
            
        completed += self.data[x][:j+len(BOX_BYTES)]
        completed += self.boxData

        return completed
    

    def saveToFile(self):
        completed = self.combineData()

        if (self.varOverwrite.get() == 1):
            newFn = self.varFilename.get()
        else:
            newFn = self.varNewFile.get()

        
        with open(newFn, "wb") as f:
            f.write(completed)

        print("Sylveons added to first empty slots in boxes.")
    

    


def main():
    app = Application()
    #app.openFile()
    #app.createSylveons()


if (__name__ == "__main__"):
    main()







