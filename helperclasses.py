import heapq
import curses

class StatusMessageDisplay:
    def __init__(self, max_messages=20, width=45):
        self.messages = []
        self.max_messages = max_messages
        self.width = width
    
    def add_message(self, message):
        """Adds a new message to the debug log."""
        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)  # Remove the oldest message
        self.messages.append(message)
    
    def draw(self, stdscr, start_x, start_y):
        """Draws the debug messages on the right side of the screen."""
        stdscr.addstr(start_y, start_x, "DEBUG LOG:", curses.A_BOLD)
        for i, message in enumerate(self.messages[-self.max_messages:]):
            stdscr.addstr(start_y + 1 + i, start_x, f"> {message[:self.width]}")

# Global instance for debug logging
status_display = StatusMessageDisplay() 

class Pathfinding:
    def __init__(self, ship):
        self.ship = ship

    def find_path(self, start, goal):
        # finds the shortest path using A* algorithm.
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            y, x = current
            neighbors = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
            for neighbor in neighbors:
                ny, nx = neighbor
                if not (0 <= ny < len(self.ship.layout) and 0 <= nx < len(self.ship.layout[0])):
                    continue  # Out of bounds
                if not self.ship.is_walkable(ny, nx):
                    continue  # Not walkable

                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No valid path found
    

