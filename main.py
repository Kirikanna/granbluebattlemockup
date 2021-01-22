import random


# define the Character class

class Character(object):
    def __init__(self, name, hp, attack, defense, chargecap, status, command, position):
        self.name = name
        self.hp = hp
        self.currenthp = self.hp
        self.attack = attack
        self.defense = defense
        self.chargecap = chargecap
        self.currentcharge = 0
        self.status = status
        self.command = command
        self.position = position
        self.targeting = 1
        self.chargeattackused = False
        self.skill = []

    def __bool__(self):
        if "KO" in self.status:
            return False
        return True

    def __str__(self):
        return self.name

    def getstats(self):
        return f"{self.name}: HP {self.currenthp}/{self.hp}, Attack {self.attack} " \
               f"Defense {self.defense}, Charge {self.currentcharge}/{self.chargecap}, " \
               f"Status {self.status}"


# define the Enemy class
class Enemy(object):
    def __init__(self, name, hp, attack, defense, status, command, eposition, cooldown):
        self.name = name
        self.hp = hp
        self.currenthp = hp
        self.attack = attack
        self.defense = defense
        self.status = status
        self.command = command
        self.eposition = eposition
        self.cooldown = cooldown
        self.turnsleft = cooldown
        self.skill = []

    def __bool__(self):
        if "KO" in self.status:
            return False

    def __str__(self):
        return self.name

    def getstats(self):
        return f"{self.name}: HP {self.currenthp}/{self.hp}, Attack {self.attack} " \
               f"Defense {self.defense}, Status {self.status}, Turns before using Skill: {self.turnsleft}"


# define skills
class Skills(object):
    def __init__(self, name, power, cooldown, effects, targets):
        self.name = name
        self.power = power
        self.cooldown = cooldown
        self.turnsleft = 0
        self.effects = effects
        self.targets = targets

    def getskillinfo(self):
        return f"{self.name} | Power {self.power} | Cooldown {self.turnsleft} " \
               f" | Effects {self.effects}" \
               f"| Targets: {targettype[self.targets]}"


# define skills
class EnemySkills(object):
    def __init__(self, name, power, effects, targets):
        self.name = name
        self.power = power
        self.effects = effects
        self.targets = targets


# battle variables


# characters
# Character(name, maxhp, attack, defense, chargecap, currentcharge
Megu = Character("Megu", 20, 5, 0, 100, [], "", 1)
Bonk = Skills("Bonk", 20, 5, [], 1)
Bonks = Skills("Bonks", 20, 5, [], 2)
Bonkss = Skills("Bonkss", 20, 5, [], 1)
Megu.skill.append(Bonk)
Megu.skill.append(Bonks)
Megu.skill.append(Bonkss)
Tomoka = Character("Tomoka", 30, 10, 0, 100, [], "", 2)

# Enemy
# Enemy(name, maxhp, attack, defense, chargecap, currentcharge
Dummy = Enemy("Dummy", 200, 2, 1, [], "1", 1, 3)
LumberingStrike = EnemySkills("Lumber Strike", 20, [], 1)
Dummy.skill.append(LumberingStrike)
Dummy1 = Enemy("Dummy1", 30, 2, 1, [], "1", 2, 2)
LumberingStrike2 = EnemySkills("Lumber Strikes", 20, [], 1)
Dummy1.skill.append(LumberingStrike2)
Dummy2 = Enemy("Dummy2", 30, 2, 1, [], "1", 3, 4)
LumberingStrike3 = EnemySkills("Lumber Strikess", 20, [], 1)
Dummy2.skill.append(LumberingStrike3)

battle = False

premadeparty = [Megu, Tomoka]
party = premadeparty
numberko = 0
enemyparty = [Dummy, Dummy1, Dummy2]
attackordefend = {0: "doing nothing", 1: "attacking", 2: "defending", 3: "skill", 4: "execute action"}
targettype = {0: "self", 1: "one enemy", 2: "all enemies", 3: "one ally", 4: "whole party", 5: "random enemy"
    , 6: "random ally"}
tar = 0
chargeattacks = 0


def battleturn(partybattle, enemybattle):
    displaypartystats()
    displayenemystats()
    partytarget = playertarget()
    girlcommand()
    enemysizecheck = len(enemyparty)
    print()
    for girls in enemybattle:
        print(girls.getstats())

    for girls in partybattle:
        print(f"{girls.name} is {attackordefend.get(girls.command)}")
        girlattack(girls, partytarget)
        if enemysizecheck > len(enemyparty):
            enemysizecheck = len(enemyparty)
            partytarget = 0
            print(f"Targeted enemy defeated. Retargeting {enemyparty[partytarget].name} this turn.")

    chainburstcheck()
    checkifenemydead()

    for enemies in enemybattle:
        enemyattack(enemies)

    skillrecovercooldown()
    skillrecovercooldownenemy()

    return checkbattlefinish(battle)


def checkbattlefinish(battledone):
    if battledone is True:
        print("Battle has finished.")
        return exit()
    else:
        battleturn(party, enemyparty)


def displaypartystats():
    print("Party Status")
    for girls in party:
        print(girls.getstats())


def displayenemystats():
    print("Enemy status")
    position = 0
    for enemies in enemyparty:
        position = position + 1
        print(f"{position} {enemies.getstats()}")


def playertarget():
    targetget = 0
    print("Who are you targeting?")
    while targetget < 1 or targetget > len(enemyparty):
        try:
            targetget = int(input())
        except ValueError:
            print("Enter a number please.")
    targetget = targetget - 1
    print(f"Targeting {enemyparty[targetget].name} this turn.")
    return targetget

def girlcommand():
    command = ""
    for girls in party:
        if "KO" not in girls.status:
            print(girls.getstats())
            print(f"Command for {girls.name}?")
            while command != 1 and command != 2:
                try:
                    command = int(input("1 to attack, 2 to defend, 3 for skill list\n"))
                    if command == 3:
                        skilllist(girls)
                except ValueError:
                    print("Enter a number please.")
            girls.command = command
            command = ""
        else:
            girls.command = 0
            print(f"{girls.name} is unable to act!")
    return 0


def skilllist(girls):
    command = 0
    numberofskills = len(girls.skill)
    print(f"{girls.name}'s skills")
    while command > 0 or command <= numberofskills:
        position = 0
        for skills in girls.skill:
            position = position + 1
            print(f"{position} {skills.getskillinfo()}")
        command = int(input("Use which skill?"))
        if command > numberofskills:
            print("Going back to commands.")
            break
        if girls.skill[command - 1].turnsleft > 0:
            print(
                f"{girls.name}'s {girls.skill[command - 1].name} is on cooldown for {girls.skill[command - 1].turnsleft}"
                f" turns.")
        else:
            print(f"Using {girls.name}'s {girls.skill[command - 1].name}")
            girls.skill[command - 1].turnsleft = girls.skill[command - 1].turnsleft + girls.skill[command - 1].cooldown


def skillrecovercooldown():
    i = 0
    for girls in party:
        for skills in girls.skill:
            if girls.skill[i].turnsleft > 0:
                girls.skill[i].turnsleft = girls.skill[i].turnsleft - 1
            i = i + 1


def skillrecovercooldownenemy():
    for enemy in enemyparty:
        if enemy.turnsleft > 0:
            enemy.turnsleft = enemy.turnsleft - 1

def setchargebarzero(girls):
     girls.currentcharge = 0

def damagecalc(attacker, defender):
    result = attacker.attack - defender.defense
    return result

def damageresult(defender,finaldamage):
    if finaldamage <= 0:
        print(f"{defender.name} does not take any damage.")
    else:
        defender.currenthp = defender.currenthp - finaldamage
        print(f"{defender.name} takes {finaldamage} damage!")


def girlattack(girls, partystarget):
    targetposition = 0
    for target in enemyparty:
        if girls.command == 1 and partystarget == targetposition:
            if girls.currentcharge == girls.chargecap:
                #Sets flag for chain burst
                girls.chargeattackused = True

                print(f"{girls.name} uses a charge attack!")
                damage = (girls.attack * 3)
                setchargebarzero(girls)
            else:
                print(f"{girls.name} attacks {target.name}!")
                girls.currentcharge = girls.currentcharge + 20
                if girls.currentcharge > girls.chargecap: girls.currentcharge = girls.chargecap
                damage = damagecalc(girls, target)
            damageresult(target, damage)
            checkifenemydead()
        targetposition = targetposition + 1



def checkifenemydead():
    for enemy in enemyparty:
        if enemy.currenthp <= 0:
            enemy.status.append("KO")
        while "KO" in enemy.status:
            for enemy in enemyparty:
                if "KO" in enemy.status:
                    print(f"{enemy.name} has been defeated.")
                    enemyparty.remove(enemy)
                if not enemyparty:
                    print("VICTORY!")
                    checkbattlefinish(True)


def chainburstcheck():
    bonusdamage = 0
    chargeattacksthisturn = 0
    for girls in party:
        if girls.chargeattackused:
            bonusdamage = bonusdamage + girls.attack
            chargeattacksthisturn = chargeattacksthisturn + 1
            girls.chargeattackused = False
    if chargeattacksthisturn > 1:
        print("More than one charge attack this turn! Bonus damage!")
        bonusdamage = bonusdamage * chargeattacksthisturn
        for targets in enemyparty:
            damageresult(targets, bonusdamage)
        checkifenemydead()


def enemyattack(enemy):
    i = 0
    pttarget = random.choice(party)
    while (bool(pttarget)) is False:
        pttarget = random.choice(party)

    pttarget = str(pttarget)
    for girls in party:
        if pttarget == girls.name:
            if enemy.turnsleft == 0:
                print(f"{enemy.name} uses a skill!")
                # skill effects here
                enemy.turnsleft = enemy.turnsleft + enemy.cooldown
            else:
                print(f"{enemy.name} attacks {girls.name}!")
                damage = damagecalc(enemy, girls)
                if girls.command == 2:
                    damage = round(damage / 2)
                    print("Damage partially blocked!")
                if damage < 0: damage = 0
                damageresult(girls, damage)
                checkifpartydefeat()
                i = i + 1


def checkifpartydefeat():
    koedcount = 0
    for girls in party:
        if girls.currenthp <= 0 and "KO" not in girls.status:
            girls.status.append("KO")
            girls.currenthp = 0
            print(f"{girls.name} was knocked out.")
        if "KO" in girls.status: koedcount = koedcount + 1
        if koedcount >= len(party):
            print("Defeat...")
            checkbattlefinish(True)


battleturn(party, enemyparty)
