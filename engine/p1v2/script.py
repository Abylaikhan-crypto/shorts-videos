# My Stepdad Is a Cop — Part 1 (2-minute version). (speaker, text, gap_after[, speed])
VOICES = {"M": ("af_heart", 1.06, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[
        ("N", "My stepdad Dale is a cop. Everyone in our town calls him a hero.", 0.35),
        ("N", "But nobody knows who he becomes when the front door closes.", 0.0)],
        sfx=[("boom", None, None, 0.0)]),
    dict(id="b", lead=0.2, tail=0.3, lines=[
        ("N", "My name is Maya. I'm fourteen. And this is the story nobody believed.", 0.0)],
        sfx=[]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("N", "After my real dad left, it was just me and Mom.", 0.3),
        ("N", "She worked two jobs, and still cried over the bills at night.", 0.0, 0.97)],
        sfx=[]),
    dict(id="d", lead=0.25, tail=0.35, lines=[
        ("N", "Then one rainy night, our car broke down on the highway... and a police officer pulled over to help.", 0.3),
        ("D", "Rough night, ma'am? Don't worry. I've got you.", 0.0)],
        sfx=[("rain", None, None, 0.0), ("siren", 0, 13, 0.0)]),
    dict(id="e", lead=0.2, tail=0.35, lines=[
        ("N", "His name was Dale. He fixed our car, then our sink, then pretty much everything.", 0.25),
        ("N", "He taught me to ride a bike. He made pancakes shaped like stars.", 0.25),
        ("N", "He even came to my school play, and clapped louder than anyone.", 0.3),
        ("N", "For the first time in years, Mom laughed for real.", 0.0)],
        sfx=[("chime", 3, None, 0.0)]),
    dict(id="f", lead=0.2, tail=0.4, lines=[
        ("N", "A year later, they got married. At the wedding, Dale knelt down and made me a promise.", 0.3),
        ("D", "Nobody's ever gonna hurt you again, kiddo. That's my job.", 0.45),
        ("N", "And I believed him.", 0.0, 0.92)],
        sfx=[("chime", None, None, 0.1)]),
    dict(id="g", lead=0.2, tail=0.4, lines=[
        ("N", "Three weeks after the wedding, I knocked over my juice at dinner.", 0.75),
        ("D", "Are you really that clumsy?!", 0.3, 1.0),
        ("D", "Clean it up. Now.", 0.45, 0.9),
        ("N", "Mom jumped up to help me... and that's when I saw it.", 0.3),
        ("N", "A dark bruise on her wrist. Shaped like fingers.", 0.35, 0.95),
        ("N", "She pulled her sleeve down... and didn't say a word.", 0.0, 0.95)],
        sfx=[("clink", 0, 6, 0.1), ("boom", 1, None, -0.32), ("clink", 1, None, -0.3), ("boom", 4, 1, -0.05)]),
    dict(id="h", lead=0.2, tail=0.45, lines=[
        ("N", "That night, I stopped him in the hallway.", 0.3),
        ("M", "Did you hurt my mom?", 0.35, 1.0),
        ("N", "He grabbed my wrist so hard, my fingers went numb.", 0.35),
        ("D", "You want your mom crying over bills again? Then you keep your mouth shut.", 0.4),
        ("D", "Besides... who do you think they'll believe? A kid... or a cop?", 0.0)],
        sfx=[("heartbeat", None, None, 0.0), ("boom", 2, 1, -0.05), ("boom", 4, 7, -0.05)]),
    dict(id="i", lead=0.3, tail=0.5, lines=[
        ("N", "Later, I heard Mom stop outside my door.", 0.5),
        ("N", "She waited a second...", 0.6, 0.92),
        ("N", "Then she walked away.", 0.6, 0.92),
        ("N", "I cried until the sun came up.", 0.0, 0.95)],
        sfx=[("steps", 2, None, 0.0)]),
    dict(id="j", lead=0.2, tail=0.6, lines=[
        ("N", "The next morning, I wore long sleeves. In July.", 0.0)],
        sfx=[("tick", 0, 8, 0.0)]),
    dict(id="k", lead=0.2, tail=0.35, lines=[
        ("N", "But our school counselor, Ms. Alvarez, noticed anyway.", 0.3),
        ("A", "Maya, sweetheart... what happened to your wrist?", 0.35),
        ("N", "I tried to lie. But my voice cracked... and I told her everything.", 0.35),
        ("A", "You did the right thing, honey. I'm calling someone right now.", 0.0)],
        sfx=[]),
    dict(id="l", lead=0.2, tail=2.8, lines=[
        ("N", "Two hours later, a police car pulled up outside the school.", 0.4),
        ("N", "And the officer who walked through that door... was Dale.", 0.55),
        ("D", "Hey, kiddo. Heard you've been telling stories.", 0.0, 0.92)],
        sfx=[("siren", 0, 5, 0.0), ("boom", 1, 9, 0.0), ("riser", 2, None, 0.6)]),
]
