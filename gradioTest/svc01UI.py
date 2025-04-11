import gradio as gr
app = gr.Blocks()
with app:
    with gr.Tabs() as tabs:
        with gr.TabItem("转换"):
            model_name = gr.Dropdown(label="模型")
            #model_name = gr.Dropdown(label="模型", choices=models, value=models[0])
            vc_vocal = gr.Audio(label="上传人声",interactive=True)
            #vc_vocal_micro = gr.Audio(label="麦克风输入(优先于上传的音频)",source="microphone",interactive=True)
            vc_vocal_micro = gr.Audio(label="麦克风输入(优先于上传的音频)",interactive=True)

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
        #vc_convert.click(convert_fn, [model_name, vc_vocal,vc_vocal_micro,vc_transform,auto_f0,cluster_ratio, slice_db, noise_scale], [vc_output1, vc_output2,vc_vocal_result])
        #vc_go_compose.click(go_compose_fn,vc_output2,vc_vocal_result)
        #vc_compose.click(compose_fn,[vc_vocal_result,vc_instrumental,mixing_ratio],[vc_output3,vc_output4])
        #gr.Examples(
       #examples=[[build_dir+"/examples/vocals/blue_vocal.wav",build_dir+"/examples/instruments/blue_instrument.wav"]],
        #inputs=[vc_vocal,vc_instrumental]
    #)

app.launch()