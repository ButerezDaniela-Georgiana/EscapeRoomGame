import os
import pygame


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = 4

        self.direction = "down"
        self.moving = False

        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.sprite_size = (64, 72)

        self.animations = {
            "down": [],
            "up": [],
            "left": [],
            "right": [],
        }

        self.load_sprites()

    def load_sprites(self):
        path = os.path.join("assets", "player_sheet.png")

        if not os.path.exists(path):
            return

        sheet = pygame.image.load(path).convert_alpha()

        frame_rects = {
            "down": [
                pygame.Rect(16, 4, 72, 100),
                pygame.Rect(104, 4, 72, 100),
                pygame.Rect(192, 4, 72, 100),
                pygame.Rect(280, 4, 72, 100),
            ],
            "up": [
                pygame.Rect(16, 120, 72, 100),
                pygame.Rect(104, 120, 72, 100),
                pygame.Rect(192, 120, 72, 100),
                pygame.Rect(280, 120, 72, 100),
            ],
            "left": [
                pygame.Rect(16, 236, 64, 100),
                pygame.Rect(96, 236, 64, 100),
                pygame.Rect(176, 236, 64, 100),
                pygame.Rect(256, 236, 64, 100),
            ],
            "right": [
                pygame.Rect(20, 352, 64, 100),
                pygame.Rect(100, 352, 64, 100),
                pygame.Rect(180, 352, 64, 100),
                pygame.Rect(260, 352, 64, 100),
            ],
        }

        for direction, rects in frame_rects.items():
            for rect in rects:
                frame = sheet.subsurface(rect).copy()
                frame = pygame.transform.scale(frame, self.sprite_size)
                self.animations[direction].append(frame)

    def move(self, keys, bounds, obstacles=None):
        if obstacles is None:
            obstacles = []

        dx, dy = 0, 0
        self.moving = False

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
            self.direction = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
            self.direction = "down"

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direction = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direction = "right"

        if dx != 0 or dy != 0:
            self.moving = True
            self.update_animation()
        else:
            self.animation_index = 0

        if dx != 0:
            test_rect = self.rect.copy()
            test_rect.x += dx

            if test_rect.left < bounds.left:
                test_rect.left = bounds.left
            if test_rect.right > bounds.right:
                test_rect.right = bounds.right

            if not any(test_rect.colliderect(ob) for ob in obstacles):
                self.rect.x = test_rect.x

        if dy != 0:
            test_rect = self.rect.copy()
            test_rect.y += dy

            if test_rect.top < bounds.top:
                test_rect.top = bounds.top
            if test_rect.bottom > bounds.bottom:
                test_rect.bottom = bounds.bottom

            if not any(test_rect.colliderect(ob) for ob in obstacles):
                self.rect.y = test_rect.y

    def update_animation(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frames = self.animations[self.direction]
            if frames:
                self.animation_index = (self.animation_index + 1) % len(frames)

    def draw(self, screen):
        frames = self.animations.get(self.direction, [])

        if frames:
            frame = frames[self.animation_index % len(frames)]
            sprite_rect = frame.get_rect(center=self.rect.center)

            sprite_rect.y -= 24

            screen.blit(frame, sprite_rect)
        else:
            pygame.draw.rect(screen, (220, 140, 90), self.rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=8)