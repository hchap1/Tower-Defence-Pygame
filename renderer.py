import pygame, os
from vector import *

class Mouse:
    def __init__(self, position, buttons):
        self.position = Vector.component_from_tuple(position)
        self.left = buttons[0]
        self.right = buttons[2]

    def get_pressed(self, button = "left"):
        if button == "left" and self.left: return True
        elif button == "right" and self.right: return True
        else: return False

    def index_map(button:str)-> int:
        if button == "left":  return 0
        if button == "right": return 2

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
    
    def continue_looping(self)-> bool:
        for event in self.events:
            if event.type == pygame.QUIT:
                return False
        else: return True

class Renderer:
    def __init__(self, width:int, height:int):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), vsync=True)
        self.font = pygame.font.Font("freesansbold.ttf", 40)
        self.clock = pygame.time.Clock()
        self.assets = {}
        self.thumbnails = {}

    def draw_rotated(self, image, position, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = position).center)
        self.screen.blit(rotated_image, new_rect)

    def load_asset(self, asset:str, width:int):
        self.assets[asset] = pygame.image.load("assets/%s.png" % asset).convert_alpha()
        self.assets[asset] = pygame.transform.scale(self.assets[asset], (width, width))
        self.thumbnails[asset] = pygame.transform.scale(self.assets[asset], (40, 40))

    def clear_screen(self)-> float:
        self.screen.fill((255, 255, 255))
        dt = self.clock.tick(60)
        return dt

    def update_screen(self):
        pygame.display.update()
    
    def draw_text(self, text:str, x:int, y:int, colour:tuple):
        text = self.font.render(text, False, colour)
        self.screen.blit(text, (x, y))

    def main_loop(self)-> tuple:
        dt = self.clear_screen()
        self.draw_text("FPS: %s" % round(1000 / dt), 10, 10, (0, 0, 0))
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        events_obj = Events(events, keys, Mouse(pygame.mouse.get_pos(), mouse))
        return (dt, events_obj)

    def draw_bg(self, name:str):
        self.screen.blit(self.assets[name], (0, 0))

    def draw_tower(self, tower, scalar:int, rotation:float=0):
        if rotation == 0: self.screen.blit(self.assets[tower.name], tower.location.multiply(scalar).get_position())
        else: self.draw_rotated(self.assets[tower.name], tower.location.multiply(scalar).get_position(), rotation)

    def draw_enemy(self, enemy, scalar:int):
        self.screen.blit(self.assets[enemy.name], enemy.position.multiply(scalar).get_position())

    def selection_square(self, location:Vector, scalar:int):
        square = pygame.surface.Surface((scalar, scalar))
        square.fill((0, 0, 255))
        square.set_alpha(150)
        self.screen.blit(square, (location.multiply(scalar).get_position()))

    def draw_rect(self, position:Vector, size:Vector, colour:tuple):
        x, y = position.get_position()
        w, h = size.get_position()
        pygame.draw.rect(self.screen, colour, pygame.Rect(x, y, w, h))

    def draw_line(self, a:Vector, b:Vector, scalar:int, colour:tuple):
        pygame.draw.line(self.screen, colour, a.multiply(scalar).get_position(), b.multiply(scalar).get_position(), 5)

    def quit():
        pygame.quit()
