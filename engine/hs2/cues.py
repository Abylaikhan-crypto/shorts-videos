MOOD = {"a": "tense", "b": "tense", "c": "tense", "d": "dark", "e": "dark", "f": "mystery", "g": "dark", "h": "tense", "i": "dark", "j": "tense",
        "k": "tense", "l": "dark"}
AMB = {k: ("room", 0.8) for k in "abcdefghijkl"}
CUES = [
    ("a", "slip", "swish", 0.4), ("a", "shut", "door_close", 0.5),
    ("b", "call", "click", 0.5), ("b", "shaking", "heartbeat", 0.6),
    ("c", "eight", "hit", 0.5),
    ("d", "hatch", "creak", 0.9), ("d", "ladder", "door_open", 0.6), ("d", "one", "thud", 0.6), ("d", "two", "thud", 0.65), ("d", "three", "thud", 0.7),
    ("e", "shadow", "whoosh", 0.4), ("e", "man", "hit", 0.6), ("e", "hoodie", "sting", 0.7),
    ("f", "sense", "riser", 0.4), ("f", "food", "swish", 0.3), ("f", "hoodie", "swish", 0.3), ("f", "noises", "creak", 0.6),
    ("g", "knocks", lambda: __import__("sfx2").thud(0.25, 150), 1.2), ("g", "softly", lambda: __import__("sfx2").thud(0.25, 150), 1.0), ("g", "awake", "sting", 0.7),
    ("h", "growls", "heartbeat", 0.6), ("h", "four", "hit", 0.6),
    ("i", "handle", "door_unlock", 0.8), ("i", "turns", "creak", 0.7), ("i", "sits", "thud", 0.4), ("i", "room", "sting", 0.5),
    ("k", "lights", "phone_dead", 0.8), ("k", "slats", "hit", 0.6),
    ("l", "turns", "creak", 0.4), ("l", "smiles", "sting", 1.0), ("l", "what", "riser", 0.4),
]
