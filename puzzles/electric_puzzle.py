import pygame


class ElectricPuzzle:
    def __init__(self, screen_width, screen_height):
        self.active = False
        self.solved = False
        self.just_failed = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.panel_rect = pygame.Rect(180, 80, 920, 560)

        self.left_points = [
            {"pos": (330, 260), "color": (80, 140, 220), "id": 2},
            {"pos": (330, 360), "color": (220, 80, 80), "id": 0},
            {"pos": (330, 460), "color": (80, 200, 120), "id": 1},
        ]

        self.right_points = [
            {"pos": (950, 260), "color": (80, 200, 120), "id": 1},
            {"pos": (950, 360), "color": (80, 140, 220), "id": 2},
            {"pos": (950, 460), "color": (220, 80, 80), "id": 0},
        ]

        self.selected_left = None
        self.connections = []

        self.error_timer = 0
        self.error_message = ""

    def reset_connections(self):
        self.selected_left = None
        self.connections = []

    def update(self):
        if self.error_timer > 0:
            self.error_timer -= 1
            if self.error_timer == 0:
                self.reset_connections()
                self.error_message = ""

    def handle_event(self, event):
        if not self.active or self.solved:
            return

        if self.error_timer > 0:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
                self.selected_left = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            for point in self.left_points:
                px, py = point["pos"]
                if (mx - px) ** 2 + (my - py) ** 2 <= 24 ** 2:
                    self.selected_left = point["id"]
                    return

            for point in self.right_points:
                px, py = point["pos"]
                if (mx - px) ** 2 + (my - py) ** 2 <= 24 ** 2:
                    if self.selected_left is not None:
                        chosen_pair = (self.selected_left, point["id"])

                        self.connections = [c for c in self.connections if c[0] != self.selected_left]

                        if chosen_pair[0] != chosen_pair[1]:
                            self.connections.append(chosen_pair)
                            self.selected_left = None
                            self.error_timer = 28
                            self.error_message = "Scurtcircuit! Conexiunile au fost resetate."
                            self.just_failed = True
                            return

                        
                        self.connections.append(chosen_pair)
                        self.selected_left = None
                        self.check_solution()
                        return

    def check_solution(self):
        correct = [(0, 0), (1, 1), (2, 2)]
        if sorted(self.connections) == correct:
            self.solved = True
            self.active = False

    def draw_point(self, screen, point, selected=False):
        radius = 26 if selected else 22
        pygame.draw.circle(screen, point["color"], point["pos"], radius)
        pygame.draw.circle(screen, (20, 20, 20), point["pos"], radius, 3)

        if selected:
            glow = pygame.Surface((90, 90), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*point["color"], 60), (45, 45), 34)
            screen.blit(glow, (point["pos"][0] - 45, point["pos"][1] - 45))

    def draw_connections(self, screen):
        for left_id, right_id in self.connections:
            left_point = next(p for p in self.left_points if p["id"] == left_id)
            right_point = next(p for p in self.right_points if p["id"] == right_id)

            color = left_point["color"]
            width = 8

            if self.error_timer > 0 and left_id != right_id:
                color = (255, 210, 90)
                width = 10

            pygame.draw.line(screen, color, left_point["pos"], right_point["pos"], width)

    def draw_error_effect(self, screen):
        if self.error_timer <= 0:
            return

        alpha = min(170, self.error_timer * 6)
        flash = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        flash.fill((255, 90, 60, alpha))
        screen.blit(flash, (0, 0))

        for left_id, right_id in self.connections:
            if left_id != right_id:
                left_point = next(p for p in self.left_points if p["id"] == left_id)
                right_point = next(p for p in self.right_points if p["id"] == right_id)

                mx = (left_point["pos"][0] + right_point["pos"][0]) // 2
                my = (left_point["pos"][1] + right_point["pos"][1]) // 2

                pygame.draw.circle(screen, (255, 240, 120), (mx, my), 18)
                pygame.draw.line(screen, (255, 255, 255), (mx - 18, my - 10), (mx + 14, my + 6), 3)
                pygame.draw.line(screen, (255, 255, 255), (mx - 10, my + 16), (mx + 8, my - 14), 3)

    def draw(self, screen, title_font, font, small_font):
        if not self.active:
            return

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (24, 28, 38), self.panel_rect, border_radius=18)
        pygame.draw.rect(screen, (220, 220, 220), self.panel_rect, 3, border_radius=18)

        title_surface = title_font.render("PANOU ELECTRIC", True, (240, 240, 240))
        title_rect = title_surface.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 42))
        screen.blit(title_surface, title_rect)

        info_surface = font.render(
            "Conectează firele de aceeași culoare pentru a restabili alimentarea.",
            True,
            (185, 190, 205),
        )
        info_rect = info_surface.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 95))
        screen.blit(info_surface, info_rect)

        hint_surface = small_font.render(
            "Click pe un fir din stânga, apoi pe terminalul corect din dreapta. ESC = închide",
            True,
            (165, 170, 180),
        )
        hint_rect = hint_surface.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 22))
        screen.blit(hint_surface, hint_rect)

        inner = pygame.Rect(
            self.panel_rect.x + 100,
            self.panel_rect.y + 150,
            self.panel_rect.width - 200,
            320
        )
        pygame.draw.rect(screen, (16, 18, 24), inner, border_radius=14)

        self.draw_connections(screen)

        for point in self.left_points:
            self.draw_point(screen, point, selected=(self.selected_left == point["id"]))

        for point in self.right_points:
            self.draw_point(screen, point, selected=False)

        if self.error_message:
            err = font.render(self.error_message, True, (255, 170, 120))
            err_rect = err.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 68))
            screen.blit(err, err_rect)

        self.draw_error_effect(screen)