exec(open("/home/claude/short/ng_voices.py").read())
SCENES = [
    dict(id="a", lead=0.12, tail=0.4, lines=[("N", "The new girl said hi... then told me what I wrote in my diary last night.", 0.0)], sfx=[("boom", 0, 9, 0.0)]),
    dict(id="b", lead=0.2, tail=0.35, lines=[
        ("N", "My name is Mia. I don't talk much. But every night, I write everything in my diary.", 0.3),
        ("N", "Every secret. Every crush. Every fear. Nobody has ever read it. Nobody even knows it exists.", 0.35),
        ("N", "Mom works night shifts. So most evenings, it's just me, my desk, and my old teddy bear, Mr. Buttons.", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("N", "Then Harper transferred to our school. Perfect hair. Perfect smile. And she sat right next to me.", 0.3),
        ("H", "Hi! You're Mia, right? I love your sweater. Is it the one your grandma knitted... before she passed away?", 0.35),
        ("H", "We're going to be best friends. I can feel it.", 0.4),
        ("N", "I froze. I had written that in my diary... the night before.", 0.0)], sfx=[("boom", 2, 1, 0.0)]),
    dict(id="d", lead=0.2, tail=0.35, lines=[
        ("N", "At lunch, she leaned in and whispered.", 0.3),
        ("H", "Ethan? Really? You think his laugh sounds like music?", 0.35),
        ("N", "Those were my exact words. From my diary. I hadn't told a single person.", 0.35),
        ("N", "I looked around the cafeteria. Nobody had ever seen my diary. Nobody.", 0.0)], sfx=[]),
    dict(id="e", lead=0.2, tail=0.35, lines=[
        ("N", "So I set a trap. I wrote a fake secret, something I had never said out loud.", 0.3),
        ("N", "I hid five hundred dollars inside the old oak tree behind the school.", 0.35),
        ("N", "And the next morning... there was Harper. Her arm deep inside the oak tree.", 0.3),
        ("H", "Oh! Mia! I was just... looking for my earring.", 0.4),
        ("N", "There was no money. There never was. Only my diary knew about it.", 0.0)], sfx=[]),
    dict(id="f", lead=0.2, tail=0.35, lines=[
        ("N", "That night, I locked my door. I hid my diary under my pillow. And I stayed awake until sunrise, watching.", 0.3),
        ("N", "I checked the window. Locked. The closet. Empty. Nobody came in. Nobody touched it.", 0.35),
        ("H", "Good morning, Mia! You look tired. You really shouldn't stay up so late.", 0.0)], sfx=[("heartbeat", 1, None, 0.0)]),
    dict(id="g", lead=0.2, tail=2.8, lines=[
        ("N", "My diary never left my room. So how did she know?", 0.45),
        ("N", "Then I looked at my desk... and my teddy bear's eye blinked. Red.", 0.4, 0.94),
        ("N", "Mr. Buttons. The bear that sat on my desk every night... facing my diary.", 0.0, 0.95)],
        sfx=[("boom", 1, 9, 0.0), ("riser", 1, None, 0.5)]),
]
