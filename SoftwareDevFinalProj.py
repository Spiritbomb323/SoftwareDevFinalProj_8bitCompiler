import tkinter as tk
#import TextInputBasicCompiler as BC

win = tk.Tk()
win.geometry("600x600")
win.title("Compiler")

firstHalfByte = ""
RegisterBit_1 = ""
RegisterBit_2 = ""

InstructionStr = ""
FirstReg = ""
SecondReg = ""

InstructionByteList = []
InstructionReadableList = []

output_data = tk.Text(win, width= 20, height=20, font="Roboto 10")
output_data.place(x=250, y=50)

readable_data = tk.Text(win, width=20, height=20, font="Roboto 10")
readable_data.place(x=430, y=50)

def enableRegButtons():
    R0_Button["state"] = "normal"
    R1_Button["state"] = "normal"
    R2_Button["state"] = "normal"
    R3_Button["state"] = "normal"

def enableSubRegButtons():
    R0_ButtonSUB["state"] = "normal"
    R1_ButtonSUB["state"] = "normal"
    R2_ButtonSUB["state"] = "normal"
    R3_ButtonSUB["state"] = "normal"

def change(x):
    global firstHalfByte
    global InstructionStr

    if x == 0:
        firstHalfByte = "1000"
        InstructionStr = "Add"
        ADD_Button["state"] = "disabled"
        SHR_Button["state"] = "normal"
    if x == 1:
        firstHalfByte = "1001"
        InstructionStr = "Shift right"
        SHR_Button["state"] = "disabled"
        ADD_Button["state"] = "normal"

    enableRegButtons()

def disableAll():
    R0_Button["state"] = "disabled"
    R1_Button["state"] = "disabled"
    R2_Button["state"] = "disabled"
    R3_Button["state"] = "disabled"

    R0_ButtonSUB["state"] = "disabled"
    R1_ButtonSUB["state"] = "disabled"
    R2_ButtonSUB["state"] = "disabled"
    R3_ButtonSUB["state"] = "disabled"



def submit_data():
    if firstHalfByte != "":
        InstructionByteList.append(finalByte)
        InstructionReadableList.append(finalInstStr)
        print(InstructionByteList)
        print(InstructionReadableList)
        disableAll()
        SHR_Button["state"] = "normal"
        ADD_Button["state"] = "normal"

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
    enableSubRegButtons()

def changeBits2(x):
    global RegisterBit_2
    global SecondReg
    global finalInstStr
    global finalByte
    output_data.delete('1.0', tk.END)
    readable_data.delete('1.0', tk.END)
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
    finalInstStr = InstructionStr + " " + FirstReg + " -> " +SecondReg
    #InstructionByteList.append(finalByte)
    output_data.insert(tk.INSERT, finalByte + "\n")
    readable_data.insert(tk.INSERT, finalInstStr)
    #output_data.insert(tk.INSERT, RegisterBit_1)
    #output_data.insert(tk.INSERT, RegisterBit_2)
    #print(output_data[0])


#Buttons_Label = tk.Label(win, text="Instruction Buttons")
#Buttons_Label.place(x=0, y=30)

R0_ButtonSUB = tk.Button(win, text="R0", font="Roboto 7", command=lambda: changeBits2(0))
R0_ButtonSUB.place(x=100, y=80)

R1_ButtonSUB = tk.Button(win, text="R1", font="Roboto 7", command=lambda: changeBits2(1))
R1_ButtonSUB.place(x=125, y=80)

R2_ButtonSUB = tk.Button(win, text="R2", font="Roboto 7", command=lambda: changeBits2(2))
R2_ButtonSUB.place(x=150, y=80)

R3_ButtonSUB = tk.Button(win, text="R3", font="Roboto 7", command=lambda: changeBits2(3))
R3_ButtonSUB.place(x=175, y=80)


R0_Button = tk.Button(win, text="R0", font="Roboto 7", command=lambda: changeBits(0))
R0_Button.place(x=100, y=50)

R1_Button = tk.Button(win, text="R1", font="Roboto 7", command=lambda: changeBits(1))
R1_Button.place(x=125, y=50)

R2_Button = tk.Button(win, text="R2", font="Roboto 7", command=lambda: changeBits(2))
R2_Button.place(x=150, y=50)

R3_Button = tk.Button(win, text="R3", font="Roboto 7", command=lambda: changeBits(3))
R3_Button.place(x=175, y=50)

R0_Button["state"] = "disabled"
R1_Button["state"] = "disabled"
R2_Button["state"] = "disabled"
R3_Button["state"] = "disabled"

R0_ButtonSUB["state"] = "disabled"
R1_ButtonSUB["state"] = "disabled"
R2_ButtonSUB["state"] = "disabled"
R3_ButtonSUB["state"] = "disabled"

ADD_Button = tk.Button(win, text="ADD", font="Roboto 10", command=lambda: change(0))
ADD_Button.place(x=50, y=50)

SHR_Button = tk.Button(win, text="SHR", font="Roboto 10", command=lambda: change(1))
SHR_Button.place(x=50, y=80)

Submit_Button = tk.Button(win, text="Enter", font= "Roboto 10", command=submit_data)
Submit_Button.place(x=250, y = 10)

print(RegisterBit_1)


win.mainloop()