import pygame
from ship import Ship
from ui_pyg import ShipView, StatusView

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Luminous Drift")
    clock = pygame.time.Clock()

    ship = Ship()
    ship_view = ShipView(ship)
    status_view = StatusView(ship)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Map key events to your game logic
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_w:
                    ship.travel_system.select_jump(-1)
                elif event.key == pygame.K_s:
                    ship.travel_system.select_jump(1)
                elif event.key == pygame.K_j:
                    message = ship.travel_system.execute_jump()
                    if message:
                        status_view.add_message(message)
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    ship.crew.select_crew_member(event.key - pygame.K_1)
                elif event.key in [pygame.K_p, pygame.K_e, pygame.K_m, pygame.K_o]:
                    ship.crew.assign_role(chr(event.key))

        ship.update()

        # Drawing
        screen.fill((30, 30, 30))  # Clear screen with a dark color
        ship_view.render(screen)
        status_view.render(screen)
        pygame.display.flip()

        clock.tick(60)  # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()