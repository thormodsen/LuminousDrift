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
            # Assign new class to the crew member
            self.members[self.selected_index] = role_map[role_letter](name, self.ship, position)
            status_display.add_message(f"{name} is assigned as {role_map[role_letter]}")

    def update(self):
        """Updates each crew member's tasks."""
        for member in self.members:
            member.perform_task()

    def count_roles(self):
        """Counts how many crew members are assigned to each role."""
        role_counts = {"Pilot": 0, "Engineer": 0, "Medic": 0, "Radar Operator": 0, "Researcher": 0}
        for member in self.members:
            if member.role in role_counts:
                role_counts[member.role] += 1
        return role_counts