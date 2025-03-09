import random
from pathfinding import Pathfinding

class Maintenance:
    def __init__(self, ship, crew):
        self.ship = ship
        self.crew = crew
        self.pathfinder = Pathfinding(ship)
        self.engine_heat = 0  # Heat level (simulated for now)
        self.maintenance_crew_index = 0  # Assign first crew member as maintenance
        
        # Lounge area (multiple positions)
        self.lounge_positions = [(3, 16), (3, 17), (4, 16), (4, 17)]  
        self.engine_position = (3, 7)  # Engine room position
        self.task = "idle"
        self.work_counter = 0  # Tracks how long they work before stopping
        self.path = []  # Holds the computed path

    def update(self):
        #Check engine status and assign tasks
        if self.engine_heat > 5 and self.task not in ["moving_to_engine", "working"]:
            self.task = "moving_to_engine"
            self.path = self.pathfinder.find_path(self.crew.positions[self.maintenance_crew_index], self.engine_position)
        elif self.engine_heat < 2 and self.task == "working":
            self.task = "moving_to_lounge"
            target_pos = random.choice(self.lounge_positions)
            self.path = self.pathfinder.find_path(self.crew.positions[self.maintenance_crew_index], target_pos)

        self.execute_task()

    def execute_task(self):
        #Move crew to assigned task location and perform actions
        if self.task in ["moving_to_engine", "moving_to_lounge"]:
            self.follow_path()
        elif self.task == "working":
            if self.work_counter > 0:
                self.work_counter -= 1 # just working
            elif self.work_counter == 0:
                self.engine_heat = max(0, self.engine_heat - 1)  # Apply maintenance (reduce heat)
                self.work_counter = 3 # create new workload, the amounts of loops it take for 1 maintenance
            else:
                self.task = "moving_to_lounge"

    def follow_path(self):
        #Move along the computed path
        if self.path:
            next_position = self.path.pop(0)
            self.crew.positions[self.maintenance_crew_index] = next_position
        else:
            self.task = "working" if self.task == "moving_to_engine" else "idle"