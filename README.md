# FTServo_Python
FEETECH BUS Servo Python library

cd sms_sts

修改read/write.py中

```
portHandler = PortHandler('/dev/[你的串口名]')# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
```

读取舵机状态信息

```
python read.py
```

写入舵机配置/控制指令

```
python write.py
```

中位校准

```
python set_2048.py
```

设置最大最小角度限制(在脚本中修改数值)

```
python set_angle_limits.py
```