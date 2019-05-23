from __future__ import print_function
import time, sys, signal, atexit
from upm import pyupm_mic as upmMicrophone
from upm import pyupm_mhz16 as upmMhz16
from upm import pyupm_temperature as upmtemp
import pythonping as pp
import boto3
import socket
import datetime
from decimal import *
import pytz

yourkeyid='something'
yoursecretkeyid='something'

def main():
    dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=yourkeyid,
    aws_secret_access_key=yoursecretkeyid,
    region_name='us-east-1')
    table = dynamodb.Table('iotfinal')
    eastern = pytz.timezone('US/Eastern')
    # Instantiate a MHZ16 serial CO2 sensor on uart 0.
    # This example was tested on the Grove CO2 sensor module.
    myCO2 = upmMhz16.MHZ16(0)

    ip='192.168.1.1'
    
    ## Exit handlers ##
    # This stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit,
    # including functions from myCO2
    def exitHandler():
        print("Exiting")
        sys.exit(0)
    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)
    # make sure port is initialized properly.  9600 baud is the default.
    if (not myCO2.setupTty(upmMhz16.cvar.int_B9600)):
        print("Failed to setup tty port parameters")
        sys.exit(0)

    # Initiate the Temperature sensor object using A3
    temp = upmtemp.Temperature(3)
    
    # Attach microphone1 to analog port A0
    myMic1 = upmMicrophone.Microphone(0)
    threshContext1 = upmMicrophone.thresholdContext()
    threshContext1.averageReading = 0
    threshContext1.runningAverage = 0
    threshContext1.averagedOver = 2
    # Attach microphone2 to analog port A1
    myMic2 = upmMicrophone.Microphone(1)
    threshContext2 = upmMicrophone.thresholdContext()
    threshContext2.averageReading = 0
    threshContext2.runningAverage = 0
    threshContext2.averagedOver = 2
    # Attach microphone3 to analog port A2
    myMic3 = upmMicrophone.Microphone(2)
    threshContext3 = upmMicrophone.thresholdContext()
    threshContext3.averageReading = 0
    threshContext3.runningAverage = 0
    threshContext3.averagedOver = 2

    # Infinite loop, ends when script is cancelled
    # Repeatedly, take a sample every 2 microseconds;
    # find the average of 128 samples; and
    # print a running graph of dots as averages
    while(1):
        ######measure dealy#########
        delay=pp.verbose_ping(ip)

        ######## Get Temperature ########
        celsius = temp.value()
        ######## Get Co2 concentration ########
        if (not myCO2.getData()):
            print("Failed to retrieve data")
        else:
            outputStr = ("CO2 concentration: {0} PPM ".format(myCO2.getGas()))
            print(outputStr)
            co2 = myCO2.getGas()
        ####### microphone 1 #######
        buffer1 = upmMicrophone.uint16Array(128)
        len1 = myMic1.getSampledWindow(2, 128, buffer1)
        ####### microphone 2 #######
        buffer2 = upmMicrophone.uint16Array(128)
        len2 = myMic2.getSampledWindow(2, 128, buffer2)
        ####### microphone 3 #######
        buffer3 = upmMicrophone.uint16Array(128)
        len3 = myMic3.getSampledWindow(2, 128, buffer3)
        if len1:
            thresh1 = myMic1.findThreshold(threshContext1, 30, buffer1, len1)
            myMic1.printGraph(threshContext1)
            if(thresh1):
                print("Threshold mic1 is ", thresh1)
                #print("-----------------------------")
        if len2:
            thresh2 = myMic2.findThreshold(threshContext2, 30, buffer2, len2)
            myMic2.printGraph(threshContext2)
            if(thresh2):
                print("Threshold mic2 is ", thresh2)
                #print("-----------------------------")
        if len3:
            thresh3 = myMic3.findThreshold(threshContext3, 30, buffer3, len3)
            myMic3.printGraph(threshContext3)
            if(thresh3):
                print("Threshold mic3 is ", thresh3)
                #print("-----------------------------")
        print(int(datetime.datetime.now(eastern).strftime("%Y%m%d%H%M")))
        table.put_item(
                Item={
                    'time':int(datetime.datetime.now(eastern).strftime("%Y%m%d%H%M")),
                    'microphone1':thresh1,
                    'microphone2':thresh2,
                    'microphone3':thresh3,
                    'Co2 concentration(ppm)':int(co2),
                    'temp':celsius,
                    'delay':Decimal(delay),
                    'people':100
                }
            )
        time.sleep(60)
    
if __name__ == '__main__':
    main()

