from helperclasses import Pathfinding
from helperclasses import status_display

class CrewMember:
    def __init__(self, name, role, ship, position):
        self.ship = ship
        self.pathfinder = Pathfinding(ship)
        self.path = []  # Holds the computed path

        self.name = name
        self.role = role
        self.position = position
        self.task = "Idle"
        self.symbol = "@"

    def assign_role(self, new_role):
        self.role = new_role

    def assign_task(self, task):
        """Assigns a task to the crew member."""
        self.task = task

    def perform_task(self):
        """Override this method in subclasses."""
        pass

    def follow_path(self):
        #Move along the computed path
        if self.path:
            next_position = self.path.pop(0)
            self.position = next_position
        else:
            self.task = "No path"


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
        if self.task in ["Idle"]:
            if self.position != self.ship.room_positions["medbay"]:
                self.path = self.pathfinder.find_path(self.position, self.ship.room_positions["medbay"])
                status_display.add_message(f"Go to medbay; {self.position} - {self.ship.room_positions['medbay']}")
                status_display.add_message(self.path)
                self.task = "Going_to_medbay"
        
        elif self.task in ["Going_to_medbay"]:
            self.follow_path()
        

class Offduty(CrewMember):
    def __init__(self, name, ship, position):
        super().__init__(name, "Offduty", ship, position)