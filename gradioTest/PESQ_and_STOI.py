from pesq import pesq
from pystoi import stoi
import numpy as np
import librosa# 示例：调用一个假设的POLQA API进行计算





def load_audio(file_path, sr=16000):
    # 加载音频文件
    audio, _ = librosa.load(file_path, sr=sr)
    return audio

# 示例音频文件路径
original_audio_path = '.\wavDuibi\JJBDBYB.wav'
processed_audio_path = '.\wavDuibi\SYZBDBYB.wav'

# 加载音频文件
original_audio = load_audio(original_audio_path)
processed_audio = load_audio(processed_audio_path)

# 确保音频长度相同
min_len = min(len(original_audio), len(processed_audio))
original_audio = original_audio[:min_len]
processed_audio = processed_audio[:min_len]

# 计算PESQ（使用窄带模式）
pesq_score = pesq(16000, original_audio, processed_audio, 'nb')
print(f"PESQ: {pesq_score}")

# 计算STOI
stoi_score = stoi(original_audio, processed_audio, 16000)
print(f"STOI: {stoi_score}")



# POLQA（Perceptual Objective Listening Quality Assessment）
# 是继PESQ之后的一种更先进的语音质量评估算法，适用于宽带和超宽带语音以及现代通信网络。



