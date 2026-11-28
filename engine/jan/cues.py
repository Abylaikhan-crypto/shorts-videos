MOOD = {"a": "sad", "b": "sad", "c": "warm", "d": "tense", "e": "tense", "f": "warm", "g": "action", "h": "warm", "i": "sad", "j": "sad",
        "k": "sad", "l": "warm", "m": "warm"}
AMB = {"a": ("room", 1), "b": ("room", 0.8), "d": ("rain", 1.4), "e": ("hall", 1), "g": ("room", 1), "i": ("room", 0.7), "j": ("room", 0.7)}
CUT_WHOOSH = 0.08
CUES = [
    ("a", "kids", "swish", 0.2),
    ("b", "walked", "door_open", 0.5),
    ("c", "locker", "door_unlock", 0.6), ("c", "bike", "click", 0.5),
    ("d", "storm", "thunder", 0.8), ("d", "out", "power_down", 0.9), ("d", "buses", lambda: __import__("sfx2").brakes(1.0), 0.3),
    ("e", "panicking", "heartbeat", 0.5),
    ("f", "lights", "power_up", 0.9), ("f", "gym", "swell", 0.6),
    ("g", "started", "hit", 0.5), ("g", "generator", "power_up", 0.6),
    ("h", "blankets", "paper", 0.4), ("h", "running", "thud", 0.3),
    ("i", "hands", "sting", 0.35),
    ("j", "photo", "paper", 0.6), ("j", "badge", "swish", 0.3),
    ("k", "fire", "hit", 0.5), ("k", "anyone", "swell", 0.6),
    ("l", "clapping", lambda: __import__("sfx2").norm(__import__("sfx2").bp(__import__("sfx2").noise(4.0), 500, 6000) * (abs(__import__("sfx2").noise(4.0)) > 2.2), 0.6), 0.9),
    ("m", "walter", "swell", 0.5),
]
