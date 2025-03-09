import curses

class TravelSystem:
    def __init__(self, ship):
        self.ship = ship
        self.locations = [
            {"name": "Trade Hub", "fuel_cost": 5, "hull_cost": 0},
            {"name": "Nebula", "fuel_cost": 5, "hull_cost": 10},
            {"name": "Deep Space", "fuel_cost": 10, "hull_cost": 15}
        ]
        self.selected_index = 0  # Tracks which jump is selected

    def display_jump_options(self, stdscr, pos):
        """Displays available jump locations and their costs."""
        stdscr.addstr(pos, 2, "🚀 Available Jumps (Select Destination)", curses.A_BOLD)

        for i, loc in enumerate(self.locations):
            marker = ">" if i == self.selected_index else " "
            stdscr.addstr(pos + 1 + i, 2, f"{marker} {chr(ord('A') + i)}. {loc['name']} - {loc['fuel_cost']} Fuel, -{loc['hull_cost']} Hull")


    def select_jump(self, direction):
        """Moves selection up or down."""
        self.selected_index = max(0, min(self.selected_index + direction, len(self.locations) - 1))

    def execute_jump(self):
        """Performs the jump, deducting fuel and hull integrity."""
        selected_location = self.locations[self.selected_index]
        if self.ship.fuel >= selected_location["fuel_cost"]:
            self.ship.fuel -= selected_location["fuel_cost"]
            self.ship.hull_integrity = max(0, self.ship.hull_integrity - selected_location["hull_cost"])
            self.ship.current_location = selected_location["name"]
        else:
            return "Not enough fuel!"  # Feedback for UI