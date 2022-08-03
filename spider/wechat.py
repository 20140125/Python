#!/usr/bin/python3
import time

import pyautogui
import pyperclip
import random

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1
# 截图
# pyautogui.screenshot('a.png', region=(414, 149, 800, 600))
# time.sleep(5)
# 定位微信ICON位置
pyautogui.click(1678, 1063)
# 定位到搜索框
pyautogui.click(94, 37)
pyperclip.copy('Sir\n')
pyautogui.hotkey('ctrl', 'v')
# pyautogui.typewrite('abcd\n', interval=0.25)
pyautogui.press('enter')
messages = ['你是不是傻！', '你怕不是脑子进水了！', '小伙子，还是太年轻！', '还玩不？小伙子！', '你怕不是秀逗了吧？']
for i in range(0, len(messages), 1):
    # 定位表情icon
    pyautogui.click(341, 865)
    # 墨镜
    pyautogui.click(365, 592)
    message = messages[i]  # random.randint(0, len(messages) - 1) 随机
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    # 大笑
    pyautogui.click(213, 735)
    # 点击发送按钮
    pyautogui.click(1840, 1011)
    # 延迟1s继续
    time.sleep(1)
