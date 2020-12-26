from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time

#这里改成你的统一认证用户名和密码
user_name = '2019122031'
pwd = 'Su120401'

try:
	# 加上这两句话不打开浏览器
	#option = webdriver.ChromeOptions()
	# option.add_argument('headless') # 设置option
	#browser = webdriver.Chrome(options=option)
	browser = webdriver.Edge("C:/Program Files (x86)/Microsoft/Edge/Application/msedgedriver.exe")

	browser.get("http://service.chd.edu.cn/infoplus/form/XSYQSB/start")

	#time.sleep(5)

	# 或者设置7天免登陆，或记住密码

	# 输用户名和密码
	user_name_input = browser.find_element_by_id("username")
	user_name_input.send_keys(user_name)
	user_pwd_input = browser.find_element_by_id("password")
	user_pwd_input.send_keys(pwd)

	login_button = browser.find_element_by_id("login_submit")
	ActionChains(browser).move_to_element(login_button).click(login_button).perform()
		

	time.sleep(10)
	#browser.get("http://service.chd.edu.cn/infoplus/form/XSYQSB/start")

	# 是否缺课
	max_times = 10
	for i in range(max_times):
		try:
			zc = browser.find_element_by_xpath("//*[@id='V0_CTRL142']")
			break
		except NoSuchElementException:
			time.sleep(5)
			if i == max_times:
				print('Time_out!')
				ex = Exception('Time_out')
				raise ex

	ActionChains(browser).move_to_element(zc).click(zc).perform()


	# 点击填写下午体温的位置
	wz = browser.find_element_by_xpath("/html/body/div[4]/form/div/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[23]/td[4]/div/font/div/span/span[1]/span/span[1]")
	ActionChains(browser).move_to_element(wz).click(wz).perform()

	# 输入下午的体温
	jtwz = browser.find_element_by_xpath("/html/body/span/span/span[1]/input")
	jtwz.send_keys('36.5')
	time.sleep(1)
	jtwz.send_keys('\n')

	# 提交
	tpost = browser.find_element_by_xpath("/html/body/div[4]/form/div/div[1]/div[2]/ul/li[1]/a/nobr")
	ActionChains(browser).move_to_element(tpost).click(tpost).perform()

	# 如有其它相关说明，请点击备注，或直接批注在填表内容处
	time.sleep(3)
	max_times = 5
	for i in range(max_times):
		try:
			tpost = browser.find_element_by_xpath("/html/body/div[7]/div/div[2]/button[1]")
		except NoSuchElementException:
			time.sleep(5)
			if i == max_times:
				print('Time_out!')
				ex = Exception('Time_out')
				raise ex

	ActionChains(browser).move_to_element(tpost).click(tpost).perform()


	# 填写成功，好
	time.sleep(5)
	tpost = browser.find_element_by_xpath("/html/body/div[8]/div/div[2]/button")
	ActionChains(browser).move_to_element(tpost).click(tpost).perform()

	time.sleep(10)

	#关闭浏览器
	browser.quit()
	print('成功')

except:
	browser.quit()