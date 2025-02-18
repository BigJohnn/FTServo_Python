import sys
sys.path.append("..")
from scservo_sdk import *

# 初始化端口（保持与write.py相同配置）
portHandler = PortHandler('/dev/tty.usbmodem58FA0830591')
packetHandler = sms_sts(portHandler)

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

scs_id = packetHandler.ReadID()
if scs_id == 254:
    print('未检测到有效舵机!')
    quit()

try:
    res, err = packetHandler.WriteAngleLimits(scs_id=scs_id, min_angle=1950, max_angle=2200)
    if res != COMM_SUCCESS:
        print("通信错误: %s" % packetHandler.getTxRxResult(res))
        quit()
    elif err != 0:
        print("舵机错误: %s" % packetHandler.getRxPacketError(err))
        quit()
    else:
        print("[ID:%03d] 成功设置角度限制 - 最小角度:%d, 最大角度:%d" % (scs_id, 1950, 2200))
        
except KeyboardInterrupt:
    print("\n校准中断")
finally:
    portHandler.closePort()