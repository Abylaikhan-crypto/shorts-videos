VOICES = {"N": ("af_sky", 1.0, 1.0), "MO": ("af_sarah", 0.98, 1.0), "DOC": ("am_eric", 0.95, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "I pretended to be sick to skip a math test. Worst decision of my life.", 0.0)], sfx=[]),
    dict(id="b", lead=0.2, tail=0.3, lines=[("N", "I coughed. I groaned. I even pressed my forehead against the heater to make it hot.", 0.3),
        ("MO", "Oh no, honey, you're burning up! We're going to the doctor. Right now.", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.3, lines=[("N", "The doctor looked at me for exactly three seconds. Then he winked at my mom.", 0.3),
        ("DOC", "Hmm. This is serious. No phone. No TV. No sweets. Just plain soup... for three whole days.", 0.0)], sfx=[("boom", 1, 3, 0.0)]),
    dict(id="d", lead=0.2, tail=0.3, lines=[("N", "Three days. No phone. Plain soup. I almost confessed right there in the office.", 0.0)], sfx=[]),
    dict(id="e", lead=0.2, tail=2.6, lines=[("N", "And when I finally went back to school... the math test had been moved. To that exact day.", 0.35),
        ("N", "I took it anyway. I got a C. Lesson learned.", 0.0)], sfx=[("tick", 1, 5, 0.0)]),
]
