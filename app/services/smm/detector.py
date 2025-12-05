from app.models.platform import Platform


def detect_platform(name: str, platforms: list[Platform]) -> Platform | None:
    text = name.lower()

    for platform in platforms:
        keywords = platform.keywords.lower().split(",") if platform.keywords else []
        for kw in keywords:
            if kw.strip() and kw.strip() in text:
                return platform

    return None
