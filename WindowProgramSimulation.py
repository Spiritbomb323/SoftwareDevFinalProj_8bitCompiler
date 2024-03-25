import tkinter as tk
import math


def simulateProgram(InstList, InstByteList, tick):
    Sim_win = tk.Tk()
    Sim_win.geometry("320x300")
    Sim_win.title("Simulate")

    global index
    global Reg0
    global Reg1
    global Reg2
    global Reg3
    index = 0
    Reg0 = 0
    Reg1 = 0
    Reg2 = 0
    Reg3 = 0

    ticSpeed = int(tick * 1000)

    dict = {
        "R0": Reg0,
        "R1": Reg1,
        "R2": Reg2,
        "R3": Reg3
    }

    RAM = [""] * 255
    for y in range(len(InstList)):
        RAM[y] = InstList[y]

    #print(RAM)
    


    

    Reg0_label = tk.Label(Sim_win, font="Roboto 10", text="Register 0")
    Reg1_label = tk.Label(Sim_win, font="Roboto 10", text="Register 1")
    Reg2_label = tk.Label(Sim_win, font="Roboto 10", text="Register 2")
    Reg3_label = tk.Label(Sim_win, font="Roboto 10", text="Register 3")

    Reg0_label.place(x=20, y=20)
    Reg1_label.place(x=90, y=20)
    Reg2_label.place(x=160, y=20)
    Reg3_label.place(x=230, y=20)

    Reg0_text = tk.Text(Sim_win, width= 8, height= 1, font="Roboto 10")
    Reg1_text = tk.Text(Sim_win, width= 8, height= 1, font="Roboto 10")
    Reg2_text = tk.Text(Sim_win, width= 8, height= 1, font="Roboto 10")
    Reg3_text = tk.Text(Sim_win, width= 8, height= 1, font="Roboto 10")

    Reg0_text.place(x=20, y=50)
    Reg1_text.place(x=90, y=50)
    Reg2_text.place(x=160, y=50)
    Reg3_text.place(x=230, y=50)


    def byteToNum(x):
        accum = 0
        BinValues = [128, 64, 32, 16, 8, 4, 2, 1]
        for num in range(len(x)):
            if x[num - 1] == "1":
                accum += BinValues[num - 1]
        return(accum)
        
    def decimalToBinary(n):
        zeroList = ["0","00","000","0000","00000","000000","0000000",]
        binary = "{0:b}".format(int(n))

        if len(binary) != 8:
            output = zeroList[7 - len(binary)] + binary     
            return output
        else:
            return binary

    #byteToNum("00101010")
            


    def calculate():
        
        def setTimer():
            global index
            global timeee
            global Reg0
            global Reg1
            global Reg2
            global Reg3

            #for x in RAM:
                #if x == "":
                    #break
                #print(x)

            if index <= len(RAM) - 1 and index < len(InstList):
                print(str(index) + " " + RAM[index])
                

                words = RAM[index].split(" ")
                if words[0] == "ADD":
                    sum = dict.get(words[1]) + dict.get(words[3])
                    dict.update({words[3]: sum})
                if words[0] == "DATA":
                    nextbyte = int(RAM[index + 1])
                    dict.update({words[3]: nextbyte})
                    index += 1
                if words[0] == "Shift" and words[1] == "right":
                    #byte = InstByteList[index]
                    byte = math.floor(dict.get(words[2]) / 2)
                    dict.update({words[4]: byte})
                    #print(byte)
                    #byte2 = "0" + str(byte[:7])
                    #print(byte)
                    #print(byte2)
                    

                if words[0] == "Shift" and words[1] == "left":
                    byte = dict.get(words[2])
                    byte *= 2
                    dict.update({words[4]: byte})

                if words[0] == "NOT":
                    print("Store")

                if words[0] == "AND":
                    print("Store")

                if words[0] == "OR":
                    print("Store")

                Reg0_text.delete('1.0', tk.END)
                Reg1_text.delete('1.0', tk.END)
                Reg2_text.delete('1.0', tk.END)
                Reg3_text.delete('1.0', tk.END)

                Reg0_text.insert(tk.INSERT, dict.get("R0"))
                Reg1_text.insert(tk.INSERT, dict.get("R1"))
                Reg2_text.insert(tk.INSERT, dict.get("R2"))
                Reg3_text.insert(tk.INSERT, dict.get("R3"))
                
                #print(words)
                #if words[0] == "Jump to":
                    #nextbyte = x[index + 1]
                    #index = int(nextbyte) 
                #else:
                index += 1   
                timeee = Sim_win.after(ticSpeed, setTimer)
            else:
                Sim_win.after_cancel(timeee)
            
        timeee = Sim_win.after(ticSpeed, setTimer)
        index = 0


    sampleButton = tk.Button(Sim_win, font="Roboto 10", text="Run", command=calculate)
    sampleButton.place(x=50, y=150)

    Sim_win.mainloop()

 