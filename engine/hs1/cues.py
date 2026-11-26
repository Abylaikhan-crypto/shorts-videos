MOOD = {"a": "dark", "b": "mystery", "c": "mystery", "d": "tense", "e": "tense", "f": "tense", "g": "tense", "h": "dark", "i": "dark", "j": "tense",
        "k": "none", "l": "dark"}
AMB = {k: ("room", 1.0) for k in "abcdefghijkl"}
AMB.update({"b": ("hall", 0.8), "d": ("room", 0.8)})
CUES = [
    ("a", "speaker", "swish", 0.3), ("a", "three", "hit", 0.6), ("a", "kitchen", "sting", 0.6),
    ("b", "biscuit", "swish", 0.3),
    ("c", "growling", "heartbeat", 0.5),
    ("d", "camera", "click", 0.6), ("d", "fridge", "static", 0.25), ("d", "nobody", "hit", 0.5),
    ("e", "plate", "thud", 0.25), ("e", "fork", "click", 0.5), ("e", "someone", "sting", 0.6),
    ("f", "buzzes", "phone_dead", 0.6), ("f", "attic", "hit", 0.5),
    ("g", "lock", "door_unlock", 0.5), ("g", "locked", "door_unlock", 0.7), ("g", "occupants", "riser", 0.5), ("g", "two", "hit", 1.0),
    ("h", "else", "sting", 0.8), ("h", "time", "heartbeat", 0.7),
    ("i", "creaks", "creak", 1.0), ("i", "footsteps", "steps", 0.6), ("i", "moving", "steps", 0.5), ("i", "right", "heartbeat", 0.6),
    ("k", "stop", "hit", 0.4), ("k", "whispers", "riser", 0.4),
    ("l", 0.1, "static", 0.25), ("l", "what", "sting", 0.6),
]
