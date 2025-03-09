import curses
from ship import Ship

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Set input timeout
    
    ship = Ship()
    
    while True:
        stdscr.clear()
        
        # Draw ship layout
        ship.draw(stdscr)
        ship.update()
        
        # Display UI sections
        ship.display_status(stdscr, 1)
        ship.crew.display_crew_members(stdscr, 5)
        ship.travel_system.display_jump_options(stdscr, 10)
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('w'):  # Move selection up
            ship.travel_system.select_jump(-1)
        elif key == ord('s'):  # Move selection down
            ship.travel_system.select_jump(1)
        elif key == ord('j'):  # Execute jump
            message = ship.travel_system.execute_jump()
            if message:
                stdscr.addstr(14, 2, message, curses.A_BOLD)

        elif ord('1') <= key <= ord('9'):  # Select crew member (1-9)
            ship.crew.select_crew_member(key - ord('1'))
        elif key in [ord('p'), ord('e'), ord('m')]:  # Assign role
            ship.crew.assign_role(chr(key))
        else:
            pass

        
if __name__ == "__main__":
    curses.wrapper(main)