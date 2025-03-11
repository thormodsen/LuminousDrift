from crew import Crew
from travel_system import TravelSystem

class Ship:
    def __init__(self):
        self.ship_y = 0  # Will be set dynamically
        self.ship_x = 60
        self.layout = [
            "0123456789012345678901234567890",
            "1##############################",
            "2#                            #",
            "3#    ##L   L###########      #",
            "4#    #        #       #      #",
            "5#    #        #       #      #",
            "6#    ###########M  M###      #",
            "7#                            #",
            "8#                            #",
            "9#    ###C  C###########      #",
            "0#    #        #       #      #",
            "1#    #        #       #      #",
            "2#    ###########E  E###      #",
            "3#                            #",
            "4##############################",
            "0123456789012345678901234567890"

        ]

        self.room_positions = {
            "lounge": (self.ship_y + 4, self.ship_x + 10),
            "kitchen": (self.ship_y + 11, self.ship_x + 10),
            "garden": (self.ship_y + 11, self.ship_x + 18),
            "medbay": (self.ship_y + 4, self.ship_x + 18)
        }

        self.distance_traveled = 0
        self.speed = 0
        self.max_speed = 10
        self.evasion = 0  # Evasive maneuvers effect
        self.auto_repair = False  # Engineer auto-repair
        self.early_hazard_warning = False  # Radar Operator effect
        self.threat_assessment = False  # Radar Operator level 2 effect
        self.fuel = 50  # Initial fuel amount
        self.hull_integrity = 100  # Initial hull health
        self.current_location = "Starting Point"

        self.travel_system = TravelSystem(self)
        self.crew = Crew(self)

    def update(self):
        """Update the ship's state, including crew tasks."""
        self.crew.update()

    def get_layout(self):
        """Return the ship's layout along with its top-left position."""
        return self.layout, self.ship_y, self.ship_x

    def is_walkable(self, y, x):
        """Check if the given position is walkable (i.e., an empty space)."""
        return self.layout[y][x] == ' '