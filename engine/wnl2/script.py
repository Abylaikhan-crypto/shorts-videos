NAT = "Read in a calm, natural, quiet storytelling voice, like telling a friend something unsettling late at night. Not dramatic, not theatrical"
VOICES = {"N": ("gemini:Orus", 1, 1, NAT),
          "CAP": ("gemini:Iapetus", 1, 1, "Read as an airline captain speaking on the cabin PA. Calm, controlled, a little tired, with tension underneath"),
          "CP": ("gemini:Iapetus", 1, 1, "Read as a tired airline captain speaking quietly and urgently to one person in the cockpit"),
          "FA": ("gemini:Kore", 1, 1, "Read as a frightened flight attendant trying to stay professional, quiet and quick"),
          "MAN": ("gemini:Algenib", 1, 1, "Read as a cold, calm, quiet man. Slow and threatening")}
RADIO = ["CAP"]
SCENES = [
    dict(id="a", lead=0.15, tail=0.3, lines=[('N', "Every head on the plane turns to you. Fourteen C. You walk down the aisle. Past Nina. Past the man in one A. This time, he doesn't look up.", 0.0)], sfx=[]),
    dict(id="b", lead=0.15, tail=0.3, lines=[('N', 'The cockpit door clicks open. Just enough for one person.', 0.0)], sfx=[]),
    dict(id="c", lead=0.15, tail=0.3, lines=[('N', 'Inside, the captain is alone. The co-pilot is slumped against the window. Breathing, but out cold.', 0.0)], sfx=[]),
    dict(id="d", lead=0.15, tail=0.3, lines=[('CP', "Food poisoning. Came on an hour ago. I can't leave this seat. Not for a second.", 0.0)], sfx=[]),
    dict(id="e", lead=0.15, tail=0.3, lines=[('N', 'He points at a red light on the panel. Landing gear. Unsafe.', 0.0)], sfx=[]),
    dict(id="f", lead=0.15, tail=0.3, lines=[('CP', "The wheels won't come down. If we land like this, at this weight, nobody walks away. The passenger list says you fixed planes for six years. Is that true?", 0.0)], sfx=[]),
    dict(id="g", lead=0.15, tail=0.3, lines=[('N', "It is. You haven't touched a plane in years. But you nod.", 0.0)], sfx=[]),
    dict(id="h", lead=0.15, tail=0.3, lines=[('CP', "There's a hatch in the floor behind you. It leads to the equipment bay. There's a manual release down there. Pull it, and the wheels drop.", 0.0)], sfx=[]),
    dict(id="i", lead=0.15, tail=0.3, lines=[('N', "You climb down a cold metal ladder. It's dark. It's loud. And it's freezing.", 0.0)], sfx=[]),
    dict(id="j", lead=0.15, tail=0.3, lines=[('N', "Your flashlight finds the release handle. You pull. It doesn't move. Something is jammed in the mechanism.", 0.0)], sfx=[]),
    dict(id="k", lead=0.15, tail=0.3, lines=[('N', "A metal case. Silver. Locked. Wedged right where it shouldn't be. You turn it over. There's a luggage tag. Seat one A.", 0.0)], sfx=[]),
    dict(id="l", lead=0.15, tail=2.6, lines=[('N', 'And then, above you, the hatch slams shut. You hear the lock turn.', 0.4), ('N', 'Fuel. Forty-one minutes. What would you do? The final part is coming.', 0.0)], sfx=[]),
]
