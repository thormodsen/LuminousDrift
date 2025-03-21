import curses
from ship import Ship
from ui import ShipView, StatusView, Starfield
from helperclasses import status_display

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Set input timeout

    ship = Ship() #test ship
    ship_view = ShipView(ship)
    status_view = StatusView(ship, status_display)

    # Initialize starfield with the window size
    height, width = stdscr.getmaxyx()
    starfield = Starfield(height, width)

    status_display.add_message("Game Started")

    while True:
        stdscr.clear()

        # Update and render starfield
        starfield.update()
        starfield.render(stdscr)

        # Update and render ship and crew
        ship.update()
        ship_view.render(stdscr)

        # Update and render status view
        status_view.render(stdscr)
        
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('w'):
            ship.travel_system.select_jump(-1)
        elif key == ord('s'):
            ship.travel_system.select_jump(1)
        elif key == ord('j'):
            message = ship.travel_system.execute_jump()
            if message:
                stdscr.addstr(14, 2, message, curses.A_BOLD)
        elif ord('1') <= key <= ord('9'):
            ship.crew.select_crew_member(key - ord('1'))
        elif key in [ord('p'), ord('e'), ord('m'), ord('o')]:
            ship.crew.assign_role(chr(key))
        else:
            pass

if __name__ == "__main__":
    curses.wrapper(main)