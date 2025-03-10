import curses

class ShipView:
    def __init__(self, ship):
        self.ship = ship

    def render(self, window):
        layout, base_y, base_x = self.ship.get_layout()
        for i, row in enumerate(layout):
            try:
                window.addstr(base_y + i, base_x, row)
            except curses.error:
                pass  # Terminal may be too small
        # Render crew members on the ship:
        for member in self.ship.crew.members:
            try:
                window.addstr(member.position[0], member.position[1], member.symbol)
            except curses.error:
                pass

class StatusView:
    def __init__(self, ship, status_display):
        self.ship = ship
        self.status_display = status_display

    def render(self, window):
        try:
            window.addstr(1, 2, "Ship Status", curses.A_BOLD)
            window.addstr(2, 2, f"Fuel: {self.ship.fuel}/100  Hull: {self.ship.hull_integrity}/100")
            window.addstr(3, 2, f"Location: {self.ship.current_location}")
            # Render the debug log on the right:
            self.status_display.draw(window, window.getmaxyx()[1] - 50, 1)
        except curses.error:
            pass