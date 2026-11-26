MOOD = {"a": "tense", "b": "mystery", "c": "sad", "d": "sad", "e": "mystery", "f": "tense", "g": "dark", "h": "tense", "i": "action",
        "j": "tense", "k": "dark", "l": "dark"}
AMB = {"a": ("hall", 1), "b": ("hall", 1), "c": ("hall", 0.8), "d": ("hall", 0.8), "e": ("room", 1), "f": ("hall", 1), "g": ("rain", 1.6),
       "h": ("hall", 1), "i": ("room", 1), "j": ("hall", 0.6), "k": ("hall", 0.8), "l": ("hall", 0.6)}
CUES = [
    ("a", 0.0, "clock_tick", 0.5), ("a", "next", "sting", 0.7),
    ("b", "carpet", "swish", 0.3), ("b", "before", "hit", 0.4),
    ("c", "burned", "hit", 0.8), ("c", "burned", "static", 0.25, 0.0, 0.3),
    ("d", "crying", "gasp", 0.3, -0.3), ("d", "standing", "sting", 0.5),
    ("e", "searching", "door_open", 0.7, 0.4), ("e", "bed", "steps", 0.4), ("e", "stuck", "clock_tick", 0.9), ("e", "fourteen", "hit", 0.6),
    ("f", "ticket", "paper", 1.0), ("f", "night", "hit", 0.6),
    ("g", "rain", "thunder", 0.6), ("g", "bright", "brakes", 0.8, 0.0, -0.3), ("g", "lights#1", "crash", 0.7, 0.0, 0.6),
    ("h", "flickers", "tv_on", 1.0, -0.2), ("h", "leave", "sting", 0.5),
    ("i", "maya", "door_open", 0.6, 0.4), ("i", "nothing", "door_close", 0.5, 0.4), ("i", "desk", "paper", 0.6, -0.3), ("i", "nothing#1", "thud", 0.4),
    ("j", "pocket", "swish", 0.4), ("j", "cold", "heartbeat", 0.7),
    ("k", "key", "card_slide", 1.0), ("k", "key", "hit", 0.8), ("k", "everyone", "sting", 0.9), ("k", "everyone", "murmur", 0.4),
    ("l", "would", "riser", 0.5),
]
