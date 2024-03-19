from vector import Vector
from renderer import Renderer
import pygame

i = Vector(1, 0)
j = Vector(0, 1)

renderer = Renderer(800, 900)
running = True

class TowerData:
    def __init__(self, renderer:Renderer):
        self.towers = {}

        with open("data/towers.txt", "r") as tower_data:
            raw = tower_data.readlines()[1:]

        # Save data
        for tower in raw:
            data   = tower.strip("\n").split(" ")
            name   = data[0]
            cost   = int(data[1])
            range  = float(data[2])
            damage = float(data[3])
            delay  = int(data[4])

            self.towers[name] = (cost, range, damage, delay)
            renderer.load_asset(name, 160)

class Tower:
    def __init__(self, name, location:Vector, tower_data:TowerData):
        self.name = name
        self.location = location

        # Load data from towerdata
        self.cost, self.range, self.damage, self.delay = tower_data.towers[name]
        self.rotation = 180
        self.cooldown = self.delay

        self.level = 1
        self.kills = 0
        self.temp_kills = 0
        self.kill_thresh = 2

    def level_up(self):
        if self.level < 10:
            self.level += 1
            self.delay *= 0.9
            self.cost *= 1.2
            self.damage *= 1.1

    def target(self, enemies:list, dt:float):

        if self.temp_kills >= self.kill_thresh:
            self.temp_kills = 0
            self.kill_thresh *= 2
            # Level up
            self.level_up()

        self.cooldown -= dt
        target = None
        count = 0

        for enemy in enemies:
            target_vector = enemy.position.subtract(self.location)
            if target_vector.magnitude <= self.range:
                target = enemy
                count += 1
                if (self.name != "sniper" or count > 1): break

        if target != None:
            self.rotation = target_vector.direction + 180
            if self.cooldown <= 0:
                self.cooldown = self.delay
                target.health -= self.damage
                if target.health <= 0:
                    self.kills += 1
                    self.temp_kills += 1
        return target

class EnemyData:
    def __init__(self, renderer:Renderer):
        self.enemies = {}

        with open("data/enemies.txt", "r") as enemy_data:
            raw = enemy_data.readlines()[1:]

        # Save data
        for enemy in raw:
            data   = enemy.strip("\n").split(" ")
            name   = data[0]
            health = int(data[1])
            speed  = int(data[2])

            self.enemies[name] = (health, speed)
            renderer.load_asset(name, 160)

class Enemy:
    def __init__(self, name:str, enemy_data:EnemyData):
        self.name = name
        self.health, self.speed = enemy_data.enemies[name]
        self.max_health = self.health
        self.position = Vector(1, -1)
        self.next_checkpoint = 0

    def move(self, dt:float, path_squares:list)-> bool:
        scalar = dt * 0.0005
        movement = Vector.component_from_tuple(path_squares[self.next_checkpoint]).subtract(self.position).normalize().multiply(self.speed * scalar)
        if Vector.component_from_tuple(path_squares[self.next_checkpoint]).subtract(self.position).magnitude > 0.01:
            self.position = self.position.add(movement)
        else:
            self.next_checkpoint += 1
            if self.next_checkpoint == len(path_squares):
                return True
        if self.health <= 0:
            return True
        return False
        
# Load background into renderer
renderer.load_asset("map", 800)
tower_data = TowerData(renderer)
enemy_data = EnemyData(renderer)
selection = Vector(0, 0)

money = 25

path_squares = [(1,0),(1,1),(2,1),(3,1),(3,2),(3,3),(2,3),(1,3),(1,4),(1,5)]

towers = [Tower("blaster", Vector(1,2), tower_data)]
enemies = []

countdown = 0
enemy_cooldown = 5000

while running:
    dt, events = renderer.main_loop()
    countdown -= dt
    if countdown <= 0:
        countdown = enemy_cooldown
        enemy_cooldown *= 0.9
        if enemy_cooldown < 500: enemy_cooldown = 500
        enemies.append(Enemy("red", enemy_data))
    running = events.continue_looping()
    if events.keydown(pygame.K_UP):
        selection = selection.subtract(j)
    if events.keydown(pygame.K_DOWN):
        selection = selection.add(j)
    if events.keydown(pygame.K_RIGHT):
        selection = selection.add(i)
    if events.keydown(pygame.K_LEFT):
        selection = selection.subtract(i)
    if events.keydown(pygame.K_2) and selection.get_position() not in path_squares:
        if money >= tower_data.towers["blaster"][0]:
            money -= tower_data.towers["blaster"][0]
            towers.append(Tower("blaster", selection, tower_data))
    if events.keydown(pygame.K_1) and selection.get_position() not in path_squares:
        if money >= tower_data.towers["turret"][0]:
            money -= tower_data.towers["turret"][0]
            towers.append(Tower("turret", selection, tower_data))
    if events.keydown(pygame.K_3) and selection.get_position() not in path_squares:
        if money >= tower_data.towers["machine"][0]:
            money -= tower_data.towers["machine"][0]
            towers.append(Tower("machine", selection, tower_data))
    if events.keydown(pygame.K_4) and selection.get_position() not in path_squares:
        if money >= tower_data.towers["sniper"][0]:
            money -= tower_data.towers["sniper"][0]
            towers.append(Tower("sniper", selection, tower_data))
    if events.keydown(pygame.K_SPACE):
        for tower in towers:
            if tower.location.get_position() == selection.get_position():
                if money >= tower.cost:
                    money -= tower.cost
                    tower.level_up()
    if events.keydown(pygame.K_BACKSPACE):
        for tower in towers:
            if tower.location.get_position() == selection.get_position():
                money += tower.cost
                towers.remove(tower)

    renderer.draw_bg("map")

    dead_enemies = []

    for tower in towers: 
        x, y = tower.location.multiply(160).get_position()
        target = tower.target(enemies, dt)
        if target != None and tower.name == "sniper":
            renderer.draw_line(tower.location.add(Vector(0.5,0.5)), target.position.add(Vector(0.5,0.5)), 160, (255, 0, 0))
        renderer.draw_tower(tower, 160, rotation = tower.rotation)
        renderer.draw_text(str(tower.level), x, y, (219, 172, 52))
        if selection.get_position() == tower.location.get_position(): 
            renderer.draw_text("UPGRADE: $%s" % round(tower.cost), 350, 10, (255, 255, 255))
        
    for enemy in enemies[::-1]: 
        dead = enemy.move(dt, path_squares)
        renderer.draw_enemy(enemy, 160)
        if dead: dead_enemies.append(enemy)

        renderer.draw_rect(enemy.position.multiply(160).subtract(Vector(0, 40)), Vector(160, 20), (255, 0, 0))
        renderer.draw_rect(enemy.position.multiply(160).subtract(Vector(0, 40)), Vector((enemy.health / enemy.max_health) * 160, 20), (0, 255, 0))

    renderer.draw_rect(Vector(0, 800), Vector(800,100), (105, 176, 205))

    renderer.selection_square(selection, 160)
    money = int(money)
    renderer.draw_text("YOU HAVE $%s" % money, 400, 830, (219, 172, 52))

    x_pos = -80
    for tower in tower_data.towers.keys():
        x_pos += 90
        renderer.draw_rotated(renderer.thumbnails[tower], (x_pos, 850), 0)
        renderer.draw_text("$%s" % tower_data.towers[tower][0], x_pos, 800, (0, 0, 0))

    renderer.update_screen()

    # Clean up
    for enemy in dead_enemies: 
        money += 10000#int(enemy.max_health / 2)
        enemies.remove(enemy)

renderer.quit()