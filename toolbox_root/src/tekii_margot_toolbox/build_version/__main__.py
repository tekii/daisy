import sys

from . import generate, major_valid_since

version = generate(
    short_sha=sys.argv[1] if len(sys.argv) > 1 else None,
)

with open("VERSION", "w") as vout:
    vout.write(str(version))

print(
    f"VERSION file is now {version}, API version{version.major} is valid {version.minor} seconds since {major_valid_since.get(version.major)}"
)
