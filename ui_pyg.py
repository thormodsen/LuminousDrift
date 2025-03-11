import pygame

class ShipView:
    def __init__(self, ship):
        self.ship = ship
        # Define fonts, colors, or load images as needed.
        self.font = pygame.font.SysFont("monospace", 20)
    
    def render(self, surface):
        text = self.font.render("Hello Pedro!", True, (255, 255, 255))
        surface.blit(text, (10, 10))
        # Draw the ship representation.
        # For example, draw the ship's grid or modules.
        """
        for module in self.ship.modules:
            rect = pygame.Rect(module.x, module.y, module.width, module.height)
            pygame.draw.rect(surface, (70, 130, 180), rect)  # Steel blue color
            text = self.font.render(module.name, True, (255, 255, 255))
            surface.blit(text, (module.x + 5, module.y + 5))
        """
    
class StatusView:
    def __init__(self, ship):
        self.ship = ship
        self.font = pygame.font.SysFont("monospace", 18)
        self.messages = []  # Use a list to store status messages
    
    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > 5:  # Keep only the last 5 messages
            self.messages.pop(0)
    
    def render(self, surface):
        # Render messages at the bottom of the screen.
        y_offset = surface.get_height() - (len(self.messages) * 22) - 10
        for message in self.messages:
            text = self.font.render(message, True, (255, 255, 255))
            surface.blit(text, (10, y_offset))
            y_offset += 22