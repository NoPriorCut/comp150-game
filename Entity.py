import pygame
import random
import ImageFiles
import Helper
import EnemyAttacks
# Classes used by Entity type Objects


pygame.init()
'''
windowHeight = 150
windowWidth = 450

screen = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)
'''

enemy_list = []

class Entity:
    # index is used to keep track of entities
    entity_index = 0  # Declaration of static Index
    # Declaration of static alignment for all Entities
    entity_alignment = ('Aggressive', 'Passive', 'Friendly')
    defaultHealth = 100

    def __init__(self):
        # subname is a unique identifier that uses the index
        self.subname = 'Entity' + str(Entity.entity_index)
        name = 'Placeholder name'
        # Importing index into the Entity-specific variable
        self.index = Entity.entity_index

        # Incrementing the index of all entities
        Entity.entity_index += 1

        # defining where the entity is encountered (by default, nowhere)
        self.on_encounter = False
        self.on_battle = False

        # setting alignment to passive as a default
        self.alignment = Entity.entity_alignment[1]

        # To do: define states, as to specify what
        # images and animations to incorporate into lists


class Enemy(Entity):

    numberOfOnscreenEnemies = 0

    def __init__(self):
        Entity.__init__(self)
        self.on_battle = True
        self.alignment = Entity.entity_alignment[0]
        self.health = Entity.defaultHealth  # * (enemyLevel * 0.1)
        self.sprite = ImageFiles.images['Enemy']  # [random.randint(0, len(ImageFiles.images) - 1)]
        self.chance_to_attack = 1

        self.time_since_attack = pygame.time.get_ticks()

        self.attack_cooldown = random.randint(50, 200)

        self.max_attack_chance = 1000

        lane_is_occupied = True
        self.lane_key = 'middle'

        self.damage = 10

        while lane_is_occupied:
            self.lane_key = random.choice(list(Helper.LANES))
            lane_is_occupied = Helper.LANES[self.lane_key][1]

        Helper.LANES[self.lane_key][1] = True
        self.pos = [
                    Helper.LANES[self.lane_key][0][0] - int(self.sprite.get_width() / 2),
                    Helper.LANES[self.lane_key][0][1] - int(self.sprite.get_height() / 2)
                    ]
        Enemy.numberOfOnscreenEnemies += 1

    def is_hit(self, damage):
        self.health = self.health - damage
        # play_sound(enemy_hit)

    def enemy_update(self):

        attack = random.randint(1, self.max_attack_chance)
        if attack <= self.chance_to_attack and pygame.time.get_ticks() - self.time_since_attack > self.attack_cooldown:
            print('ATTACK on lane ' + self.lane_key)
            EnemyAttacks.enemy_attack_sprite(self.lane_key, self)

    def __del__(self):
        try:
            Helper.LANES[self.lane_key][1] = False
            Enemy.numberOfOnscreenEnemies -= 1
            del self
        except AttributeError:
            print('Thank you for playing Wing Commander!')



class EnemyBoss(Enemy):

    def __init__(self):
        Enemy.__init__(self)
