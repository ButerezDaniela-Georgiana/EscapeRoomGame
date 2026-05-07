import pygame


class ChemistryPuzzle:
    def __init__(self, screen_width, screen_height):
        self.active = False
        self.solved = False
        self.has_glue = False
        self.just_failed = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.panel_rect = pygame.Rect(290, 130, 700, 360)

        self.slot_1 = pygame.Rect(430, 185, 72, 38)
        self.slot_2 = pygame.Rect(515, 185, 72, 38)
        self.beaker_rect = pygame.Rect(735, 175, 145, 82)

        self.red_rect = pygame.Rect(385, 255, 88, 120)
        self.blue_rect = pygame.Rect(495, 255, 88, 120)
        self.yellow_rect = pygame.Rect(605, 255, 88, 120)
        self.mix_button = pygame.Rect(745, 300, 135, 46)

        self.selected_colors = []
        self.result_color = (175, 175, 180)

        self.explosion_timer = 0
        self.success_timer = 0

    def reset_mix(self):
        self.selected_colors = []
        self.result_color = (175, 175, 180)

    def update(self):
        if self.explosion_timer > 0:
            self.explosion_timer -= 1

        if self.success_timer > 0:
            self.success_timer -= 1
            if self.success_timer == 0:
                self.active = False

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active = False
            self.reset_mix()
            return

        if self.solved:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if self.red_rect.collidepoint(pos) and len(self.selected_colors) < 2:
                self.selected_colors.append("red")
            elif self.blue_rect.collidepoint(pos) and len(self.selected_colors) < 2:
                self.selected_colors.append("blue")
            elif self.yellow_rect.collidepoint(pos) and len(self.selected_colors) < 2:
                self.selected_colors.append("yellow")
            elif self.mix_button.collidepoint(pos):
                self.mix_colors()

    def mix_colors(self):
        if len(self.selected_colors) != 2:
            self.explosion_timer = 22
            self.just_failed = True
            self.reset_mix()
            return

        if sorted(self.selected_colors) == ["blue", "red"]:
            self.result_color = (158, 92, 204)
            self.solved = True
            self.has_glue = True
            self.success_timer = 36
        else:
            self.explosion_timer = 22
            self.just_failed = True
            self.reset_mix()

    def draw_bottle(self, screen, rect, liquid_color, label, small_font):
        pygame.draw.rect(screen, (232, 232, 238), rect, border_radius=16)
        pygame.draw.rect(screen, (40, 42, 50), rect, 2, border_radius=16)

        neck = pygame.Rect(rect.x + 22, rect.y - 8, rect.width - 44, 16)
        pygame.draw.rect(screen, (215, 215, 220), neck, border_radius=5)
        pygame.draw.rect(screen, (40, 42, 50), neck, 2, border_radius=5)

        liquid_rect = pygame.Rect(rect.x + 11, rect.y + 33, rect.width - 22, rect.height - 46)
        pygame.draw.rect(screen, liquid_color, liquid_rect, border_radius=12)

        surf = small_font.render(label, True, (35, 35, 40))
        screen.blit(surf, surf.get_rect(center=(rect.centerx, rect.y + 16)))

    def draw(self, screen, title_font, font, small_font):
        if not self.active:
            return

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (22, 26, 36), self.panel_rect, border_radius=22)
        pygame.draw.rect(screen, (220, 220, 225), self.panel_rect, 3, border_radius=22)

        inner = pygame.Rect(
            self.panel_rect.x + 24,
            self.panel_rect.y + 92,
            self.panel_rect.width - 48,
            self.panel_rect.height - 128
        )
        pygame.draw.rect(screen, (14, 18, 28), inner, border_radius=18)

        title = title_font.render("STAȚIE CHIMICĂ", True, (240, 240, 240))
        screen.blit(title, title.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 34)))

        hint = small_font.render("Țintă: MOV", True, (190, 165, 250))
        screen.blit(hint, hint.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 68)))

        pygame.draw.rect(screen, (240, 240, 245), self.slot_1, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 55), self.slot_1, 2, border_radius=10)
        pygame.draw.rect(screen, (240, 240, 245), self.slot_2, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 55), self.slot_2, 2, border_radius=10)

        select_label = small_font.render("Selectat", True, (210, 210, 215))
        screen.blit(select_label, select_label.get_rect(center=(360, 202)))

        mapping = {
            "red": ("R", (220, 80, 80)),
            "blue": ("B", (80, 140, 220)),
            "yellow": ("G", (235, 210, 80)),
        }

        if len(self.selected_colors) >= 1:
            txt, color = mapping[self.selected_colors[0]]
            surf = font.render(txt, True, color)
            screen.blit(surf, surf.get_rect(center=self.slot_1.center))

        if len(self.selected_colors) >= 2:
            txt, color = mapping[self.selected_colors[1]]
            surf = font.render(txt, True, color)
            screen.blit(surf, surf.get_rect(center=self.slot_2.center))

        pygame.draw.rect(screen, (236, 236, 242), self.beaker_rect, border_radius=14)
        pygame.draw.rect(screen, (35, 35, 40), self.beaker_rect, 2, border_radius=14)
        liquid_rect = pygame.Rect(self.beaker_rect.x + 14, self.beaker_rect.y + 36, self.beaker_rect.width - 28, 30)
        pygame.draw.rect(screen, self.result_color, liquid_rect, border_radius=9)
        recip = small_font.render("Recipient", True, (25, 25, 25))
        screen.blit(recip, recip.get_rect(center=(self.beaker_rect.centerx, self.beaker_rect.y + 16)))

        self.draw_bottle(screen, self.red_rect, (220, 82, 82), "Roșu", small_font)
        self.draw_bottle(screen, self.blue_rect, (84, 136, 214), "Albastru", small_font)
        self.draw_bottle(screen, self.yellow_rect, (230, 208, 84), "Galben", small_font)

        pygame.draw.rect(screen, (112, 184, 124), self.mix_button, border_radius=14)
        pygame.draw.rect(screen, (20, 20, 20), self.mix_button, 2, border_radius=14)
        mix = font.render("MIX", True, (22, 22, 22))
        screen.blit(mix, mix.get_rect(center=self.mix_button.center))

        if self.solved:
            msg = small_font.render("Adeziv creat.", True, (110, 220, 145))
            screen.blit(msg, msg.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 24)))
        else:
            msg = small_font.render("2 sticluțe -> MIX | ESC", True, (170, 175, 185))
            screen.blit(msg, msg.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 24)))

        if self.explosion_timer > 0:
            flash = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            flash.fill((255, 120, 50, 90))
            screen.blit(flash, (0, 0))

            boom = font.render("Greșit!", True, (255, 200, 120))
            screen.blit(boom, boom.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 58)))