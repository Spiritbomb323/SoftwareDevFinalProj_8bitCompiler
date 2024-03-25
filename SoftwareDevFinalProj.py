import tkinter as tk
from WindowProgramSimulation import simulateProgram

#setup variables
win = tk.Tk()
win.geometry("600x600")
win.title("Compiler")

#represents the unique code associated with the buttons
firstHalfByte = ""
#two digit code for the first and second registers ie "00", "10"
RegisterBit_1 = ""
RegisterBit_2 = ""

#variables used in the readable code text boxes, not bit versions of the variables above
InstructionStr = ""
FirstReg = ""
SecondReg = ""

#variables for tracking the data from the Jump if instruction
JMPIF_Byte = ""
JMPIFByteList = ["0", "0", "0", "0"]
JMPIFReadableList = ["", "", "", "", ""]

ButtonList = []
RegisterButtonList = []

#stores all data created by the user. Used for saving and loading.
InstructionByteList = []
InstructionReadableList = []

yMargin = 40
index = 0

#variables to know if instruction buttons are being used.
usingDataInstruction = False
usingJMPRInstruction = False
usingJMPInstruction = False
usingIOInstruction = False
usingCustByteInstruction = False


### Setup Text Boxes -----------------------------------------
output_data = tk.Text(win, width= 21, height=20, font="Roboto 10")
output_data.place(x=250, y=50 + yMargin)

readable_data = tk.Text(win, width=21, height=20, font="Roboto 10")
readable_data.place(x=430, y=50 + yMargin)

nextByte = tk.Label(win, text="Next byte: ", font="Roboto 10")
nextByte.place(x=175, y=7 + yMargin)

nextByteData = tk.Text(win, width= 21, height= 1, font="Robot 10")
nextByteData.place(x=250, y=10 + yMargin)

readableNextByte = tk.Text(win, width= 21, height= 1, font="Roboto 10")
readableNextByte.place(x=430, y=10 + yMargin)

#file loading and saving window ------------------------------------
def openFileWindow():
    file_win = tk.Tk()
    file_win.geometry("220x100")
    file_win.title("File")

    #file Saving, copies instructionByteList and instructionreadableList to a file.
    def FileSave():
        fileName = fileNameEntry.get()
        if len(fileName) > 0:
            userFile = open(fileName + ".txt", "w")
            index = 0
            for item in InstructionByteList:
                userFile.write(item + "|" + InstructionReadableList[index] + "\n")
                index += 1
            userFile.close()
        file_win.destroy()
    
    #file loading. loads data from file and inserts back into instructionbytelist, instructionreadablelist, and the text boxes.
    def FileLoad():
        fileName = fileNameEntry.get()
        if len(fileName) > 0:
            userFile = open(fileName + ".txt", "r")
            readFile = userFile.readlines()
            userFile.close()
            resetAll()
            index = 0
            for line in readFile:
                readLines = line.split("|")
                readLines[1] = readLines[1].replace("\n", "")
                InstructionByteList.append(readLines[0])
                InstructionReadableList.append(readLines[1])
                output_data.configure(state="normal")
                readable_data.configure(state="normal")
                output_data.insert(tk.INSERT, str(index) + " - " + readLines[0] + "\n")
                readable_data.insert(tk.INSERT, str(index) + " - " + readLines[1]+ "\n")
                index += 1
        file_win.destroy()

    #buttons, labels, and entrys for this window.
    fileNameLabel = tk.Label(file_win, font="Roboto 10", text="File Name: ")
    fileNameLabel.place(x=10, y=10)

    fileNameEntry = tk.Entry(file_win, font="Roboto 10", width= 15)
    fileNameEntry.place(x=90, y= 10)

    saveButton = tk.Button(file_win, text="Save", font="Roboto 10", command=FileSave)
    saveButton.place(x=50, y=50)
    
    LoadButton = tk.Button(file_win, text="Load", font="Roboto 10", command=FileLoad)
    LoadButton.place(x=100, y=50)

#disables or enables IO instruction sub buttons.
def manageIOButtonStates(x):
    if x == False:
        IO_InData["state"] = "disabled"
        IO_InAddr["state"] = "disabled"
        IO_OutData["state"] = "disabled"
        IO_OutAddr["state"] = "disabled"
    if x == True:
        IO_InData["state"] = "normal"
        IO_InAddr["state"] = "normal"
        IO_OutData["state"] = "normal"
        IO_OutAddr["state"] = "normal"

#updates the next byte section when using the IO sub button instructions
def ioButtonDataInsert(string, bit):
    global finalInstStr
    global finalByte
    nextByteData.delete('1.0', tk.END)
    readableNextByte.delete('1.0', tk.END)

    finalInstStr = InstructionStr + ": " + string + " --> " + FirstReg
    finalByte = firstHalfByte + bit + RegisterBit_1

    nextByteData.insert(tk.END, finalByte + "\n")
    readableNextByte.insert(tk.END, finalInstStr + "\n")

#IO instruction button setup
def IOButtonData(x):
    Submit_Button["state"] = "normal"
    if x == 1:
        ioButtonDataInsert("In Data", "00")
    if x == 2:
        ioButtonDataInsert("In Addr", "01")
    if x == 3:
        ioButtonDataInsert("Out Data", "10")
    if x == 4:
        ioButtonDataInsert("Out Addr", "11")
        
IO_InData = tk.Button(win, text="In Data", font="Roboto 8", command=lambda: IOButtonData(1))
IO_InAddr = tk.Button(win, text="In Address", font="Roboto 8", command=lambda: IOButtonData(2))
IO_OutData = tk.Button(win, text="Out Data", font="Roboto 8", command=lambda: IOButtonData(3))
IO_OutAddr = tk.Button(win, text="Out Address", font="Roboto 8", command=lambda: IOButtonData(4))

#connecting the jump if buttons (CAEZ), with data. 
def manageJMPIF(x):
    if x == 1:
        JMPIF_C["state"] = "disabled"
        JMPIFByteList[0] = "1"
        JMPIFReadableList[0] = "C"
    if x == 2:
        JMPIF_A["state"] = "disabled"
        JMPIFByteList[1] = "1"
        JMPIFReadableList[1] = "A"
    if x == 3:
        JMPIF_E["state"] = "disabled"
        JMPIFByteList[2] = "1"
        JMPIFReadableList[2] = "E"
    if x == 4:
        JMPIF_Z["state"] = "disabled"
        JMPIFByteList[3] = "1"
        JMPIFReadableList[3] = "Z"

#checks which buttons  are pressed, then submits it.
def JMPIFSubmit_Button():
    global finalByte
    global finalInstStr
    JMPIF_BYTECAEZ = JMPIFByteList[0] + JMPIFByteList[1] + JMPIFByteList[2] + JMPIFByteList[3]
    JMPIF_ReadableCAEZ = JMPIFReadableList[0] + JMPIFReadableList[1] + JMPIFReadableList[2] + JMPIFReadableList[3]
    finalByte = firstHalfByte + JMPIF_BYTECAEZ
    finalInstStr = InstructionStr + " --> " + JMPIF_ReadableCAEZ
    if JMPIF_BYTECAEZ != "0000":
        submit_data()

JMPIF_C = tk.Button(win, text= "Carry", font="Roboto 8", command= lambda: manageJMPIF(1))
JMPIF_A = tk.Button(win, text= "A >", font="Roboto 8", command= lambda: manageJMPIF(2))
JMPIF_E = tk.Button(win, text= "Equal", font="Roboto 8", command= lambda: manageJMPIF(3))
JMPIF_Z = tk.Button(win, text= "Zero", font="Roboto 8", command= lambda: manageJMPIF(4))

JMPIF_Submit = tk.Button(win, text="Submit", font="Roboto 7", command= JMPIFSubmit_Button)

#places or removes the JMPIF sub buttons
def ManageJMPIFVis(x):
    if x == True:
        JMPIF_C.place(x=80, y=532)
        JMPIF_A.place(x=120, y=532)
        JMPIF_E.place(x=150, y=532)
        JMPIF_Z.place(x=190, y=532)
        JMPIF_Submit.place(x=250, y=532)
    if x == False:
        JMPIF_C.place_forget()
        JMPIF_A.place_forget()
        JMPIF_E.place_forget()
        JMPIF_Z.place_forget()
        JMPIF_Submit.place_forget()

#places or removes the IO elements.
def manageIOElements(x):
    if x == "show":
        
        IO_InData.place(x=60, y=472)
        IO_InAddr.place(x=110, y=472)
        IO_OutData.place(x=180, y=472)
        IO_OutAddr.place(x=240, y=472)
    if x == "hide":
        
        IO_InData.place_forget()
        IO_InAddr.place_forget()
        IO_OutData.place_forget()
        IO_OutAddr.place_forget()

manageIOElements("hide")


def UsingGlobalInstructionVariables(x):
    global usingDataInstruction
    global usingJMPRInstruction
    global usingJMPInstruction
    global usingIOInstruction
    global usingCustByteInstruction
    usingDataInstruction = x
    usingJMPRInstruction = x
    usingJMPInstruction = x
    usingIOInstruction = x
    usingCustByteInstruction = x

#translates digits to binary while inserting 0's so that it is still formated correctly.
def decimalToBinary(n):
    zeroList = ["0","00","000","0000","00000","000000","0000000",]
    binary = "{0:b}".format(int(n))

    if len(binary) != 8:
        output = zeroList[7 - len(binary)] + binary     
        return output
    else:
        return binary

### Moves the strings from the "next byte" text boxes into the main text boxes -----------------------------------
def submit_data():
    global index
    if firstHalfByte != "":
        
        InstructionByteList.append(finalByte)
        InstructionReadableList.append(finalInstStr)

        output_data.configure(state="normal")
        readable_data.configure(state="normal")
        output_data.insert(tk.INSERT, str(index) + " - " + finalByte + "\n")
        readable_data.insert(tk.INSERT, str(index) + " - " + finalInstStr + "\n")
        output_data.configure(state="disabled")
        readable_data.configure(state="disabled")
        index += 1
        UsingGlobalInstructionVariables(False)
        manageIOElements("hide")
        disableAll()
        for x in ButtonList:
            x["state"] = "normal"

### Method for submitting the Entry from the DATA instruction -----------------------------------------
def submit_DataInstByte():
    global finalByte
    global finalInstStr
    validByte = True
    byte = dataEntry.get()
    if byte.isnumeric(): 
        if len(byte) <= 3 and len(byte) >= 1:
            byte = int(byte)
            if byte <= 255:
                if usingDataInstruction == True or usingJMPInstruction == True:
                    submit_data()
                    finalByte = str(decimalToBinary(byte))
                    finalInstStr = str(byte)
                    submit_data()
                    disableDataInstructionExtra()
                elif (usingCustByteInstruction == True):
                    finalByte = str(decimalToBinary(byte))
                    finalInstStr = str(byte)
                    submit_data()
                    disableDataInstructionExtra()
        elif len(byte) == 8:
            byte = str(byte)
            for x in byte:
                if x != "0" and x != "1":
                    validByte = False
            if validByte == True:
                if usingDataInstruction == True or usingJMPInstruction == True:
                    submit_data()
                    finalByte = byte
                    finalInstStr = byte
                    submit_data()
                    disableDataInstructionExtra()
                elif (usingCustByteInstruction == True):
                    finalByte = byte
                    finalInstStr = byte
                    submit_data()
                    disableDataInstructionExtra()
        
### GUI For DATA instruction -----------------------------------------
dataLabel = tk.Label(win, text="Enter byte or number(<= 255): ", font="Roboto 10")
dataEntry = tk.Entry(win, font="Roboto 10", width=15)
dataSubmit = tk.Button(win, text="Submit", font="Roboto 7", command=submit_DataInstByte)

### Functions for resetting GUI buttons -----------------------------------------
def resetAll():
    global index
    global JMPIFByteList
    global JMPIFReadableList
    index = 0
    UsingGlobalInstructionVariables(False)
    output_data.configure(state="normal")
    readable_data.configure(state="normal")

    output_data.delete('1.0', tk.END)
    readable_data.delete('1.0', tk.END)
    nextByteData.delete('1.0', tk.END)
    readableNextByte.delete('1.0', tk.END)
    disableDataInstructionExtra()
    manageIOElements("hide")
    for x in ButtonList:
        x["state"] = "normal"
    disableAll()
    InstructionByteList.clear()
    InstructionReadableList.clear()
    output_data.configure(state="disabled")
    readable_data.configure(state="disabled")
    ManageJMPIFVis(False)
    JMPIFByteList = ["0", "0", "0", "0"]
    JMPIFReadableList = ["", "", "", "", ""]
    JMPIF_C["state"] = "normal"
    JMPIF_A["state"] = "normal"
    JMPIF_E["state"] = "normal"
    JMPIF_Z["state"] = "normal" 

def disableAll():
    for x in RegisterButtonList:
        x["state"] = "disabled"

def State_ChangeRegButtons(z):
    for x in range(4, 8):
        if z == "enable":
            RegisterButtonList[x]["state"] = "normal"
        if z == "disable":
            RegisterButtonList[x]["state"] = "disabled"

def State_changeSubRegButtons(z):
    for x in range(0, 4):
        if z == "enable":
            RegisterButtonList[x]["state"] = "normal"
        if z == "disable":
            RegisterButtonList[x]["state"] = "disabled"

def enableAllExcept(button):
    for x in ButtonList:
        x["state"] = "normal"
    button["state"] = "disabled"

### Disable the data instruction GUI --------------------------------
def disableDataInstructionExtra():
    JMPIF_Button.place(x=20, y=530)
    dataEntry.place_forget()
    dataLabel.place_forget()
    dataSubmit.place_forget()

### Enable the data instruction GUI --------------------------------
def dataInstructionEntry():
    disableDataInstructionExtra()
    JMPIF_Button.place_forget()
    dataLabel.place(x=20, y=530)
    dataEntry.place(x=20, y=555)
    dataSubmit.place(x=150, y=555)

### functions for setting up the GUI Buttons --------------------------------
def setupButton(button, byte, text):
    global firstHalfByte
    global InstructionStr
    global JMPIFByteList
    global JMPIFReadableList
    State_changeSubRegButtons("disable")
    Submit_Button["state"] = "disabled"
    firstHalfByte = byte
    InstructionStr = text
    enableAllExcept(button)
    if byte != "001000":
        disableDataInstructionExtra()
    if byte != "0111":
        manageIOElements("hide")
    if byte != "0101":
        JMPIFByteList = ["0", "0", "0", "0"]
        JMPIFReadableList = ["", "", "", "", ""]
        JMPIF_C["state"] = "normal"
        JMPIF_A["state"] = "normal"
        JMPIF_E["state"] = "normal"
        JMPIF_Z["state"] = "normal" 
        ManageJMPIFVis(False)

#this is for instructions that don't require registers
def usingNoRegisters():
    global finalInstStr
    global finalByte
    nextByteData.delete('1.0', tk.END)
    readableNextByte.delete('1.0', tk.END)

    finalInstStr = InstructionStr
    finalByte = firstHalfByte

    nextByteData.insert(tk.END, finalByte + "\n")
    readableNextByte.insert(tk.END, finalInstStr + "\n")

#main function for setting up and enabling buttons, gives a button a name, associated 4 bits.
def SetupButtons(x):
    global usingDataInstruction
    global usingJMPRInstruction
    global usingJMPInstruction
    global usingIOInstruction
    global usingCustByteInstruction
    UsingGlobalInstructionVariables(False)
    if x == 0:
        setupButton(ADD_Button, "1000", "ADD")
    if x == 1:
        setupButton(SHR_Button, "1001", "Shift right")
    if x == 2:
        setupButton(SHL_Button, "1010", "Shift left")
    if x == 3:
        setupButton(NOT_Button, "1011", "NOT")
    if x == 4:
        setupButton(AND_Button, "1100", "AND")
    if x == 5:
        setupButton(OR_Button, "1101", "OR")
    if x == 6:
        setupButton(XOR_Button, "1110", "XOR")
    if x == 7:
        setupButton(CMP_Button, "1111", "COMPARE")
    if x == 8:
        setupButton(LD_Button, "0000", "LOAD")
    if x == 9:
        setupButton(ST_Button, "0001", "STORE")
    if x == 10:
        setupButton(DATA_Button, "001000", "DATA into")
        usingDataInstruction = True
        Submit_Button["state"] = "disabled"
        State_changeSubRegButtons("disable")
        
    if x == 11:
        setupButton(JMPR_Button, "001100", "Jump Reg")
        usingJMPRInstruction = True
        Submit_Button["state"] = "disabled"
        State_changeSubRegButtons("disable")

    if x == 12:
        setupButton(JMP_Button, "01000000", "Jump to ->")
        usingJMPInstruction = True
        usingNoRegisters()
        dataInstructionEntry()
        State_ChangeRegButtons("disable")
    
    if x == 13:
        setupButton(CLF_Button, "01100000", "Clear Flags")
        usingNoRegisters()
        Submit_Button["state"] = "normal"
        State_ChangeRegButtons("disable")
    
    if x == 14:
        setupButton(IO_Button, "0111", "IO")
        manageIOElements("show")
        usingIOInstruction = True
        manageIOButtonStates(False)

    if x == 15:
        usingCustByteInstruction = True
        dataInstructionEntry()
        Submit_Button["state"] = "disabled"
        enableAllExcept(CustByte_Button)
        manageIOElements("hide")
        JMPIF_C["state"] = "normal"
        JMPIF_A["state"] = "normal"
        JMPIF_E["state"] = "normal"
        JMPIF_Z["state"] = "normal" 
        ManageJMPIFVis(False)

    if x == 16:
        setupButton(JMPIF_Button, "0101", "Jump if")
        usingNoRegisters()
        ManageJMPIFVis(True)
        
    if x != 12 and x != 13 and x != 15 and x != 16:
        State_ChangeRegButtons("enable")

#for instructions that only use one register.
def usingSingleRegister():
    global finalInstStr
    global finalByte
    nextByteData.delete('1.0', tk.END)
    readableNextByte.delete('1.0', tk.END)

    finalInstStr = InstructionStr + " --> " + FirstReg
    finalByte = firstHalfByte + RegisterBit_1

    nextByteData.insert(tk.END, finalByte + "\n")
    readableNextByte.insert(tk.END, finalInstStr + "\n")

### Function used by main Registers 0-3 -------------------------------------
def changeBits(x):
    global RegisterBit_1
    global FirstReg
    if x == 0:
        RegisterBit_1 = "00"
        FirstReg = "R0"
    if x == 1:
        RegisterBit_1 = "01"
        FirstReg = "R1"
    if x == 2:
        RegisterBit_1 = "10"
        FirstReg = "R2"
    if x == 3:
        RegisterBit_1 = "11"
        FirstReg = "R3"
 
    if (usingIOInstruction == True):
        manageIOButtonStates(True)
        State_changeSubRegButtons("disable")
    elif (usingDataInstruction == True):
        usingSingleRegister()
        dataInstructionEntry()
        
    elif (usingJMPRInstruction == True):
        usingSingleRegister()
        Submit_Button["state"] = "normal"
    else:
        State_changeSubRegButtons("enable")

### Function used by Sub Registers 0-3 -------------------------------------
def changeBits2(x):
    global RegisterBit_2
    global SecondReg
    global finalInstStr
    global finalByte

    nextByteData.delete('1.0', tk.END)
    readableNextByte.delete('1.0', tk.END)
    
    if x == 0:
        RegisterBit_2 = "00"
        SecondReg = "R0"
    if x == 1:
        RegisterBit_2 = "01"
        SecondReg = "R1"
    if x == 2:
        RegisterBit_2 = "10"
        SecondReg = "R2"
    if x == 3:
        RegisterBit_2 = "11"
        SecondReg = "R3"
    
    finalByte = firstHalfByte + RegisterBit_1 + RegisterBit_2
    finalInstStr = InstructionStr + " " + FirstReg + " -> " + SecondReg

    nextByteData.insert(tk.END, finalByte + "\n")
    readableNextByte.insert(tk.END, finalInstStr + "\n")
    Submit_Button["state"] = "normal"

def instantiateButton(z, x1, y1):
    ButtonList.append(z)
    z.place(x=x1, y=y1)

def instantiateRegisterButton(z, x1, y1):
    RegisterButtonList.append(z)
    z.place(x=x1, y=y1)

### Initialize Register Buttons -------------------------------------
R0_ButtonSUB = tk.Button(win, text="R0", font="Roboto 7", command=lambda: changeBits2(0), disabledforeground="light gray")
instantiateRegisterButton(R0_ButtonSUB, 70, 80)
R1_ButtonSUB = tk.Button(win, text="R1", font="Roboto 7", command=lambda: changeBits2(1), disabledforeground="light gray")
instantiateRegisterButton(R1_ButtonSUB, 95, 80)
R2_ButtonSUB = tk.Button(win, text="R2", font="Roboto 7", command=lambda: changeBits2(2), disabledforeground="light gray")
instantiateRegisterButton(R2_ButtonSUB, 120, 80)
R3_ButtonSUB = tk.Button(win, text="R3", font="Roboto 7", command=lambda: changeBits2(3), disabledforeground="light gray")
instantiateRegisterButton(R3_ButtonSUB, 145, 80)

R0_Button = tk.Button(win, text="R0", font="Roboto 7", command=lambda: changeBits(0), disabledforeground="light gray")
instantiateRegisterButton(R0_Button, 70, 50)
R1_Button = tk.Button(win, text="R1", font="Roboto 7", command=lambda: changeBits(1), disabledforeground="light gray")
instantiateRegisterButton(R1_Button, 95, 50)
R2_Button = tk.Button(win, text="R2", font="Roboto 7", command=lambda: changeBits(2), disabledforeground="light gray")
instantiateRegisterButton(R2_Button, 120, 50)
R3_Button = tk.Button(win, text="R3", font="Roboto 7", command=lambda: changeBits(3), disabledforeground="light gray")
instantiateRegisterButton(R3_Button, 145, 50)

disableAll()

### Initialize Instruction Buttons -------------------------------------
ADD_Button = tk.Button(win, text="ADD", font="Roboto 10", command=lambda: SetupButtons(0))
instantiateButton(ADD_Button, 20, 50)

SHR_Button = tk.Button(win, text="SHR", font="Roboto 10", command=lambda: SetupButtons(1))
instantiateButton(SHR_Button, 20, 80)

SHL_Button = tk.Button(win, text="SHL", font="Roboto 10", command=lambda: SetupButtons(2))
instantiateButton(SHL_Button, 20, 110)

NOT_Button = tk.Button(win, text="NOT", font="Roboto 10", command=lambda: SetupButtons(3))
instantiateButton(NOT_Button, 20, 140)

AND_Button = tk.Button(win, text="AND", font="Roboto 10", command=lambda: SetupButtons(4))
instantiateButton(AND_Button, 20, 170)

OR_Button = tk.Button(win, text="OR", font="Roboto 10", command=lambda: SetupButtons(5))
instantiateButton(OR_Button, 20, 200)

XOR_Button = tk.Button(win, text="XOR", font="Roboto 10", command=lambda: SetupButtons(6))
instantiateButton(XOR_Button, 20, 230)

CMP_Button = tk.Button(win, text="CMP", font="Roboto 10", command=lambda: SetupButtons(7))
instantiateButton(CMP_Button, 20, 260)

LD_Button = tk.Button(win, text="LOAD", font="Roboto 10", command=lambda: SetupButtons(8))
instantiateButton(LD_Button, 20, 290)

ST_Button = tk.Button(win, text="STORE", font="Roboto 10", command=lambda: SetupButtons(9))
instantiateButton(ST_Button, 20, 320)

DATA_Button = tk.Button(win, text="DATA", font="Roboto 10", command=lambda: SetupButtons(10))
instantiateButton(DATA_Button, 20, 350)

JMPR_Button = tk.Button(win, text="JMPR", font="Roboto 10", command=lambda: SetupButtons(11))
instantiateButton(JMPR_Button, 20, 380)

JMP_Button = tk.Button(win, text="JMP", font="Roboto 10", command=lambda: SetupButtons(12))
instantiateButton(JMP_Button, 20, 410)

CLF_Button = tk.Button(win, text="CLF", font="Roboto 10", command=lambda: SetupButtons(13))
instantiateButton(CLF_Button, 20, 440)

IO_Button = tk.Button(win, text="IO", font="Roboto 10", command=lambda: SetupButtons(14))
instantiateButton(IO_Button, 20, 470)

CustByte_Button = tk.Button(win, text="Custom Byte", font="Roboto 10", command=lambda: SetupButtons(15))
instantiateButton(CustByte_Button, 20, 500)

JMPIF_Button = tk.Button(win, text="JMPIF", font="Roboto 10", command=lambda: SetupButtons(16))
instantiateButton(JMPIF_Button, 20, 530)

Submit_Button = tk.Button(win, text="Enter", font= "Roboto 10", command=submit_data, background="light green", activebackground="green")
Submit_Button.place(x=20, y = 10)

Reset_Button = tk.Button(win, text="Reset", font="Roboto 10", command=resetAll, background= "pink", activebackground="red")
Reset_Button.place(x=520, y=10)

fileButton = tk.Button(win, text="File", font="Roboto 10", command=openFileWindow)
fileButton.place(x=480, y=10)

runFileButton = tk.Button(win, text="Run", font="Roboto 10", command=lambda: simulateProgram(InstructionReadableList, InstructionByteList, 0.5))
runFileButton.place(x=440, y=10)

win.mainloop()
