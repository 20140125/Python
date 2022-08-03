#!/usr/bin/python3
import time

import pyautogui
# import pyperclip

pyautogui.FAILSAFE = False

time.sleep(1)
pyautogui.click(1920, 1048)
print(pyautogui.position())
# 打开谷歌浏览器
time.sleep(1)
pyautogui.doubleClick(x=41, y=644, button='left')  # 鼠标在（41，644）位置左击两下
print('打开谷歌浏览器')
# 浏览器全屏
time.sleep(1)
pyautogui.click(x=1509, y=25, button='left')  # 鼠标在（1509，25）位置左击
print('设置浏览器全屏')
# 单击输入框
time.sleep(1)
pyautogui.click(x=736, y=426, button='left')  # 鼠标在（193，54）位置左击
print('定位Google输入框')
# 输入文本内容
time.sleep(1)
# 支持键入中文
# pyperclip.copy('https://m.toutiao.com/video/7106071553246396964/?from_page_type=feed&upstream_biz=toutiao_m&a11y_config=000\n')
# pyautogui.hotkey('ctrl', 'v')
pyautogui.typewrite('https://m.toutiao.com/video/7106071553246396964/?from_page_type=feed&upstream_biz=toutiao_m&a11y_config=000\n', interval=0.3)
print('输入视频地址')
time.sleep(1)
pyautogui.press('enter')  # 按下并松开（轻敲）回车键
print('确定文本内容')
time.sleep(1)
pyautogui.press('f12')
print('开发者工具')
# 手机模式
time.sleep(1)
pyautogui.click(x=49, y=633, button='left')
print('手机模式')
# 设置
time.sleep(1)
pyautogui.click(x=1874, y=634, button='left')
print('Dock settings')
# 左右分屏
time.sleep(1)
pyautogui.click(x=1894, y=669, button='left')
print('开发者模式左右分屏')
for i in range(0, 3, 1):
    # 移动鼠标到页面
    pyautogui.moveTo(633, 571, 1)
    print('移动鼠标到页面')
    # 下滑2000格
    pyautogui.scroll(-600)
    print('下滑600格')
    # 点击视频播放
    time.sleep(2)
    pyautogui.click(x=660, y=500, button='left')
    print('点击获取视频详情')
    # 视频播放
    time.sleep(3)
    pyautogui.click(x=656, y=307, button='left')
    print('点击播放按钮播放视频')
    time.sleep(10)
    print('10S视频播放成功')

# 关闭浏览器
time.sleep(5)
pyautogui.click(1897, 13)
print('关闭浏览器')
