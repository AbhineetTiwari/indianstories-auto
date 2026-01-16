import os
import requests
import subprocess
from datetime import datetime

# ---------------- CONFIG ----------------
HF_TOKEN = os.environ.get("HF_TOKEN")
WORKDIR = "work"
os.makedirs(WORKDIR, exist_ok=True)

# ---------------------------------------
def generate_story():
    prompt = (
        "Write a very short children friendly Indian god story "
        "in Hindi (4 lines only). Include a moral at the end."
    )

    url = "https://api-inference.huggingface.co/models/google/gemma-2b-it"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    r = requests.post(url, headers=headers, json=payload)
    text = r.json()[0]["generated_text"]

    story_path = f"{WORKDIR}/story.txt"
    with open(story_path, "w", encoding="utf-8") as f:
        f.write(text)

    return text, story_path


def generate_image():
    prompt = (
        "cartoon style illustration of Indian god story for children, "
        "soft colors, kids book illustration, animated look"
    )

    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    r = requests.post(url, headers=headers, json={"inputs": prompt})
    img_path = f"{WORKDIR}/image.png"

    with open(img_path, "wb") as f:
        f.write(r.content)

    return img_path


def generate_voice(story_text):
    voice_path = f"{WORKDIR}/voice.mp3"
    subprocess.run([
        "edge-tts",
        "--voice", "hi-IN-MadhurNeural",
        "--text", story_text,
        "--write-media", voice_path
    ])
    return voice_path


def generate_video():
    video_path = f"{WORKDIR}/short.mp4"
    subprocess.run([
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", f"{WORKDIR}/image.png",
        "-i", f"{WORKDIR}/voice.mp3",
        "-t", "30",
        "-vf", "scale=1080:1920,zoompan=z='zoom+0.0005'",
        "-c:v", "libx264",
        "-c:a", "aac",
        video_path
    ])
    return video_path


# ---------------- RUN ----------------
print("🚀 IndianStories automation started")

story, _ = generate_story()
generate_image()
generate_voice(story)
generate_video()

print("✅ Short video generated successfully")
