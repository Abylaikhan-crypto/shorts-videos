VOICES = {"N": ("am_onyx", 0.88, 0.98), "MOM": ("af_sarah", 0.88, 0.95), "WH": ("af_nicole", 0.82, 0.84), "LL": ("bm_george", 0.95, 0.92),
          "NB": ("bf_emma", 0.88, 0.92)}
SENT_PAUSE = 0.45
COMMA_PAUSE = 0.2
SCENES = [
    dict(id="a", lead=0.3, tail=0.25, lines=[("N", "You chose C. You tear the kitchen apart. And inside the salt jar, there's one last scrap of paper.", 0.0)], sfx=[("crash", 0, 9, 0.0)]),
    dict(id="b", lead=0.15, tail=0.25, lines=[("N", "Rule four. Pour salt across the doorway. Hold on until the elevator dings, at three thirty-three.", 0.0)], sfx=[("boom", 0, 0, 0.0)]),
    dict(id="c", lead=0.15, tail=0.25, lines=[("N", "You grab the salt. The chain falls. The door starts to open.", 0.0)], sfx=[("clink", 0, 6, 0.0)]),
    dict(id="d", lead=0.15, tail=0.25, lines=[("N", "You throw yourself against it, and pour the salt in one long line.", 0.0)], sfx=[("crash", 0, 2, 0.0)]),
    dict(id="e", lead=0.15, tail=0.25, lines=[("N", "The knocking turns into scratching. Long, slow scratching. All the way down the door.", 0.0)], sfx=[]),
    dict(id="f", lead=0.15, tail=0.25, lines=[("WH", "Let me in. Let me in. Let me in.", 0.0)], sfx=[("heartbeat", None, None, 0.0)]),
    dict(id="g", lead=0.15, tail=0.25, lines=[("N", "Three thirty-one. Three thirty-two. The hallway lights go out. One. By. One.", 0.0)], sfx=[("tick", 0, 0, 0.0), ("tick", 0, 2, 0.0)]),
    dict(id="h", lead=0.15, tail=0.25, lines=[("N", "Three thirty-three.", 0.6), ("N", "Ding. Then silence.", 0.0)], sfx=[("chime", 1, 0, 0.0)]),
    dict(id="i", lead=0.15, tail=0.25, lines=[("N", "In the morning, you call the landlord. You ask what happened to the last tenant.", 0.3),
        ("LL", "He opened the door.", 0.0)], sfx=[]),
    dict(id="j", lead=0.15, tail=0.25, lines=[("N", "Then you check the doorbell camera. Three oh seven A M.", 0.4),
        ("N", "The person knocking on your door was you.", 0.0)], sfx=[("boom", 1, 6, 0.0)]),
    dict(id="k", lead=0.2, tail=2.8, lines=[("N", "Would you have opened the door? Follow for the next story.", 0.0)], sfx=[("riser", 0, None, 0.0)]),
]
