"""Check if datetime is UTC time."""

from datetime import datetime

UTC_NAMES = [
    x.lower()
    for x in (
        "UTC",
        "Zulu",
        "Universal",
        "Etc/UTC",
        "Etc/Universal",
        "Etc/Zulu",
    )
]


def check_tz_name_for_utc(dt: datetime) -> bool:
    """Check to see if the timezone name is on the list of UTC equivalents.

    Figuring out if the timezone is actually UTC is surprisingly hard.

    datetime.UTC != Zoneinfo("UTC")

    datetime.utcoffset()==timedelta() just means offset is zero AT THAT MOMENT. It
    could be true for a non-utc timezone with DST.

    Checking the name is PROBABLY correct, but depends on the particular tzinfo
    implementation.

    Args:
        dt (datetime): The datetime to check. Must be an aware datetime.

    Returns:
        bool: True if tzname is on the list, case insensitive. ["UTC", "Zulu", "Etc/UTC"]
    """
    tzname = dt.tzname()
    if tzname is None:
        raise ValueError(
            f"dt={dt!r} is probably a nieve datetime. Timezone name is None."
        )
    return tzname.lower() in UTC_NAMES
