# Program SI534x boards with Arduino UNO and I2C

Load the I2CUniSi534x.ino firmware in the arduino board editing first the I2C address of your silicon board (replace Si5341/4 value and edit it 
in the Write/Read and Page functions).  
Execute the arducom.py program using python3 (not tested with python2) which will open the interactive interface 
```
python3 arducom.py
```
If it doesn't work, try first to install the library *pyserial*
```
pip install pyserial
```
Generate the csv file obtained via ClockBuilder Pro (being careful to remove the Summary header from the option of
the register file (export Menù of CBPro) selecting the C option and inserting the filename. 
Afterwards you can load the I2C.in file (now regenerated), using the option L. 
Some seconds will pass before the configuration is loaded. 

# Hardware jumpers to set

All the ENB jumpers for the outputs must be set in order to have a VDD in the outputs (otherwise you won't be able 
to see the signal). By short-circuiting 2.5/3.3V pins to the center one you can get those amplitudes. If left open, the signals
will have an amplitude of ~1.8V.  
To program the clock generator via I2C, the I2C_SEL pin must be set to high using the 3.3 V signal of the Arduino and the SDA/SCLK inputs 
of the SI534x board must be connected (including a pull-up resistor of ~4 kOhm to the 3.3 V of Arduino) to the SDA/SCL pin outs of the UNO board.  
The MCU jumpers of SDA and SCLK must be disconnected for this specific purpose (J36 on Si5341 and J17 on Si5344).  
