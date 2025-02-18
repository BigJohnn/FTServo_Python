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

# 中位校准核心代码
try:
    # 移动到中位位置（2048）
    res, err = packetHandler.TorqueEnable(scs_id=scs_id, enable=128)
    if res != COMM_SUCCESS:
        print("校准失败: " + packetHandler.getTxRxResult(res))
        quit()
    elif err != 0:
        print("舵机返回错误: " + packetHandler.getRxPacketError(err))
        quit()
    else:
        print("中位校准成功,当前位置已设为2048")
        
except KeyboardInterrupt:
    print("\n校准中断")
finally:
    portHandler.closePort()