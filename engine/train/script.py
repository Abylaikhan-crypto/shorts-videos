VOICES = {"N": ("am_onyx", 0.92, 0.98), "W": ("am_eric", 0.98, 0.95)}
SENT_PAUSE = 0.42
COMMA_PAUSE = 0.18
SCENES = [
    dict(id="a", lead=0.2, tail=0.25, lines=[("N", "Imagine you fall asleep on the last train home.", 0.0)], sfx=[]),
    dict(id="b", lead=0.15, tail=0.25, lines=[("N", "You wake up. The car is empty. Every single seat.", 0.0)], sfx=[("boom", 0, 2, 0.0)]),
    dict(id="c", lead=0.15, tail=0.25, lines=[("N", "The screen above the door says, next stop. And then, nothing. Just a blank line.", 0.0)], sfx=[("beep", 0, 6, 0.0)]),
    dict(id="d", lead=0.15, tail=0.25, lines=[("N", "Your phone has no signal. And the train is going faster than it should.", 0.0)], sfx=[]),
    dict(id="e", lead=0.15, tail=0.25, lines=[("N", "You have three options. Pull the emergency brake. Walk to the driver. Or wait.", 0.0)], sfx=[("tick", 0, 4, 0.0)]),
    dict(id="f", lead=0.15, tail=0.25, lines=[("N", "You walk to the front. You knock on the cabin door. It swings open.", 0.0)], sfx=[("knock", 0, 9, 0.0)]),
    dict(id="g", lead=0.15, tail=0.3, lines=[("N", "Nobody is driving.", 0.0)], sfx=[("boom", 0, 0, 0.0)]),
    dict(id="h", lead=0.15, tail=0.25, lines=[("N", "Then the train slows down. Orange lights. Rows of empty trains. A depot.", 0.0)], sfx=[]),
    dict(id="i", lead=0.15, tail=0.25, lines=[("N", "A worker with a flashlight bangs on the window.", 0.3),
        ("W", "Fell asleep, huh? Happens every Friday. At night, the trains drive themselves here.", 0.0)], sfx=[("knock", 0, 6, 0.0)]),
    dict(id="j", lead=0.15, tail=2.6, lines=[("N", "Would you have pulled the brake? Follow for more.", 0.0)], sfx=[]),
]
