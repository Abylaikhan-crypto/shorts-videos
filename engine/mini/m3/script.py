VOICES = {"N": ("af_bella", 0.95, 1.0), "MO": ("af_sarah", 0.95, 1.0), "W": ("af_sky", 0.92, 1.0)}
SCENES = [
    dict(id="a", lead=0.12, tail=0.3, lines=[("N", "I found a note inside a library book. It was written twenty years ago... by my mom.", 0.0)], sfx=[("boom", 0, 15, 0.0)]),
    dict(id="b", lead=0.2, tail=0.3, lines=[("N", "It was an old book about writing stories. On the very last page, someone had written...", 0.3),
        ("W", "If you find this, I hope you're braver than me. Write your story. Love, L.", 0.0)], sfx=[]),
    dict(id="c", lead=0.2, tail=0.3, lines=[("N", "L. My mom's name is Laura. And that was her handwriting. I'd know it anywhere.", 0.0)], sfx=[]),
    dict(id="d", lead=0.2, tail=0.3, lines=[("N", "At dinner, I put the note on the table. Mom went completely silent.", 0.3),
        ("MO", "I wanted to be a writer. But everyone told me it wasn't a real job. So I gave up... and left that note for someone braver.", 0.0, 0.93)], sfx=[]),
    dict(id="e", lead=0.2, tail=2.6, lines=[("N", "That night, I wrote a reply on the same page, and put the book back on the shelf.", 0.35),
        ("N", "Two weeks later, Mom bought a notebook. She's on chapter four.", 0.0)], sfx=[("chime", 1, None, 0.0)]),
]
