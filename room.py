import pygame


class Room:
    def __init__(self):

        self.bounds = pygame.Rect(90, 95, 1100, 560)

        self.electric_panel = pygame.Rect(130, 120, 120, 90)
        self.document_table = pygame.Rect(470, 130, 220, 110)
        self.wardrobe = pygame.Rect(860, 120, 190, 150)
        self.exit_door = pygame.Rect(1110, 340, 70, 130)
        self.chemistry_table = pygame.Rect(240, 430, 240, 115)

    def get_obstacles(self, found_key=False):
        obstacles = [
            self.document_table.inflate(-10, -10),
            self.wardrobe.inflate(-8, -8),
            self.chemistry_table.inflate(-10, -10),
        ]

        if not found_key:
            obstacles.append(self.exit_door.inflate(-8, -8))

        return obstacles

    def draw_room_base(self, screen):
        screen.fill((8, 10, 15))

        pygame.draw.rect(screen, (18, 22, 32), self.bounds, border_radius=24)
        pygame.draw.rect(screen, (50, 58, 75), self.bounds, 3, border_radius=24)

        inner_floor = self.bounds.inflate(-24, -24)
        pygame.draw.rect(screen, (12, 16, 24), inner_floor, border_radius=20)

        for x in range(inner_floor.x + 40, inner_floor.right, 90):
            pygame.draw.line(screen, (18, 23, 32), (x, inner_floor.y), (x, inner_floor.bottom), 1)
        for y in range(inner_floor.y + 40, inner_floor.bottom, 90):
            pygame.draw.line(screen, (18, 23, 32), (inner_floor.x, y), (inner_floor.right, y), 1)

    def draw_light_effect(self, screen, power_on):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)

        if not power_on:
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            glow = pygame.Surface((220, 180), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (130, 130, 170, 45), (0, 0, 220, 180))
            screen.blit(glow, (80, 80))
        else:
            pygame.draw.ellipse(overlay, (255, 235, 180, 18), (280, 40, 700, 220))
            pygame.draw.ellipse(overlay, (255, 235, 180, 8), (170, 5, 900, 300))
            screen.blit(overlay, (0, 0))

    def draw_shadow(self, screen, rect, offset=(6, 6), radius=12):
        shadow_rect = rect.move(offset[0], offset[1])
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=radius)

    def draw_electric_panel(self, screen, power_on):
        rect = self.electric_panel
        self.draw_shadow(screen, rect, radius=10)

        body = (70, 76, 90) if power_on else (48, 52, 62)
        pygame.draw.rect(screen, body, rect, border_radius=10)
        pygame.draw.rect(screen, (170, 175, 185), rect, 2, border_radius=10)

        inner = rect.inflate(-20, -22)
        pygame.draw.rect(screen, (24, 26, 34), inner, border_radius=8)

        for i in range(3):
            pygame.draw.circle(screen, (170, 70, 70), (rect.x + 28 + i * 24, rect.y + 24), 5)

        pygame.draw.rect(screen, (92, 98, 116), (rect.x + 20, rect.y + 48, rect.width - 40, 20), border_radius=6)

    def draw_chemistry_table(self, screen):
        rect = self.chemistry_table
        self.draw_shadow(screen, rect, radius=12)

        pygame.draw.rect(screen, (92, 68, 48), rect, border_radius=12)
        pygame.draw.rect(screen, (60, 44, 30), rect, 2, border_radius=12)

        top_surface = pygame.Rect(rect.x + 8, rect.y + 8, rect.width - 16, rect.height - 16)
        pygame.draw.rect(screen, (106, 78, 54), top_surface, border_radius=10)

        bottles = [
            ((220, 82, 82), rect.x + 28),
            ((84, 136, 214), rect.x + 84),
            ((230, 208, 84), rect.x + 140),
        ]

        for color, x in bottles:
            bottle = pygame.Rect(x, rect.y + 18, 34, 58)
            pygame.draw.rect(screen, (225, 225, 232), bottle, border_radius=7)
            pygame.draw.rect(screen, (46, 46, 52), bottle, 2, border_radius=7)
            pygame.draw.rect(screen, color, (x + 5, rect.y + 38, 24, 28), border_radius=5)

        beaker = pygame.Rect(rect.right - 55, rect.y + 18, 34, 48)
        pygame.draw.rect(screen, (228, 228, 235), beaker, border_radius=6)
        pygame.draw.rect(screen, (46, 46, 52), beaker, 2, border_radius=6)

    def draw_document_table(self, screen):
        rect = self.document_table
        self.draw_shadow(screen, rect, radius=12)

        pygame.draw.rect(screen, (90, 66, 47), rect, border_radius=12)
        pygame.draw.rect(screen, (60, 44, 30), rect, 2, border_radius=12)

        top_surface = pygame.Rect(rect.x + 8, rect.y + 8, rect.width - 16, rect.height - 16)
        pygame.draw.rect(screen, (106, 78, 54), top_surface, border_radius=10)

        paper_1 = pygame.Rect(rect.x + 24, rect.y + 22, 72, 36)
        paper_2 = pygame.Rect(rect.x + 110, rect.y + 28, 68, 32)
        for paper in [paper_1, paper_2]:
            pygame.draw.rect(screen, (236, 226, 198), paper, border_radius=5)
            pygame.draw.rect(screen, (128, 110, 84), paper, 1, border_radius=5)

    def draw_wardrobe(self, screen):
        rect = self.wardrobe
        self.draw_shadow(screen, rect, radius=12)

        pygame.draw.rect(screen, (80, 58, 44), rect, border_radius=12)
        pygame.draw.rect(screen, (54, 38, 28), rect, 3, border_radius=12)

        left = pygame.Rect(rect.x + 10, rect.y + 10, rect.width // 2 - 15, rect.height - 20)
        right = pygame.Rect(rect.x + rect.width // 2 + 5, rect.y + 10, rect.width // 2 - 15, rect.height - 20)

        pygame.draw.rect(screen, (98, 72, 54), left, border_radius=8)
        pygame.draw.rect(screen, (98, 72, 54), right, border_radius=8)

        pygame.draw.circle(screen, (188, 164, 92), (left.right - 11, left.centery), 4)
        pygame.draw.circle(screen, (188, 164, 92), (right.x + 11, right.centery), 4)

    def draw_exit_door(self, screen):
        rect = self.exit_door
        self.draw_shadow(screen, rect, radius=10)

        pygame.draw.rect(screen, (72, 96, 72), rect, border_radius=8)
        pygame.draw.rect(screen, (44, 58, 44), rect, 3, border_radius=8)
        pygame.draw.circle(screen, (190, 165, 90), (rect.right - 11, rect.centery), 4)

    def draw_labels(self, screen, font, power_on):
        color = (145, 150, 160) if power_on else (118, 120, 130)

        labels = [
            ("Panou", self.electric_panel.centerx, self.electric_panel.bottom + 18),
            ("Birou", self.document_table.centerx, self.document_table.bottom + 18),
            ("Dulap", self.wardrobe.centerx, self.wardrobe.bottom + 18),
            ("Ușă", self.exit_door.centerx, self.exit_door.bottom + 16),
            ("Chimie", self.chemistry_table.centerx, self.chemistry_table.bottom + 18),
        ]

        for text, x, y in labels:
            surf = font.render(text, True, color)
            screen.blit(surf, surf.get_rect(center=(x, y)))

    def draw(self, screen, power_on):
        self.draw_room_base(screen)
        self.draw_electric_panel(screen, power_on)
        self.draw_document_table(screen)
        self.draw_wardrobe(screen)
        self.draw_exit_door(screen)
        self.draw_chemistry_table(screen)
        self.draw_light_effect(screen, power_on)