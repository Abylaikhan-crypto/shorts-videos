import requests, base64, sys, time, json, os
from concurrent.futures import ThreadPoolExecutor
K=open('/home/claude/.secrets/gemini_key').read().strip()
B="https://aiplatform.googleapis.com/v1/projects/566811517046/locations/us-central1/publishers/google/models/veo-3.1-fast-generate-001"
exec(open('/home/claude/short/jan/shots.py').read())
PL={p['id']:p for p in json.load(open('/home/claude/short/jan/plan.json'))}
KEEP=(" Keep exactly the same 2D hand-drawn art style, ink outlines, flat colors and character designs as the image. Smooth natural motion, "
      "no new characters appear, no text appears, no speech, mouths mostly closed, no scene cuts.")
only=set(sys.argv[1:])
def run(s):
    sid=s[0]; out=f"/home/claude/short/jan/clips/{sid}.mp4"
    if os.path.exists(out) and not only: return sid,'skip'
    body={"instances":[{"prompt":s[5]+KEEP,"image":{"bytesBase64Encoded":base64.b64encode(open(f"/home/claude/short/jan/key/{sid}.png",'rb').read()).decode(),"mimeType":"image/png"}}],
          "parameters":{"aspectRatio":"9:16","durationSeconds":PL[sid]['veo'],"sampleCount":1,"generateAudio":False,"resolution":"720p"}}
    for a in range(10):
        try:
            r=requests.post(B+":predictLongRunning?key="+K,json=body,timeout=120)
            if r.status_code!=200: time.sleep(20*(a+1)); continue
            op=r.json()["name"]
            for i in range(80):
                time.sleep(8)
                q=requests.post(B+":fetchPredictOperation?key="+K,json={"operationName":op},timeout=60).json()
                if q.get("done"):
                    vs=q.get("response",{}).get("videos",[])
                    if vs and "bytesBase64Encoded" in vs[0]:
                        open(out,"wb").write(base64.b64decode(vs[0]["bytesBase64Encoded"])); return sid,'ok'
                    print(sid,'bad',str(q)[:200],flush=True); break
        except Exception as e: print(sid,'exc',e,flush=True)
        time.sleep(15)
    return sid,'FAIL'
todo=[s for s in SHOTS if not only or s[0] in only]
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(run,todo): print(r,flush=True)
