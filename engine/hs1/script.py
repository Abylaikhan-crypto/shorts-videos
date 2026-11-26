exec(open("/home/claude/short/hs_voices.py").read())
S = lambda i, lines, tail=0.3: dict(id=i, lead=0.15, tail=tail, lines=lines, sfx=[])
SCENES = [
    S("a", [("N", "Imagine your smart speaker wakes you up at three oh seven in the morning.", 0.3), ("NOVA", "Motion detected. Kitchen.", 0.0)]),
    S("b", [("N", "You're home alone this weekend. Your parents are at a wedding, three states away. It's just you, and your dog, Biscuit.", 0.0)]),
    S("c", [("N", "But Biscuit isn't asleep. He's standing by your bedroom door. Staring up at the ceiling. And growling.", 0.0)]),
    S("d", [("N", "You open the kitchen camera on your phone. The fridge door is wide open. But there's nobody there.", 0.0)]),
    S("e", [("N", "Then you notice the counter. A plate. A fork. Half a sandwich. Someone was just eating in your kitchen.", 0.0)]),
    S("f", [("N", "Your phone buzzes. A voice message from Mom.", 0.3), ("MOM", "Honey, why is the attic light on? I can see it in the app.", 0.0)]),
    S("g", [("N", "Nobody has been in the attic for years. You tell the speaker to lock every door.", 0.3), ("NOVA", "All doors locked. Occupants detected. Two.", 0.0)]),
    S("h", [("N", "Two. You. And someone else. Someone who's been inside the house the whole time.", 0.0)]),
    S("i", [("N", "Above your ceiling, the wood creaks. Slow footsteps. Moving toward the attic hatch. Right outside your room.", 0.0)]),
    S("j", [("N", "You have three options. Hide in your closet. Run for the front door. Or call nine one one, and stay very, very quiet.", 0.0)]),
    S("k", [("N", "Biscuit starts barking. The footsteps stop. And then, very softly, the speaker on your nightstand whispers.", 0.0)]),
    S("l", [("HSP", "Go back to sleep.", 0.6), ("N", "What would you do? Part two is coming.", 0.0)], tail=2.6),
]
