import pygame


class Menu:
    def __init__(self, width, height, title_font, font, small_font):
        self.width = width
        self.height = height
        self.title_font = title_font
        self.font = font
        self.small_font = small_font

        self.state = "main"

        self.start_button = pygame.Rect(width // 2 - 120, 365, 240, 60)
        self.instructions_button = pygame.Rect(width // 2 - 120, 445, 240, 60)
        self.exit_button = pygame.Rect(width // 2 - 120, 525, 240, 60)

        self.back_button = pygame.Rect(60, 55, 120, 50)

    def draw_button(self, screen, rect, text):
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)

        bg = (28, 34, 46) if not hovered else (50, 65, 90)
        border = (180, 185, 200)

        shadow = rect.move(0, 4)
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=14)

        pygame.draw.rect(screen, bg, rect, border_radius=14)
        pygame.draw.rect(screen, border, rect, 2, border_radius=14)

        text_surf = self.font.render(text, True, (235, 235, 240))
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.state == "main":
                if self.start_button.collidepoint(event.pos):
                    return "start"

                if self.instructions_button.collidepoint(event.pos):
                    return "instructions"

                if self.exit_button.collidepoint(event.pos):
                    return "exit"

            elif self.state == "instructions":
                if self.back_button.collidepoint(event.pos):
                    return "back"

        return None

    def draw_main(self, screen):
        screen.fill((8, 10, 15))

        panel = pygame.Rect(250, 90, 780, 560)
        pygame.draw.rect(screen, (18, 22, 32), panel, border_radius=24)
        pygame.draw.rect(screen, (170, 175, 190), panel, 2, border_radius=24)

        title = self.title_font.render("ESCAPE ROOM", True, (235, 235, 240))
        screen.blit(title, title.get_rect(center=(self.width // 2, 175)))

        lines = [
            "Te trezești într-o cameră necunoscută.",
            "Lumina lipsește. Tăcerea apasă.",
            "Cineva a fost aici înaintea ta...",
            "și a lăsat indicii în urmă."
        ]

        y = 245
        for line in lines:
            text = self.small_font.render(line, True, (180, 185, 200))
            screen.blit(text, text.get_rect(center=(self.width // 2, y)))
            y += 34

        self.draw_button(screen, self.start_button, "Start")
        self.draw_button(screen, self.instructions_button, "Instructions")
        self.draw_button(screen, self.exit_button, "Exit")

    def draw_instructions(self, screen):
        screen.fill((8, 10, 15))

        panel = pygame.Rect(200, 80, 880, 560)
        pygame.draw.rect(screen, (18, 22, 32), panel, border_radius=24)
        pygame.draw.rect(screen, (170, 175, 190), panel, 2, border_radius=24)

        title = self.title_font.render("INSTRUCTIONS", True, (235, 235, 240))
        screen.blit(title, title.get_rect(center=(self.width // 2, 145)))

        lines = [
            "Mișcare: W A S D sau săgeți",
            "Interacțiune: E",
            "",
            "Scopul tău:",
            "• repară circuitul electric",
            "• creează un compus corect",
            "• reconstruiește documentul",
            "• găsește cheia și evadează",
            "",
            "Nu toate răspunsurile sunt evidente."
        ]

        y = 235
        for line in lines:
            text = self.small_font.render(line, True, (200, 205, 215))
            screen.blit(text, text.get_rect(center=(self.width // 2, y)))
            y += 32

        self.draw_button(screen, self.back_button, "Back")

    def draw(self, screen):
        if self.state == "main":
            self.draw_main(screen)
        else:
            self.draw_instructions(screen)