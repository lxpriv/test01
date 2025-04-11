#该应用创建工具共包含三个区域，顶部工具栏，左侧代码区，右侧交互效果区，其中右侧交互效果是通过左侧代码生成的，存在对照关系。
#顶部工具栏：运行、保存、新开浏览器打开、实时预览开关，针对运行和在浏览器打开选项进行重要说明：
#[运行]：交互效果并非实时更新，代码变更后，需点击运行按钮获得最新交互效果。
#[在浏览器打开]：新建页面查看交互效果。
#以下为应用创建工具的示例代码

import io
import os

import gradio as gr
import librosa
import numpy as np
import soundfile
from inference.infer_tool import Svc
import logging
import os
import paddle

build_dir=os.getcwd()
if build_dir == "/home/aistudio":
    build_dir += "/build"
model_dir=build_dir+'/trained_models'

# 列出当前目录下的所有文件和文件夹
files_and_folders = os.listdir(model_dir)

cache_model = {}


# 筛选出文件夹
models = [item for item in files_and_folders if os.path.isdir(os.path.join(model_dir, item)) and not item.startswith('.')]


def convert_fn(model_name, input_audio,input_audio_micro, vc_transform, auto_f0,cluster_ratio, slice_db, noise_scale):
    try:
        if model_name in cache_model:
            model = cache_model[model_name]
        else:
            if paddle.device.is_compiled_with_cuda()==False and len(cache_model)!=0:
                return f"目前运行环境为CPU，受制于平台算力，每次启动本项目只允许加载1个模型，当前已加载{next(iter(cache_model))}",None,None
            config_path = f"{build_dir}/trained_models/{model_name}/config.json"
            model = Svc(f"{build_dir}/trained_models/{model_name}/{model_name}.pdparams", config_path,mode="test")
            cache_model[model_name] = model
        if input_audio is None and input_audio_micro is None:
            return "请上传音频", None,None
        if input_audio_micro is not None:
            input_audio = input_audio_micro
        sampling_rate, audio = input_audio
        duration = audio.shape[0] / sampling_rate
        audio = (audio / np.iinfo(audio.dtype).max).astype(np.float32)
        if len(audio.shape) > 1:
            audio = librosa.to_mono(audio.transpose(1, 0))
        if sampling_rate != 16000:
            audio = librosa.resample(audio, orig_sr=sampling_rate, target_sr=16000)
        print(audio.shape)
        out_wav_path = "temp.wav"
        soundfile.write(out_wav_path, audio, 16000, format="wav")
        print(cluster_ratio, auto_f0, noise_scale)
        _audio = model.slice_inference(out_wav_path, model_name, vc_transform, slice_db, cluster_ratio, auto_f0, noise_scale,empty_cache=True)
        del model
        return "转换成功", (44100, _audio),(44100, _audio)
    except Exception as e:
        import traceback
        return traceback.format_exc() , None,None
def go_compose_fn(audio):
    return audio

def compose_fn(input_vocal,input_instrumental,mixing_ratio=0.5):
    try:
        outlog = "混音成功"
        if input_vocal is None:
            return "请上传人声", None
        if input_instrumental is None:
            return "请上传伴奏", None
        vocal_sampling_rate, vocal = input_vocal
        vocal_duration = vocal.shape[0] / vocal_sampling_rate
        vocal = (vocal / np.iinfo(vocal.dtype).max).astype(np.float32)
        if len(vocal.shape) > 1:
            vocal = librosa.to_mono(vocal.transpose(1, 0))
        if vocal_sampling_rate != 44100:
            vocal = librosa.resample(vocal, orig_sr=vocal_sampling_rate, target_sr=44100)

        instrumental_sampling_rate, instrumental = input_instrumental
        instrumental_duration = instrumental.shape[0] / instrumental_sampling_rate
        instrumental = (instrumental / np.iinfo(instrumental.dtype).max).astype(np.float32)
        if len(instrumental.shape) > 1:
            instrumental = librosa.to_mono(instrumental.transpose(1, 0))
        if instrumental_sampling_rate != 44100:
            instrumental = librosa.resample(instrumental, orig_sr=instrumental_sampling_rate, target_sr=44100)
        if len(vocal)!=len(instrumental):
            min_length = min(len(vocal),len(instrumental))
            instrumental = instrumental[:min_length]
            vocal = vocal[:min_length]
            outlog = "人声伴奏长度不一致，已自动截断较长的音频"

        mixed_audio = (1 - mixing_ratio) * vocal + mixing_ratio * instrumental
        mixed_audio_data = mixed_audio.astype(np.float32)
        return outlog,(44100,mixed_audio_data)
    except Exception as e:
        import traceback
        return traceback.format_exc() , None
app = gr.Blocks()
with app:
    with gr.Tabs() as tabs:
        with gr.TabItem("转换"):
            model_name = gr.Dropdown(label="模型", choices=models, value=models[0])
            vc_vocal = gr.Audio(label="上传人声",interactive=True)
            vc_vocal_micro = gr.Audio(label="麦克风输入(优先于上传的音频)",source="microphone",interactive=True)
            vc_transform = gr.Number(label="变调", value=0)
            cluster_ratio = gr.Number(label="聚类模型混合比例", value=0)
            auto_f0 = gr.Checkbox(label="自动f0预测", value=False)
            slice_db = gr.Number(label="切片阈值", value=-40)
            noise_scale = gr.Number(label="noise_scale", value=0.4)
            vc_convert = gr.Button("转换", variant="primary")
            vc_output1 = gr.Textbox(label="输出信息")
            vc_output2 = gr.Audio(label="输出音频",interactive=False)

        with gr.TabItem("混音"):
            vc_vocal_result = gr.Audio(label="上传人声",interactive=True)
            vc_go_compose = gr.Button("使用转换后音频", variant="primary")
            vc_instrumental = gr.Audio(label="上传伴奏")
            mixing_ratio = gr.Slider(0, 1, value=0.6,step=0.01,label="混音比例", info="人声:伴奏")
            vc_compose = gr.Button("混音", variant="primary")
            vc_output3 = gr.Textbox(label="输出信息")
            vc_output4 = gr.Audio(label="输出音频",interactive=False)
        vc_convert.click(convert_fn, [model_name, vc_vocal,vc_vocal_micro,vc_transform,auto_f0,cluster_ratio, slice_db, noise_scale], [vc_output1, vc_output2,vc_vocal_result])
        vc_go_compose.click(go_compose_fn,vc_output2,vc_vocal_result)
        vc_compose.click(compose_fn,[vc_vocal_result,vc_instrumental,mixing_ratio],[vc_output3,vc_output4])
        gr.Examples(
        examples=[[build_dir+"/examples/vocals/blue_vocal.wav",build_dir+"/examples/instruments/blue_instrument.wav"]],
        inputs=[vc_vocal,vc_instrumental]
    )

app.launch()
