import pygame
from vector import *

class Mouse:
    def __init__(self, position, buttons):
        self.position = Vector.component_from_tuple(position)
        self.left = buttons[1]
        self.right = buttons[3]

    def get_pressed(self, button = "left"):
        if button == "left" and self.left: return True
        elif button == "right" and self.right: return True
        else: return False

    def index_map(button:str)-> int:
        if button == "left":  return 1
        if button == "right": return 3
        return 0

class Events:
    def __init__(self, events:tuple, keys:tuple, mouse:Mouse):
        self.events = events
        self.keys = keys
        self.mouse = mouse

    def keydown(self, keycode:int)-> bool:
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == keycode:
                    return True
        return False
    
    def buttondown(self, button:str)-> bool:
        index = self.mouse.index_map(button)
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == index: return True
        return False

    def get_key(self, keycode:int)-> bool:
        return self.keys[keycode]
    
    def get_button(self, button:str)-> bool:
        return self.mouse.get_pressed(button)

class Renderer:
    def __init__(self, width:int, height:int):
        self.screen = pygame.display.set_mode((width, height), vsync=True)
        self.font = pygame.font.Font("freesansbold.ttf", 25)
        self.clock = pygame.time.Clock()

    def clear_screen(self)-> int:
        self.screen.fill((255, 255, 255))
        dt = self.clock.tick(60)
        return dt

    def update_screen(self):
        pygame.display.update()
    
    def draw_text(self, text:str, x:int, y:int, colour:tuple):
        text = self.font.render(text, False, colour)
        self.screen.blit(text, (x, y))

    def main_loop(self)-> int:
        dt = self.clear_screen()
        self.draw_text("FPS: %s" % round(1000 / dt), 10, 10, (0, 0, 0))
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
