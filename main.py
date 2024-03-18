from vector import *
from renderer import *

renderer = Renderer(800, 800)
running = True

while running:
    dt = renderer.main_loop()