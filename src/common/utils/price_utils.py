import re

def parse_price(price_str: str | None) -> int | None:
    if not price_str:
        return None
    numeric = re.sub(r"[^\d]", "", price_str)
    return int(numeric)
