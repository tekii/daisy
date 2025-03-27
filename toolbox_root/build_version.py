import os, sys
import datetime

with open("VERSION.in", "r") as vin:
    major = vin.read()

minor = str(int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000))
local = "+" + sys.argv[1] if len(sys.argv) > 1 else ""

with open("VERSION", "w") as vout:
    version = f"{major}.post{minor}{local}"
    vout.write(version)
    print(f"VERSION file is now {version}")
