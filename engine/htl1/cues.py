MOOD = {"a": "mystery", "b": "mystery", "c": "dark", "d": "tense", "e": "tense", "f": "tense", "g": "tense", "h": "tense", "i": "tense",
        "j": "none", "k": "dark", "l": "dark"}
AMB = {"a": ("room", 1), "b": ("fog", 1.2), "c": ("room", 1), "d": ("hall", 1), "e": ("hall", 1), "f": ("hall", 1), "g": ("hall", 1),
       "h": ("hall", 1), "i": ("hall", 0.6), "j": ("hall", 0.5), "k": ("hall", 1), "l": ("hall", 0.8)}
CUES = [
    ("a", 0.0, "riser", 0.5), ("a", "room", "hit", 0.8), ("a", "bus", "brakes", 0.35, 0.3),
    ("b", "dead", "phone_dead", 0.8), ("b", "window", "thud", 0.4), ("b", "fog", "swish", 0.4),
    ("c", "turns", "tv_on", 1.0, 0.2), ("c", "one", "sting", 0.7),
    ("d", "open", "door_open", 0.9, -0.2), ("d", "one#1", "door_open", 0.6, 0.5, 0.2), ("d", "too", "door_open", 0.5, -0.6), ("d", "quiet", "murmur", 0.5),
    ("e", "businessman", "phone_dead", 0.4, 0.3), ("e", "boy", "gasp", 0.3),
    ("f", "joke", "hit", 0.35), ("f", "lawyer", "door_slam", 0.25, 0.5),
    ("g", "elevator", "elevator_dead", 1.0), ("g", "locked", "reader_denied", 0.9, 0.2), ("g", "card", "hit", 0.4),
    ("h", "calm", "heartbeat", 0.4),
    ("i", "search", "paper", 0.6), ("i", "break", "door_slam", 0.6), ("i", "wait", "door_close", 0.6),
    ("j", "lights", "power_down", 1.0), ("j", "darkness", "heartbeat", 0.8), ("j", "screams", "scream", 0.9, 0.4, -0.2),
    ("k", "back", "power_up", 0.9), ("k", "gone", "sting", 0.8), ("k", "sign", "creak", 0.5),
    ("l", "checked", "hit", 0.9), ("l", "who", "riser", 0.4),
]
