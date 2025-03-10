import heapq
import curses

class StatusMessageDisplay:
    def __init__(self, max_messages=20, width=45):
        self.messages = []
        self.max_messages = max_messages
        self.width = width
    
    def add_message(self, message):
        """Adds a new message to the debug log."""
        if not isinstance(message, str):
            message = str(message)  # Ensure message is a string

        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)  # Remove the oldest message
        self.messages.append(message)

    def draw(self, stdscr, start_x, start_y):
        """Draws the debug messages on the right side of the screen safely."""
        height, width = stdscr.getmaxyx()

        # Ensure we are not writing outside the screen
        safe_x = min(start_x, width - 1)
        
        stdscr.addstr(start_y, safe_x, "DEBUG LOG:", curses.A_BOLD)
        for i, message in enumerate(self.messages[-self.max_messages:]):
            # Truncate message to fit screen width
            truncated_message = message[:max(0, width - safe_x - 1)]
            try:
                stdscr.addstr(start_y + i + 1, safe_x, truncated_message)
            except curses.error:
                pass  # Ignore if the message cannot be printed
    
# Global instance for debug logging
status_display = StatusMessageDisplay() 

class Pathfinding:
    def __init__(self, ship):
        self.ship = ship

    def find_path(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        status_display.add_message(f"Finding path from {start} to {goal}")

        while open_set:
            _, current = heapq.heappop(open_set)
            #status_display.add_message(f"Exploring: {current}")

            if current == goal:
                #status_display.add_message(f"Goal reached: {goal}")
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

                # Adjust for ship offset
                adjusted_ny = ny - self.ship.ship_y
                adjusted_nx = nx - self.ship.ship_x

                # Bounds check
                if not (0 <= adjusted_ny < len(self.ship.layout) and 0 <= adjusted_nx < len(self.ship.layout[0])):
                    #status_display.add_message(f"Out of bounds: {neighbor} (Adjusted: {adjusted_ny}, {adjusted_nx})")
                    continue  

                # Walkability check
                if not self.ship.is_walkable(adjusted_ny, adjusted_nx):
                    #status_display.add_message(f"Blocked: {neighbor} (Adjusted: {adjusted_ny}, {adjusted_nx})")
                    continue  

                # Distance calculation
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    #status_display.add_message(f"Adding to queue: {neighbor} with f-score {f_score[neighbor]}")

        status_display.add_message("No path found.")
        return []  # No valid path found
    

