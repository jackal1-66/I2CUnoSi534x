import serial
import time 

arduino = serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=0)
print("Arduino rebooting, wait 2 seconds")
time.sleep(2)

def write(man):
    if man == 1:
        arduino.write(b'0')
        page = input("Select page ").encode()
        arduino.write(page)
        reg = input("Select register ").encode()
        arduino.write(reg)    
        time.sleep(0.01)
        reg = input("Select value to Write ").encode()
        arduino.write(reg)
        time.sleep(0.1)
    else:
        print("Load function not implemented yet.")    

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
            while not '\\n'in str(data):
                time.sleep(0.1)
                temp = arduino.readline()
                if temp.decode():
                    data = (data.decode()+temp.decode()).encode()
            data = data.decode()      
            #ddata = data.decode()
            print(data)
        elif command.upper() == 'W':
            write(1)
        elif command.upper() == 'L':
            write(0)    
        else:
            print("Try with \'R\', \'W\' or \'L\'.")    