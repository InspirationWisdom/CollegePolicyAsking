# -*- coding: utf-8 -*-

from naoqi import ALProxy
import requests
import time
import json

robot_ip = ''  # replace with your robot's IP address
port = 9559

audio_recorder = ALProxy("ALAudioRecorder", robot_ip, port)

audio_file_path = "/home/nao/my_audio.wav"

channels = [1, 1, 1, 1]
audio_format = "wav"
sample_rate = 16000

print("start recording...")
audio_recorder.startMicrophonesRecording(audio_file_path, audio_format, sample_rate, channels)

time.sleep(10)

audio_recorder.stopMicrophonesRecording()
print("recording stopped and saved to:", audio_file_path)

server_url = "http://172.20.10.12:8888/ChatAI"

print("start sending audio to server...")

with open(audio_file_path, 'rb') as f:
    files = {'file': (audio_file_path, f, 'audio/wav')}
    response = requests.post(server_url, files=files)

print("start speaking...")

tts = ALProxy("ALTextToSpeech", robot_ip, port)
tts.setLanguage("Chinese")
tts.pCall("say",str(response.text))