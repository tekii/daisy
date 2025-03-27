import sys
import datetime
from packaging import version

now = datetime.datetime.now(datetime.timezone.utc)
major = 0
major_valid_since = datetime.datetime(
    year=2025,
    month=3,
    day=27,
    hour=6,
    minute=35,
    second=0,
    microsecond=0,
    tzinfo=datetime.timezone.utc,
    fold=1,
)
minor = int((now - major_valid_since).total_seconds())
local = "+" + sys.argv[1] if len(sys.argv) > 1 else ""

v = version.Version(f"{major}.{minor}{local}")

with open("VERSION", "w") as vout:
    vout.write(str(v))
    print(f"VERSION file is now {v}, API v{major} is valid since {major_valid_since}")
