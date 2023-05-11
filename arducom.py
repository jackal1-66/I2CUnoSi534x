import serial
import time 

arduino = serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=0)
print("Arduino rebooting, wait 2 seconds")
time.sleep(2)      #Necessary because Arduino reboots when the Serial communication is opened

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
        time.sleep(0.1)
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
                arduino.write(b'0')
                page = inputs[0].encode()
                arduino.write(page)
                time.sleep(0.01)
                reg = inputs[1].encode()
                arduino.write(reg)    
                time.sleep(0.01)
                val = inputs[2].encode()
                arduino.write(val)
                time.sleep(0.1)
                del inputs
        if(check):        
            print("Registers loaded from file.") 
        else:
            print("Error in loading registers")
            print("Check line "+str(cycle)+ " of I2C.in")           

while True:
        print("Enter R to read, W to write, or L to load file")
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
        else:
            print("Try with \'R\', \'W\' or \'L\'.")    