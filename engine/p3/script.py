# My Stepdad Is a Cop — Part 3 (final)
VOICES = {"N": ("af_heart", 0.98, 1.0), "M": ("af_heart", 1.04, 1.0), "MO": ("af_nicole", 0.95, 1.0), "P": ("bf_emma", 0.95, 1.0), "X": ("af_kore", 0.98, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[
        ("N", "Last time, Dale heard my secret phone... and he was one step away from finding it.", 0.0)],
        sfx=[("heartbeat", None, None, 0.0)]),
    dict(id="b", lead=0.2, tail=0.35, lines=[
        ("N", "His hand was right there. And then...", 0.9),
        ("N", "Mom dropped a plate. On purpose.", 0.3),
        ("D", "What is wrong with you?!", 0.35),
        ("MO", "I'm sorry, Dale. My hands are just tired.", 0.35),
        ("N", "While he yelled at her, Mom looked right at me. And for the first time... she was protecting me.", 0.0)],
        sfx=[("crash", 0, None, 2.85), ("boom", 0, None, 2.85)]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("N", "I grabbed the phone and ran. Out the back door, barefoot, through the rain.", 0.3),
        ("N", "Lightning lit up the whole street. I could hear him shouting my name behind me.", 0.25),
        ("D", "Maya!", 0.4),
        ("N", "I didn't stop until I reached Mrs. Patterson's porch.", 0.0)],
        sfx=[("rain", None, None, 0.0), ("boom", 1, 0, 0.0), ("knock", 3, None, 2.6)]),
    dict(id="d", lead=0.2, tail=0.35, lines=[
        ("P", "Maya? Oh my goodness, child... come inside!", 0.35),
        ("N", "I played her the recording, and gave her Ms. Alvarez's card. Her hands were shaking when she dialed.", 0.35),
        ("P", "Ms. Alvarez? Maya is safe with me. You need to hear this... and we're calling the State Police. Not the local ones.", 0.0)],
        sfx=[]),
    dict(id="e", lead=0.2, tail=0.4, lines=[
        ("N", "The next morning, two cars pulled up. Not from Dale's department. The State Police.", 0.35),
        ("D", "Guys, come on. We're on the same team.", 0.35),
        ("X", "We listened to the recording, Officer Brooks. You're under arrest.", 0.4),
        ("D", "This is a mistake! Ask anyone in this town!", 0.4),
        ("N", "As they walked him out, he looked at me. And for the first time... I wasn't afraid.", 0.0)],
        sfx=[("siren", 0, 4, 0.0), ("boom", 2, 7, 0.0)]),
    dict(id="f", lead=0.2, tail=0.4, lines=[
        ("N", "In court, his lawyer said I made it all up. Then they played my recording. The whole room went silent.", 0.35),
        ("N", "And my recording wasn't the only thing they found. Two other families came forward.", 0.3),
        ("N", "He had done this before.", 0.0, 0.92)],
        sfx=[("boom", 2, None, 0.0)]),
    dict(id="g", lead=0.3, tail=0.4, lines=[
        ("N", "A month later, we moved into a tiny apartment across town. It was small... but it was quiet.", 0.4),
        ("MO", "I'm so sorry, baby. I should have protected you.", 0.4),
        ("M", "We protected each other, Mom.", 0.0)],
        sfx=[("chime", 2, None, 0.3)]),
    dict(id="h", lead=0.2, tail=3.4, lines=[
        ("N", "Mom goes to therapy now. So do I. Some days are still hard.", 0.4),
        ("N", "Nobody believed me... until I made them listen.", 0.4),
        ("N", "If something like this is happening to you, tell someone you trust. You are not alone.", 0.0, 0.95)],
        sfx=[("chime", 2, None, 0.0)]),
]
