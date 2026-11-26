VOICES = {"N": ("am_onyx", 0.88, 0.98), "MOM": ("af_sarah", 0.88, 0.95), "WH": ("af_nicole", 0.82, 0.84), "LL": ("bm_george", 0.95, 0.92),
          "NB": ("bf_emma", 0.88, 0.92)}
SENT_PAUSE = 0.45
COMMA_PAUSE = 0.2
SCENES = [
    dict(id="a", lead=0.3, tail=0.25, lines=[("N", "Your heart is pounding. One hundred and twenty beats per minute. And it can hear every single one.", 0.0)], sfx=[("heartbeat", None, None, 0.0)]),
    dict(id="b", lead=0.15, tail=0.25, lines=[("N", "You need to slow it down. Breathe in for four seconds. Hold for four. Out for four.", 0.0)], sfx=[]),
    dict(id="c", lead=0.15, tail=0.25, lines=[("N", "One hundred. Ninety. Eighty. The knocking gets quieter.", 0.0)], sfx=[("knock", 0, 6, 0.0)]),
    dict(id="d", lead=0.15, tail=0.25, lines=[("N", "Then the TV turns on by itself. It's showing the hallway camera.", 0.0)], sfx=[("beep", 0, 3, 0.0)]),
    dict(id="e", lead=0.15, tail=0.25, lines=[("N", "The hallway light flickers. And every time it goes dark, something is standing there. Too tall. Too thin.", 0.0)], sfx=[("boom", 0, 12, 0.0)]),
    dict(id="f", lead=0.15, tail=0.25, lines=[("N", "You find the missing piece of the note, stuck under a fridge magnet.", 0.3),
        ("N", "Rule three. It will try to make you say, come in. Don't say anything. Not one word.", 0.0)], sfx=[("boom", 1, 0, 0.0)]),
    dict(id="g", lead=0.15, tail=0.25, lines=[("N", "Knock. Knock. Then a new voice. Old. Sweet.", 0.25),
        ("NB", "Honey, it's Missus Patel from nine B. I heard screaming. Are you okay?", 0.0)], sfx=[("knock", 0, 0, 0.0), ("knock", 0, 1, 0.0)]),
    dict(id="h", lead=0.15, tail=0.25, lines=[("N", "You almost answer. Then you remember. Nine B has been empty for six years.", 0.0)], sfx=[("boom", 0, 7, 0.0)]),
    dict(id="i", lead=0.15, tail=0.25, lines=[("N", "The voice changes.", 0.3),
        ("WH", "You can't stay quiet forever.", 0.0)], sfx=[]),
    dict(id="j", lead=0.15, tail=0.25, lines=[("N", "And then you hear it. The chain on your door. Sliding. Slowly. By itself.", 0.0)], sfx=[("clink", 0, 7, 0.0)]),
    dict(id="k", lead=0.15, tail=2.6, lines=[("N", "You have three seconds. A, hold the door. B, hide in the bathroom. C, find the last rule.", 0.3),
        ("N", "Comment A, B, or C. The final part is coming.", 0.0)], sfx=[("riser", 1, None, 0.0)]),
]
