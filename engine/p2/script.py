# My Stepdad Is a Cop — Part 2
VOICES = {"N": ("af_heart", 0.98, 1.0), "M": ("af_heart", 1.04, 1.0), "MO": ("af_nicole", 0.95, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[
        ("N", "Last time, I finally told someone the truth.", 0.3),
        ("N", "And the officer they sent to my school... was my stepdad.", 0.0)],
        sfx=[("boom", 1, 9, 0.0)]),
    dict(id="b", lead=0.2, tail=0.35, lines=[
        ("D", "Ma'am, she's a great kid. But she's clumsy... and she's got a big imagination.", 0.35),
        ("A", "Officer, these marks look like someone grabbed her.", 0.35),
        ("D", "Careful, ma'am. Accusing a police officer is a very serious thing.", 0.4, 0.92),
        ("N", "I watched Ms. Alvarez's face change. She was scared of him too.", 0.4),
        ("N", "But when Dale turned to sign the papers, she slipped something into my pocket.", 0.3),
        ("A", "If you ever need me, call this number. Day or night.", 0.0, 0.9)],
        sfx=[]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("N", "The ride home was silent. He kept watching me in the mirror.", 0.4),
        ("D", "You embarrassed me today, kiddo. That won't happen again.", 0.35, 0.92),
        ("D", "Phone. Now.", 0.4, 0.9),
        ("N", "He took my phone, my laptop... even my house key.", 0.0)],
        sfx=[("rain", None, None, 0.0)]),
    dict(id="d", lead=0.2, tail=0.35, lines=[
        ("N", "Mom was waiting at the door. I ran to her, but she just whispered...", 0.35),
        ("MO", "Please, baby... just don't make him angry.", 0.45),
        ("N", "That night, I heard him laughing on the phone with his buddies from the station... like nothing had happened.", 0.35),
        ("N", "That's when I understood. If anyone was going to save us... it had to be me.", 0.0)],
        sfx=[]),
    dict(id="e", lead=0.2, tail=0.35, lines=[
        ("N", "But Dale didn't know about my old phone.", 0.25),
        ("N", "The screen was cracked, but the voice recorder still worked.", 0.3),
        ("N", "I charged it under my blanket, and practiced every night. Where to hide it. How to press record without looking.", 0.0)],
        sfx=[("tick", 1, 8, 0.0)]),
    dict(id="f", lead=0.2, tail=0.35, lines=[
        ("N", "Two nights later, he started yelling at Mom again. I hid the phone on the kitchen shelf, and pressed record.", 0.35),
        ("D", "You think anyone will believe you over me? You leave, and you lose everything. The house. Your job. Her.", 0.4),
        ("MO", "Dale, please... she can hear you.", 0.35),
        ("N", "My hands were shaking so hard, I was sure he could hear my heartbeat.", 0.0)],
        sfx=[("tick", 0, 19, 0.0), ("heartbeat", 3, None, -0.2)]),
    dict(id="g", lead=0.2, tail=0.4, lines=[
        ("N", "I had almost everything I needed.", 0.4),
        ("N", "And then... my phone beeped.", 0.5),
        ("D", "What was that?", 0.4, 0.92),
        ("N", "He turned around... and walked straight toward the shelf.", 0.0)],
        sfx=[("beep", 1, 4, 0.05), ("heartbeat", None, None, 0.0)]),
    dict(id="h", lead=0.1, tail=2.7, lines=[
        ("N", "His hand was inches away.", 0.0, 0.95)],
        sfx=[("boom", 0, 4, 0.1), ("riser", None, None, 0.1)]),
]
