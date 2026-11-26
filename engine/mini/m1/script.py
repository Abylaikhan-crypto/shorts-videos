VOICES = {"N": ("am_adam", 0.95, 1.0), "DA": ("am_michael", 1.0, 1.0), "F": ("am_onyx", 0.95, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "At three in the morning, our dog Max would not stop barking.", 0.0)], sfx=[("boom", 0, 1, 0.0)]),
    dict(id="b", lead=0.2, tail=0.3, lines=[("N", "We'd adopted him from the shelter just one week earlier. Dad was furious.", 0.3),
        ("DA", "Max! Quiet! Everyone's trying to sleep!", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.3, lines=[("N", "But Max didn't stop. He grabbed my sleeve with his teeth, and pulled me toward the door.", 0.3),
        ("N", "Then he ran to Mom and Dad's room and did the exact same thing.", 0.0)], sfx=[]),
    dict(id="d", lead=0.2, tail=0.3, lines=[("N", "So we followed him outside, in our pajamas, in the cold. My head was spinning. Mom felt dizzy too.", 0.0)], sfx=[]),
    dict(id="e", lead=0.2, tail=0.3, lines=[("F", "Carbon monoxide. Your detector's battery was dead. One more hour inside... and none of you would have woken up.", 0.0)], sfx=[("siren", None, None, 0.0)]),
    dict(id="f", lead=0.2, tail=2.6, lines=[("N", "The shelter told us Max had been returned three times... for barking too much at night.", 0.4),
        ("N", "He was never a bad dog. He was just waiting for someone to listen.", 0.0)], sfx=[("chime", 1, None, 0.0)]),
]
