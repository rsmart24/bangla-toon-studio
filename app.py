import os
import gradio as gr
from renderer import render

def go(script, wav, timing=None, style=None, progress=gr.Progress()):
    if not script:
        raise gr.Error("বাংলা স্ক্রিপ্ট TXT ফাইল দিন।")
    if not wav:
        raise gr.Error("ভয়েসওভার WAV ফাইল দিন।")
    if os.path.splitext(wav)[1].lower() != ".wav":
        raise gr.Error("ভয়েসওভার অবশ্যই WAV ফাইল হতে হবে।")
    result = render(script, wav, timing, style, progress)
    return result, "রেন্ডার সম্পন্ন। টাইমিং JSON না থাকলে ক্যাপশন আনুমানিকভাবে ভাগ করা হয়েছে।"

with gr.Blocks(title="Bangla Toon Studio") as demo:
    gr.Markdown("# 🎬 Bangla Toon Studio — Hybrid 2D\nস্ক্রিপ্ট ও WAV দিয়ে পরীক্ষামূলক কার্টুন ভিডিও তৈরি করুন।")
    with gr.Row():
        script = gr.File(label="বাংলা স্ক্রিপ্ট (.txt)", file_types=["text"], type="filepath")
        wav = gr.File(label="ভয়েসওভার (.wav)", file_types=["audio"], type="filepath")
    with gr.Row():
        timing = gr.File(label="টাইমিং JSON (ঐচ্ছিক)", file_types=[".json"], type="filepath")
        style = gr.File(label="স্টাইল শিট (ঐচ্ছিক)", file_types=[".png", ".jpg", ".jpeg"], type="filepath")
    btn = gr.Button("Render MP4", variant="primary")
    video = gr.Video(label="তৈরি ভিডিও")
    status = gr.Textbox(label="অবস্থা")
    btn.click(go, [script, wav, timing, style], [video, status])

demo.launch(share=True)
