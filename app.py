from appium import webdriver
import aircv as ac
import time
import os


imsrc_name = None
imobj_name = None
img_location = [['confirm', 'confirm_button'], ['ani', 'ani_skip'], ['resoult', 'resoult_button']]

desired_caps = {}
desired_caps['platformName'] = "Android"         # 声明是ios还是Android系统
desired_caps['platformVersion'] = '7.1.2'        # Android内核版本号，可以在夜神模拟器设置中查看   
desired_caps['deviceName'] = '127.0.0.1:62001'   # 连接的设备名称
desired_caps['noReset'] = True
desired_caps['appPackage'] = 'com.userjoy.sin_mcard'    # apk的包名
desired_caps['appActivity'] = 'com.unity3d.player.UnityPlayerActivity'  # apk的launcherActivity
desired_caps['newCommandTimeout'] = '10000'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)          # 建立 session

def set_img_name(img_name):
	img_fullname = img_name + '.png'
	return img_fullname

def get_size():
	phone_screen_size_width = driver.get_window_size()['width']
	phone_screen_size_height = driver.get_window_size()['height']
	return(phone_screen_size_width, phone_screen_size_height)

def screen_shot():
	i = 0
	save_file = False
	while save_file != True:
		filename = ('screen_shot' + str(i) + '.png')
		print(filename)
		if os.path.isfile(filename):
			print('檔案存在。')
			i = i + 1
		else:
			print('檔案不存在。')
			driver.get_screenshot_as_file(filename)#截屏手機
			save_file = True

def matchImg(confidence):#imgsrc=原始圖像，imgobj=待查找的圖片
    imsrc = ac.imread(imsrc_name)
    imobj = ac.imread(imobj_name)
 
    match_result = ac.find_template(imsrc, imobj, confidence)
    if match_result is not None:
        match_result['shape']=(imsrc.shape[1],imsrc.shape[0])#0為高，1為寬

    return match_result

def tab_image():
	confidencevalue = 0.8  # 定義相似度
	position = matchImg(confidencevalue)# 用第一步的方法，實際就是find_template()方法

	if position != None:
		x, y = position['result']
		driver.tap([(x, y)])

def swip_right(t):
	screen_size = get_size()
	x1 = int(screen_size[0] * 0.05)
	y1 = int(screen_size[1] * 0.5)
	x2 = int(screen_size[0] * 0.75)
	driver.swipe(x1, y1, x2, y1, t)

while True:
	mode = input('Enter operator(tap, swip, shot, q): ')
	if mode == 'tap':
		#driver.find_elements_by_id('com.userjoy.sin_mcard:id/view_platform_item_v')[0].click()
		tab_image()
	if mode == 'match':
		print(matchImg(0.5))
		tab_image()
	if mode == 'shot':
		screen_shot()
	if mode == 'swip':
		swip_right(100)
	if mode == 'auto':
		while True:
			time.sleep(2)
			imsrc_name = set_img_name(img_location[0][0])
			imobj_name = set_img_name(img_location[0][1])
			tab_image()

			time.sleep(3)
			swip_right(100)

			time.sleep(1)
			imsrc_name = set_img_name(img_location[1][0])
			imobj_name = set_img_name(img_location[1][1])
			tab_image()

			time.sleep(1)
			tab_image()

			time.sleep(2)
			imsrc_name = set_img_name(img_location[2][0])
			imobj_name = set_img_name(img_location[2][1])
			tab_image()
	if mode == 'q':
		print('Exit')
		driver.quit()      # 退出 session
		time.sleep(5)
		break

# def main():
# 	tab_image()

# main()