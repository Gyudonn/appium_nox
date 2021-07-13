from appium import webdriver
import aircv as ac

imsrc = None
imobj = None

desired_caps = {}
desired_caps['platformName'] = "Android"         # 声明是ios还是Android系统
desired_caps['platformVersion'] = '7.1.2'        # Android内核版本号，可以在夜神模拟器设置中查看   
desired_caps['deviceName'] = '127.0.0.1:62001'   # 连接的设备名称
desired_caps['noReset'] = True
desired_caps['appPackage'] = 'com.userjoy.sin_mcard'    # apk的包名
desired_caps['appActivity'] = 'com.unity3d.player.UnityPlayerActivity'  # apk的launcherActivity
desired_caps['newCommandTimeout'] = '10000'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)          # 建立 session

def get_size():
	phone_screen_size_width = driver.get_window_size()['width']
	phone_screen_size_height = driver.get_window_size()['height']

	return(phone_screen_size_width, phone_screen_size_height)

def matchImg(imgsrc,imgobj,confidence):#imgsrc=原始圖像，imgobj=待查找的圖片
    imsrc = ac.imread('oring.png')
    imobj = ac.imread('icon.png')
 
    match_result = ac.find_template(imsrc,imobj,confidence)
    if match_result is not None:
        match_result['shape']=(imsrc.shape[1],imsrc.shape[0])#0為高，1為寬

    return match_result

def tab_image():
	photo_position = driver.get_screenshot_as_file('oring.png')#截屏手機
	confidencevalue = 0.8  # 定義相似度
	position = matchImg(imsrc, imobj, confidencevalue)# 用第一步的方法，實際就是find_template()方法
	print(matchImg(imsrc, imobj, confidencevalue))

	if position != None:
		x, y = position['result']
		driver.tap([(x, y)])


def swip_right(t):
	l=get_size()
	x1=int(l[0]*0.05)
	y1=int(l[1]*0.5)
	x2=int(l[0]*0.75)
	driver.swipe(x1, y1, x2, y1, t)

while True:
	mode = input('Enter operator: ')
	if mode == 't':
		#driver.find_elements_by_id('com.userjoy.sin_mcard:id/view_platform_item_v')[0].click()
		tab_image()
	if mode == 'q':
		print('Exit')
		driver.quit()      # 退出 session
		continue
	if mode == 's':
		swip_right(100)
	if mode == 'unity':
		driver.find_elements_by_class_name("android.view.View")[0]


# def main():
# 	tab_image()

# main()