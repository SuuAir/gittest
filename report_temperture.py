import time
import pyautogui

# 用于输入法切换
from win32con import WM_INPUTLANGCHANGEREQUEST
import win32gui
import win32api
from report_func import *
import os


info_list = [
    ['Air','754798373','2019122031','Su120401']  # 不能有中文
]

manager = 'Air'
fail_list=[]
max_try_times = 10 # 最大进行次数
retry_intvl = 10  # 重试时间间隔


pyautogui.press('esc')
print('5 s后开始')
time.sleep(5) 

for info in info_list:
    receiver = info[0]
    qq_num=info[1]
    user_name = info[2]
    pwd = info[3]
   
    # 填报体温
    result = report_temperature(user_name,pwd,max_try_times,retry_intvl)
    #result = True
    
    if result == False:  # 失败
        fail_list.append(receiver)
    else:
        send_msg(receiver, qq_num, max_try_times, retry_intvl)
                  
if len(fail_list) > 0:
    send_msg(manager, qq_num, max_try_times, retry_intvl, fail_list)
    
hwnd = win32gui.GetForegroundWindow()
result = win32api.SendMessage(hwnd,WM_INPUTLANGCHANGEREQUEST,0,0x8040804)   # 切换为中文键盘布局的搜狗输入法，result==0代表设置成功

print('15 s后睡眠')
time.sleep(15)
os.system('nircmd standby')   # 休眠