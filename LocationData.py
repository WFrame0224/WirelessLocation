# -*- coding: utf-8 -*

"""
    此程序实现收到节点的定位数据
"""
import sys
import serial
import time
import os


class LocationData():
    '''
        此类为定位节点的数据汇总，保存在指定的txt文件夹中
    '''

    def __init__(self, AnchorInfo, serial_port='COM7',serial_baud=9600):
        '''
        serial_baud:波特率，AnchorInfo:是一个列表，按照节点的顺序排列
       '''
        self.serial_baud = serial_baud
        self.serial_port = serial_port
        self.AnchorInfo = AnchorInfo
        # 串口实例化 
        self.nodes = serial.Serial(self.serial_port,self.serial_baud)
        # 设置停止等待时间，超时后进行下一次接收
        self.nodes.timeout = 1
#         self.nodes.write_timeout = 1    
        # 清除接收缓存区
        self.nodes.flushInput()
        # 清除接收发送缓存区
        self.nodes.flushOutput()
        
    def get_location_data(self):
        '''
                此程序实现定位数据的读取与保存
                返回：读到的数据长度，和数据存储区
        '''
        self.RxData_buf = b''
#         self.RxData_len = len(self.AnchorInfo) * 45
#         RxData_buf = self.nodes.read(self.RxData_len)
        for i in range(0,len(self.AnchorInfo)):
            self.RxData_buf += self.nodes.read(45) 
        # 清除缓存区，准备下一次接收
        self.nodes.flushInput()
        
        return len(self.RxData_buf.decode()) , self.RxData_buf.decode()
    
    def send_commd(self):
        '''
            发送读取RSSI读取命令'ba01ba'，连发10次，间隔50ms, 之后再发一次‘get’
        '''
        self.Tx_commd = 'ba'
        self.RssiNum = 10
        for i in range(1,self.RssiNum):
            commd = self.Tx_commd + '0' + str(i) + self.Tx_commd
            self.nodes.write(str.encode(commd))    # 发送通信数据，给节点读取RSSI
            time.sleep(0.05)
            # 清除发送缓存区
            self.nodes.flushOutput()
        # 数量少一次，再补一次
        commd = self.Tx_commd + str(10) + self.Tx_commd
        self.nodes.write(str.encode(commd))
        time.sleep(0.05)
        # 清除发送缓存区
        self.nodes.flushOutput()
        
        self.get_Rssi_commd()
        
    
    def get_Rssi_commd(self):
        self.Rx_commd = 'get'
        # 发送数据读取命令，等待节点发送回来RSSI
        self.nodes.write(str.encode(self.Rx_commd))
        time.sleep(0.05)
        # 清除发送缓存区
        self.nodes.flushOutput()
    
    def saveData2File(self,Savefilename,Datastream):
        '''
                将读取的数据保存在文件名为‘Savefilename’的文件中，文件名以云台的坐标位置为准
        '''
        if not(os.path.exists(Savefilename) and os.path.isfile(Savefilename)):
            with open(Savefilename,'w') as file_object:
                file_object.write(Datastream)
                file_object.write("\n")
        else:
            with open(Savefilename,'a') as file_object:
                file_object.write(Datastream)
                file_object.write("\n")

    def mkdir1(self,path):
        folder = os.path.exists(path)
 
        if not folder:                      #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)                #makedirs 创建文件时如果路径不存在会创建这个路径
            print("---  new folder...  ---")
            print("---  OK  ---")
     
        else:
            print("---  There is this folder!  ---")
    @staticmethod
    def mkdir(path):
        folder = os.path.exists(path)
 
        if not folder:                      #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)                #makedirs 创建文件时如果路径不存在会创建这个路径
            print("---  new folder...  ---")
            print("---  OK  ---")
     
        else:
            print("---  There is this folder!  ---")

    



        
        

    

        
        
        
        
