exec(open("/home/claude/short/hs_voices.py").read())
S = lambda i, lines, tail=0.3: dict(id=i, lead=0.15, tail=tail, lines=lines, sfx=[])
SCENES = [
    S("a", [("N", "He stands up. One step toward the closet. Then another. You can see his eyes through the slats.", 0.0)]),
    S("b", [("N", "And then, red and blue lights flood the window. Sirens. Doors slamming outside.", 0.3), ("DIAZ", "Police! Nobody move!", 0.0)]),
    S("c", [("N", "The man panics. He runs for the hallway, back toward the attic. But Biscuit is faster. He grabs the hoodie, and he does not let go.", 0.0)]),
    S("d", [("N", "Boots thunder up the stairs. It's over in seconds.", 0.3), ("DIAZ", "We got him. You're safe now. You can come out.", 0.0)]),
    S("e", [("N", "Officer Diaz climbs into the attic with a flashlight. And what she finds up there makes her go very quiet.", 0.0)]),
    S("f", [("N", "A sleeping bag. Empty food boxes. Your missing phone charger. And a notebook. Day one. Day two. Day forty one.", 0.0)]),
    S("g", [("DIAZ", "His name is Daniel Hale. He grew up in this house, and lost it years ago. He's been living above you for forty one days.", 0.0)]),
    S("h", [("N", "Forty one days. Every single night, he was right above your bed. Listening.", 0.0)]),
    S("i", [("N", "Your parents drive all night to get home. Mom hugs you so tight you can barely breathe.", 0.3), ("MOM", "I'm never leaving you alone again. Never.", 0.0)]),
    S("j", [("N", "And Biscuit? He gets the biggest steak of his life.", 0.0)]),
    S("k", [("N", "One week later. Three oh seven in the morning. The speaker wakes you up again.", 0.3), ("NOVA", "Motion detected. Attic.", 0.0)]),
    S("l", [("NOVA", "Occupants detected. Four.", 0.4), ("N", "There are only three of you. Would you go check? Follow for the next story.", 0.0)], tail=2.6),
]
