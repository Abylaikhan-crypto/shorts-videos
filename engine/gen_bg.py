"""python gen_bg.py <outdir> name1 name2 ...  (prompts from PROMPTS)"""
import json, base64, urllib.request, sys, time, os
KEY = open('/home/claude/.secrets/gemini_key').read().strip()
STYLE = (" Vertical 9:16 background for an animated YouTube Short. Stylized 3D cartoon look like a Pixar film background, clean shapes, "
         "rich detail, cinematic lighting, soft haze, no people, no characters, no text, no letters, no words.")
PROMPTS = {
    "room714": "Old hotel room at night seen from the foot of the bed: a double bed with white sheets, a boxy old TV glowing blue on a wooden dresser, a window with thick gray fog outside, a dim bedside lamp, vintage patterned wallpaper, eerie and quiet.",
    "room_tv": "Close view of an old boxy television on a wooden dresser in a dark vintage hotel room, the screen glowing cold blue and lighting the wall, a little haze.",
    "window_fog": "Hotel room window at night with heavy curtains, outside only thick featureless gray fog pressing against the glass, cold light.",
    "corridor": "Long narrow vintage hotel corridor, symmetrical one-point perspective, deep red patterned carpet, brass wall sconces with warm light, many wooden doors with brass numbers on both sides, eerie and endless, slight haze.",
    "corridor_dark": "The same long vintage hotel corridor almost completely dark, only a green emergency exit light at the far end and faint reflections on the red carpet, very eerie.",
    "elevator": "Closed vintage brass elevator doors in an old hotel hallway, an unlit floor indicator above, warm dim sconce light, scratched metal.",
    "stair_door": "Heavy gray metal stairwell door in an old hotel hallway with a small key card reader glowing red next to it, cold light, slightly dirty walls.",
    "lobby": "Abandoned old grand hotel lobby at night, long wooden front desk, dusty chandelier, a staircase, faded red carpet, soft warm and blue light through dust.",
    "bus_rain": "Inside a city bus at night during heavy rain, seen down the aisle toward the windshield, blinding bright headlights glaring through the wet windshield, raindrops, blue and white light.",
    "hospital": "Quiet hospital room in the morning, a bed with white sheets, heart monitor with green lines, window with warm golden sunrise light, soft and hopeful.",
    "light_door": "An open heavy stairwell door in a dark hotel hallway with brilliant warm white light pouring out of it onto the carpet, glowing, peaceful and mysterious.",
}


REF = os.environ.get("REF")  # style anchor image: every new background copies its look
REFTXT = ("The attached image is the STYLE REFERENCE for a whole animated series. Create a NEW, different scene in exactly the same "
          "art style: same stylized 3D cartoon rendering, same level of detail and texture, same soft painterly shading, same lens and haze, "
          "same color grading and contrast. Do not copy its layout or objects. New scene: ")


def gen(name, out):
    parts = [{"text": PROMPTS[name] + STYLE}]
    if REF:
        parts = [{"inlineData": {"mimeType": "image/png", "data": base64.b64encode(open(REF, "rb").read()).decode()}},
                 {"text": REFTXT + PROMPTS[name] + STYLE}]
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "9:16"}}}
    url = f"https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-2.5-flash-image:generateContent?key={KEY}"
    for i in range(6):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            r = json.loads(urllib.request.urlopen(req, timeout=180).read())
            for p in r["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    open(f"{out}/{name}.png", "wb").write(base64.b64decode(p["inlineData"]["data"])); return True
        except Exception as e:
            print("retry", name, str(e)[:120], flush=True); time.sleep(10 * (i + 1))
    return False


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for n in sys.argv[2:]:
        if os.path.exists(f"{out}/{n}.png"): continue
        print(n, gen(n, out), flush=True)
