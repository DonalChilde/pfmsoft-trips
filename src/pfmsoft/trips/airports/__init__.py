"""Load airport database dict."""

import airportsdata

AIRPORTS_DICT = airportsdata.load("IATA")


def airport_from_iata(iata: str) -> airportsdata.Airport:
    """Get an `Airport` based on iata code."""
    data = AIRPORTS_DICT.get(iata.upper(), None)
    if data is None:
        raise ValueError(f"Tried to find iata={iata}, but no airport found.")
    return data
