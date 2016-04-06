#!/usr/bin/env python

#Simple example on how to send and receive data to the Mbed over USB (on Linux) using pyUSB 1.0

import os
import sys
import rospy
import usb.core
import usb.util
from geometry_msgs.msg import Twist
from time import sleep
import random

t = float(0)

def callback(msg):
    global t
    rospy.loginfo("Received a /float message!")
    t = msg
 
# handler called when a report is received
def rx_handler(data):
    print 'recv: ', data        
 
def findHIDDevice(mbed_vendor_id, mbed_product_id):
    global t
    rospy.init_node('linear_pos_listener')
    rospy.Subscriber("/linear_pos", float, callback)
    # Find device
    hid_device = usb.core.find(idVendor=mbed_vendor_id,idProduct=mbed_product_id)
    while not rospy.is_shutdown():

        if not hid_device:
            print "No device connected"
        else:
            sys.stdout.write('mbed found\n')
            if hid_device.is_kernel_driver_active(0):
                try:
                    hid_device.detach_kernel_driver(0)
                except usb.core.USBError as e:
                    sys.exit("Could not detatch kernel driver: %s" % str(e))
            try:
                hid_device.set_configuration()
                hid_device.reset()
            except usb.core.USBError as e:
                sys.exit("Could not set configuration: %s" % str(e))
        
            endpoint = hid_device[0][(0,0)][0]      
        
            while True:
                data = "%.2f"%(t)
                        
                #read the data
                bytes = hid_device.read(endpoint.bEndpointAddress, 8)
                rx_handler(bytes)
 
                hid_device.write(1, data)
 
if __name__ == '__main__':
    # The vendor ID and product ID used in the Mbed program
    mbed_vendor_id = 0x1234 
    mbed_product_id = 0x0006
 
    # Search the Mbed, attach rx handler and send data
    findHIDDevice(mbed_vendor_id, mbed_product_id)
