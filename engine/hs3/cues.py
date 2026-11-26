MOOD = {"a": "dark", "b": "action", "c": "action", "d": "action", "e": "mystery", "f": "dark", "g": "sad", "h": "dark", "i": "warm", "j": "warm",
        "k": "none", "l": "dark"}
AMB = {k: ("room", 0.8) for k in "abcdefghl"}
AMB.update({"i": ("room", 0.5), "j": ("room", 0.5), "k": ("room", 1.0)})
CUES = [
    ("a", "stands", "creak", 0.6), ("a", "step", "thud", 0.5), ("a", "another", "thud", 0.6), ("a", "eyes", "sting", 0.8),
    ("b", "red", "hit", 0.8), ("b", "sirens", lambda: __import__("sfx2").brakes(1.2), 0.3), ("b", "doors", "door_slam", 0.8), ("b", "police", "door_slam", 0.5),
    ("c", "runs", "steps", 0.8), ("c", "faster", "whoosh", 0.6), ("c", "grabs", "hit", 0.7),
    ("d", "boots", "steps", 1.0), ("d", "over", "door_slam", 0.6), ("d", "safe", "swell", 0.5),
    ("e", "climbs", "creak", 0.6), ("e", "quiet", "sting", 0.6),
    ("f", "bag", "swish", 0.3), ("f", "boxes", "swish", 0.3), ("f", "charger", "swish", 0.3), ("f", "notebook", "paper", 0.8), ("f", "forty", "hit", 0.8),
    ("g", "hale", "hit", 0.4),
    ("h", "forty", "sting", 0.7), ("h", "listening", "heartbeat", 0.6),
    ("i", "hugs", "swell", 0.6),
    ("j", "steak", "swish", 0.4),
    ("k", "later", "whoosh", 0.4), ("k", "three", "clock_tick", 0.4), ("k", "motion", "riser", 0.4),
    ("l", "four", "hit", 1.0), ("l", "four", "sting", 0.8), ("l", "would", "riser", 0.4),
]
