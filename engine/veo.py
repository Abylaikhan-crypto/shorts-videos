"""python veo.py <image.png> <out.mp4> "<prompt>" [seconds]  — image-to-video via Vertex Veo (express key)"""
import requests, base64, sys, time, json
K=open('/home/claude/.secrets/gemini_key').read().strip()
img, out, prompt = sys.argv[1], sys.argv[2], sys.argv[3]; dur=int(sys.argv[4]) if len(sys.argv)>4 else 4
B="https://aiplatform.googleapis.com/v1/projects/566811517046/locations/us-central1/publishers/google/models/"
body={"instances":[{"prompt":prompt,"image":{"bytesBase64Encoded":base64.b64encode(open(img,'rb').read()).decode(),"mimeType":"image/png"}}],
      "parameters":{"aspectRatio":"9:16","durationSeconds":dur,"sampleCount":1,"generateAudio":False,"resolution":"720p"}}
for m in sys.argv[5:] or ["veo-3.1-fast-generate-001","veo-3.0-fast-generate-001","veo-2.0-generate-001"]:
    r=requests.post(B+m+":predictLongRunning?key="+K,json=body,timeout=120)
    print(m, r.status_code, r.text[:200], flush=True)
    if r.status_code!=200: continue
    op=r.json()["name"]
    for i in range(90):
        time.sleep(8)
        q=requests.post(B+m+":fetchPredictOperation?key="+K,json={"operationName":op},timeout=60).json()
        if q.get("done"):
            if "error" in q: print("ERR",q["error"]); break
            v=q["response"]["videos"][0]
            open(out,"wb").write(base64.b64decode(v["bytesBase64Encoded"])); print("saved",out,"after",(i+1)*8,"s"); sys.exit()
    break
