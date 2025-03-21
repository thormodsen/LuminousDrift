import curses
import random


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
            # Render ship status
            window.addstr(1, 0, "🚀 Ship Status", curses.A_BOLD)
            window.addstr(2, 2, f"Fuel: {self.ship.fuel}/100  Hull: {self.ship.hull_integrity}/100")
            window.addstr(3, 2, f"Food: {self.ship.food_storage:.1f}")
            window.addstr(4, 2, f"Location: {self.ship.current_location}")

            # Render crew status
            pos = 6
            window.addstr(pos, 0, "👻 Crew Status", curses.A_BOLD)
            for i, member in enumerate(self.ship.crew.members):
                marker = ">" if i == self.ship.crew.selected_index else " "
                style = curses.A_BOLD if i == self.ship.crew.selected_index else curses.A_NORMAL
                window.addstr(pos + 1 + i, 2, f"{marker} {i+1}. {member.name} ({member.role}) - Task: {member.task}", style)
            
            # Render jump options from travel_system
            pos += len(self.ship.crew.members) + 3  # Move down the screen
            self.ship.travel_system.display_jump_options(window, pos)  # Call jump display function


            # Render the debug log on the right:
            self.status_display.draw(window, window.getmaxyx()[1] - 50, 1)
        except curses.error:
            pass


class Starfield:
    def __init__(self, height, width, density=0.015):
        self.height = height
        self.width = width
        self.density = density
        self.stars = []

    def update(self):
        # Move stars to the left
        for star in self.stars:
            #star[1] -= 1
            star[0] += 1

        # Remove stars that are off-screen
        #self.stars = [s for s in self.stars if s[1] >= 0]
        self.stars = [s for s in self.stars if s[0] <= self.height]

        # Randomly add new stars on the right
        #for _ in range(int(self.height * self.density)):
        for _ in range(int(self.width * self.density)):
            #y = random.randint(0, self.height - 1)
            #self.stars.append([y, self.width - 1])
            x = random.randint(0, self.width - 1)
            self.stars.append([0, x])

    def render(self, window):
        for y, x in self.stars:
            try:
                window.addstr(y, x, '.', curses.color_pair(0))
            except curses.error:
                pass