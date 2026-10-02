import asyncio
import math
import os
import sys
from datetime import datetime

import pygame

WIDTH, HEIGHT = 1200, 720
FPS = 60
IS_WEB = sys.platform == "emscripten"

SKY = (185, 225, 250)
SKY2 = (218, 239, 252)
WHITE = (255, 255, 255)
DARK = (38, 45, 56)
PANEL = (244, 247, 250)
PANEL_BORDER = (205, 214, 223)
GREEN = (83, 171, 92)
GREEN_DARK = (46, 125, 61)
ROAD = (67, 72, 82)
ROAD_LINE = (245, 220, 93)
RED = (220, 71, 65)
BLUE = (60, 120, 210)
YELLOW = (250, 198, 53)
ORANGE = (245, 140, 45)
BROWN = (112, 78, 50)
WINDOW = (155, 215, 242)
GRAY = (130, 140, 150)
PURPLE = (128, 84, 196)

SCENE_W = 900
PANEL_X = SCENE_W

paused = False
speed = 1.0
animation_time = 0.0
screenshot_count = 0


def draw_text(surface, text, font, color, pos):
    image = font.render(text, True, color)
    surface.blit(image, pos)


def draw_cloud(surface, x, y, scale=1.0):
    parts = [
        (x, y + 18 * scale, 30 * scale),
        (x + 28 * scale, y, 38 * scale),
        (x + 66 * scale, y + 16 * scale, 31 * scale),
        (x + 32 * scale, y + 28 * scale, 42 * scale),
    ]
    for cx, cy, radius in parts:
        pygame.draw.circle(surface, WHITE, (int(cx), int(cy)), int(radius))


def draw_tree(surface, x, y):
    pygame.draw.rect(surface, BROWN, (x - 10, y, 20, 72), border_radius=4)
    pygame.draw.circle(surface, GREEN_DARK, (x - 25, y - 6), 34)
    pygame.draw.circle(surface, GREEN, (x + 8, y - 16), 40)
    pygame.draw.circle(surface, GREEN_DARK, (x + 34, y + 3), 31)
    pygame.draw.circle(surface, GREEN, (x - 2, y - 42), 32)


def draw_house(surface, x, y, body_color):
    pygame.draw.rect(surface, body_color, (x, y, 120, 125), border_radius=4)
    pygame.draw.polygon(surface, (126, 73, 55), [(x - 10, y), (x + 60, y - 58), (x + 130, y)])
    pygame.draw.rect(surface, (90, 58, 42), (x + 48, y + 64, 28, 61))
    pygame.draw.rect(surface, WINDOW, (x + 14, y + 28, 30, 30))
    pygame.draw.rect(surface, WINDOW, (x + 80, y + 28, 26, 30))
    pygame.draw.line(surface, WHITE, (x + 29, y + 28), (x + 29, y + 58), 2)
    pygame.draw.line(surface, WHITE, (x + 14, y + 43), (x + 44, y + 43), 2)


def draw_car(surface, x, y):
    pygame.draw.ellipse(surface, (45, 48, 53), (x + 5, y + 48, 126, 17))
    pygame.draw.rect(surface, RED, (x, y + 18, 135, 38), border_radius=10)
    pygame.draw.polygon(surface, RED, [(x + 24, y + 18), (x + 49, y - 8), (x + 99, y - 8), (x + 119, y + 18)])
    pygame.draw.polygon(surface, WINDOW, [(x + 51, y + 14), (x + 57, y - 2), (x + 76, y - 2), (x + 76, y + 14)])
    pygame.draw.polygon(surface, WINDOW, [(x + 82, y + 14), (x + 82, y - 2), (x + 96, y - 2), (x + 110, y + 14)])
    for wheel_x in (x + 30, x + 105):
        pygame.draw.circle(surface, DARK, (int(wheel_x), int(y + 57)), 14)
        pygame.draw.circle(surface, GRAY, (int(wheel_x), int(y + 57)), 6)
    pygame.draw.circle(surface, YELLOW, (int(x + 129), int(y + 35)), 6)


def draw_ball(surface, x, y, angle):
    pygame.draw.circle(surface, PURPLE, (int(x), int(y)), 20)
    dx = int(math.cos(angle) * 16)
    dy = int(math.sin(angle) * 16)
    pygame.draw.line(surface, WHITE, (int(x - dx), int(y - dy)), (int(x + dx), int(y + dy)), 3)
    pygame.draw.circle(surface, WHITE, (int(x), int(y)), 5)


def reset_animation():
    global animation_time, speed, paused
    animation_time = 0.0
    speed = 1.0
    paused = False


def save_desktop_screenshot(screen):
    global screenshot_count
    if IS_WEB:
        return None
    screenshot_count += 1
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidencias")
    os.makedirs(folder, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"captura_{screenshot_count:02d}_{stamp}.png"
    path = os.path.join(folder, filename)
    pygame.image.save(screen, path)
    return filename


async def main():
    global paused, speed, animation_time

    pygame.init()
    pygame.display.set_caption("Actividad 5.3 - Animación 2D en Python")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("arial", 30, bold=True)
    font_sub = pygame.font.SysFont("arial", 20, bold=True)
    font_text = pygame.font.SysFont("arial", 17)
    font_small = pygame.font.SysFont("arial", 14)

    running = True
    flash_message = ""
    flash_timer = 0.0

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    reset_animation()
                    flash_message = "Animación reiniciada"
                    flash_timer = 2.0
                elif event.key == pygame.K_s:
                    filename = save_desktop_screenshot(screen)
                    flash_message = f"Captura guardada: {filename}" if filename else "Captura disponible en escritorio"
                    flash_timer = 3.0
                elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                    speed = min(3.0, speed + 0.25)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed = max(0.25, speed - 0.25)

        if not paused:
            animation_time += dt * speed

        if flash_timer > 0:
            flash_timer -= dt

        screen.fill(SKY)
        pygame.draw.rect(screen, SKY2, (0, 0, SCENE_W, 190))

        sun_x, sun_y = 105, 100
        sun_pulse = 34 + 3 * math.sin(animation_time * 2.2)
        pygame.draw.circle(screen, YELLOW, (sun_x, sun_y), int(sun_pulse))
        ray_angle = animation_time * 0.8
        for i in range(12):
            angle = ray_angle + i * math.pi / 6
            x1 = sun_x + math.cos(angle) * 48
            y1 = sun_y + math.sin(angle) * 48
            x2 = sun_x + math.cos(angle) * 62
            y2 = sun_y + math.sin(angle) * 62
            pygame.draw.line(screen, ORANGE, (x1, y1), (x2, y2), 4)

        cloud1_x = (90 + animation_time * 28) % (SCENE_W + 180) - 120
        cloud2_x = (510 + animation_time * 18) % (SCENE_W + 220) - 140
        draw_cloud(screen, cloud1_x, 100, 0.85)
        draw_cloud(screen, cloud2_x, 165, 0.65)

        pygame.draw.rect(screen, (121, 199, 104), (0, 360, SCENE_W, 190))
        draw_house(screen, 150, 320, (242, 188, 118))
        draw_house(screen, 340, 330, (237, 167, 185))
        draw_house(screen, 550, 315, (154, 198, 225))
        draw_tree(screen, 90, 375)
        draw_tree(screen, 750, 372)

        ball_x = 640 + 60 * math.sin(animation_time * 0.9)
        ball_y = 455 - abs(math.sin(animation_time * 2.2)) * 95
        draw_ball(screen, ball_x, ball_y, animation_time * 5)

        pygame.draw.rect(screen, ROAD, (0, 550, SCENE_W, 170))
        for x in range(-40, SCENE_W + 80, 120):
            offset = int((animation_time * 120) % 120)
            pygame.draw.rect(screen, ROAD_LINE, (x + offset, 628, 62, 8), border_radius=4)

        car_x = ((animation_time * 150) % (SCENE_W + 180)) - 160
        car_y = 584 + 4 * math.sin(animation_time * 5)
        draw_car(screen, car_x, car_y)

        pygame.draw.rect(screen, PANEL, (PANEL_X, 0, WIDTH - PANEL_X, HEIGHT))
        pygame.draw.line(screen, PANEL_BORDER, (PANEL_X, 0), (PANEL_X, HEIGHT), 2)

        draw_text(screen, "ACTIVIDAD 5.3", font_title, DARK, (935, 35))
        draw_text(screen, "Animación 2D", font_sub, BLUE, (935, 78))
        draw_text(screen, "Alumno:", font_small, DARK, (935, 108))
        draw_text(screen, "Amaury Jahaziel", font_small, GRAY, (935, 126))
        draw_text(screen, "Gordillo Hernandez", font_small, GRAY, (935, 144))
        pygame.draw.line(screen, PANEL_BORDER, (930, 168), (1170, 168), 1)

        draw_text(screen, "Configuración", font_sub, DARK, (935, 180))
        config = [
            "Software: Python + Pygame",
            f"Resolución: {WIDTH} x {HEIGHT}",
            f"FPS objetivo: {FPS}",
            f"FPS actual: {clock.get_fps():.1f}",
            f"Velocidad: {speed:.2f}x",
            f"Tiempo: {animation_time:.1f} s",
            f"Estado: {'PAUSADO' if paused else 'REPRODUCIENDO'}",
        ]
        y = 214
        for line in config:
            draw_text(screen, line, font_text, DARK, (935, y))
            y += 26

        pygame.draw.line(screen, PANEL_BORDER, (930, 405), (1170, 405), 1)
        draw_text(screen, "Elementos animados", font_sub, DARK, (935, 420))

        items = [
            "• Auto: traslación",
            "• Nubes: desplazamiento",
            "• Pelota: salto + rotación",
            "• Sol: pulso + giro",
            "• Carretera: efecto de movimiento",
        ]
        y = 454
        for line in items:
            draw_text(screen, line, font_text, DARK, (935, y))
            y += 23

        pygame.draw.line(screen, PANEL_BORDER, (930, 575), (1170, 575), 1)
        draw_text(screen, "Controles", font_sub, DARK, (935, 590))
        draw_text(screen, "ESPACIO: pausa   R: reiniciar", font_small, DARK, (935, 620))
        draw_text(screen, "+ / -: velocidad   ESC: salir", font_small, DARK, (935, 645))
        draw_text(screen, "S: captura (escritorio)", font_small, DARK, (935, 670))

        if flash_timer > 0:
            box = pygame.Rect(200, 20, 510, 45)
            pygame.draw.rect(screen, (35, 41, 50), box, border_radius=12)
            draw_text(screen, flash_message, font_text, WHITE, (220, 33))

        pygame.display.flip()
        await asyncio.sleep(0)


asyncio.run(main())
