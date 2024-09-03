class Boat:
    def __init__(
        self,
        name,
        engine=None,
        console=None,
        rod_holders=0,
        steering_wheel=None,
        outriggers=None,
    ):
        self.name = name
        self.engine = engine
        self.console = console
        self.rod_holders = rod_holders
        self.steering_wheel = steering_wheel
        self.outriggers = outriggers

    def customize(self, component, value):
        setattr(self, component, value)
