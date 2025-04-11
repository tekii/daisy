import pytest
import datetime

from tekii_margot_toolbox.build_version import generate, major_valid_since, major


def test_major():

    start = major_valid_since.get(major)
    end = start + datetime.timedelta(seconds=60)

    diff = end - start

    version = generate(version_now=end)

    assert version.major == major
    # assert version.minor == 60
    assert version.minor == int(diff.total_seconds())


def test_vX_since_minute():
    since = major_valid_since.get(0)
    assert since.minute == 35
    since = major_valid_since.get(1)
    assert since.minute == 22
