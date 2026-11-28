NAT = "Read in a warm, calm, natural storytelling voice, like telling a friend a true story. Gentle pauses. Not dramatic, not theatrical"
VOICES = {"N": ("gemini:Orus", 1, 1, NAT), "MIA": ("gemini:Leda", 1, 1, "Read as a shy fifteen-year-old girl, soft and emotional")}
RADIO = []
S = lambda i, lines, tail=0.3: dict(id=i, lead=0.15, tail=tail, lines=lines, sfx=[])
SCENES = [
    S("a", [("N", "Every day at lunch, the old janitor ate alone in the boiler room. The kids called him the Ghost. Nobody even knew his name.", 0.0)]),
    S("b", [("N", "Nobody, except Mia. The new girl. One day she walked in with her tray, because she had nowhere else to sit.", 0.0)]),
    S("c", [("N", "He didn't talk much. But every week, he quietly fixed something for her. Her locker. Her bike. Her broken headphones.", 0.0)]),
    S("d", [("N", "Then, one Friday in January, the storm came. The power went out. The heating died. And the buses couldn't reach the school.", 0.0)]),
    S("e", [("N", "Three hundred students, trapped in a freezing building. The teachers were panicking.", 0.0)]),
    S("f", [("N", "And then, the lights came back on. Only in one place. The gym.", 0.0)]),
    S("g", [("N", "The janitor had started an old generator in the basement. One that nobody even knew still worked.", 0.0)]),
    S("h", [("N", "All night, he carried blankets, made hot soup, and kept that generator running.", 0.0)]),
    S("i", [("N", "At four in the morning, Mia found him asleep on a bench. His hands were black with oil, and burned.", 0.0)]),
    S("j", [("N", "A photo had fallen out of his jacket. A firefighter, holding a little girl. And a fire chief's badge.", 0.0)]),
    S("k", [("N", "Twenty years ago, he was the city's fire chief. He lost his own daughter in a fire he couldn't stop.", 0.3), ("N", "That night, he didn't lose anyone.", 0.0)]),
    S("l", [("N", "On Monday, three hundred students lined the hallway. And when he walked in, they started clapping.", 0.0)]),
    S("m", [("N", "Nobody calls him the Ghost anymore. His name is Walter.", 0.4), ("N", "Would you have sat with him?", 0.0)], tail=1.8),
]
