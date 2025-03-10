import curses
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
            "cockpit": (self.ship_y + 10, self.ship_x + 8),
            "engine_room": (self.ship_y + 10, self.ship_x + 15),
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
        self.crew = Crew(self)  # Initialize crew

    def update(self):
        self.crew.update()  # Update crew actions

    def display_status(self, stdscr, pos):
        """Displays ship status (fuel, hull, location)."""
        stdscr.addstr(pos,   2,  "📊 Ship Status", curses.A_BOLD)
        stdscr.addstr(pos+1, 2, f"🔋 Fuel: {self.fuel}/100     🛠 Hull: {self.hull_integrity}/100")
        stdscr.addstr(pos+2, 2, f"📍 Location: {self.current_location}")

    def draw(self, stdscr):
        for i, row in enumerate(self.layout):
            stdscr.addstr(self.ship_y + i, self.ship_x, row)

        """Draws crew members on the screen."""
        for member in self.crew.members:
            stdscr.addstr(member.position[0], member.position[1], member.symbol)

    def is_walkable(self, y, x):
        """Check if the position is walkable (empty space)"""
        return self.layout[y][x] == ' '  
