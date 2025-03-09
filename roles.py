class CrewMember:
    def __init__(self, name, role, ship, position):
        self.name = name
        self.role = role
        self.ship = ship
        self.position = position
        self.task = "Idle"

    def assign_task(self, task):
        """Assigns a task to the crew member."""
        self.task = task

    def perform_task(self):
        """Override this method in subclasses."""
        pass

class Pilot(CrewMember):
    def __init__(self, name, ship, position):
        super().__init__(name, "Pilot", ship, position)

    def perform_task(self):
        if self.task == "navigate":
            self.ship.set_speed(1)  # Pilot increases speed

class Engineer(CrewMember):
    def __init__(self, name, ship, position):
        super().__init__(name, "Engineer", ship, position)

    def perform_task(self):
        if self.task == "repair":
            self.ship.engine_heat = max(0, self.ship.engine_heat - 5)

class Medic(CrewMember):
    def __init__(self, name, ship, position):
        super().__init__(name, "Medic", ship, position)

    def perform_task(self):
        if self.task == "heal":
            print(f"{self.name} is healing injured crew members.")