MODEL_PROFILES = {
    "PA3X": {
        "GLOBAL",
        "MULTISAMP",
        "PAD",
        "PCM",
        "PERFORM",
        "SONGBOOK",
        "SOUND",
        "STYLE",
    },
    "PA4X": {
        "GLOBAL",
        "KEYBOARDSET",
        "MULTISAMP",
        "PAD",
        "PCM",
        "SONGBOOK",
        "SOUND",
        "STYLE",
        "VOICEPRESET",
    },
}

def identify_model(folder_names):
    names = {name.upper() for name in folder_names}
    scores = {
        model: len(names & expected)
        for model, expected in MODEL_PROFILES.items()
    }

    if not any(scores.values()):
        return "UNKNOWN"

    best_score = max(scores.values())
    best = [
        model for model, score in scores.items()
        if score == best_score
    ]

    if len(best) != 1:
        return "UNKNOWN"

    return best[0]
