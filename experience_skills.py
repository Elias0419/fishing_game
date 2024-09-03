class Skill:
    pass

class FreshwaterSkill(Skill):
    pass

class SaltwaterSkill(Skill):
    pass

class BoatingSkill(Skill):
    pass

class FlyFishing(FreshwaterSkill):
    pass

class TunaFishing(SaltwaterSkill, BoatingSkill):
    pass
