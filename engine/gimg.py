"""Gemini image helper: img(prompt, out, refs=[paths], aspect='9:16')"""
import requests, base64, time
K = open('/home/claude/.secrets/gemini_key').read().strip()
U = f"https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-2.5-flash-image:generateContent?key={K}"
STYLE = ("Hand-drawn 2D illustration in the style of a modern indie animated short film: clean confident ink outlines, flat cel shading, "
         "muted blue-violet shadows and warm orange sunlight, subtle paper grain, slightly exaggerated cartoon proportions, cinematic composition. "
         "No text, no letters, no watermark.")
def img(prompt, out, refs=(), aspect="9:16", tries=8):
    parts = []
    for r in refs:
        parts.append({"inlineData": {"mimeType": "image/png", "data": base64.b64encode(open(r, 'rb').read()).decode()}})
    pre = ("Use the attached reference images to keep the SAME characters (same face, hair, clothes, colors, proportions) and the SAME art style. " if refs else "")
    parts.append({"text": pre + prompt + " " + STYLE})
    for a in range(tries):
        try:
            r = requests.post(U, json={"contents": [{"role": "user", "parts": parts}],
                                       "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}, timeout=240)
            for p in r.json()["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    open(out, "wb").write(base64.b64decode(p["inlineData"]["data"])); return True
            print("noimg", r.text[:200])
        except Exception as e: print("err", e, getattr(r, 'text', '')[:200])
        time.sleep(15 * (a + 1))
    return False
