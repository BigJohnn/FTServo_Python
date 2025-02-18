#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available SCServo model on this example : All models using Protocol SCS
# This example is tested with a SCServo(STS/SMS), and an URT
#

import sys
import os
import time

sys.path.append("..")
from scservo_sdk import *                      # Uses FTServo SDK library


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler('/dev/tty.usbmodem58FA0830591')# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sms_sts(portHandler)
    
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate 1000000
if portHandler.setBaudRate(1000000):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

scs_id= packetHandler.ReadID()
if 254 == scs_id:
    print('no valid servo connected!!')
else: 
    id=scs_id

    while True:
        # Read the current position of servo motor (ID1)
        scs_present_position, scs_present_speed, scs_comm_result, scs_error = packetHandler.ReadPosSpeed(id)
        if scs_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(scs_comm_result))
        else:
            print("[ID:%03d] PresPos:%d PresSpd:%d" % (id, scs_present_position, scs_present_speed))
        if scs_error != 0:
            print(packetHandler.getRxPacketError(scs_error))
        time.sleep(1)
        # 读取当前电流值
        scs_present_current, scs_comm_result, scs_error = packetHandler.ReadCurrent(id)
        if scs_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(scs_comm_result))
        else:
            print("[ID:%03d] PresCurrent:%d mA" % (id, scs_present_current))
        if scs_error != 0:
            print(packetHandler.getRxPacketError(scs_error))
        
        # 读取当前电压值
        scs_present_voltage, scs_comm_result, scs_error = packetHandler.ReadVoltage(id)
        if scs_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(scs_comm_result))
        else:
            print("[ID:%03d] PresVoltage:%.1f V" % (id, scs_present_voltage))
        if scs_error != 0:
            print(packetHandler.getRxPacketError(scs_error))

        # 读取当前温度值
        scs_present_temp, scs_comm_result, scs_error = packetHandler.ReadTemperature(id)
        if scs_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(scs_comm_result))
        else:
            print("[ID:%03d] PresTemp:%d °C" % (id, scs_present_temp))
        if scs_error != 0:
            print(packetHandler.getRxPacketError(scs_error))

        # 读取当前负载值
        scs_present_load, scs_comm_result, scs_error = packetHandler.ReadLoad(id)
        if scs_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(scs_comm_result))
        else:
            print("[ID:%03d] PresLoad:%.1f%%" % (id, scs_present_load))
        if scs_error != 0:
            print(packetHandler.getRxPacketError(scs_error))

        # 读取最大最小角度限制
        min_angle, max_angle, scs_comm_result, scs_error = packetHandler.ReadAngleLimits(id)
        if scs_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(scs_comm_result))
        else:
            print("[ID:%03d] 最小角度限制:%d, 最大角度限制:%d" % (id, min_angle, max_angle))
        if scs_error != 0:
            print(packetHandler.getRxPacketError(scs_error))

# Close port
portHandler.closePort()
