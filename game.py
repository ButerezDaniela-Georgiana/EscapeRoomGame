import pygame

from player import Player
from room import Room
from menu import Menu
from ui import draw_message_box, draw_interaction_hint, draw_progress_tracker
from sound_manager import SoundManager
from puzzles.electric_puzzle import ElectricPuzzle
from puzzles.chemistry_puzzle import ChemistryPuzzle
from puzzles.document_puzzle import DocumentPuzzle
from puzzles.wardrobe_puzzle import WardrobePuzzle

WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "Escape Room"

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("consolas", 30, bold=True)
        self.menu_title_font = pygame.font.SysFont("consolas", 52, bold=True)
        self.font = pygame.font.SysFont("consolas", 24)
        self.small_font = pygame.font.SysFont("consolas", 18)
        self.tiny_font = pygame.font.SysFont("consolas", 16)

        self.running = True
        self.state = "menu"   

        self.sound = SoundManager()
        self.menu = Menu(WIDTH, HEIGHT, self.menu_title_font, self.font, self.small_font)

        self.pause_button = pygame.Rect(20, 20, 70, 42)
        self.resume_button = pygame.Rect(WIDTH // 2 - 120, 300, 240, 55)
        self.main_menu_button = pygame.Rect(WIDTH // 2 - 120, 375, 240, 55)

        self.reset_game_state()

    def reset_game_state(self):
        self.player = Player(180, 560)
        self.room = Room()

        self.power_on = False
        self.has_glue = False
        self.document_repaired = False
        self.found_key = False

        self.message = "Camera e cufundată în întuneric. Doar panoul electric mai pâlpâie slab."

        self.electric_puzzle = ElectricPuzzle(WIDTH, HEIGHT)
        self.chemistry_puzzle = ChemistryPuzzle(WIDTH, HEIGHT)
        self.document_puzzle = DocumentPuzzle(WIDTH, HEIGHT)
        self.wardrobe_puzzle = WardrobePuzzle(WIDTH, HEIGHT)

    def near_rect(self, obj_rect, extra=42):
        return self.player.rect.colliderect(obj_rect.inflate(extra, extra))

    def draw_button(self, rect, text):
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)

        bg = (28, 34, 46) if not hovered else (50, 65, 90)
        border = (180, 185, 200)

        shadow = rect.move(0, 4)
        pygame.draw.rect(self.screen, (0, 0, 0), shadow, border_radius=12)

        pygame.draw.rect(self.screen, bg, rect, border_radius=12)
        pygame.draw.rect(self.screen, border, rect, 2, border_radius=12)

        text_surf = self.small_font.render(text, True, (235, 235, 240))
        self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def draw_pause_button(self):
        self.draw_button(self.pause_button, "||")

    def handle_menu_events(self, event):
        action = self.menu.handle_event(event)

        if action == "start":
            self.sound.play(self.sound.button_click)
            self.reset_game_state()
            self.state = "playing"
            self.sound.play_music("ambient_room.mp3", volume=0.5)

        elif action == "instructions":
            self.sound.play(self.sound.button_click)
            self.menu.state = "instructions"

        elif action == "exit":
            self.sound.play(self.sound.button_click)
            self.running = False

        elif action == "back":
            self.sound.play(self.sound.button_click)
            self.menu.state = "main"

    def handle_playing_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.pause_button.collidepoint(event.pos):
                self.sound.play(self.sound.button_click)
                self.state = "paused"
                return

        if self.electric_puzzle.active:
            self.electric_puzzle.handle_event(event)

            if self.electric_puzzle.just_failed:
                self.sound.play(self.sound.puzzle_error)
                self.electric_puzzle.just_failed = False

            if self.electric_puzzle.solved and not self.power_on:
                self.power_on = True
                self.sound.play(self.sound.puzzle_success)
                self.message = "Lumina revine treptat. În cameră se disting acum masa de chimie, biroul și dulapul."
            return

        if self.chemistry_puzzle.active:
            self.chemistry_puzzle.handle_event(event)

            if self.chemistry_puzzle.just_failed:
                self.sound.play(self.sound.puzzle_error)
                self.chemistry_puzzle.just_failed = False

            if self.chemistry_puzzle.solved and not self.has_glue:
                self.has_glue = True
                self.document_puzzle.has_glue = True
                self.sound.play(self.sound.puzzle_success)
                self.message = "Amestecul s-a stabilizat într-un adeziv violet. Documentul rupt de pe birou poate fi refăcut."
            return

        if self.document_puzzle.active:
            self.document_puzzle.handle_event(event)

            if self.document_puzzle.just_failed:
                self.sound.play(self.sound.puzzle_error)
                self.document_puzzle.just_failed = False

            if self.document_puzzle.solved and not self.document_repaired:
                self.document_repaired = True
                self.sound.play(self.sound.puzzle_success)
                self.message = "Mesajul refăcut te avertizează limpede: cheia e ascunsă sub hainele vechi din dulap."
            return

        if self.wardrobe_puzzle.active:
            self.wardrobe_puzzle.handle_event(event)

            if self.wardrobe_puzzle.solved and not self.found_key:
                self.found_key = True
                self.sound.play(self.sound.puzzle_success)
                self.message = "Sub hainele vechi ai găsit o cheie. Încuietoarea ușii ar trebui să cedeze."
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.near_rect(self.room.electric_panel):
                if not self.power_on:
                    self.electric_puzzle.active = True
                    self.message = "Panoul e deschis, iar firele sunt încurcate."
                else:
                    self.message = "Curentul funcționează deja."

            elif self.near_rect(self.room.chemistry_table):
                if not self.power_on:
                    self.message = "În bezna asta nu poți lucra aici. Mai întâi trebuie să aprinzi lumina."
                elif not self.has_glue:
                    self.chemistry_puzzle.active = True
                    self.message = "Pe masă sunt trei substanțe colorate. Ai nevoie de un compus violet."
                else:
                    self.message = "Ai deja adezivul pregătit."

            elif self.near_rect(self.room.document_table):
                if not self.power_on:
                    self.message = "Fără lumină nu poți cerceta documentul."
                elif not self.has_glue:
                    self.message = "Foaia este sfâșiată în bucăți. Fără un adeziv bun nu poate fi citită."
                elif not self.document_repaired:
                    self.document_puzzle.active = True
                    self.message = "Fragmentele trebuie puse în ordinea corectă."
                else:
                    self.message = "Documentul a fost deja refăcut."

            elif self.near_rect(self.room.wardrobe):
                if not self.document_repaired:
                    self.message = "Un dulap vechi, greu și prăfuit. Fără un indiciu, pare doar încă un colț uitat."
                elif not self.found_key:
                    self.wardrobe_puzzle.active = True
                    self.message = "Dacă testamentul spune adevărul, cheia ar trebui să fie ascunsă sub haine."
                else:
                    self.message = "Ai găsit deja cheia ascunsă."

            elif self.near_rect(self.room.exit_door):
                if not self.power_on:
                    self.message = "Ușa rămâne blocată în întuneric."
                elif not self.found_key:
                    self.message = "Clanța nu cedează. Încuietoarea cere o cheie."
                else:
                    self.sound.play(self.sound.puzzle_success)
                    self.state = "finished"
                    self.message = "Ușa se deschide încet. Aerul rece din exterior pătrunde în cameră."

    def handle_paused_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.sound.play(self.sound.button_click)
            self.state = "playing"
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.resume_button.collidepoint(event.pos):
                self.sound.play(self.sound.button_click)
                self.state = "playing"
                return

            if self.main_menu_button.collidepoint(event.pos):
                self.sound.play(self.sound.button_click)
                self.state = "menu"
                self.sound.stop_music()
                return

    def handle_finished_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.sound.play(self.sound.button_click)
            self.state = "menu"
            self.sound.stop_music()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == "menu":
                self.handle_menu_events(event)
            elif self.state == "playing":
                self.handle_playing_events(event)
            elif self.state == "paused":
                self.handle_paused_events(event)
            elif self.state == "finished":
                self.handle_finished_events(event)

    def update(self):
        if self.state != "playing":
            return

        self.electric_puzzle.update()
        self.chemistry_puzzle.update()
        self.document_puzzle.update()
        self.wardrobe_puzzle.update()

        if (
            not self.electric_puzzle.active
            and not self.chemistry_puzzle.active
            and not self.document_puzzle.active
            and not self.wardrobe_puzzle.active
        ):
            keys = pygame.key.get_pressed()
            obstacles = self.room.get_obstacles(self.found_key)
            self.player.move(keys, self.room.bounds, obstacles)

    def draw_world_hints(self):
        if self.near_rect(self.room.electric_panel) and not self.power_on:
            draw_interaction_hint(
                self.screen,
                "[E] Panou electric",
                self.small_font,
                self.room.electric_panel.centerx,
                self.room.electric_panel.y - 18
            )

        elif self.near_rect(self.room.chemistry_table) and self.power_on and not self.has_glue:
            draw_interaction_hint(
                self.screen,
                "[E] Stație chimică",
                self.small_font,
                self.room.chemistry_table.centerx,
                self.room.chemistry_table.y - 18
            )

        elif self.near_rect(self.room.document_table) and self.power_on:
            label = "[E] Document rupt" if self.has_glue else "[E] Birou"
            draw_interaction_hint(
                self.screen,
                label,
                self.small_font,
                self.room.document_table.centerx,
                self.room.document_table.y - 18
            )

        elif self.near_rect(self.room.wardrobe) and self.power_on:
            draw_interaction_hint(
                self.screen,
                "[E] Dulap",
                self.small_font,
                self.room.wardrobe.centerx,
                self.room.wardrobe.y - 18
            )

        elif self.near_rect(self.room.exit_door) and self.power_on:
            draw_interaction_hint(
                self.screen,
                "[E] Ușă",
                self.small_font,
                self.room.exit_door.centerx,
                self.room.exit_door.y - 18
            )

    def draw_game(self):
        self.room.draw(self.screen, self.power_on)
        self.room.draw_labels(self.screen, self.tiny_font, self.power_on)
        self.player.draw(self.screen)

        draw_progress_tracker(
            self.screen,
            self.small_font,
            self.power_on,
            self.has_glue,
            self.document_repaired,
            self.found_key
        )

        self.draw_world_hints()
        draw_message_box(self.screen, self.message, self.small_font)
        self.draw_pause_button()

        self.electric_puzzle.draw(self.screen, self.title_font, self.font, self.small_font)
        self.chemistry_puzzle.draw(self.screen, self.title_font, self.font, self.small_font)
        self.document_puzzle.draw(self.screen, self.title_font, self.font, self.small_font)
        self.wardrobe_puzzle.draw(self.screen, self.title_font, self.font, self.small_font)

    def draw_paused(self):
        self.draw_game()

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 170, 220, 340, 220)
        pygame.draw.rect(self.screen, (20, 24, 34), panel, border_radius=20)
        pygame.draw.rect(self.screen, (220, 220, 225), panel, 3, border_radius=20)

        title = self.title_font.render("PAUSE", True, (235, 235, 240))
        self.screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 45)))

        self.draw_button(self.resume_button, "Resume")
        self.draw_button(self.main_menu_button, "Main Menu")

    def draw_finished(self):
        self.room.draw(self.screen, self.power_on)
        self.room.draw_labels(self.screen, self.tiny_font, self.power_on)
        self.player.draw(self.screen)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(310, 180, 660, 220)
        pygame.draw.rect(self.screen, (20, 24, 34), panel, border_radius=20)
        pygame.draw.rect(self.screen, (220, 220, 225), panel, 3, border_radius=20)

        title = self.title_font.render("AI EVADAT", True, (115, 220, 145))
        self.screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 55)))

        line1 = self.small_font.render(
            "Ai descoperit cheia ascunsă și ai deschis ușa.",
            True,
            (225, 225, 230)
        )
        self.screen.blit(line1, line1.get_rect(center=(panel.centerx, panel.y + 110)))

        line2 = self.small_font.render(
            "ESC pentru a reveni la meniu",
            True,
            (180, 185, 195)
        )
        self.screen.blit(line2, line2.get_rect(center=(panel.centerx, panel.y + 160)))

    def draw(self):
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "paused":
            self.draw_paused()
        elif self.state == "finished":
            self.draw_finished()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        self.sound.stop_music()
        pygame.quit()