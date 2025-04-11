from pydub import AudioSegment

def convert_to_mono(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    mono_audio = audio.set_channels(1)
    mono_audio.export(output_path, format="wav")

# 示例音频文件路径
input_file = ".\wavDuibi\SYZBDBYB.wav"
output_file = ".\wavDuibi\SYZBDBYB.wav"
convert_to_mono(input_file, output_file)
#  .\wavDuibi\JJBDBYB.wav
#  .\wavDuibi\SYZBDBYB.wav