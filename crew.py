import curses
from roles import Pilot, Engineer, Medic

class Crew:
    def __init__(self, ship):
        self.ship = ship
        self.members = []
        self.initialize_crew()
        self.selected_index = 0  # Default selected crew member

    def initialize_crew(self):
        """Starts with 3 crew members and assigns default roles."""
        self.members.append(Medic("Alice", self.ship, (3, 5)))
        self.members.append(Medic("Bob", self.ship, (4, 6)))
        self.members.append(Medic("Charlie", self.ship, (5, 7)))

    def select_crew_member(self, index):
        """Selects a crew member by index (1-9)."""
        if 0 <= index < len(self.members):
            self.selected_index = index

    def assign_role(self, role_letter):
        """Assigns a new role based on input letter."""
        name = self.members[self.selected_index].name
        position = self.members[self.selected_index].position

        role_map = {
            'p': Pilot,
            'e': Engineer,
            'm': Medic
        }

        if role_letter in role_map:
            self.members[self.selected_index] = role_map[role_letter](name, self.ship, position)


    def update(self):
        """Updates each crew member's tasks."""
        for member in self.members:
            member.perform_task()


    def display_crew_members(self, stdscr, pos):
        """Displays crew information on the UI, with the selected crew member in bold."""
        stdscr.addstr(pos, 2, "🕺 Crewmembers and roles", curses.A_BOLD)
        
        for i, member in enumerate(self.members):
            marker = ">" if i == self.selected_index else " "
            style = curses.A_BOLD if i == self.selected_index else curses.A_NORMAL
            stdscr.addstr(pos + 1 + i, 2, f"{marker} {i+1}. {member.name} ({member.role}) - Task: {member.task}", style)

    def count_roles(self):
        """Counts how many crew members are assigned to each role."""
        role_counts = {"Pilot": 0, "Engineer": 0, "Medic": 0, "Radar Operator": 0, "Researcher": 0}
        for member in self.members:
            if member.role in role_counts:
                role_counts[member.role] += 1
        return role_counts