VOICES = {"N": ("af_bella", 0.95, 1.0), "LI": ("af_sarah", 0.92, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "On my birthday, I got a text from a number I didn't know. Happy birthday, sweetheart. Mom loves you.", 0.0)], sfx=[("tick", 0, 9, 0.0)]),
    dict(id="b", lead=0.2, tail=0.3, lines=[("N", "My mom passed away two years ago. For a second... I couldn't breathe.", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.3, lines=[("N", "I wrote back: I think you have the wrong number. But thank you. Today, I really needed that.", 0.0)], sfx=[]),
    dict(id="d", lead=0.2, tail=0.3, lines=[("N", "Five minutes later, she called me. Her name was Linda.", 0.3),
        ("LI", "My daughter used to have this number. She passed away last year. I still text her... on her birthday.", 0.4, 0.92),
        ("N", "Her daughter and I had the same birthday.", 0.0)], sfx=[("boom", 2, 1, 0.0)]),
    dict(id="e", lead=0.2, tail=2.6, lines=[("N", "Now, every year, Linda sends me a birthday text. And every year... I send one back.", 0.0)], sfx=[("chime", 0, None, 0.0)]),
]
