from dataclasses import dataclass


@dataclass
class Bait:
    amount: int
    name: str = "Generic Bait"
    generic_type: str = "bait"
    specific_type: str = "generic_bait"
    subtype: str = "generic_bait_subtype"


@dataclass
class Worm(Bait):
    name: str = "Worm"
    specific_type: str = "worm"
    subtype: str = "live_bait"
