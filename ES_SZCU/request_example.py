import requests

# 服务器的URL地址和端点
server_url = "http://localhost:8888/ChatAI"  # 替换为您的服务器的实际URL

# 要上传的文件路径
file_path = "./converted_audio_mono.wav"  # 替换为您要上传的文件路径

try:
    # 以二进制模式打开文件
    with open(file_path, 'rb') as f:
        # 使用requests的文件上传功能
        files = {'file': (file_path, f, 'audio/wav')}  # 设置上传的文件类型
        response = requests.post(server_url, files=files)

    # 输出服务器响应
    print("服务器响应: ", response.text)

except Exception as e:
    print("文件上传时出错:", e)
