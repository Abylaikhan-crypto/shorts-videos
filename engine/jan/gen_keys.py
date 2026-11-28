import sys, os; sys.path.insert(0,'/home/claude/short'); from gimg import img
from concurrent.futures import ThreadPoolExecutor
exec(open('/home/claude/short/jan/shots.py').read())
only=set(sys.argv[1:])
def job(s):
    sid,sc,w,refs,kp,mp=s
    out=f"/home/claude/short/jan/key/{sid}.png"
    if os.path.exists(out) and not only: return sid,'skip'
    return sid, img(kp, out, refs=[f"/home/claude/short/jan/ref/{r}.png" for r in refs])
todo=[s for s in SHOTS if not only or s[0] in only]
with ThreadPoolExecutor(1) as ex:
    for r in ex.map(job, todo): print(r, flush=True)
