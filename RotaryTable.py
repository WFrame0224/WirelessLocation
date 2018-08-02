#-*- coding: utf-8 -*

# 此程序为与转台通信，向转台发送转动命令

import serial
import serial.tools.list_ports
import time
import json




class RotaryTable():
     
    '''
        此类创建一个转台相关的类，用于实现转台的自由控制
    '''
    
    def __init__(self,serial_port='COM5', serial_baud=9600, angle_MAX=360, angle_MIN=0):
        
        ## 转台通信参数设置 ##
        # 设置转台波特率
        self.serila_baud = serial_baud
        # 设置转台端口
        self.serial_port = serial_port
        # 实例化转台通信端口
        self.RT = serial.Serial(self.serial_port,self.serila_baud)
        
        ### 转台物理参数设置 ###
        # 设置转台的旋转方向
        self.RT_dir = '0'
        # 设置转台最大最小角度
        self.__angle_MAX = angle_MAX
        self.__angle_MIN = angle_MIN
        # 设置电机旋转时间消耗
        self.__rotate_Time = 1
    
    def set_rotate_Time(self,rotate_Time):
        # 设置电机旋转时间消耗
        self.__rotate_Time =  rotate_Time  
    
    def get_angle(self):
        """
            从文件中得到当前角度
        """
        filename = 'current_angle.json'
        with open(filename) as f_obj:
            angle = json.load(f_obj)
        return angle

    def update_angle(self):
        """
            更新当前角度，并保存至文件中
        """
        filename = 'current_angle.json'
        with open(filename, 'w') as f_obj:
            json.dump(self.currentAngle, f_obj)

    def set_angle(self,angle):
        """
            可以使用该函数设置初始角度，不过你要先调用这个函数
        """
        filename = 'current_angle.json'
        with open(filename, 'w') as f_obj:
            json.dump(angle, f_obj)
    
    def rotate(self,RT_angle):
        '''
                此函数实现,转台的某个角度转动
        '''
        self.commd = 'ab' + self.RT_dir + str(RT_angle) + 'ab'
#         self.RT.write(str.encode(self.commd))
    
        # 电机转动的时间消耗
        if RT_angle == 3:
            time.sleep(self.__rotate_Time + 0.5)
        elif RT_angle == 6:
            time.sleep(self.__rotate_Time * 2 + 0.5)
        else:
            time.sleep(self.__rotate_Time * 3 + 0.5)
            
        # 清除发送缓存区
        self.RT.flushOutput()
    
    def rotate_clock(self,RT_angle):
        '''
            此程序实现转台顺时针旋转
        '''
        # 判断设置角度是否合法，目前硬件只是支持3,6,9度的设置
        if RT_angle in [3,6,9]:
            self.D_angle = RT_angle
        else:
            print('angle setting error')
            return -1
            # -----此处需要异常处理
            
        self.RT_dir = '1'
        # 得到当前角度
        self.currentAngle = self.get_angle()
#         if (self.currentAngle == self.__angle_MAX):
#             # self.RT_dir = '0'
#             print('-------------------Setting OverMAX------------------')
#             # raise MotorError('OverMAX!',self.currentAngle)
#             roate_status = False
#             return roate_status
#         elif (self.currentAngle + self.D_angle > self.__angle_MAX):
#             self.rotate(self.__angle_MAX - self.currentAngle)
#             self.currentAngle = self.__angle_MAX
#             # self.RT_dir = '0'
#             roate_status = True
#         else:
        self.rotate(self.D_angle)
        self.currentAngle = self.currentAngle + self.D_angle
        roate_status = True
        
        # 更新并保存当前角度
        self.update_angle()
            
        return roate_status
        
    def rotate_anticlock(self,RT_angle):
        '''
            此程序实现转台逆时针旋转
        '''   
        if RT_angle in [3,6,9]:
            self.D_angle = RT_angle
        else:
            print('angle setting error')
            return -1
            # -----此处需要异常处理
        
        self.RT_dir = '0'
        # 得到当前角度
        self.currentAngle = self.get_angle()
#         if (self.currentAngle == self.__angle_MIN):
#             # self.RT_dir = '1'
#             print('---------------Setting OverMIN!------------------')
#             # raise MotorError('OverMIN!',self.currentAngle)
#             rotate_status = False
#             return rotate_status
#         elif (self.currentAngle - self.D_angle < self.__angle_MIN):
#             self.rotate(self.currentAngle - self.__angle_MIN)
#             self.currentAngle = self.__angle_MIN
#             # self.RT_dir = '1'
#             rotate_status = True
#         else:
        self.rotate(self.D_angle)
        self.currentAngle = self.currentAngle - self.D_angle
        rotate_status = True
        
        # 更新并保存当前角度
        self.update_angle()
            
        return rotate_status
       
    def RT_rotate(self,RT_dir,RT_angle):
        '''
            用于实现顺时针与逆时针方向转台角度的旋转
        '''
        # 检查旋转方向
        if RT_dir == 1:
            self.RT_dir = '1'
            self.rotate_clock(RT_angle)
        elif RT_dir == -1:
            self.RT_dir = '0'
            self.rotate_anticlock(RT_angle)
        else:
            raise MotorError('Dir seeting error!')
    
    def RT_rotate2_initANGLE(self, initAngle=0):
        '''
            本程序实现根据当前保存的角度值，将转台的转至期望的初始角度
            initAngle:转台的初始角度
        '''
        # 首先判断角度的合理性
        if (initAngle > self.__angle_MAX) or (initAngle < self.__angle_MIN):
            print('初始角度设置有误！！！！请重新设置')
            return
        
        self.__ANGLE = initAngle
        
        # 读取当前的角度
        self.currentAngle = self.get_angle()
        # 进行角度判断并回转
        if self.__ANGLE > self.currentAngle:                # 如果期望的初始角度 > 当前角度，则应该反转
            while not (self.get_angle() ==  self.__ANGLE):
                self.RT_rotate(1, 3)
                print('-------------' + str(self.get_angle()) + '----------------')
        else:
            while not (self.get_angle() ==  self.__ANGLE): # 如果期望的初始角度 <= 当前角度，则应该正转
                self.RT_rotate(-1, 3)
                print('-------------' + str(self.get_angle()) + '----------------')
        print('当前角度为：'+ str(self.get_angle()))
    
    def RT_rotate2_destAngle(self,destAngle):
        '''
            程序实现从MIN，或者MAX角度 转动到目的角度
        '''
        angle1 = destAngle - self.__angle_MIN
        angle2 = self.__angle_MAX - destAngle
        if angle1 <= angle2:    # 目的角度距 __angle_MIN 较近，从 __angle_MIN 开始转动
            while not (self.get_angle() ==  destAngle):
                self.RT_rotate(1, 3)
                print('-------------' + str(self.get_angle()) + '----------------')
        else:                   # 目的角度距 __angle_MAX 较近，从 __angle_MAX 开始转动
            self.set_angle(self.__angle_MAX)
            while not (self.get_angle() ==  destAngle):
                self.RT_rotate(-1, 3)
                print('-------------' + str(self.get_angle()) + '----------------')  
        print('当前角度为：'+ str(self.get_angle()))
        
    def RT_rotate2_MIN(self):
        '''
            此程序将转台转至初始状态，无需人工干预
        '''    
        self.currentAngle = self.get_angle()
        # 根据不同的角度，进行快速的归零
        
        # 范围在(180~360)，则朝着360的范围归零
        if  (self.currentAngle <= self.__angle_MAX) and  (self.currentAngle >= self.__angle_MAX/2):
            while not (self.currentAngle == self.__angle_MAX):
                self.rotate_clock(3)
                self.currentAngle = self.get_angle()
                
                print(self.currentAngle)
            # 以圆周进行旋转，最大角度和最小角度重合后，重新设置为最小角度
            self.set_angle(self.__angle_MIN)
        
        # 范围在(0~180)，则朝着0的范围归零        
        elif (self.currentAngle >= self.__angle_MIN) and  (self.currentAngle <= self.__angle_MAX/2):
            while not (self.currentAngle == self.__angle_MIN):
                self.rotate_anticlock(3)
                self.currentAngle = self.get_angle()
                
                print(self.currentAngle)
                
    def RT_rotate_free(self,RT_dir,RT_angle):
        '''
            程序实现电机的自由方向的自由旋转，在校正电机时使用，没有进行角度的保存、设置、更新等操作
            RT_angle: 旋转的最终角度
        '''
        current_Angle = 0   # 只是方便程序员进行使用 

        if (RT_dir == 1) and (RT_angle % 3 == 0):
            self.RT_dir = '1'
            for i in range(1,(RT_angle // 9) + 1):
                current_Angle += 9
                self.rotate(9)
                print('----------------- 已经旋转：' + str(current_Angle) + '-----------------------')
            for i in range(1,((RT_angle % 9) // 6) + 1):
                current_Angle += 6
                self.rotate(6)
                print('----------------- 已经旋转：' + str(current_Angle) + '-----------------------')
            for i in range(1,(((RT_angle % 9) % 6) // 3) + 1):
                current_Angle += 3
                self.rotate(3)
                print('----------------- 已经旋转：' + str(current_Angle) + '-----------------------')
        elif (RT_dir == -1) and (RT_angle % 3 == 0):
            self.RT_dir = '0'
            for i in range(1,(RT_angle // 9) + 1):
                current_Angle -= 9
                self.rotate(9)
                print('----------------- 已经旋转：' + str(current_Angle) + '-----------------------')
            for i in range(1,((RT_angle % 9) // 6) + 1):
                current_Angle -= 6
                self.rotate(6)
                print('----------------- 已经旋转：' + str(current_Angle) + '-----------------------')
            for i in range(1,(((RT_angle % 9) % 6) // 3) + 1):
                current_Angle -= 3
                self.rotate(3)
                print('----------------- 已经旋转：' + str(current_Angle) + '-----------------------')
        else:
            print('---------- 旋转方向出错，或者角度设置 非 3 的倍数，请检查重新设置！！！---------')
            return


class MotorError(Exception):
    '''
        此类定义一个简单的错误异常
    '''
    def __init__(self,ErrorInfo,value = 0):
        super(MotorError,self).__init__(self)
        self.errorinfo = ErrorInfo
        self.value = value
    def __str__(self):
        return self.errorinfo             

        