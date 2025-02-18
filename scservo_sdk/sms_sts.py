#!/usr/bin/env python

from .scservo_def import *
from .protocol_packet_handler import *
from .group_sync_read import *
from .group_sync_write import *

#波特率定义
SMS_STS_1M = 0
SMS_STS_0_5M = 1
SMS_STS_250K = 2
SMS_STS_128K = 3
SMS_STS_115200 = 4
SMS_STS_76800 = 5
SMS_STS_57600 = 6
SMS_STS_38400 = 7

#内存表定义
#-------EPROM(只读)--------
SMS_STS_MODEL_L = 3
SMS_STS_MODEL_H = 4

#-------EPROM(读写)--------
SMS_STS_ID = 5
SMS_STS_BAUD_RATE = 6
SMS_STS_MIN_ANGLE_LIMIT_L = 9
SMS_STS_MIN_ANGLE_LIMIT_H = 10
SMS_STS_MAX_ANGLE_LIMIT_L = 11
SMS_STS_MAX_ANGLE_LIMIT_H = 12
SMS_STS_CW_DEAD = 26
SMS_STS_CCW_DEAD = 27
SMS_STS_OFS_L = 31
SMS_STS_OFS_H = 32
SMS_STS_MODE = 33

#-------SRAM(读写)--------
SMS_STS_TORQUE_ENABLE = 40
SMS_STS_ACC = 41
SMS_STS_GOAL_POSITION_L = 42
SMS_STS_GOAL_POSITION_H = 43
SMS_STS_GOAL_TIME_L = 44
SMS_STS_GOAL_TIME_H = 45
SMS_STS_GOAL_SPEED_L = 46
SMS_STS_GOAL_SPEED_H = 47
SMS_STS_LOCK = 55

#-------SRAM(只读)--------
SMS_STS_PRESENT_POSITION_L = 56
SMS_STS_PRESENT_POSITION_H = 57
SMS_STS_PRESENT_SPEED_L = 58
SMS_STS_PRESENT_SPEED_H = 59
SMS_STS_PRESENT_LOAD_L = 60
SMS_STS_PRESENT_LOAD_H = 61
SMS_STS_PRESENT_VOLTAGE = 62
SMS_STS_PRESENT_TEMPERATURE = 63
SMS_STS_MOVING = 66
SMS_STS_PRESENT_CURRENT_L = 69
SMS_STS_PRESENT_CURRENT_H = 70

class sms_sts(protocol_packet_handler):
    def __init__(self, portHandler):
        protocol_packet_handler.__init__(self, portHandler, 0)
        self.groupSyncWrite = GroupSyncWrite(self, SMS_STS_ACC, 7)

    def WritePosEx(self, scs_id, position, speed, acc):
        txpacket = [acc, self.scs_lobyte(position), self.scs_hibyte(position), 0, 0, self.scs_lobyte(speed), self.scs_hibyte(speed)]
        return self.writeTxRx(scs_id, SMS_STS_ACC, len(txpacket), txpacket)

    def ReadPos(self, scs_id):
        scs_present_position, scs_comm_result, scs_error = self.read2ByteTxRx(scs_id, SMS_STS_PRESENT_POSITION_L)
        return self.scs_tohost(scs_present_position, 15), scs_comm_result, scs_error

    def ReadSpeed(self, scs_id):
        scs_present_speed, scs_comm_result, scs_error = self.read2ByteTxRx(scs_id, SMS_STS_PRESENT_SPEED_L)
        return self.scs_tohost(scs_present_speed, 15), scs_comm_result, scs_error

    def ReadPosSpeed(self, scs_id):
        scs_present_position_speed, scs_comm_result, scs_error = self.read4ByteTxRx(scs_id, SMS_STS_PRESENT_POSITION_L)
        scs_present_position = self.scs_loword(scs_present_position_speed)
        scs_present_speed = self.scs_hiword(scs_present_position_speed)
        return self.scs_tohost(scs_present_position, 15), self.scs_tohost(scs_present_speed, 15), scs_comm_result, scs_error

    def ReadMoving(self, scs_id):
        moving, scs_comm_result, scs_error = self.read1ByteTxRx(scs_id, SMS_STS_MOVING)
        return moving, scs_comm_result, scs_error

    def SyncWritePosEx(self, scs_id, position, speed, acc):
        txpacket = [acc, self.scs_lobyte(position), self.scs_hibyte(position), 0, 0, self.scs_lobyte(speed), self.scs_hibyte(speed)]
        return self.groupSyncWrite.addParam(scs_id, txpacket)

    def RegWritePosEx(self, scs_id, position, speed, acc):
        txpacket = [acc, self.scs_lobyte(position), self.scs_hibyte(position), 0, 0, self.scs_lobyte(speed), self.scs_hibyte(speed)]
        return self.regWriteTxRx(scs_id, SMS_STS_ACC, len(txpacket), txpacket)

    def RegAction(self):
        return self.action(BROADCAST_ID)

    def WheelMode(self, scs_id):
        return self.write1ByteTxRx(scs_id, SMS_STS_MODE, 1)

    def WriteSpec(self, scs_id, speed, acc):
        speed = self.scs_toscs(speed, 15)
        txpacket = [acc, 0, 0, 0, 0, self.scs_lobyte(speed), self.scs_hibyte(speed)]
        return self.writeTxRx(scs_id, SMS_STS_ACC, len(txpacket), txpacket)

    def LockEprom(self, scs_id):
        return self.write1ByteTxRx(scs_id, SMS_STS_LOCK, 1)

    def unLockEprom(self, scs_id):
        return self.write1ByteTxRx(scs_id, SMS_STS_LOCK, 0)

    def ReadCurrent(self, scs_id):
        """
        读取实时电流值（单位：mA）
        返回：电流值(有符号), 通信结果, 错误码
        """
        # 读取两个字节的原始电流数据（69-70地址）
        raw_current, scs_comm_result, scs_error = self.read2ByteTxRx(scs_id, SMS_STS_PRESENT_CURRENT_L)
        
        # 假设6.5mA/bit的转换比例（具体需参考手册）
        current = self.scs_tohost(raw_current, 15) * 6.5  # 15表示16位有符号数
        return current, scs_comm_result, scs_error

    def ReadVoltage(self, scs_id):
        """
        读取实时电压（单位：0.1V）
        返回：电压值, 通信结果, 错误码
        """
        voltage, result, error = self.read1ByteTxRx(scs_id, SMS_STS_PRESENT_VOLTAGE)
        return voltage * 0.1, result, error  # 根据手册实际转换比例调整

    def ReadTemperature(self, scs_id):
        """
        读取实时温度（单位：摄氏度）
        返回：温度值, 通信结果, 错误码
        """
        return self.read1ByteTxRx(scs_id, SMS_STS_PRESENT_TEMPERATURE)

    def ReadLoad(self, scs_id):
        """
        读取实时负载（单位：%）
        返回：负载百分比(有符号), 通信结果, 错误码
        """
        raw_load, result, error = self.read2ByteTxRx(scs_id, SMS_STS_PRESENT_LOAD_L)
        # 转换为有符号百分比（正=逆时针负载，负=顺时针负载）
        load_percent = self.scs_tohost(raw_load, 15) * 0.1  # 根据手册调整比例系数
        return load_percent, result, error

    def ReadID(self):
        """
        读取舵机ID
        参数:
            scs_id: 舵机ID,默认为广播ID(0xFE)
        返回：ID值, 通信结果, 错误码
        """
        return self.scan_ids()

    def ReadAngleLimits(self, scs_id):
        """
        读取舵机最大最小角度限制
        返回：最小角度, 最大角度, 通信结果, 错误码
        """
        # 读取最小角度限制(2字节)
        min_angle, result1, error1 = self.read2ByteTxRx(scs_id, SMS_STS_MIN_ANGLE_LIMIT_L)
        
        # 读取最大角度限制(2字节) 
        max_angle, result2, error2 = self.read2ByteTxRx(scs_id, SMS_STS_MAX_ANGLE_LIMIT_L)

        # 返回通信错误中较严重的一个
        if result1 != COMM_SUCCESS:
            return min_angle, max_angle, result1, error1
        elif result2 != COMM_SUCCESS:
            return min_angle, max_angle, result2, error2
            
        return min_angle, max_angle, COMM_SUCCESS, 0
    
    def WriteAngleLimits(self, scs_id, min_angle, max_angle):
        """
        设置舵机最大最小角度限制
        参数:
            scs_id: 舵机ID
            min_angle: 最小角度限制值(0~4095)
            max_angle: 最大角度限制值(0~4095)
        返回: 通信结果, 错误码
        """
        # 写入最小角度限制(2字节)
        result1, error1 = self.write2ByteTxRx(scs_id, SMS_STS_MIN_ANGLE_LIMIT_L, min_angle)
        
        # 写入最大角度限制(2字节)
        result2, error2 = self.write2ByteTxRx(scs_id, SMS_STS_MAX_ANGLE_LIMIT_L, max_angle)
        
        # 返回通信错误中较严重的一个
        if result1 != COMM_SUCCESS:
            return result1, error1
        return result2, error2
    
    def TorqueEnable(self, scs_id, enable):
        """
        设置舵机扭矩开关
        参数:
            scs_id: 舵机ID
            enable: 0=关闭扭力输出, 1=打开扭力输出, 128=当前位置校正为2048
        返回: 通信结果, 错误码
        """
        return self.write1ByteTxRx(scs_id, SMS_STS_TORQUE_ENABLE, enable)