import os, math, json, wave, shutil, subprocess, tempfile, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1920,1080,30
P={"paper":"#F6F1E7","terracotta":"#C8643B","gold":"#F2A900","red":"#B3202A","teal":"#1F7A74","jute":"#D9B88F","ink":"#1B1A22"}
def duration(wav):
    with wave.open(wav,"rb") as f: return f.getnframes()/f.getframerate()
def font(size):
    for p in ["/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try:return ImageFont.truetype(p,size)
            except:pass
    return ImageFont.load_default()
def captions(script, timing, dur):
    if timing and os.path.exists(timing):
        try:
            d=json.loads(Path(timing).read_text(encoding="utf-8"))
            words=d.get("words",d if isinstance(d,list) else [])
            if words and all("start" in x and "end" in x for x in words):
                out=[]; buf=[]
                for x in words:
                    buf.append(str(x.get("text","")))
                    if len(buf)>=4 or str(x.get("text","")).endswith(("।","?","!")):
                        out.append((float(buf[0].get("start",0)) if isinstance(buf[0],dict) else float(x["start"]),float(x["end"])," ".join(str(y.get("text","")) for y in words[max(0,len(out)*4):len(out)*4+len(buf)])))
                        buf=[]
                if out:return out
        except:pass
    parts=[x.strip() for x in re.split(r"(?<=[।!?])\\s+|\\n+",script) if x.strip()] or [script]
    n=sum(max(1,len(x)) for x in parts); t=0; out=[]
    for s in parts:
        e=t+dur*max(1,len(s))/n; out.append((t,e,s)); t=e
    return out
def frame(t, caption):
    im=Image.new("RGB",(W,H),P["paper"]); d=ImageDraw.Draw(im)
    d.ellipse((1450-int(t*8)%100,55,1770-int(t*8)%100,375),fill=P["gold"])
    d.rectangle((0,650,W,H),fill=P["jute"])
    for i in range(7):
        x=i*330-int(t*12)%330
        d.rectangle((x,435,x+220,660),fill=P["terracotta"],outline=P["ink"],width=7)
        d.polygon([(x-15,435),(x+110,345),(x+235,435)],fill=P["red"],outline=P["ink"])
        d.rectangle((x+80,520,x+140,660),fill=P["paper"],outline=P["ink"],width=5)
    for x in range(-100,W+200,240):
        xx=x-int(t*22)%240; d.ellipse((xx,835,xx+170,1000),fill=P["teal"])
    cx=900+int(math.sin(t*.5)*28); cy=500+int(math.sin(t*2.4)*7); ink=P["ink"]; skin="#A96543"
    d.line((cx-42,cy+130,cx-65,cy+235),fill=ink,width=35); d.line((cx+42,cy+130,cx+65,cy+235),fill=ink,width=35)
    d.line((cx-65,cy+235,cx-85,cy+235),fill=P["terracotta"],width=28); d.line((cx+65,cy+235,cx+85,cy+235),fill=P["terracotta"],width=28)
    d.rounded_rectangle((cx-90,cy+35,cx+90,cy+180),radius=45,fill=P["teal"],outline=ink,width=9)
    d.ellipse((cx-108,cy-160,cx+108,cy+70),fill=skin,outline=ink,width=9)
    d.pieslice((cx-112,cy-175,cx+112,cy+55),180,360,fill=ink,outline=ink,width=7)
    for ex in (cx-43,cx+43): d.ellipse((ex-9,cy-35,ex+9,cy-7),fill=ink)
    mh=8+int((math.sin(t*13)+1)*8); d.ellipse((cx-22,cy+12-mh//2,cx+22,cy+12+mh//2),fill=ink)
    d.line((cx+70,cy+80,cx+150,cy+55+int(math.sin(t*3)*12)),fill=ink,width=27)
    d.ellipse((cx+132,cy+35,cx+168,cy+71),fill=skin,outline=ink,width=6)
    if caption:
        f=font(46); b=d.textbbox((0,0),caption,font=f); tw=b[2]-b[0]
        while tw>1450 and f.size>26:
            f=font(f.size-2); b=d.textbbox((0,0),caption,font=f); tw=b[2]-b[0]
        x=(W-tw)//2; y=875
        d.rounded_rectangle((x-38,y,x+tw+38,y+95),radius=26,fill=ink)
        d.text((x,y+18),caption,font=f,fill=P["paper"])
    return im
def render(script_file,wav_file,json_file=None,style_file=None,progress=None):
    ff=shutil.which("ffmpeg")
    if not ff: raise RuntimeError("FFmpeg পাওয়া যায়নি; Colab setup cell চালান।")
    dur=duration(wav_file)
    if dur<=0: raise RuntimeError("WAV duration পড়া যায়নি।")
    script=Path(script_file).read_text(encoding="utf-8").strip()
    caps=captions(script,json_file,dur); total=max(1,math.ceil(dur*FPS)); out="/content/bangla_toon_v1.mp4"
    with tempfile.TemporaryDirectory() as td:
        for i in range(total):
            t=i/FPS; cap=next((s for a,b,s in caps if a<=t<b),"")
            frame(t,cap).save(os.path.join(td,f"{i:06d}.jpg"),quality=92)
            if progress and i%30==0: progress(i/total,desc=f"ফ্রেম {i}/{total}")
        cmd=[ff,"-y","-framerate",str(FPS),"-i",os.path.join(td,"%06d.jpg"),"-i",wav_file,"-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out]
        p=subprocess.run(cmd,capture_output=True,text=True)
        if p.returncode: raise RuntimeError(p.stderr[-1800:])
    return out
