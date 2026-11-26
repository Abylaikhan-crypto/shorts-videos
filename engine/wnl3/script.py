NAT = "Read in a calm, natural, quiet storytelling voice, like telling a friend something unsettling late at night. Not dramatic, not theatrical"
VOICES = {"N": ("gemini:Orus", 1, 1, NAT),
          "CAP": ("gemini:Iapetus", 1, 1, "Read as an airline captain speaking on the cabin PA. Calm, controlled, a little tired, with tension underneath"),
          "CP": ("gemini:Iapetus", 1, 1, "Read as a tired airline captain speaking quietly and urgently to one person in the cockpit"),
          "FA": ("gemini:Kore", 1, 1, "Read as a frightened flight attendant trying to stay professional, quiet and quick"),
          "MAN": ("gemini:Algenib", 1, 1, "Read as a cold, calm, quiet man. Slow and threatening")}
RADIO = ["CAP"]
SCENES = [
    dict(id="a", lead=0.15, tail=0.3, lines=[('N', "You're locked in the equipment bay. The engines are so loud, nobody can hear you banging on the hatch.", 0.0)], sfx=[]),
    dict(id="b", lead=0.15, tail=0.3, lines=[('N', 'Fuel. Thirty-eight minutes. You have three options. Wait for someone to find you. Try to break the hatch. Or fix the wheels yourself, right now.', 0.0)], sfx=[]),
    dict(id="c", lead=0.15, tail=0.3, lines=[('N', 'You choose the wheels. The case is too heavy to lift. But its handle is steel. You jam it under the lever, and you push. Hard.', 0.0)], sfx=[]),
    dict(id="d", lead=0.15, tail=0.3, lines=[('N', 'Something snaps. The whole plane shudders. And below you, with a deafening roar, the wheels drop.', 0.0)], sfx=[]),
    dict(id="e", lead=0.15, tail=0.3, lines=[('N', "Up in the cabin, Nina hears the noise. She runs to the hatch. It's jammed shut. From the outside.", 0.0)], sfx=[]),
    dict(id="f", lead=0.15, tail=0.3, lines=[('N', 'She turns around. The man from one A is standing right behind her.', 0.3), ('MAN', "Sit down. That case isn't yours. And neither is this plane.", 0.0)], sfx=[]),
    dict(id="g", lead=0.15, tail=0.3, lines=[('N', "But four passengers are already out of their seats. And they don't sit down.", 0.0)], sfx=[]),
    dict(id="h", lead=0.15, tail=0.3, lines=[('N', 'The hatch opens. Nina pulls you up. And on the panel, the red light turns green.', 0.0)], sfx=[]),
    dict(id="i", lead=0.15, tail=0.3, lines=[('CAP', 'Ladies and gentlemen, this is your captain. Please fasten your seatbelts. We will be landing, after all.', 0.0)], sfx=[]),
    dict(id="j", lead=0.15, tail=0.3, lines=[('N', 'Six minutes of fuel left. The wheels touch the runway just as the sun comes up. The whole plane cheers.', 0.0)], sfx=[]),
    dict(id="k", lead=0.15, tail=0.3, lines=[('N', 'Police are waiting at the gate. For the man in one A. And for his case. It was full of gold.', 0.4), ('CP', 'Fourteen C. Lucky we had you.', 0.0)], sfx=[]),
    dict(id="l", lead=0.15, tail=2.6, lines=[('N', 'Would you have gone down there? Follow for the next story.', 0.0)], sfx=[]),
]
