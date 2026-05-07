import pygame


class DocumentPuzzle:
    def __init__(self, screen_width, screen_height):
        self.active = False
        self.solved = False
        self.has_glue = False
        self.just_failed = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.panel_rect = pygame.Rect(190, 95, 900, 500)
        self.board_rect = pygame.Rect(255, 175, 430, 280)
        self.side_rect = pygame.Rect(730, 165, 275, 335)

        self.slot_rects = [
            pygame.Rect(315, 230, 150, 72),
            pygame.Rect(480, 230, 150, 72),
            pygame.Rect(315, 315, 150, 72),
            pygame.Rect(480, 315, 150, 72),
        ]

        self.piece_rects = [
            pygame.Rect(785, 205, 175, 62),
            pygame.Rect(785, 278, 175, 62),
            pygame.Rect(785, 351, 175, 62),
            pygame.Rect(785, 424, 175, 62),
        ]

        self.apply_glue_button = pygame.Rect(780, 520, 185, 42)

        self.placed = [None, None, None, None]
        self.selected_piece = None

        self.success_timer = 0
        self.error_timer = 0
        self.feedback_message = ""

        self.piece_labels = [
            ["Dacă citești", "aceste rânduri,"],
            ["înseamnă că", "ai ajuns aici."],
            ["Cheia e sub", "hainele vechi"],
            ["din dulap.", "Nu te opri."],
        ]

    def all_slots_filled(self):
        return all(piece is not None for piece in self.placed)

    def arrangement_is_correct(self):
        return self.placed == [0, 1, 2, 3]

    def remove_piece_from_slot(self, slot_index):
        self.placed[slot_index] = None

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active = False
            self.selected_piece = None
            return

        if self.solved:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            for piece_id, rect in enumerate(self.piece_rects):
                if rect.collidepoint(pos):
                    if piece_id not in self.placed:
                        self.selected_piece = piece_id
                    return

            for slot_index, slot_rect in enumerate(self.slot_rects):
                if slot_rect.collidepoint(pos):
                    if self.selected_piece is None and self.placed[slot_index] is not None:
                        self.remove_piece_from_slot(slot_index)
                        self.feedback_message = ""
                        return

                    if self.selected_piece is not None:
                        self.placed[slot_index] = self.selected_piece
                        self.selected_piece = None
                        self.feedback_message = ""
                        return

            if self.apply_glue_button.collidepoint(pos):
                if not self.has_glue:
                    self.feedback_message = "Îți lipsește adezivul."
                    self.error_timer = 35
                    self.just_failed = True
                    return

                if not self.all_slots_filled():
                    self.feedback_message = "Mai lipsesc fragmente."
                    self.error_timer = 35
                    self.just_failed = True
                    return

                if not self.arrangement_is_correct():
                    self.feedback_message = "Fragmentele nu se potrivesc. Ordinea este greșită."
                    self.error_timer = 45
                    self.just_failed = True
                    return

                self.solved = True
                self.success_timer = 45
                self.feedback_message = ""
                return

    def update(self):
        if self.success_timer > 0:
            self.success_timer -= 1
            if self.success_timer == 0:
                self.active = False

        if self.error_timer > 0:
            self.error_timer -= 1
            if self.error_timer == 0:
                self.feedback_message = ""

    def draw_background(self, screen):
        pygame.draw.rect(screen, (22, 26, 36), self.panel_rect, border_radius=22)
        pygame.draw.rect(screen, (220, 220, 225), self.panel_rect, 3, border_radius=22)

        pygame.draw.rect(screen, (90, 66, 47), self.board_rect, border_radius=18)
        pygame.draw.rect(screen, (66, 48, 35), self.board_rect, 3, border_radius=18)

        pygame.draw.rect(screen, (14, 18, 28), self.side_rect, border_radius=16)

    def draw_piece(self, screen, rect, lines, small_font, selected=False):
        paper = (238, 228, 202) if not selected else (246, 237, 214)
        edge = (122, 104, 80)

        pygame.draw.rect(screen, paper, rect, border_radius=8)
        pygame.draw.rect(screen, edge, rect, 2, border_radius=8)

        total_lines = len(lines)
        line_gap = 20
        start_y = rect.centery - ((total_lines - 1) * line_gap) // 2

        for i, line in enumerate(lines):
            surf = small_font.render(line, True, (55, 45, 40))
            screen.blit(surf, surf.get_rect(center=(rect.centerx, start_y + i * line_gap)))

    def draw_slots(self, screen):
        for rect in self.slot_rects:
            pygame.draw.rect(screen, (168, 145, 112), rect, border_radius=8)
            pygame.draw.rect(screen, (106, 86, 62), rect, 2, border_radius=8)

    def draw_completed_document(self, screen, font, small_font):
        doc_rect = pygame.Rect(315, 205, 320, 180)
        pygame.draw.rect(screen, (240, 228, 200), doc_rect, border_radius=10)
        pygame.draw.rect(screen, (112, 96, 72), doc_rect, 2, border_radius=10)

        title = font.render("Mesaj refăcut", True, (55, 45, 40))
        screen.blit(title, title.get_rect(center=(doc_rect.centerx, doc_rect.y + 24)))

        lines = [
            "Dacă citești aceste rânduri,",
            "înseamnă că ai ajuns până aici.",
            "Cheia e ascunsă sub hainele vechi",
            "din dulap. Nu te opri acum."
        ]

        y = doc_rect.y + 62
        for line in lines:
            surf = small_font.render(line, True, (58, 48, 42))
            screen.blit(surf, surf.get_rect(center=(doc_rect.centerx, y)))
            y += 24

    def draw_error_effect(self, screen):
        if self.error_timer <= 0:
            return

        alpha = min(80, self.error_timer * 2)
        flash = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        flash.fill((180, 40, 40, alpha))
        screen.blit(flash, (0, 0))

    def draw(self, screen, title_font, font, small_font):
        if not self.active:
            return

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        screen.blit(overlay, (0, 0))

        self.draw_background(screen)

        title = title_font.render("DOCUMENT RUPT", True, (240, 240, 240))
        screen.blit(title, title.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 24)))

        if self.solved:
            subtitle = small_font.render("Mesajul a fost refăcut.", True, (115, 220, 145))
            screen.blit(subtitle, subtitle.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 58)))

            self.draw_completed_document(screen, font, small_font)

            footer = small_font.render("Se închide...", True, (170, 175, 185))
            screen.blit(footer, footer.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 18)))
            return

        subtitle = small_font.render("Rearanjează fragmentele și lipește-le.", True, (185, 190, 205))
        screen.blit(subtitle, subtitle.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 58)))

        self.draw_slots(screen)

        for slot_index, piece_id in enumerate(self.placed):
            if piece_id is not None:
                self.draw_piece(
                    screen,
                    self.slot_rects[slot_index],
                    self.piece_labels[piece_id],
                    small_font
                )

        available = small_font.render("Fragmente", True, (210, 210, 215))
        screen.blit(available, available.get_rect(center=(self.side_rect.centerx, self.side_rect.y + 18)))

        for piece_id, rect in enumerate(self.piece_rects):
            if piece_id not in self.placed:
                self.draw_piece(
                    screen,
                    rect,
                    self.piece_labels[piece_id],
                    small_font,
                    selected=(self.selected_piece == piece_id)
                )

        btn_color = (110, 178, 122) if self.has_glue else (110, 110, 118)
        pygame.draw.rect(screen, btn_color, self.apply_glue_button, border_radius=12)
        pygame.draw.rect(screen, (20, 20, 20), self.apply_glue_button, 2, border_radius=12)

        text = "Aplică adezivul" if self.has_glue else "Lipsește adezivul"
        surf = small_font.render(text, True, (20, 20, 20))
        screen.blit(surf, surf.get_rect(center=self.apply_glue_button.center))

        if self.feedback_message:
            feedback_color = (255, 180, 140) if self.error_timer > 0 else (165, 170, 180)
            feedback = small_font.render(self.feedback_message, True, feedback_color)
            screen.blit(feedback, feedback.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 44)))

        footer = small_font.render("piesă -> slot | click slot = scoate", True, (165, 170, 180))
        screen.blit(footer, footer.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 18)))

        self.draw_error_effect(screen)