from dataclasses import dataclass


@dataclass
class Bait:
    amount: int
    name: str = "Generic Bait"
    generic_type: str = "bait"
    specific_type: str = "generic_bait"
    subtype: str = "generic_bait_subtype"

@dataclass
class Lure(Bait):
    name: "Generic Lure"

@dataclass
class LightJig(Bait):
    pass

@dataclass
class HeavyJig(Bait):
    pass

@dataclass
class CastMasterLight(Bait):
    pass

@dataclass
class CastMasterMid(Bait):
    pass

@dataclass
class CastMasterHeavy(Bait):
    pass

@dataclass
class PopperSmall(Bait):
    pass

@dataclass
class PopperLarge(Bait):
    pass

@dataclass
class UmbrellaRig(Bait):
    pass

@dataclass
class TunaRig(Bait):
    pass

@dataclass
class Chum(Bait):
    name: str = "Generic Chum"

@dataclass
class FishBlood(Chum):
    pass

@dataclass
class TunaMeat(Chum):
    pass

@dataclass
class Bunker(Chum):
    pass

@dataclass
class TheChumBucket(Chum):
    pass

@dataclass
class MackeralSoup(Chum):
    pass

@dataclass
class Worm(Bait):
    name: str = "Worm"
    specific_type: str = "worm"
    subtype: str = "live_bait"

@dataclass
class Squid(Bait):
    name: str = "Squid"

@dataclass
class Menhaden(Bait):
    name: str = "Menhaden"

@dataclass
class ButterFish(Bait):
    name: str = "ButterFish"

@dataclass
class Minnow(Bait):
    name: str = "Minnow"

@dataclass
class Nightcrawler(Bait):
    name: str = "Nightcrawler"

@dataclass
class Bloodworm(Bait):
    name: str = "Bloodworm"

@dataclass
class Leech(Bait):
    name: str = "Leech"

@dataclass
class CutBait(Bait):
    name: str = "Cut Bait"

@dataclass
class Herring(Bait):
    name: str = "Herring"

@dataclass
class Sardine(Bait):
    name: str = "Sardine"

@dataclass
class Mackerel(Bait):
    name: str = "Mackerel"

@dataclass
class Clam(Bait):
    name: str = "Clam"

@dataclass
class Crab(Bait):
    name: str = "Crab"

@dataclass
class Mullet(Bait):
    name: str = "Mullet"

@dataclass
class Eel(Bait):
    name: str = "Eel"

@dataclass
class Anchovy(Bait):
    name: str = "Anchovy"

@dataclass
class Pilchard(Bait):
    name: str = "Pilchard"

@dataclass
class Shrimp(Bait):
    name: str = "Shrimp"

@dataclass
class Grub(Bait):
    name: str = "Grub"

@dataclass
class Crickets(Bait):
    name: str = "Crickets"

@dataclass
class Grasshoppers(Bait):
    name: str = "Grasshoppers"

@dataclass
class Maggots(Bait):
    name: str = "Maggots"

@dataclass
class Mealworms(Bait):
    name: str = "Mealworms"

@dataclass
class Hellgrammites(Bait):
    name: str = "Hellgrammites"

@dataclass
class Crawfish(Bait):
    name: str = "Crawfish"

@dataclass
class Salamanders(Bait):
    name: str = "Salamanders"

@dataclass
class Frogs(Bait):
    name: str = "Frogs"

@dataclass
class CornKernel(Bait):
    name: str = "Corn Kernel"

@dataclass
class Marshmallows(Bait):
    name: str = "Marshmallows"

@dataclass
class CheeseChunks(Bait):
    name: str = "Cheese Chunks"

@dataclass
class HotDogPieces(Bait):
    name: str = "Hot Dog Pieces"

@dataclass
class DoughBalls(Bait):
    name: str = "Dough Balls"

@dataclass
class Salmon(Bait):
    name: str = "Salmon"

@dataclass
class Trout(Bait):
    name: str = "Trout"

@dataclass
class Bass(Bait):
    name: str = "Bass"

@dataclass
class Bluegill(Bait):
    name: str = "Bluegill"

@dataclass
class Sucker(Bait):
    name: str = "Sucker"

@dataclass
class Shiners(Bait):
    name: str = "Shiners"

@dataclass
class Scallops(Bait):
    name: str = "Scallops"

@dataclass
class Oysters(Bait):
    name: str = "Oysters"

@dataclass
class Mussels(Bait):
    name: str = "Mussels"

@dataclass
class Octopus(Bait):
    name: str = "Octopus"

@dataclass
class Sandworms(Bait):
    name: str = "Sandworms"

@dataclass
class Lugworms(Bait):
    name: str = "Lugworms"

@dataclass
class Ragworms(Bait):
    name: str = "Ragworms"
