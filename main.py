import pyaudio
import wave
import time
import threading
import asyncio
from shazamio import Shazam

# 音频流参数
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 2  # 双声道
RATE = 44100  # 采样率
CHUNK = 1024  # 每次读取的帧数
RECORD_SECONDS = 30  # 录音时间限制（秒）
WAVE_OUTPUT_FILENAME = "output.wav"  # 输出文件名

# 初始化音频
audio = pyaudio.PyAudio()

# 获取输入设备索引
def get_input_device_index(device_name):
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_name in device_info['name']:
            return device_info['index']
    return None

# 打开音频流
def open_stream(input_device_index):
    """根据输入设备索引打开音频流"""
    return audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=input_device_index, frames_per_buffer=CHUNK)

# 录音函数
def record_audio(frames, record_seconds, stop_event, input_device_index):
    """录音函数"""
    print("正在录音，等待识别结果或 30 秒自动停止...")
    start_time = time.time()
    stream = open_stream(input_device_index)  # 打开音频流
    try:
        while not stop_event.is_set() and (time.time() - start_time) < record_seconds:
            data = stream.read(CHUNK)
            frames.append(data)
    finally:
        stream.stop_stream()
        stream.close()

# 停止录音和保存文件的函数
def stop_and_save(stop_event, frames, filename):
    """停止录音和保存文件"""
    stop_event.set()
    print(f"录音文件已保存为：{filename}")
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# 异步音频识别函数
async def recognize_audio(file_path):
    """音频识别函数"""
    shazam = Shazam()
    info = await shazam.recognize(file_path)  # 使用 recognize 方法
    if 'track' in info:
        print("识别结果：")
        print(f"歌曲标题: {info['track'].get('title', '未知')}")
        print(f"艺术家: {info['track'].get('subtitle', '未知')}")
    else:
        print("未识别到歌曲")

# 主函数
async def main():
    global frames, stop_event
    frames = []
    stop_event = threading.Event()

    # 用户选择输入源
    input_source = int(input("选择输入源（0:麦克风, 1:扬声器, 2:输入音频文件路径）: "))

    if input_source == 0:
        input_device_index = 0  # 假设麦克风是第一个设备
    elif input_source == 1:
        input_device_index = get_input_device_index("What U Hear")  # 获取What U Hear设备的索引
        if input_device_index is None:
            print("未找到What U Hear设备，请检查您的系统设置。")
            return
    elif input_source == 2:
        file_path = input("输入音频文件路径: ")
        await recognize_audio(file_path)  # 直接识别输入的音频文件
        return  # 退出主函数
    else:
        print("无效的输入源选项")
        return  # 退出主函数

    # 启动录音线程
    record_thread = threading.Thread(target=record_audio, args=(frames, RECORD_SECONDS, stop_event, input_device_index))
    record_thread.start()

    # 等待一段时间或直到录音停止
    await asyncio.sleep(RECORD_SECONDS)  # 等待30秒
    if not stop_event.is_set():
        stop_and_save(stop_event, frames, WAVE_OUTPUT_FILENAME)  # 停止录音并保存文件

    # 识别保存的音频文件
    await recognize_audio(WAVE_OUTPUT_FILENAME)  # 调用异步识别函数

if __name__ == "__main__":
    asyncio.run(main())