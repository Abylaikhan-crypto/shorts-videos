"""python gen_music.py mood1 mood2 ... -> music/<mood>_<i>.wav (Lyria 2, ~33 s, 48k stereo, instrumental)"""
import requests, base64, sys, os, time
K = open('/home/claude/.secrets/gemini_key').read().strip()
U = f"https://aiplatform.googleapis.com/v1/publishers/google/models/lyria-002:predict?key={K}"
BASE = " Cinematic underscore for a short animated thriller, instrumental, steady tempo, no big changes, loopable, mixed quietly under narration."
P = {
    "tense": "Tense suspense underscore, slow ticking pulse, low string ostinato, dark synth drone, 90 bpm, anxious.",
    "dark": "Dark eerie ambient horror underscore, deep drones, distant metallic textures, sparse low piano notes, unsettling.",
    "sad": "Sad emotional underscore, soft solo piano with warm strings, slow, melancholic and tender.",
    "warm": "Hopeful emotional underscore, gentle piano and warm strings swelling softly, uplifting, bittersweet relief.",
    "mystery": "Mysterious curious underscore, plucked pizzicato strings, music box, soft celesta, dreamlike and uneasy.",
    "action": "Urgent driving thriller underscore, fast pulsing synth bass, staccato strings, building tension, 120 bpm.",
}
NEG = "vocals, singing, voice, lyrics, loud drums, electric guitar"
for mood in sys.argv[1:]:
    for i in range(3):
        out = f"music/{mood}_{i}.wav"
        if os.path.exists(out): continue
        for a in range(5):
            try:
                r = requests.post(U, json={"instances": [{"prompt": P[mood] + BASE, "negative_prompt": NEG, "seed": 1000 + i * 17}], "parameters": {}}, timeout=200)
                if r.status_code == 200:
                    open(out, "wb").write(base64.b64decode(r.json()["predictions"][0]["bytesBase64Encoded"])); print("ok", out, flush=True); break
                print("err", r.status_code, r.text[:150], flush=True)
            except Exception as e: print("exc", e, flush=True)
            time.sleep(10 * (a + 1))
