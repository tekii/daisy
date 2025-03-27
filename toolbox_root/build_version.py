import os
import datetime

with open("VERSION.in", "r") as vin:
    major = vin.read()

minor = str(int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000))
short_sha = os.environ.get("SHORT_SHA", "")
local = "+" + short_sha if short_sha != "" else ""

with open("VERSION", "w") as vout:
    version = f"{major}.post{minor}{local}"
    vout.write(version)
