def title_and_strip(value: str) -> str:
    """Capitalizes words and strips trailing/leading whitespaces."""
    return str.title(value).strip()


def clean_optional_text(value: str | None) -> str | None:
    """Strips whitespaces if text exists, otherwise returns None."""
    return value.strip() if value else None


def round_rating(value: float) -> float:
    """Rounds the rating to a single decimal place."""
    return round(value, 1)
