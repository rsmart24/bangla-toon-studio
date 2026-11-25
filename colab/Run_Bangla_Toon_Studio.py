# Google Colab-এ চালানোর নির্দেশনা
# Cell 1: Runtime setup
!apt-get -qq update
!apt-get -qq install -y ffmpeg fonts-noto-core
!pip -q install gradio Pillow

# Cell 2: আপনার নির্দিষ্ট repository clone করুন
!git clone https://github.com/rsmart24/bangla-toon-studio.git
%cd bangla-toon-studio

# Cell 3: Gradio app চালু করুন
!python app.py
# শেষ হলে Gradio-এর public URL খুলুন। Colab free session সাময়িক; disconnect হতে পারে।
