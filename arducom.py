#!/usr/bin/python3

import serial
import time 
import argparse

arduino = serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=0) #for eic /dev/ARDUINOI2C
print("Arduino rebooting, wait 2 seconds")
time.sleep(2)      #Necessary because Arduino reboots when the Serial communication is opened

parser = argparse.ArgumentParser(prog='I2C Silab Programmer', description='Read/Write, Load and create configuration files for Silab5341/4')
parser.add_argument('-i', '--interactive', action='store_true', help='Run the program in interactive mode')  # Set interactive program

def write(man):
    if man == 1:
        arduino.write(b'0')
        page = input("Select page ").encode()
        arduino.write(page)
        time.sleep(0.01)
        reg = input("Select register ").encode()
        arduino.write(reg)    
        time.sleep(0.01)
        val = input("Select value to Write ").encode()
        arduino.write(val)
        time.sleep(0.01)
    else:
        #This function gets all the lines in file "I2C.in" and write the register in a loop
        #The syntax of the file is page, register and value to write. 
        filename = "I2C.in"
        cycle = -1
        with open(filename) as file:
            for line in file:
                cycle += 1
                inputs = line.split()
                check = True
                errline = -1
                if(len(inputs) == 3):
                    for var in inputs:
                        if int(var,16) > 0xFF:
                            print("Wrong syntax on file.")
                            check = False
                            break
                else:
                    print("Wrong syntax on file.")
                    check = False 
                if(not check):
                    break         
                arduino.write(b'7')
                if((inputs[0] == "B" or inputs[0] == "0B") and inputs[1] == "4E" and inputs[2] == "1A"):
                    time.sleep(0.3) #needed when resetting PLL before setting peculiar registers for Si5341
                if((inputs[0] == "5" or inputs[0] == "05") and inputs[1] == "40" and (inputs[2] == "1" or inputs[2] == "01")):  
                    time.sleep(0.3) #needed when resetting PLL before setting peculiar registers for Si5344  
                page = (inputs[0]+'\r').encode()
                arduino.write(page)
                time.sleep(0.01)
                reg = (inputs[1]+'\r').encode()
                arduino.write(reg)    
                time.sleep(0.01)
                val = (inputs[2]+'\r').encode()
                arduino.write(val)
                time.sleep(0.01)
                del inputs
        if(check):        
            print("Registers loaded from file.") 
        else:
            print("Error in loading registers")
            print("Check line "+str(cycle)+ " of I2C.in")

if(parser.interactive == True):
    while True:
            print("Enter R to read, W to write, L to load file or C to generate input file from CSV")
            command = input()
            if command.upper() == 'R':
                arduino.write(b'1')
                page = input("Select page ").encode()
                arduino.write(page)
                reg = input("Select register ").encode()
                arduino.write(reg)
                print("Register Read")
                time.sleep(0.1)
                data = arduino.readline()
                while not '\\n'in str(data):    #if this is not implemented data read is not always successful
                    time.sleep(0.1)
                    temp = arduino.readline()
                    if temp.decode():
                        data = (data.decode()+temp.decode()).encode()
                data = data.decode()      
                print(data)
            elif command.upper() == 'W':
                write(1)
            elif command.upper() == 'L':
                write(0)    
            elif command.upper() == 'C':
                csvname = input("Select CSV filename ")
                filei2c = open("I2C.in", "w")
                with open(csvname) as csv:
                    for line in csv:           
                        if ("#" in line) or ("Address" in line):
                            continue
                        treg = line.split(',')
                        tadd = treg[0][2:]
                        page = tadd[:2]
                        register = tadd[2:]
                        val = treg[1][2:]
                        filei2c.write(page+' '+register+' '+val)
                        del treg, tadd, page, register, val
                filei2c.close()        
            else:
                print("Try with \'R\', \'W\' or \'L\'.")    