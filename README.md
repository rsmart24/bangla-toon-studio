# Bangla Toon Studio

Free, Android-accessible **Hybrid 2D** cartoon video studio prototype. Source code lives here; rendering runs in a temporary Google Colab session. No paid API is used.

## Run from Android
1. Open `colab/Run_Bangla_Toon_Studio.ipynb` in GitHub and choose **Open in Colab** (or upload the notebook to Colab).
2. Run all cells from top to bottom.
3. Open the Gradio link, upload a UTF-8 Bangla `.txt` script and a `.wav` voiceover, optionally add timing `.json` and a style-sheet image, then press **Render MP4**.

## Output target
1920×1080, 30 fps, MP4 (H.264/AAC), filename `bangla_toon_v1.mp4`.

## Timing JSON
Basic supported form: `{"words":[{"text":"বাংলা","start":0.0,"end":0.5}]}`. If absent, caption timing is estimated across the audio duration; it is not forced alignment.

## Honest prototype limits
This is the first runnable foundation, not the complete v8 production system. Current rendering uses a procedural sample character, layered vector-like scenery, simple motion and captions. Full story comprehension, multiple custom character rigs, phoneme-accurate lip sync, automatic art-direction extraction from a style image, advanced sound design and shot-by-shot visual QA are future stages. Free Colab sessions are temporary, quota-limited and may disconnect; unlimited free rendering cannot be guaranteed.
