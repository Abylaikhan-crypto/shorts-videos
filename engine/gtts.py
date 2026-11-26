"""Gemini TTS (Vertex express key). gtts.speak(text, voice, style, model) -> float32 numpy @24k"""
import json, base64, urllib.request, numpy as np, time
KEY = open('/home/claude/.secrets/gemini_key').read().strip()
URL = "https://aiplatform.googleapis.com/v1/publishers/google/models/{m}:generateContent?key=" + KEY


def speak(text, voice="Charon", style="", model="gemini-2.5-pro-tts", tries=7):
    prompt = (style + ": " if style else "") + text
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for i in range(tries):
        try:
            req = urllib.request.Request(URL.format(m=model), data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            r = json.loads(urllib.request.urlopen(req, timeout=120).read())
            raw = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            return np.frombuffer(raw, "<i2").astype(np.float32) / 32768
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(8 * (i + 1))
