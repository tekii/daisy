import datetime


from tekii.margot.build_version import generate

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


def test_major():

    start = major_valid_since.get(0)
    end = start + datetime.timedelta(seconds=60)

    diff = end - start

    version = generate(
        major=0,
        valid_since=major_valid_since.get(0),
        short_sha=None,
        version_now=end,
    )

    assert version.major == 0
    # assert version.minor == 60
    assert version.minor == int(diff.total_seconds())


def test_vX_since_minute():
    since = major_valid_since.get(0)
    assert since.minute == 35
    since = major_valid_since.get(1)
    assert since.minute == 22
