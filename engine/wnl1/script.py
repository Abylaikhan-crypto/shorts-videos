NAT = "Read in a calm, natural, quiet storytelling voice, like telling a friend something unsettling late at night. Not dramatic, not theatrical"
VOICES = {"N": ("gemini:Orus", 1, 1, NAT),
          "CAP": ("gemini:Iapetus", 1, 1, "Read as an airline captain speaking on the cabin PA. Calm, controlled, a little tired, with tension underneath"),
          "CP": ("gemini:Iapetus", 1, 1, "Read as a tired airline captain speaking quietly and urgently to one person in the cockpit"),
          "FA": ("gemini:Kore", 1, 1, "Read as a frightened flight attendant trying to stay professional, quiet and quick"),
          "MAN": ("gemini:Algenib", 1, 1, "Read as a cold, calm, quiet man. Slow and threatening")}
RADIO = ["CAP"]
SCENES = [
    dict(id="a", lead=0.15, tail=0.3, lines=[('N', "Imagine you're on a night flight to Denver. Seat fourteen C. It's two fourteen in the morning, and you just woke up.", 0.0)], sfx=[]),
    dict(id="b", lead=0.15, tail=0.3, lines=[('N', 'The cabin lights are red. Nobody is talking. Then, the speakers crackle.', 0.0)], sfx=[]),
    dict(id="c", lead=0.15, tail=0.3, lines=[('CAP', 'Ladies and gentlemen, this is your captain. Please stay in your seats. We will not be landing in Denver.', 0.5), ('CAP', 'We will not be landing... at all.', 0.0)], sfx=[]),
    dict(id="d", lead=0.15, tail=0.3, lines=[('N', 'For a second, the whole plane is silent. Then everyone starts talking at once.', 0.0)], sfx=[]),
    dict(id="e", lead=0.15, tail=0.3, lines=[('N', "You look at the screen on the seat in front of you. The little plane isn't heading to Denver anymore. It's flying in circles. Over the ocean.", 0.0)], sfx=[]),
    dict(id="f", lead=0.15, tail=0.3, lines=[('N', "And in the corner, a number you've never noticed before. Fuel. One hour, fifty-eight minutes.", 0.0)], sfx=[]),
    dict(id="g", lead=0.15, tail=0.3, lines=[('N', 'A flight attendant hurries down the aisle. Her name tag says Nina. Her hands are shaking.', 0.3), ('FA', "Please, stay calm. The cockpit isn't answering. And the door code... doesn't work.", 0.0)], sfx=[]),
    dict(id="h", lead=0.15, tail=0.3, lines=[('N', "You have three options. Help the crew break into the cockpit. Find out if there's a pilot on board. Or sit down, and trust the captain.", 0.0)], sfx=[]),
    dict(id="i", lead=0.15, tail=0.3, lines=[('N', "Before you can decide, you notice the man in seat one A. Everyone else is panicking. He's reading a newspaper. Calm. Like he knew this would happen.", 0.0)], sfx=[]),
    dict(id="j", lead=0.15, tail=0.3, lines=[('N', 'He looks right at you. And smiles.', 0.0)], sfx=[]),
    dict(id="k", lead=0.15, tail=0.3, lines=[('N', 'Then the speakers crackle again.', 0.3), ('CAP', 'Passenger in seat fourteen C. Please come to the cockpit.', 0.6), ('CAP', 'Alone.', 0.0)], sfx=[]),
    dict(id="l", lead=0.15, tail=2.6, lines=[('N', "That's your seat. Would you go? Part two is coming.", 0.0)], sfx=[]),
]
