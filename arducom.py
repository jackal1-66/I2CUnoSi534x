#!/usr/bin/python3

import serial
import time 
import argparse
import os, sys

portuno = "/dev/ttyACM0"

parser = argparse.ArgumentParser(prog='./arducom.py', description='Read/Write single registers + load and create configuration files for Silab5341/4')
parser.add_argument('-i', '--interactive', action='store_true', help='run the program in interactive mode') 
parser.add_argument('-r', '--read', nargs=2, metavar=('<page>', '<register>'), help='read register of Silab, syntax <page> <register> in hexadecimal')
parser.add_argument('-w', '--write', nargs=3, metavar=('<page>', '<register>', "<value>"), help='write register of Silab, syntax <page> <register> <value> in hexadecimal')
parser.add_argument('-L', '--load', action='store_true', help='load I2C.in file (used to fully program Silab board)')
parser.add_argument('-c', '--convert', nargs=1, metavar='<filename.csv>', type=str, help='convert .csv file to I2C.in input file')

args = parser.parse_args()

arduino = None

def write(man):
    if man == 1:
        if(args.write):
            arduino.write(b'0')
            page = args.write[0].encode()
            arduino.write(page)
            time.sleep(0.01)
            reg = args.write[1].encode()
            arduino.write(reg)    
            time.sleep(0.01)
            val = args.write[2].encode()
            arduino.write(val)
            time.sleep(0.01)    
        else:        
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

if(args.interactive == True):
    arduino = serial.Serial(port=portuno,baudrate=115200,timeout=0) #for eic /dev/ARDUINOI2C
    print("Arduino rebooting, wait 2 seconds")
    time.sleep(2)      #Necessary because Arduino reboots when the Serial communication is opened
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
            if(not os.path.isfile("I2C.in")):
                print("I2C.in file does not exist")
            write(0)    
        elif command.upper() == 'C':
            csvname = input("Select CSV filename ")
            if(not os.path.isfile(csvname)):
                print("File does not exist")
                continue
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
            print(csvname+" converted")
        else:
            print("Try with \'R\', \'W\' or \'L\'.")    
else:
    if(len(sys.argv) == 1):
        print("No arguments provided, -h for help")
        quit()
    arduino = serial.Serial(port=portuno,baudrate=115200,timeout=0) #for eic /dev/ARDUINOI2C
    print("Arduino rebooting, wait 2 seconds")
    time.sleep(2)      #Necessary because Arduino reboots when the Serial communication is opened
    if(args.read):
        arduino.write(b'1')
        page = args.read[0].encode()
        arduino.write(page)
        reg = args.read[1].encode()
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
    if(args.write):  
        write(1)
    if(args.convert):
        if(not ".csv" in args.convert[0]):
            print("Wrong file format")
            quit()  
        if(not os.path.isfile(args.convert[0])):
            print("File does not exist")
            quit()
        csvname = args.convert[0]    
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
        print(csvname+" converted")    
    if(args.load):
        if(not os.path.isfile("I2C.in")):
            print("I2C.in file does not exist")
            quit()   
        write(0)    

