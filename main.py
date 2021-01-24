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
        self.togglecharge = True

    def __bool__(self):
        if "KO" in self.status:
            return False
        return True

    def __str__(self):
        return self.name

    def getstats(self):
        return f"{self.name}: HP {self.currenthp}/{self.hp}, Attack {self.attack} " \
               f"Defense {self.defense}, Charge {self.currentcharge}/{self.chargecap}, " \
               f"Status {self.status}, Charge attack: {chargeonoroff.get(self.togglecharge)}"


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
# Character(name, maxhp, attack, defense, chargecap, status
Megu = Character("Megu", 50, 5, 0, 100, [], "", 1)
Bonk = Skills("Bonk", 20, 5, [], 1)
Bonks = Skills("Bonks", 20, 5, [], 2)
Bonkss = Skills("Bonkss", 20, 5, [], 1)
Megu.skill.append(Bonk)
Megu.skill.append(Bonks)
Megu.skill.append(Bonkss)
Tomoka = Character("Tomoka", 10, 10, 0, 100, [], "", 2)

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
enemyparty = [Dummy, Dummy1, Dummy2]
chargeonoroff = {True: "On", False: "Off"}

#Placeholder for skills
targettype = {0: "self", 1: "one enemy", 2: "all enemies", 3: "one ally", 4: "whole party", 5: "random enemy"
    , 6: "random ally"}

tar = 0


def battleturn(partybattle, enemybattle):
    displaypartystats()
    displayenemystats()
    partytarget = action()
    enemysizecheck = len(enemyparty)
    print()

    for girls in partybattle:
        print(f"{girls.name} is {actiondisplay(girls.command)}")
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


def messagedisplay(message):
    battlemessage = {0: "Starting battle.",
                     1: "Turn start.",
                     2: "Who are you targeting?",
                     3: "Going back to commands.",
                     4: "More than one charge attack this turn! Bonus damage!",
                     5: "Battle has finished.",
                     6: "Defeat...",
                     7: "is definitely ready for a Charge Attack this turn!",
                     8: "Use which skill?",
                     9: "Everyone in the party that can fight will now attack."}
    return battlemessage.get(message)


def checkbattlefinish(battledone):
    if battledone is True:
        print(messagedisplay(5))
        return exit()
    else:
        battleturn(party, enemyparty)


def displaypartystats():
    i = 0
    print("Party Status")
    for girls in party:
        i = i + 1
        print(f"{i} {girls.getstats()}")



def displayenemystats():
    print("Enemy status")
    position = 0
    for enemies in enemyparty:
        position = position + 1
        print(f"{position} {enemies.getstats()}")

def actiondisplay(display):
    action = {0: "doing nothing", 1: "attacking", 2: "defending", 3: "skill", 4: "execute action"}
    return action.get(display)


def action():
    choice = ""
    target = 0
    while choice.upper() != "A" and choice != "C":
        try:
            choice = input("[A] to execute all queued actions, "
                           "[C] to choose commands manually, "
                           "Input number to manually choose a target\n")
            if choice.upper() == 'A':
                girlauto()
                return target
            if choice.upper() == 'C':
                girlcommand()
                return target
            if len(enemyparty) >= int(choice) > 0:
                totarget = int(choice) - 1
                target = totarget
                print(f"Targeting {enemyparty[target].name} this turn.")
        except ValueError:
            print("Enter a valid selection please.")


def girlauto():
    for girls in party:
        print(girls.command)
        if "KO" in girls.status and girls.command != 0:
            girls.command = 0
        if girls.command == "":
            girls.command = 1
    print(messagedisplay(9))


def girlcommand():
    command = ""
    choice = ""
    while choice.upper() != "C":
        try:
            displaypartystats()
            choice = input(f"Command who? C to go back to previous selection\n")
            if choice.upper() == 'C':
                displayenemystats()
                action()
                break
            if len(party) >= int(choice) > 0:
                i = 0
                tochoose = int(choice) - 1
                for girls in party:
                    if "KO" in girls.status and i == tochoose:
                        print(f"{girls.name} is unable to act!")
                        girlcommand()
                        break
                    if tochoose == i:
                        print(f"Making selection for {girls.name}")
                        girlcommandchoice(girls)
                    i = i + 1
                break
            else:
                print("no.")
        except ValueError:
            print("Enter a valid selection please.")
    return 0


def girlcommandchoice(girltocommand):
    command = ""
    print(girltocommand.getstats())
    print(f"Command for {girltocommand.name}?")
    if girltocommand.currentcharge == girltocommand.chargecap:
        print(f"{girltocommand.name} {messagedisplay(7)}")
    while command.upper() != 'C':
        try:
            command = input("1 to attack, 2 to defend, 3 for skill list, 4 to toggle charge attack\n"
                            "C to return to previous command\n")
            if command.upper() == 'C':
                girlcommand()
                break
            if int(command) == 1 or int(command) == 2:
                print(f"{girltocommand.name} will be {actiondisplay(int(command))}")
                girltocommand.command = int(command)
            if int(command) == 3:
                if len(girltocommand.skill) > 0:
                    skilllist(girltocommand)
                else:
                    print("No skills found.")
            if int(command) == 4:
                girltocommand.togglecharge = not girltocommand.togglecharge
                print(f"Charge attack set to {chargeonoroff.get(girltocommand.togglecharge)}")
                print(girltocommand.getstats())
        except ValueError:
            if command.upper() != 'C':
                print("Enter a number please.")



def skilllist(girls):
    command = 0
    numberofskills = len(girls.skill)
    print(f"{girls.name}'s skills (any number not in skill list returns to command list")
    while command > 0 or command <= numberofskills:
        position = 0
        for skills in girls.skill:
            position = position + 1
            print(f"{position} {skills.getskillinfo()}")
        command = int(input(messagedisplay(8)))
        if command > numberofskills or command <= 0:
            print("Returning to command list.")
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

def damageresult(defender, finaldamage):
    if finaldamage <= 0:
        print(f"{defender.name} does not take any damage.")
    else:
        defender.currenthp = defender.currenthp - finaldamage
        print(f"{defender.name} takes {finaldamage} damage!")

def chargegain(gainer, chargeamount):
    gainer.currentcharge = gainer.currentcharge + chargeamount


def girlattack(girls, partystarget):
    targetposition = 0
    for target in enemyparty:
        if girls.command == 1 and partystarget == targetposition:
            if girls.currentcharge == girls.chargecap and girls.togglecharge is True:
                #Sets flag for chain burst
                girls.chargeattackused = True
                print(f"{girls.name} uses a charge attack!")
                setchargebarzero(girls)
                damage = (girls.attack * 3)
            else:
                print(f"{girls.name} attacks {target.name}!")
                chargegain(girls, 20)
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
        print(messagedisplay(4))
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
    for girls in party:
        if girls.currenthp <= 0 and "KO" not in girls.status:
            girls.status.append("KO")
            girls.currenthp = 0
            print(f"{girls.name} was knocked out.")
    checkifwiped(girls)

def checkifwiped(girls):
    for girls in party:
        if "KO" not in girls.status:
            checkbattlefinish(False)
    print(messagedisplay(6))
    checkbattlefinish(True)


battleturn(party, enemyparty)
