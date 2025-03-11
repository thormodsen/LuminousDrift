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
                self.task = "Going_to_medbay"
        
        elif self.task in ["Going_to_medbay"]:
            self.follow_path()
        

class Offduty(CrewMember):
    def __init__(self, name, ship, position):
        super().__init__(name, "Offduty", ship, position)


class Provisioner(CrewMember):
    BASE_PRODUCTION_RATE = 1  # Food units per provisioner per second
    greens_collected = 0

    def __init__(self, name, ship, position):
        super().__init__(name, "Provisioner", ship, position)
        self.symbol = "P"  # Distinct symbol for the Provisioner
        self.has_greens = False  # Tracks if the Provisioner is carrying greens

    def perform_task(self):
        """
        Implements a cycle where the Provisioner:
          1. Moves to the garden to gather greens if not already carrying any.
          2. Moves to the kitchen to process greens into food units if carrying greens.
        """
        if self.task == "Idle":
            if not self.has_greens:
                # Need to fetch greens: head to the garden
                if self.position != self.ship.room_positions["garden"]:
                    self.path = self.pathfinder.find_path(self.position, self.ship.room_positions["garden"])
                    self.task = "Going_to_garden"
                else:
                    self.gather_greens()
            else:
                # Has greens; deliver them to the kitchen
                if self.position != self.ship.room_positions["kitchen"]:
                    self.path = self.pathfinder.find_path(self.position, self.ship.room_positions["kitchen"])
                    self.task = "Going_to_kitchen"
                else:
                    self.process_food()

        elif self.task == "Going_to_garden":
            self.follow_path()
            if self.position == self.ship.room_positions["garden"]:
                self.task = "Idle"  # Arrived; next tick will trigger gathering

        elif self.task == "Going_to_kitchen":
            self.follow_path()
            if self.position == self.ship.room_positions["kitchen"]:
                self.task = "Idle"  # Arrived; next tick will trigger processing

    def gather_greens(self):
        #print(f"{self.name} is gathering greens in the garden.")
        if self.greens_collected < 10:
            self.greens_collected += 1
            #status_display.add_message(f"{self.name} collected greens: {self.greens_collected}")
        else:
            self.has_greens = True
            self.task = "Idle"

    def process_food(self):
        #print(f"{self.name} is processing greens into food in the kitchen.")
        if self.greens_collected > 0:
            self.greens_collected -= 1
            #status_display.add_message(f"{self.name} processed greens: {self.greens_collected}")
        else:
            # Update the ship's food inventory, if applicable.
            if hasattr(self.ship, "add_food"):
                self.ship.add_food(self.BASE_PRODUCTION_RATE)  # Example: add 5 food units
            self.has_greens = False
            self.task = "Idle"