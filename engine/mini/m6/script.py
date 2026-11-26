VOICES = {"N": ("af_heart", 0.95, 1.0), "R": ("bf_emma", 0.9, 0.98), "SON": ("am_michael", 0.95, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "Every morning, our old neighbor watched me walk to school. From her window. Every. Single. Day.", 0.0)], sfx=[("boom", 0, 14, 0.0)]),
    dict(id="b", lead=0.2, tail=0.3, lines=[("N", "Honestly, it creeped me out. I started taking the long way around, just to avoid her.", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.3, lines=[("N", "Then one morning, her window was empty. An ambulance was parked outside.", 0.0)], sfx=[("siren", 0, 10, 0.0)]),
    dict(id="d", lead=0.2, tail=0.3, lines=[("N", "A week later, her son knocked on our door, and handed me a notebook. Every page had a date... and a little note.", 0.3),
        ("R", "Emma got to school safe today. She was smiling.", 0.0, 0.9)], sfx=[]),
    dict(id="e", lead=0.2, tail=2.6, lines=[("SON", "She lost her daughter, years ago, on the way to school. After that, she watched every kid on this street. Just to be sure.", 0.4),
        ("N", "Now, I wave at her window every morning. Even though it's empty.", 0.0, 0.93)], sfx=[("chime", 1, None, 0.0)]),
]
