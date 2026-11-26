exec(open("/home/claude/short/tw_voices.py").read())
SCENES = [
    dict(id="a", lead=0.12, tail=0.4, lines=[("N", "I came home from school... and saw myself sitting at the dinner table.", 0.0)],
         sfx=[("boom", 0, 10, 0.0)]),
    dict(id="b", lead=0.2, tail=0.35, lines=[
        ("N", "My name is Lily. That's my twin sister, Lana. We look exactly the same.", 0.3),
        ("N", "Same face. Same voice. Same laugh. People at school called us the copy and paste girls.", 0.3),
        ("N", "Only Mom could ever tell us apart. Or at least... that's what I thought.", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("N", "Growing up, Lana always heard the same question.", 0.3),
        ("MO", "Why can't you be more like your sister?", 0.4),
        ("N", "I got the grades. I got the awards. And last month, I got invited to interview at the Westbrook Art Academy. A full scholarship.", 0.3),
        ("N", "I've been drawing since I was four. Lana never even congratulated me.", 0.35),
        ("LA", "Congrats, I guess. Must be nice... being perfect.", 0.3),
        ("L", "Lana, that's not fair.", 0.3),
        ("LA", "Nothing in this family is fair.", 0.0, 0.95)], sfx=[("chime", 2, 14, 0.0)]),
    dict(id="d", lead=0.2, tail=0.35, lines=[
        ("N", "Then, weird things started happening.", 0.3),
        ("Z", "Thanks for the sweet message last night, Lily! You said I'm the only real friend you have... and that you can't trust Lana.", 0.3),
        ("L", "What message? I didn't send you anything.", 0.35),
        ("N", "But there it was. On her screen. Sent from my phone, at two in the morning.", 0.0)], sfx=[]),
    dict(id="e", lead=0.2, tail=0.35, lines=[
        ("N", "The next day, my boyfriend Jake wouldn't even look at me.", 0.3),
        ("J", "Why did you yell at me yesterday? In front of everyone?", 0.3),
        ("L", "Jake, I wasn't even at school yesterday. I was sick.", 0.4),
        ("J", "Lily... I saw you.", 0.0, 0.92)], sfx=[("boom", 2, 2, 0.0)]),
    dict(id="f", lead=0.2, tail=0.35, lines=[
        ("N", "And then, my sketchbook disappeared. Every drawing for my interview. Gone.", 0.35),
        ("N", "I searched everywhere. My room, my locker, my backpack. Lana just watched me from her doorway... and smiled.", 0.0)], sfx=[]),
    dict(id="g", lead=0.2, tail=0.35, lines=[
        ("N", "That Thursday, my bus broke down. I walked home in the dark... an hour late.", 0.3),
        ("N", "My phone was dead. Nobody came looking for me. Which was weird... because Mom always comes looking for me.", 0.0)], sfx=[("rain", None, None, 0.0)]),
    dict(id="h", lead=0.2, tail=2.7, lines=[
        ("N", "When I opened the door, I heard Mom laughing. And there, at the table... wearing my hoodie... was me.", 0.4),
        ("N", "Eating Mom's lasagna. Laughing at Dad's jokes. Like she'd been me her whole life.", 0.35),
        ("LA", "Oh, hey, Lana. You're late again.", 0.35),
        ("MO", "Lana, don't just stand there. Go to your room.", 0.4),
        ("N", "My own mother... thought I was my sister.", 0.0, 0.94)], sfx=[("boom", 0, 18, 0.0), ("riser", 3, None, 0.5)]),
]
