# Paper & Plot — video engine

Everything that builds the channel's videos. Rendered videos live in the folders next to this one.

## Pipeline
1. `<ep>/script.py` — voices + scenes (lines, pauses, sfx)
2. `python make_audio.py <ep>/script.py` — voice (Kokoro offline or Google Gemini TTS via `gtts.py`) → `<ep>/timeline.json`
3. `<ep>_shots.py` — shot list per scene (cuts on words), exec'd by `dna.py`
4. `python dna.py <ep> mids` (previews) / `python dna.py <ep> render` — Cairo frames → ffmpeg
5. `python mix.py <ep> out.mp4 '{"a":"tense",...}'` — music, sfx, loudness, final mp4

## Pieces
- `rig.py` — cartoon character rig and drawing helpers
- `s2.py` — style-2 camera, rooms, depth helpers
- `dna.py` — engine for style-2 episodes (shots, whip pans, captions, hook card, lighting pass, HUD)
- `hor_common.py`, `plane_common.py` — sets and props for horror / plane series
- `b3d/plane.py` — Blender (bpy) scenes rendered into 3D background plates (`pip install bpy`)
- older styles: `part1*.py`, `twins_common.py`, `ng_common.py`, `mini.py`

## Not stored here
- Kokoro model files (`kokoro-v1.0.onnx`, `voices-v1.0.bin`) — download from the kokoro-onnx release
- Google key — read from `/home/claude/.secrets/gemini_key` (never commit it)
- Fonts: Poppins (Google Fonts)
