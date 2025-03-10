import curses
from roles import Offduty, Engineer, Medic, Pilot
from helperclasses import status_display

class Crew:
    def __init__(self, ship):
        self.ship = ship
        self.members = []
        self.initialize_crew()
        self.selected_index = 0  # Default selected crew member

    def initialize_crew(self):
        """Starts crew members and assigns default roles."""
        lounge_position = self.ship.room_positions["lounge"]
        self.members.append(Offduty("Alice", self.ship, lounge_position))
        self.members.append(Offduty("Bob", self.ship, lounge_position))
        
    def select_crew_member(self, index):
        """Selects a crew member by index (1-9)."""
        if 0 <= index < len(self.members):
            self.selected_index = index

    def assign_role(self, role_letter):
        """Assigns a new role based on input letter."""
        name = self.members[self.selected_index].name
        position = self.members[self.selected_index].position

        role_map = {
            'o': Offduty,
            'e': Engineer,
            'm': Medic,
            'p': Pilot
        }

        if role_letter in role_map:
            """assign new class to crewmember"""
            self.members[self.selected_index] = role_map[role_letter](name, self.ship, position)
            status_display.add_message(f"{name} is assigned as {role_map[role_letter]}")


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

    def display_debug_crew_members(self, stdscr, pos):
        """Displays crew information on the UI, with the selected crew member in bold."""
        stdscr.addstr(pos, 2, "🪲 Crewmembers and roles [DEBUG]", curses.A_BOLD)
        
        for i, member in enumerate(self.members):
            marker = ">" if i == self.selected_index else " "
            style = curses.A_BOLD if i == self.selected_index else curses.A_NORMAL
            stdscr.addstr(pos + 1 + i, 2, f"{marker} {i+1}. {member.name} // {member.role} // {member.position} // {member.task} // {member.path}", style)


    def count_roles(self):
        """Counts how many crew members are assigned to each role."""
        role_counts = {"Pilot": 0, "Engineer": 0, "Medic": 0, "Radar Operator": 0, "Researcher": 0}
        for member in self.members:
            if member.role in role_counts:
                role_counts[member.role] += 1
        return role_counts