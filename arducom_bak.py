import serial
import time 

arduino = serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=0)
print("Arduino rebooting, wait 2 seconds")
time.sleep(2)

def read(address):
    arduino.write(b'1')
    time.sleep(0.01)
    arduino.write(address)
    time.sleep(0.01)
    data = (arduino.readline()).decode()
    return data

while True:
        print("Enter R to read register 0x0B")
        command = input()
        if command.upper() == 'R':
            arduino.write(b'1')
            #page = input("Select page ").encode()
            #print(page, b'1')
            #arduino.write(page)
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
            data = 0
        else:
            print("Try with \'R\'.")    