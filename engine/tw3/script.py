exec(open("/home/claude/short/tw_voices.py").read())
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "Last time, I found my twin's secret notebook. And the last page said: make sure the real Lily disappears.", 0.0)],
         sfx=[("heartbeat", None, None, 0.0)]),
    dict(id="b", lead=0.2, tail=0.35, lines=[
        ("N", "The next morning, there was a letter on the kitchen table.", 0.3),
        ("DA", "Lana, honey... your mother and I think a fresh start would be good for you. The boarding school in Switzerland said yes.", 0.4),
        ("MO", "We already paid the deposit. You leave on Sunday.", 0.35),
        ("N", "Lana had sent an application... in her own name. She was sending me away.", 0.35),
        ("N", "And standing behind them... she gave me a tiny wave.", 0.0)], sfx=[("boom", 3, 10, 0.0)]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("N", "I had one week. And I had one secret that Lana never noticed.", 0.4),
        ("N", "I'm left-handed. Lana isn't.", 0.4, 0.94),
        ("N", "And at dinner that first night... she was eating with her right hand.", 0.4),
        ("N", "So I made a plan. No yelling. No crying. I'd catch her in front of everyone.", 0.0)], sfx=[("chime", 1, None, 0.0)]),
    dict(id="d", lead=0.2, tail=0.4, lines=[
        ("N", "So that evening, I put the scholarship letter on the table.", 0.3),
        ("L", "Lily, the academy needs your signature tonight. Go ahead. Sign it.", 0.35),
        ("LA", "Sure. No problem.", 0.4),
        ("N", "She picked up the pen... with her right hand.", 0.4),
        ("MO", "Wait. Lily... you're left-handed.", 0.0, 0.92)], sfx=[("boom", 4, 3, 0.0)]),
    dict(id="e", lead=0.2, tail=0.4, lines=[
        ("LA", "Fine! Yes, it's me! Are you happy now?", 0.35),
        ("LA", "Do you know what it's like being the other one? Every birthday, every report card, every single day?", 0.35),
        ("LA", "Everyone always loved her more. I just wanted to know how it felt... to be the favorite.", 0.4),
        ("N", "Mom didn't yell. She just started crying.", 0.3),
        ("MO", "Oh, sweetheart... what have we done?", 0.0, 0.92)], sfx=[]),
    dict(id="f", lead=0.2, tail=0.4, lines=[
        ("N", "We didn't fix everything in one night. We started family therapy. Mom and Dad stopped comparing us.", 0.35),
        ("N", "And Lana? She picked up a guitar. Turns out she's amazing at something I can't do at all.", 0.35),
        ("N", "On my first day at the academy, she was there. Not as me. As my sister. She cheered the loudest.", 0.0)], sfx=[("chime", 1, None, 0.0)]),
    dict(id="g", lead=0.2, tail=3.0, lines=[
        ("N", "I kept my scholarship. And I finally got my sister back.", 0.4),
        ("N", "We still switch clothes sometimes. But now... we tell Mom first.", 0.4),
        ("N", "Oh... and did you notice the clue in Part One?", 0.0)], sfx=[("chime", 1, None, 0.0)]),
]
