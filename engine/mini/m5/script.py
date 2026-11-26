VOICES = {"N": ("am_puck", 0.97, 1.0), "GP": ("bm_george", 0.9, 0.97)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "My grandpa left me one last voicemail before he passed away. It made no sense.", 0.0)], sfx=[]),
    dict(id="b", lead=0.2, tail=0.3, lines=[("GP", "Hey, champ. It's Grandpa. Don't forget... check the blue box. Love you, kiddo.", 0.0, 0.9)], sfx=[("tick", None, None, 0.0)]),
    dict(id="c", lead=0.2, tail=0.3, lines=[("N", "Blue box? We searched his whole house. His closet. His attic. His garage. Nothing.", 0.0)], sfx=[]),
    dict(id="d", lead=0.2, tail=0.3, lines=[("N", "Then, after the funeral, I saw it. His old blue toolbox, sitting in the back of Dad's truck.", 0.35),
        ("N", "There were no tools inside. Just envelopes. One for every birthday... until I turn eighteen.", 0.0)], sfx=[("chime", 1, None, 0.0)]),
    dict(id="e", lead=0.2, tail=2.6, lines=[("N", "The first one said: Happy fourteenth, champ. I'm still cheering for you.", 0.4),
        ("N", "I'm saving the rest. One a year. Just like he planned.", 0.0)], sfx=[("chime", 1, None, 0.0)]),
]
