from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import pyautogui

# 用于输入法切换
from win32con import WM_INPUTLANGCHANGEREQUEST
import win32gui
import win32api
import os


def click_by_x_path(browser, x_path, max_try_times, retry_intval):

    for try_time in range(max_try_times):
        try:
            button = browser.find_element_by_xpath(x_path)
            ActionChains(browser).move_to_element(button).click(button).perform()
            break   # 找到了就退出循环
            
        except:
            if try_time == max_try_times-1:
                ex = Exception('Time_out')
                raise ex
            else:
                time.sleep(retry_intval)
                continue

def report_temperature(user_name,pwd,max_try_times,retry_intvl):
    
    
    is_success = False
    for try_time in range(max_try_times):
        
        try: 
        
            try:
                option = webdriver.ChromeOptions()
                #option.add_argument('headless') # 不打开浏览器
                browser = webdriver.Chrome(options=option)
        
            except:
                browser = webdriver.Edge("C:/Program Files (x86)/Microsoft/Edge/Application/msedgedriver.exe")
        
            browser.get("http://service.chd.edu.cn/infoplus/form/XSYQSB/start")
            # 或者设置7天免登陆，或记住密码

            # 输用户名和密码
            user_name_input = browser.find_element_by_id("username")
            user_name_input.send_keys(user_name)
            user_pwd_input = browser.find_element_by_id("password")
            user_pwd_input.send_keys(pwd)

            login_button = browser.find_element_by_id("login_submit").click()   # 直接点击，不需要下一句。但是直接点击屏幕外的元素，会出错
            #ActionChains(browser).move_to_element(login_button).click(login_button).perform() # 移动到指定元素再点击，好处是可以点击屏幕外的元素。
            time.sleep(5)


            # 点击不缺课
            x_path = "//*[@id='V0_CTRL142']"
            max_try_times = 10
            retry_intval = 5
            click_by_x_path(browser, x_path, max_try_times, retry_intval)
            

            # 点击填写下午体温的位置
            x_path = "/html/body/div[4]/form/div/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[23]/td[4]/div/font/div/span/span[1]/span/span[1]"
            max_try_times = 10
            retry_intval = 2
            click_by_x_path(browser, x_path, max_try_times, retry_intval)
            
            time.sleep(0.3)
            # 输入下午的体温
            jtwz = browser.find_element_by_xpath("/html/body/span/span/span[1]/input")
            jtwz.send_keys('36.5')
            time.sleep(1)
            jtwz.send_keys('\n')

            # 提交
            x_path = "/html/body/div[4]/form/div/div[1]/div[2]/ul/li[1]/a/nobr"
            max_try_times = 10
            retry_intval = 2
            click_by_x_path(browser, x_path, max_try_times, retry_intval)
            

            # 如有其它相关说明，请点击备注，或直接批注在填表内容处
            time.sleep(1)
            x_path = "/html/body/div[7]/div/div[2]/button[1]"
            max_try_times = 10
            retry_intval = 2
            click_by_x_path(browser, x_path, max_try_times, retry_intval)
            

            # 填写成功，好
            time.sleep(3)
            x_path = "/html/body/div[8]/div/div[2]/button"
            max_try_times = 10
            retry_intval = 2
            click_by_x_path(browser, x_path, max_try_times, retry_intval)
            
            time.sleep(3)
            is_success = True
            browser.quit()
            break
            
        except:
            if try_time == max_try_times - 1:
                break
            print("填报失败，正在重试...")
            browser.quit()
            time.sleep(retry_intvl)
            continue
    
    return is_success


def send_msg(receiver, qq_num, max_try_times, retry_intvl, fail_list=None):

    # 注意：QQ要开启按enter键发送消息，且设置-主面板-关闭主面板时隐藏到任务栏
    
    std_sleep_seconds = 0.5
    datetime_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    if fail_list != None:
        message = 'Fail_list: ' + str(fail_list)
    else:
        message = datetime_now + ' Success！'
    
    is_success = False
    
    for try_time in range(max_try_times):
        try:
            os.system('start tencent://message/?uin='+qq_num+'^&fuin=2701796462') # +'&fuin=0&Menu=yes'
            time.sleep(3*std_sleep_seconds)
            hwnd = win32gui.GetForegroundWindow()
            result = win32api.SendMessage(hwnd,WM_INPUTLANGCHANGEREQUEST,0,0x4090804)   # 切换为中文键盘布局的英文输入法，result==0代表设置成功
            pyautogui.typewrite(message)
            time.sleep(3*std_sleep_seconds)
            pyautogui.press('enter')
            time.sleep(2*std_sleep_seconds)
            pyautogui.hotkey('alt','f4')
            
            time.sleep(0.5)
            is_success = True
            break
            
        except:
            if try_time == max_try_times - 1:
                break
            print("发送失败，正在重试...")
            time.sleep(retry_intvl)
            continue
            
    return is_success