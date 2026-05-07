import pygame


class WardrobePuzzle:
    def __init__(self, screen_width, screen_height):
        self.active = False
        self.solved = False
        self.key_found = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.panel_rect = pygame.Rect(250, 110, 780, 430)
        self.wardrobe_rect = pygame.Rect(330, 180, 360, 250)

        self.cloth_rects = [
            pygame.Rect(370, 215, 70, 150),
            pygame.Rect(460, 215, 70, 150),
            pygame.Rect(550, 215, 70, 150),
        ]

        self.hidden_key_rect = pygame.Rect(485, 380, 48, 20)

        self.clothes_removed = [False, False, False]
        self.success_timer = 0


    def all_clothes_removed(self):
        return all(self.clothes_removed)

    def update(self):
        if self.success_timer > 0:
            self.success_timer -= 1
            if self.success_timer == 0:
                self.active = False

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active = False
            return

        if self.solved:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            for i, rect in enumerate(self.cloth_rects):
                if rect.collidepoint(pos) and not self.clothes_removed[i]:
                    self.clothes_removed[i] = True
                    return

            if self.all_clothes_removed() and self.hidden_key_rect.collidepoint(pos):
                self.key_found = True
                self.solved = True
                self.success_timer = 36

    def draw_hanger(self, screen, x, y):
        pygame.draw.line(screen, (170, 170, 180), (x, y), (x, y + 18), 2)
        pygame.draw.arc(screen, (170, 170, 180), (x - 7, y - 8, 14, 14), 0.5, 3.5, 2)

    def draw_cloth(self, screen, rect, color):
        pygame.draw.rect(screen, color, rect, border_radius=16)
        pygame.draw.rect(screen, (30, 30, 30), rect, 2, border_radius=16)

    def draw_key(self, screen):
        pygame.draw.rect(screen, (190, 165, 90), self.hidden_key_rect, border_radius=5)
        pygame.draw.circle(screen, (190, 165, 90), (self.hidden_key_rect.x + 8, self.hidden_key_rect.centery), 8)
        pygame.draw.circle(screen, (90, 75, 35), (self.hidden_key_rect.x + 8, self.hidden_key_rect.centery), 3)
        pygame.draw.rect(screen, (190, 165, 90), (self.hidden_key_rect.x + 20, self.hidden_key_rect.y + 6, 20, 8))

    def draw(self, screen, title_font, font, small_font):
        if not self.active:
            return

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (22, 26, 36), self.panel_rect, border_radius=22)
        pygame.draw.rect(screen, (220, 220, 225), self.panel_rect, 3, border_radius=22)

        title = title_font.render("DULAP", True, (240, 240, 240))
        screen.blit(title, title.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 28)))

        if not self.solved:
            subtitle = small_font.render("Dă hainele la o parte și caută cheia.", True, (185, 190, 205))
        else:
            subtitle = small_font.render("Ai găsit cheia ascunsă.", True, (115, 220, 145))
        screen.blit(subtitle, subtitle.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 62)))

        pygame.draw.rect(screen, (84, 62, 46), self.wardrobe_rect, border_radius=14)
        pygame.draw.rect(screen, (56, 40, 30), self.wardrobe_rect, 3, border_radius=14)

        pygame.draw.line(
            screen,
            (160, 160, 168),
            (self.wardrobe_rect.x + 30, self.wardrobe_rect.y + 38),
            (self.wardrobe_rect.right - 30, self.wardrobe_rect.y + 38),
            4
        )

        colors = [(120, 85, 100), (90, 105, 135), (115, 95, 70)]

        for i, rect in enumerate(self.cloth_rects):
            if not self.clothes_removed[i]:
                self.draw_hanger(screen, rect.centerx, rect.y - 18)
                self.draw_cloth(screen, rect, colors[i])

        compartment = pygame.Rect(self.wardrobe_rect.x + 95, self.wardrobe_rect.bottom - 52, 170, 36)
        pygame.draw.rect(screen, (68, 50, 36), compartment, border_radius=8)
        pygame.draw.rect(screen, (40, 28, 18), compartment, 2, border_radius=8)

        if self.all_clothes_removed():
            self.draw_key(screen)

        footer = small_font.render("Click pe haine | apoi pe cheie | ESC", True, (170, 175, 185))
        screen.blit(footer, footer.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 22)))