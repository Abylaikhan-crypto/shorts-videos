exec(open("/home/claude/short/ng_voices.py").read())
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "Last time, the new girl knew every secret from my diary. And my teddy bear's eye... blinked red.", 0.0)], sfx=[("boom", 0, 14, 0.0)]),
    dict(id="b", lead=0.2, tail=0.35, lines=[
        ("N", "I brought the bear to Dev. He's the smartest person I know. And honestly, my only friend.", 0.3),
        ("D", "Hold on. Why is he so heavy?", 0.3),
        ("N", "Dev cut a tiny hole in Mr. Buttons' back. I almost cried.", 0.35),
        ("D", "Mia... there's a camera in here. A real one. With Wi-Fi.", 0.35),
        ("N", "It had been pointing at my desk. At my diary. Every single night.", 0.35),
        ("D", "And it's not just recording. It's streaming. Live. To someone's phone.", 0.0)], sfx=[("boom", 3, 4, 0.0)]),
    dict(id="c", lead=0.2, tail=0.35, lines=[
        ("D", "Who gave you this bear?", 0.35),
        ("N", "My birthday. Last year. A gift from Chloe, my best friend.", 0.35),
        ("N", "We used to have sleepovers every weekend. We swore we'd be friends forever.", 0.3),
        ("N", "Then one day, her family just left. No goodbye. And she stopped answering my messages.", 0.0)], sfx=[]),
    dict(id="d", lead=0.2, tail=0.35, lines=[
        ("N", "The next morning, my phone wouldn't stop buzzing.", 0.3),
        ("N", "Someone had posted photos of my diary in the class group chat. My crush. My fears. Everything.", 0.35),
        ("N", "The whole class was laughing.", 0.3),
        ("E", "Is it true? You wrote poems about me?", 0.4),
        ("N", "I wanted to disappear.", 0.0, 0.94)], sfx=[("tick", 0, 6, 0.0), ("tick", 0, 6, 0.25), ("tick", 0, 6, 0.5)]),
    dict(id="e", lead=0.2, tail=0.35, lines=[
        ("N", "I found Harper at her locker. My hands were shaking. Everyone in the hallway stopped to watch.", 0.3),
        ("M", "Why are you doing this? I never did anything to you!", 0.35),
        ("H", "To me? No. But you really don't remember what you did to my cousin?", 0.35, 0.95),
        ("H", "You took everything from her. So now... I'm taking everything from you.", 0.0, 0.95)], sfx=[]),
    dict(id="f", lead=0.2, tail=2.8, lines=[
        ("N", "She held up her phone. A video call.", 0.4),
        ("C", "Hi, Mia. Did you miss me?", 0.4),
        ("C", "Nice diary, by the way. The poems about Ethan were my favorite.", 0.45),
        ("N", "It was Chloe. My old best friend. She'd been watching me... for a whole year.", 0.0, 0.95)],
        sfx=[("boom", 1, 0, 0.0), ("riser", 2, None, 0.5)]),
]
