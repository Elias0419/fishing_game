from dataclasses import dataclass


@dataclass
class Line:
    name: str = "Generic Line"
    generic_type: str = "generic_line"
    specific_type: str = "monofilament"
    breaking_strength_lbs: int = 10


@dataclass
class TenLbMono(Line):
    name: str = "10 lb Test Monofilament"


@dataclass
class Reel:
    name: str = "Generic Reel"
    drag_lbs: int = 10
    max_drag: int = 10


@dataclass
class Rod:
    line: Line
    reel: Reel
    name: str = "Generic Rod"
    hit_points: int = 100
    breaking_strength_lbs: int = 100


@dataclass
class Twig(Rod):
    name: str = "Twig"
    hit_points: int = 20
    breaking_strength_lbs: int = 5
