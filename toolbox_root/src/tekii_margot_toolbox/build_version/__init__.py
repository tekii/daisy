import datetime

from packaging import version

major = 1
major_valid_since = {
    0: datetime.datetime(
        year=2025,
        month=3,
        day=27,
        hour=6,
        minute=35,
        second=0,
        microsecond=0,
        tzinfo=datetime.timezone.utc,
        fold=1,
    ),
    1: datetime.datetime(
        year=2025,
        month=4,
        day=11,
        hour=6,
        minute=22,
        second=0,
        microsecond=0,
        tzinfo=datetime.timezone.utc,
        fold=1,
    ),
}


def generate(short_sha=None, version_now=None):
    """Generate a new version"""
    now = version_now if version_now is not None else datetime.datetime.now(datetime.timezone.utc)
    minor = int((now - major_valid_since.get(major)).total_seconds())
    local = "+" + short_sha if short_sha is not None else ""

    return version.Version(f"{major}.{minor}{local}")
