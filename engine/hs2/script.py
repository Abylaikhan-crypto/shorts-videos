exec(open("/home/claude/short/hs_voices.py").read())
S = lambda i, lines, tail=0.3: dict(id=i, lead=0.15, tail=tail, lines=lines, sfx=[])
SCENES = [
    S("a", [("N", "You grab Biscuit and slip into your closet. You pull the door shut. Through the slats, you can see your bedroom door.", 0.0)]),
    S("b", [("N", "You call nine one one. Your hands are shaking so hard you almost drop the phone.", 0.3), ("DISP", "Nine one one. What's your emergency?", 0.0)]),
    S("c", [("N", "You whisper that someone is in your house. In the attic.", 0.3), ("DISP", "Officers are on the way. Eight minutes. Stay on the line, and stay hidden.", 0.0)]),
    S("d", [("N", "Then you hear the attic hatch open. The ladder unfolds. One step. Two. Three.", 0.0)]),
    S("e", [("N", "A shadow passes your door. A man. Thin. Long, messy hair. And he's wearing your gray hoodie. The one you lost last month.", 0.0)]),
    S("f", [("N", "And suddenly, everything makes sense. The food that kept disappearing. Your missing hoodie. The noises you blamed on the old house.", 0.0)]),
    S("g", [("N", "The man stops at your bedroom door. He knocks. Softly. Like he's done it before.", 0.3), ("HALE", "I know you're awake.", 0.0)]),
    S("h", [("N", "Biscuit growls. You hold his mouth shut. The dispatcher whispers.", 0.3), ("DISP", "Don't make a sound. Four minutes.", 0.0)]),
    S("i", [("N", "The handle turns. The man walks in, and sits down on your bed. Then he starts talking. To nobody.", 0.3), ("HALE", "This used to be my room.", 0.0)]),
    S("j", [("N", "Your options. Stay in the closet. Run past him while he's sitting. Or let Biscuit out to distract him.", 0.0)]),
    S("k", [("N", "Then your phone lights up in the dark. A text from Mom. And the light shines right through the slats.", 0.0)]),
    S("l", [("N", "The man turns his head. Slowly. Toward the closet. And smiles.", 0.6), ("N", "What would you do? The final part is coming.", 0.0)], tail=2.6),
]
