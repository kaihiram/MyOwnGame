from random import randint, choice
from prettytable import PrettyTable


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    def choose_defence(self, heroes_list):
        random_hero = choice(heroes_list)
        self.__defence = random_hero.ability

    def attack(self, heroes_list):
        for hero in heroes_list:
            if hero.health > 0:
                if isinstance(hero, Berserk) and self.__defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    @property
    def defence(self):
        return self.__defence

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def apply_super_power(self, boss, heroes_list):
        pass

    def attack(self, boss):
        boss.health -= self.damage


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss, heroes_list):
        coeff = randint(2, 5)
        boss.health -= coeff * self.damage
        print(f'Warrior {self.name} hits critically {coeff * self.damage}.')


class Magic(Hero):
    def __init__(self, name, health, damage, boost_amount):
        super().__init__(name, health, damage, 'BOOST')
        self.boost_amount = boost_amount

    def apply_super_power(self, boss, heroes_list):
        for hero in heroes_list:
            if hero.health > 0:
                hero.damage += self.boost_amount
                print(f'Magic {self.name} boosts {hero.name} damage to {hero.damage}.')


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_DAMAGE')
        self.__blocked_damage = 0

    def apply_super_power(self, boss, heroes_list):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} damages to boss.')

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes_list):
        for hero in heroes_list:
            if hero.health > 0 and hero != self:
                hero.health += self.__heal_points


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'REVIVE')

    def apply_super_power(self, boss, heroes_list):
        # Witcher doesn't deal damage but may revive a fallen hero
        if self.health > 0:
            for hero in heroes_list:
                if hero.health <= 0:
                    print(f'Witcher {self.name} revives {hero.name}.')
                    hero.health = 100  # revive the hero with 100 health
                    self.health = 0  # Witcher dies
                    break


class Hacker(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'STEAL_HEALTH')

    def apply_super_power(self, boss, heroes_list):
        # Steal health from the boss and give it to a random hero
        if self.health > 0:
            stolen_health = randint(10, 30)
            boss.health -= stolen_health
            random_hero = choice(heroes_list)
            if random_hero.health > 0:
                random_hero.health += stolen_health
                print(f'Hacker {self.name} steals {stolen_health} health from the boss and gives it to {random_hero.name}.')


class Golem(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health * 2, damage // 2, 'TAKE_DAMAGE')

    def apply_super_power(self, boss, heroes_list):
        damage_taken = boss.damage // 5
        for hero in heroes_list:
            if hero.health > 0:
                hero.health -= damage_taken
                print(f'Golem {self.name} takes {damage_taken} damage from boss for {hero.name}.')


class Avrora(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'INVISIBLE')
        self.invisible_mode = False
        self.invisible_rounds = 0
        self.damage_returned = 0

    def apply_super_power(self, boss, heroes_list):
        if not self.invisible_mode:
            self.invisible_mode = True
            self.invisible_rounds = 2
            print(f'Avrora {self.name} goes invisible for 2 rounds.')
        elif self.invisible_rounds > 0:
            self.invisible_rounds -= 1
            print(f'Avrora {self.name} is still invisible. Rounds left: {self.invisible_rounds}.')
        else:
            self.invisible_mode = False
            print(f'Avrora {self.name} is now visible again.')

    def receive_damage(self, damage):
        if self.invisible_mode:
            self.damage_returned += damage
            return 0
        return damage


round_number = 0


def is_game_over(boss, heroes_list):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes_list:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def show_statistics(boss, heroes_list):
    boss_table = PrettyTable()
    boss_table.field_names = ["Entity", "Health", "Damage", "Ability"]
    boss_table.add_row(["BOSS", boss.health, boss.damage, boss.defence])

    heroes_table = PrettyTable()
    heroes_table.field_names = ["Entity", "Health", "Damage", "Ability"]

    for hero in heroes_list:
        heroes_table.add_row([hero.name, hero.health, hero.damage, hero.ability])

    print(f' ------------- ROUND {round_number} -------------')
    print(boss_table)
    print(heroes_table)


def play_round(boss, heroes_list):
    global round_number
    round_number += 1
    boss.choose_defence(heroes_list)
    boss.attack(heroes_list)
    for hero in heroes_list:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes_list)

    for hero in heroes_list:
        if isinstance(hero, Avrora):
            damage_to_boss = hero.damage_returned
            if damage_to_boss > 0:
                boss.health -= damage_to_boss
                print(f'Avrora {hero.name} returns {damage_to_boss} damage to the boss.')

    show_statistics(boss, heroes_list)


def start_game():
    boss = Boss(name='Minotavr', health=1200, damage=50)

    warrior_1 = Warrior(name='Asterix', health=290, damage=10)
    warrior_2 = Warrior(name='Obelix', health=280, damage=15)
    magic = Magic(name='Alice', health=270, damage=5, boost_amount=3)
    berserk = Berserk(name='Guts', health=220, damage=10)
    doc = Medic(name='Doc', health=200, damage=5, heal_points=15)
    assistant = Medic(name='Junior', health=300, damage=5, heal_points=5)
    witcher = Witcher(name='Witcher', health=250, damage=0)
    hacker = Hacker(name='Hacker', health=220, damage=8)
    golem = Golem(name='Golem', health=150, damage=10)
    avrora = Avrora(name='Avrora', health=180, damage=10)

    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant, witcher, hacker, golem, avrora]
    show_statistics(boss, heroes_list)

    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
