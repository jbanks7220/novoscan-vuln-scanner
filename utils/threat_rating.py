def cvss_score(level):
    scores = {
        "low": 3.1,
        "medium": 5.4,
        "high": 8.2,
        "critical": 9.8
    }
    return scores.get(level.lower(), 4.0)
