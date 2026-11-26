VOICES = {"N": ("am_onyx", 0.88, 0.98), "MOM": ("af_sarah", 0.88, 0.95), "WH": ("af_nicole", 0.82, 0.84), "LL": ("bm_george", 0.95, 0.92),
          "NB": ("bf_emma", 0.88, 0.92)}
SENT_PAUSE = 0.45
COMMA_PAUSE = 0.2
SCENES = [
    dict(id="a", lead=0.3, tail=0.25, lines=[("N", "It's three oh seven A M. You wake up to three slow knocks on your front door.", 0.0)], sfx=[("knock", 0, 9, 0.0)]),
    dict(id="b", lead=0.15, tail=0.25, lines=[("N", "You live alone. On the ninth floor. Nobody should be here.", 0.0)], sfx=[]),
    dict(id="c", lead=0.15, tail=0.25, lines=[("N", "You look through the peephole. The hallway is empty. Totally empty.", 0.0)], sfx=[]),
    dict(id="d", lead=0.15, tail=0.25, lines=[("N", "You check your doorbell camera. Nobody. But the knocking doesn't stop.", 0.0)], sfx=[("knock", 0, 9, 0.2)]),
    dict(id="e", lead=0.15, tail=0.25, lines=[("N", "You have three options. Open the door. Call the police. Or hide.", 0.0)], sfx=[("tick", 0, 4, 0.0)]),
    dict(id="f", lead=0.15, tail=0.25, lines=[("N", "You call nine one one. No signal. Your phone had full bars five minutes ago.", 0.0)], sfx=[("beep", 0, 3, 0.0)]),
    dict(id="g", lead=0.15, tail=0.25, lines=[("N", "Then you remember what the landlord told you on move-in day.", 0.25),
        ("LL", "If anyone knocks after three, read the note in the kitchen drawer. And don't open the door.", 0.0)], sfx=[]),
    dict(id="h", lead=0.15, tail=0.25, lines=[("N", "You run to the kitchen. Under the old batteries, there's a yellow piece of paper.", 0.0)], sfx=[("steps", 0, 0, 0.0)]),
    dict(id="i", lead=0.15, tail=0.25, lines=[("N", "Rule one. Never open the door. It can't come in unless you let it.", 0.35),
        ("N", "Rule two. It knows the voices you love. Do not answer.", 0.0)], sfx=[("boom", 0, 0, 0.0), ("boom", 1, 0, 0.0)]),
    dict(id="j", lead=0.15, tail=0.25, lines=[("N", "The rest of the note is torn off.", 0.0)], sfx=[]),
    dict(id="k", lead=0.15, tail=0.25, lines=[("N", "Then, a voice from the hallway.", 0.3),
        ("MOM", "Sweetie? It's Mom. Open the door. I'm so cold.", 0.0)], sfx=[("knock", 1, 0, 0.0)]),
    dict(id="l", lead=0.15, tail=0.25, lines=[("N", "Your mom lives eight hundred miles away. And she texted you goodnight ten minutes ago.", 0.0)], sfx=[("heartbeat", None, None, 0.0)]),
    dict(id="m", lead=0.2, tail=2.6, lines=[("WH", "I know you're awake. I can hear your heartbeat.", 0.5),
        ("N", "Would you open the door? Part two is coming.", 0.0)], sfx=[("boom", 0, 0, 0.0), ("riser", 1, None, 0.0)]),
]
