import sys
from datetime import datetime

from . import generate

if 2 < len(sys.argv) < 5:
    try:
        major = int(sys.argv[1])
        valid_since = datetime.fromisoformat(sys.argv[2])
        short_sha = sys.argv[3] if len(sys.argv) == 4 else None

        version = generate(
            major=major,
            valid_since=valid_since,
            short_sha=short_sha,
        )

        with open("VERSION", "w") as vout:
            vout.write(str(version))

        print(
            f"VERSION file is now {version}, API version{version.major}"
            f" is valid {version.minor} seconds since {valid_since}"
        )

    except Exception as e:
        print(f"Invalid argument: {str(e)}", file=sys.stderr)
        sys.exit(1)
else:
    print("Wrong argument count", file=sys.stderr)
    sys.exit(1)
