#-*- coding: UTF-8 -*

from LocationData import LocationData
from RotaryTable import RotaryTable
import os
import time

##==================创建全局实例与变量=====================

# 创建定位数据接收节点
myNode = LocationData(['1','2','3','4','6','7'],'COM14')
# 创建转台数据
myRT = RotaryTable('COM11')

# 存放角度的文件夹
AngelFolder = os.getcwd()
Angel2FileName = ''


# 当前角度变量
currentAngle = 0

# 如果：Angle_L < Angle_M 则默认为从小一直转到大，逆时针增加度数
#      Angle_L > Angle_M 则期待从大角度逆时针转到小角度，会跨越角度
Angle_L = 0
Angle_M = 0

##=======================定义函数========================
def set_Angle_LM(angle_l,angle_m):
    # 如果：Angle_L < Angle_M 则默认为从小一直转到大，逆时针增加度数
    #      Angle_L > Angle_M 则期待从大角度逆时针转到小角度，会跨越角度
    global Angle_L
    global Angle_M
    
    
    if (angle_l % 3 == 0) and (angle_m % 3 == 0):
        if (angle_m - angle_l) % 6 == 0:
            pass
        else:
            angle_m +=3
            print('您的角度将设置为：(' + str(angle_l) + ',' + str(angle_m) + ')')
    else:
        while True:
            print('---------------  您的角度下限设置非3,6,9的倍数，请关闭程序重新设置！！！   ----------')
            time.sleep(1)
                   
    Angle_L = angle_l
    Angle_M = angle_m

def set_FolderName(folder_name):
    '''
        本程序实现设置文件夹的名称
    '''
    global AngelFolder
    if type(folder_name) != type(''):
        while True:
            print('---------------- 文件夹名应该是字符串，关闭程序重新设置 ---------------')
    AngelFolder += '\\' + folder_name + '\\'
    # 创建该文件夹
    myNode.mkdir1(AngelFolder)
    

def First_Run():
    '''
        第一次使用或者电机被搬动时，人工校准电机后需要运行次函数
    '''
    print('----------  正在转至需求角度，请稍等 --------------')
    # 设置初始角度，保存
    myRT.set_angle(0)
    # 旋转至需求角度的下限
    myRT.RT_rotate2_destAngle(Angle_L)
    print('----------  已转至需求角度 --------------')

def Normal_Run():
    '''
        并非第一次运行，或者电机没有搬动，在同一个位置持续测量
    '''
    print('----------  正在转至需求角度，请稍等 --------------')
    # 旋转至需求角度的下限
    myRT.RT_rotate2_initANGLE(Angle_L)
    print('----------  已转至需求角度 --------------')

def Save_Data():
    global currentAngle
    global AngelFolder
    global Angel2FileName
    
    # 得到当前角度
    currentAngle = myRT.get_angle()
    # 得到角度对应的需要存放的文件名
    Angel2FileName = AngelFolder + str(currentAngle) + '.txt'
    
    # 发送读取数据命令
    myNode.send_commd()
    # 读取数据
    [RxData_len, RxData_buf] = myNode.get_location_data()
    print('接收到的数据长度为：' + str(RxData_len))
    print(RxData_buf)
    # 将数据保存至文件中
    myNode.saveData2File(Angel2FileName, RxData_buf)

def Run(rt_DVI=6, Mydir='+'):
    '''
        指定的角度范围内，电机旋转，并接收节点的接收数据
    '''

    if Mydir == '+':          # 逆时针旋转，角度递增
        Save_Data()
        while not (myRT.get_angle() == Angle_M):
            myRT.RT_rotate(1,rt_DVI)
            print('-----------------------' + str(myRT.get_angle()) + '度---------------------')
            Save_Data()
    elif Mydir == '-':        # 顺时针旋转，角度递减
        Save_Data()
        while not (myRT.get_angle() == Angle_M):
            myRT.RT_rotate(-1,rt_DVI)
            print('-----------------------' + str(myRT.get_angle()) + '度---------------------')
            Save_Data()
    else:                   # 如果转动范围下限=转动范围上限
        print("what are you fuck doing!!!")

##========================主函数=========================
if __name__ == '__main__':
    set_FolderName('2017261583')
    set_Angle_LM(3,300)
    First_Run()
    # Normal_Run()
    Run(6,'+')

      
