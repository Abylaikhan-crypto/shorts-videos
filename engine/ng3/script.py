exec(open("/home/claude/short/ng_voices.py").read())
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "Last time, I found out my old best friend Chloe had been spying on me for a whole year.", 0.0)], sfx=[("heartbeat", None, None, 0.0)]),
    dict(id="b", lead=0.2, tail=0.35, lines=[
        ("C", "You ruined my life, Mia! You told Mr. Grant I cheated on the final! I got expelled. We had to move!", 0.35),
        ("M", "Chloe, I never told anyone. I swear!", 0.35),
        ("C", "Liar.", 0.4),
        ("N", "And she hung up.", 0.35),
        ("N", "Expelled? Moved away... because of me? I had no idea.", 0.0)], sfx=[("boom", 2, 0, 0.0)]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("N", "I didn't tell on her. But someone did. So Dev and I went to find out who.", 0.3),
        ("N", "Mr. Grant was the teacher who caught her. If anyone knew the truth, it was him.", 0.3),
        ("D", "If the school caught her, there has to be a record. Let's just ask Mr. Grant.", 0.0)], sfx=[]),
    dict(id="d", lead=0.2, tail=0.35, lines=[
        ("T", "Mia, you didn't report anything. The hallway camera caught Chloe with the answer sheet. I found it myself.", 0.4),
        ("T", "I'm sorry nobody told you, Mia. Chloe never asked me how I found out.", 0.35),
        ("N", "He even showed us the email he sent to Chloe's parents. The date. The video. Everything.", 0.35),
        ("N", "Chloe had hated me for a whole year... for something I never did.", 0.0)], sfx=[("chime", 2, None, 0.0)]),
    dict(id="e", lead=0.2, tail=0.35, lines=[
        ("N", "So that night, I wrote one last diary entry. But this time, I didn't write. I talked. Straight into the bear's camera.", 0.35),
        ("N", "Dev waited outside my door. Just in case.", 0.3),
        ("M", "Chloe, I know you're watching. I didn't tell on you. Mr. Grant saw it on camera. Here's the email.", 0.35),
        ("M", "I missed you every single day. You were my best friend.", 0.0, 0.95)], sfx=[]),
    dict(id="f", lead=0.2, tail=0.35, lines=[
        ("N", "An hour later, my phone rang. It was Chloe. She was crying.", 0.3),
        ("C", "Mia... I'm so sorry. I was so angry. I just needed someone to blame.", 0.4),
        ("N", "We talked until three in the morning. Like nothing had ever happened.", 0.35),
        ("N", "The next day, Harper deleted every post. Then she apologized to the whole class... in front of the principal.", 0.0)], sfx=[]),
    dict(id="g", lead=0.2, tail=3.0, lines=[
        ("N", "I still write in my diary every night. But now I keep it somewhere safe.", 0.35),
        ("N", "And the bear? Dev turned it into a night light.", 0.4),
        ("N", "Chloe's coming to visit next month. And this time... she's using the front door.", 0.4),
        ("N", "So... would you forgive Chloe?", 0.0)], sfx=[("chime", 2, None, 0.0)]),
]
