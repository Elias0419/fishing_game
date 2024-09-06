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
class TwentyLbMono(Line):
    name: str = "20 lb Test Monofilament"
    breaking_strength_lbs: int = 20
    diameter_mm: float = 0.4

@dataclass
class ThirtyLbMono(Line):
    name: str = "30 lb Test Monofilament"
    breaking_strength_lbs: int = 30
    diameter_mm: float = 0.5

@dataclass
class ThirtyLbMono(Line):
    name: str = "40 lb Test Monofilament"
    breaking_strength_lbs: int = 40
    diameter_mm: float = 0.5

@dataclass
class FiftyLbBraid(Line):
    name: str = "50 lb Test Braided Line"
    specific_type: str = "braided"
    breaking_strength_lbs: int = 50
    diameter_mm: float = 0.3

@dataclass
class SixtyLbBraid(Line):
    name: str = "60 lb Test Braided Line"
    specific_type: str = "braided"
    breaking_strength_lbs: int = 60
    diameter_mm: float = 0.35



@dataclass
class Reel:
    name: str = "Generic Reel"
    drag_lbs: int = 10
    max_drag: int = 10

@dataclass
class SpinningReelSmall(Reel):
    name: str = "Spinning Reel"
    reel_type: str = "spinning"

@dataclass
class SpinningReelMid(Reel):
    name: str = "Spinning Reel"
    reel_type: str = "spinning"

@dataclass
class SpinningReelLarge(Reel):
    name: str = "Spinning Reel"
    reel_type: str = "spinning"

class FlyReel(Reel):
    name: str = "Fly Fishing Reel"
    reel_type: str = "fly"
    drag_lbs: int = 5
    max_drag: int = 8

@dataclass
class BaitcastingReel(Reel):
    name: str = "Baitcasting Reel"
    reel_type: str = "baitcasting"
    drag_lbs: int = 15
    max_drag: int = 20

@dataclass
class HeavySaltwaterReel(Reel):
    pass

@dataclass
class BigGameReelLow(Reel):
    pass


@dataclass
class BigGameReelMid(Reel):
    pass

@dataclass
class BigGameReelHigh(Reel):
    pass


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


@dataclass
class UltralightRod(Rod):
    name: str = "Ultralight Rod"
    hit_points: int = 50
    breaking_strength_lbs: int = 20



@dataclass
class HeavyDutyCasting(Rod):
    name: str = "Heavy Duty Casting Rod"
    hit_points: int = 200
    breaking_strength_lbs: int = 200


@dataclass
class MidDutyCasting(Rod):
    pass
@dataclass
class LightDutyCasting(Rod):
    pass
@dataclass
class HeavyDutyBoat(Rod):
    pass
@dataclass
class MidDutyBoat(Rod):
    pass
@dataclass
class BigGameRodMid(Rod):
    pass
@dataclass
class BigGameRodLow(Rod):
    pass
@dataclass
class BigGameRodHigh(Rod):
    pass


