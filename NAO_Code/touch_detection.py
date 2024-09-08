from naoqi import ALProxy
import os
import time

def initialize_proxies():
    try:
        global memory_proxy
        memory_proxy = ALProxy("ALMemory", '172.20.10.3', 9559)
        print("Proxies initialized successfully.")
    except Exception as e:
        print("Error initializing proxies:", e)

def on_touch_detected(value):
    if value > 0:
        print("Touch detected!")
        os.system('python final_work.py')

def setup_touch_listener():
    try:
        memory_proxy.subscribeToEvent("LeftFootBumperPressed", "TouchSubscriber", "on_touch_detected")
        memory_proxy.subscribeToEvent("RightFootBumperPressed", "TouchSubscriber", "on_touch_detected")
        print("Touch listener set up successfully.")
    except Exception as e:
        print("Error setting up touch listener:", e)

if __name__ == "__main__":
    initialize_proxies()
    setup_touch_listener()
    while True:
        time.sleep(1)
