------------------------------------
Program:

This program translates user button inputs into binary (assembly instructions). The assembly instructions represent instructions to the computer that tell it to change and operate on data. This is specifically of an 8-bit computer, which uses 8-bits or a byte. 
------------------------------------
The Registers:
 
The registers include the main 4 registers (R0, R1, R2, R3) and the Sub registers which sit below the main ones. These can be found to the right of the instruction buttons. In practice, these registers hold one byte of data and can be changed by the computer.
RA = Main Registers
RB = Sub Registers 
------------------------------------
RAM memory:

Currently a superficial concept in regards to the current program, but a very important aspect of assembly instructions. RAM is just a bunch of registers that permanently store data.
Since this is based on the design of an 8-bit computer(all data is one byte long), the maximum length of RAM is only 256 registers or 256 bytes.
Instruction takes up 1 spot in RAM, instructions like DATA and JMP require an extra Byte, so technically they take up 2 spots (more on that below). Instructions like JMPR use a byte as a number in memory to jump to. JMP preceding 5 in binary would make the program jump to the 5th byte in RAM and continue to execute instructions. In this way JMP and JMPR can be used to make loops and to jump over other instructions.  
------------------------------------
The Buttons:

Almost all of these buttons also require the use of registers to function. Some require 2 registers, designated main and sub register, which are mentioned previously. All buttons that require two registers, the output of that operation is sent to the selected Sub Register. Some buttons operate on and use RAM memory.

- ADD: Takes the data in first register selected and adds it to the second register selected. R0 - 5, R1 - 6,  ADD R0 -> R1 R1 = 11 and R0 = 5

- SHR(Shift right): Shifts all the bits in the byte over one bit to the right. (1100 0000 --> 0110 0000). 

- SHL(Shift left): Shifts all the bits in the byte over one bit to the left. (0011 0000 --> 0110 0000).

- NOT: Functions similarly to the NOT logic gate. NOTs RA and puts the answer in RB (0010 1011 --> 1101 0100)

- AND: And RA and RB and put the answer in RB (0011 1111 + 0101 1011 = 0001 1011)

- OR: Or RA and RB and put answer in RB

- XOR: Exclusive OR RA and RB into RB

- CMP(Compare): Compare RA and RB. Doing so sets off flags such as Carry, A larger, Equal, and Zero flags.

- LD(Load): Load RB from RAM address in RA.

- ST(Store): Store RB to RAM address in RA. 

- DATA: Load 8 bits into RB, the 8 bits is the byte immetiately proceding the data instruction.

- JMPR(Jump register): Jump to the address in RB.

- JMP(Jump): Jump to the address thats in the next byte
.
- CLF(Clear flags): Clear any flags that were set by previous computations.

- JCAEZ(Jump if any of the selected flags are on): This can be configured any way with the 4 flags, for example JAE is Jump if a is larger or equal to B. If any flags are on it jumps to the address thats in the next byte. 

- IO(Input/Output): The IO instruction is used to interact with outside devices like a keyboard or monitor. It has four sub instructions:
   - IN DATA: input I/O data into RB
   - IN ADDR: input I/O address into RB
   - OUT DATA: output RB to I/O as Data
   - OUT ADDR: output RB to I/O as Address
In order to access other devices, OUT ADDR needs to be used along with the correct address of the device.
--------------------------------------------------------------------------
The Text Boxes: 

There are two types of text boxes, the raw binary version(left), and the more readable code(right). 
When a instruction is ready to be created, it will show up in the two boxes designated by the "Next byte:" label. Below those is the main 2 text boxes that display the current program. When the Enter button is pressed, the data from the next byte text boxes will be moved down to these text boxes. 
The number corresponding to each instruction in the text boxes represents the location of that instruction in RAM.

The reset button clears out the text boxes and resets the buttons.
--------------------------------------------------------------------------
Examples: 

Add program: 
0 - DATA R0
1 - 0000 0101 (5)
2 - DATA R1
3 - 0000 1010 (10)
4 - ADD R0, R1

Square of number Program: 
0 - DATA R0
1 - 0000 0101 (5)
2 - DATA R1
3 - 0000 0101 (5)
4 - DATA R3
5 - 0000 0001 (1)
6 - CLF
7 - CMP R0, R2
8 - JE
9 - 0000 1110 (address 14)
10 - ADD R0, R1
11 - ADD R3, R2
12 - JMP
13 - 0000 0110 (address 6)
14 - end of program
