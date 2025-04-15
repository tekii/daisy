"""VERSION generator"""

from datetime import datetime, timezone

from packaging import version

__all__ = [
    "generate",
]


def generate(
    major: int,
    valid_since: datetime,
    short_sha: str | None = None,
    version_now: datetime | None = None,
) -> version.Version:
    """Generate a new version"""
    now = version_now if version_now is not None else datetime.now(timezone.utc)
    minor = int((now - valid_since).total_seconds())
    local = "+" + short_sha if short_sha is not None else ""

    return version.Version(f"{major}.{minor}{local}")
