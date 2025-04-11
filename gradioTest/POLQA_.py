# POLQA（Perceptual Objective Listening Quality Assessment）
# 是继PESQ之后的一种更先进的语音质量评估算法，适用于宽带和超宽带语音以及现代通信网络。

# 导入必要的库
# from musicAlgLib import compute_audio_quality
import musicAlgLib
import algorithmLib

# 定义输入音频文件路径
# path_to_reference_audio.wav
ref_file = ".\wavDuibi\JJBDBYB.wav"
# path_to_test_audio.wav
test_file = ".\wavDuibi\SYZBDBYB.wav"


# 计算POLQA评分
# 请注意，POLQA模式为0表示默认模式，1表示理想模式
# 采样率需根据具体音频情况设定，8k为窄带模式，48k为超宽带模式
polqa_score = compute_audio_quality(
    metrics='POLQA',
    testFile=test_file,
    refFile=ref_file,
    samplerate=48000,  # 根据需求选择采样率
    polqaMode=0  # 0表示默认模式，1表示理想模式
)

# 打印POLQA评分
print(f"POLQA Score: {polqa_score}")
