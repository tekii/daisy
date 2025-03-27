import sys
import datetime
from packaging import version

now = datetime.datetime.now(datetime.timezone.utc)
zero = datetime.datetime(
    year=now.year,
    month=1,
    day=1,
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
    tzinfo=datetime.timezone.utc,
    fold=1,
)
major = now.year - 2000
minor = int((now - zero).total_seconds())
local = "+" + sys.argv[1] if len(sys.argv) > 1 else ""

v = version.Version(f"{major}.{minor}{local}")

with open("VERSION", "w") as vout:
    vout.write(str(v))
    print(f"VERSION file is now {v}")
