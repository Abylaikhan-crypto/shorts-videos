VOICES = {"N": ("af_kore", 0.95, 1.0), "LL": ("af_aoede", 0.95, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "Every single day, the lunch lady gave me a double portion. Just me. Nobody else.", 0.0)], sfx=[]),
    dict(id="b", lead=0.2, tail=0.3, lines=[("N", "At first, I thought she just liked me. But then I noticed... it started right after my dad lost his job.", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.3, lines=[("N", "We never told anyone. Mom said it was our secret. Some nights, dinner was just toast. So how did she know?", 0.0)], sfx=[]),
    dict(id="d", lead=0.2, tail=0.3, lines=[("N", "On the last day of school, I finally asked her.", 0.3),
        ("LL", "Sweetheart, I was you once. Same empty lunchbox. Same brave little face. A lunch lady fed me for two whole years.", 0.0, 0.93)], sfx=[]),
    dict(id="e", lead=0.2, tail=2.6, lines=[("N", "Then she handed me an envelope. Inside was a grocery gift card, and a note: Pass it on someday.", 0.35),
        ("N", "I'm a nurse now. And I always carry snacks for the kids in the waiting room.", 0.0)], sfx=[("chime", 1, None, 0.0)]),
]
