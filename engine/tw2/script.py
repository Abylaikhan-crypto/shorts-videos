exec(open("/home/claude/short/tw_voices.py").read())
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "Last time, I came home and found my twin sister living my life. And Mom thought I was Lana.", 0.0)],
         sfx=[("boom", 0, 10, 0.0)]),
    dict(id="b", lead=0.2, tail=0.35, lines=[
        ("N", "I tried to explain. But Lana was always one step ahead.", 0.3),
        ("L", "Mom, it's me! I'm Lily! She's lying!", 0.3),
        ("LA", "Mom... she's doing it again. She's been jealous ever since the scholarship.", 0.3),
        ("MO", "Girls, enough! Lana, I am not doing this tonight.", 0.35),
        ("N", "Every time I opened my mouth, I sounded crazier.", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("N", "So I called Zoe. Our secret test. Only the real Lily would know the answer.", 0.3),
        ("Z", "Okay. What did we bury in my backyard in fourth grade?", 0.35),
        ("N", "But before I could answer, Lana texted her first. She'd read my diary. All of it.", 0.35),
        ("Z", "Lana, I don't know what's going on with you... but please, stop calling me.", 0.0)], sfx=[("tick", 2, 9, 0.0)]),
    dict(id="d", lead=0.2, tail=0.35, lines=[
        ("N", "On Monday, I ran to the academy for my interview. But the guard stopped me at the door.", 0.3),
        ("G", "Sorry, miss. Lily Carter already checked in. Ten minutes ago.", 0.35),
        ("N", "I showed him my student ID. He looked at the photo... then at me... and laughed.", 0.3),
        ("G", "Nice try, kid. You two really look alike, huh?", 0.35),
        ("N", "Through the window, I saw her. Showing my drawings. Smiling my smile.", 0.3),
        ("I", "These are wonderful, Lily. Truly.", 0.4),
        ("N", "When she walked out, she passed right by me. And whispered...", 0.3),
        ("LA", "Go home, Lana.", 0.0, 0.9)], sfx=[]),
    dict(id="e", lead=0.2, tail=0.35, lines=[
        ("N", "That night, I searched Lana's room. Under her mattress, I found a notebook.", 0.35),
        ("N", "Day one: practice her handwriting. Day twenty: learn her passwords. Day forty-seven: she still doesn't suspect a thing.", 0.3),
        ("N", "There were photos of me. Notes on how I laugh. How I tie my shoes. How I hold my...", 0.3),
        ("N", "No. That page was torn out.", 0.4, 0.94),
        ("N", "Day sixty: become Lily. Forever.", 0.0, 0.92)], sfx=[("heartbeat", None, None, 0.0)]),
    dict(id="f", lead=0.2, tail=2.8, lines=[
        ("N", "Then I turned to the last page.", 0.5),
        ("LA", "Day sixty-one. Make sure the real Lily disappears.", 0.0, 0.9)], sfx=[("boom", 1, 5, 0.0), ("riser", 1, None, 0.3)]),
]
