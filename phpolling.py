import string
import pylibftdi
import alerting as alerting
import ftdi as ftdi
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError
from pylibftdi import Driver
import time
import datetime as dt
import os

if __name__ == '__main__':

    real_raw_input = vars(__builtins__).get('raw_input', input) # used to find the correct function for python2/3
    print("Discovered FTDI serial numbers:")

    devices = ftdi.get_ftdi_device_list()
    cnt_all = len(devices)
    
    #print "\nIndex:\tSerial: "
    for i in range(cnt_all):
            print(  "\nIndex: ", i, " Serial: ", devices[i])
    print( "===================================")

    index = 0
    while True:
        index = real_raw_input("Please select a device index: ")
        try:
            dev = ftdi.AtlasDevice(devices[int(index)])
            break
        except pylibftdi.FtdiError as e:
            print( "Error, ", e)
            print( "Please input a valid index")

    print( "")
    print(">> Opened device ", devices[int(index)])
    print(">> Any commands entered are passed to the board via FTDI:")

    time.sleep(1)
    dev.flush()
    
    
    while True:
        input_val = real_raw_input("Enter command (HINT: POLL command will begin pH polling): ")
    
        # continuous polling command automatically polls the board
        if input_val.upper().startswith("POLL"):
            # Get user input for a variety of configuration items
            min_ph = float(real_raw_input("Enter minimum pH threshold for alerting (e.g. for value of 5.5, pH readings below 5.5 will trigger alert)"))
            max_ph = float(real_raw_input("Enter maximum pH threshold for alerting (e.g. for value of 7.5, pH readings above 7.5 will trigger alert)"))
            delaytime = float(real_raw_input("Enter polling interval (seconds)"))
            throttle = float(real_raw_input("Enter minimum interval between alerts (seconds)"))

            dev.send_cmd("C,0") # turn off continuous mode
            #clear all previous data
            time.sleep(1)
            dev.flush()
            
            # Read back the user input configuration values
            print("Polling sensor every %0.2f seconds, alerting on pH values outside the range (%0.2f, %0.2f), messaging throttle set to %0.2f seconds, press ctrl-c to stop polling" % (delaytime,min_ph,max_ph,throttle))

            try:
                sender = alerting.AlertSender()
                while True:
                    dev.send_cmd("R")
                    lines = dev.read_lines()
                    for i in range(len(lines)):
                        if lines[i][0] != '*':
                            ph_measurement = lines[i]
                            if float(ph_measurement) < min_ph or float(ph_measurement) > max_ph:
                                sender.send_alert(ph_measurement, throttle)
                            print("Response: " , lines[i])
                    time.sleep(delaytime)

            except KeyboardInterrupt:       # catches the ctrl-c command, which breaks the loop above
                print("Continuous polling stopped")

    else:
        # pass commands straight to board
        if len(input_val) == 0:
            lines = dev.read_lines()
            for i in range(len(lines)):
                print( lines[i])
        else:
            dev.send_cmd(input_val)
            time.sleep(1.3)
            lines = dev.read_lines()
            for i in range(len(lines)):
                print( lines[i])

    
