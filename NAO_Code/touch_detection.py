from naoqi import ALProxy
import os
import time

robot_ip = ''

# 连接到NAO机器人
def initialize_proxy():
    try:
        global touch_proxy
        touch_proxy = ALProxy("ALTouch", robot_ip, 9559)
        global tts_proxy
        tts_proxy = ALProxy("ALTextToSpeech", robot_ip, 9559)
        print("Proxies initialized successfully.")
    except Exception as e:
        print("Error initializing proxies:", e)

# 触摸事件处理函数
def on_touch_detected(name, value):
    if value:
        print("Touch detected!")
        # 调用你的Python文件
        os.system('python3 final_work.py')
        # 可选：给用户一些反馈
        tts_proxy.say("以上就是我为您找到的信息。")

# 设置触摸事件监听
def setup_touch_listener():
    try:
        touch_proxy.subscribe("TouchSubscriber")
        touch_proxy.setCallback(on_touch_detected)
        print("Touch listener set up successfully.")
    except Exception as e:
        print("Error setting up touch listener:", e)

if __name__ == "__main__":
    initialize_proxy()
    setup_touch_listener()
    while True:
        # 保持程序运行
        time.sleep(1)
