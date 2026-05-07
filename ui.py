import pygame


def draw_text(screen, text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)


def draw_message_box(screen, text, font):
    box_rect = pygame.Rect(120, 660, 1040, 42)

    shadow_rect = box_rect.move(0, 3)
    pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=12)

    pygame.draw.rect(screen, (14, 16, 24), box_rect, border_radius=12)
    pygame.draw.rect(screen, (200, 200, 210), box_rect, 2, border_radius=12)

    draw_text(
        screen,
        text,
        font,
        (225, 225, 230),
        box_rect.x + 18,
        box_rect.y + 10
    )


def draw_interaction_hint(screen, text, font, x, y):
    padding_x = 12
    padding_y = 7

    text_surface = font.render(text, True, (235, 235, 240))
    text_rect = text_surface.get_rect()

    box_rect = pygame.Rect(
        x - text_rect.width // 2 - padding_x,
        y - text_rect.height // 2 - padding_y,
        text_rect.width + padding_x * 2,
        text_rect.height + padding_y * 2
    )

    shadow_rect = box_rect.move(0, 3)
    pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=10)

    pygame.draw.rect(screen, (18, 22, 32), box_rect, border_radius=10)
    pygame.draw.rect(screen, (180, 180, 190), box_rect, 2, border_radius=10)

    screen.blit(text_surface, text_surface.get_rect(center=box_rect.center))


def draw_progress_tracker(screen, font, power_on, has_glue, document_repaired, found_key):
    panel_rect = pygame.Rect(210, 12, 860, 44)

    shadow_rect = panel_rect.move(0, 3)
    pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=12)

    pygame.draw.rect(screen, (14, 16, 24), panel_rect, border_radius=12)
    pygame.draw.rect(screen, (170, 170, 180), panel_rect, 2, border_radius=12)

    items = [
        ("Curent", power_on),
        ("Adeziv", has_glue),
        ("Document", document_repaired),
        ("Cheie", found_key),
    ]

    section_width = panel_rect.width // 4

    for i, (label, value) in enumerate(items):
        section_x = panel_rect.x + i * section_width

        if i > 0:
            pygame.draw.line(
                screen,
                (70, 75, 90),
                (section_x, panel_rect.y + 8),
                (section_x, panel_rect.bottom - 8),
                1
            )

        status_text = "DA" if value else "NU"
        status_color = (110, 220, 145) if value else (185, 185, 195)

        draw_text(
            screen,
            label,
            font,
            (220, 220, 225),
            section_x + 18,
            panel_rect.y + 12
        )

        draw_text(
            screen,
            status_text,
            font,
            status_color,
            section_x + section_width - 48,
            panel_rect.y + 12
        )