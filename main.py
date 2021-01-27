import random
from Character import Character
from Enemy import Enemy

# define skills
class Skills(object):
    def __init__(self, name, power, cooldown, effects, targets, numberofhits):
        self.name = name
        self.power = power
        self.cooldown = cooldown
        self.turnsleft = 0
        self.effects = effects
        self.targets = targets
        self.numberofhits = numberofhits

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

class Status(object):
    def __init__(self, name):
        self.name = name
        self.effects = {}
        self.attackmodtier = \
            {"Rage" : 1.2,
            "Rage2" : 1.4,
            "Weakened" : 0.5}



# battle variables

# characters
# Character(name, maxhp, attack, defense, chargecap, status
Megu = Character("Megu", 5000, 15, 0, 100, [], "", 1)
Bop = Skills("Bop (4x multiplier)", 4, 5, [], 1, 1)
Boppin = Skills("Boppin' (5x multiplier)", 5, 5, [], 2, 1)
Boppest = Skills("Boppest' (10x multiplier)", 10, 5, [], 3, 1)
HealAll = Skills("Heal All' (10x multiplier)", 20, 5, [], 4, 1)
Multibonk = Skills("Multibonk' (2x multiplier)", 2, 10, [], 7, 10)
#Rage = Status("Rage")
#KnockOut = Status("KO")
Megu.skill.append(Bop)
Megu.skill.append(Boppin)
Megu.skill.append(Boppest)
Megu.skill.append(HealAll)
Megu.skill.append(Multibonk)
Tomoka = Character("Tomoka", 1000, 20, 0, 100, [], "", 2)


Tomoka.status.append("Poison")
Tomoka.status.append("Rage")
#Tomoka.status.append(Rage)



targettype = {0: "self", 1: "one enemy", 2: "all enemies", 3: "one ally(heal)",
              4: "whole party(heal)", 5: "random enemy",
              6: "random ally", 7: "one enemy[multiple hits, carries over to other targets]"}


# Enemy
# Enemy(name, maxhp, attack, defense, chargecap, currentcharge
Dummy = Enemy("Dummy", 200, 20, 20, [], "1", 1, 3)
LumberingStrike = EnemySkills("Lumber Strike", 50, [], 2)
Dummy.skill.append(LumberingStrike)
Dummy1 = Enemy("Dummy1", 30, 20, 1, [], "1", 2, 2)
LumberingStrike2 = EnemySkills("Lumber Strikes", 100, [], 1)
Dummy2 = Enemy("Dummy2", 30, 20, 1, [], "1", 3, 4)
LumberingStrike3 = EnemySkills("Lumber Strikess", 50, [], 1)
Dummy1.skill.append(LumberingStrike)
Dummy1.skill.append(LumberingStrike2)
Dummy1.skill.append(LumberingStrike3)
Dummy2.skill.append(LumberingStrike3)

Dummy2.status.append("Poison")
Dummy.status.append("Defense Break")
Dummy.status.append("Rage")
Dummy1.status.append("Defense Break")
battle = False

premadeparty = [Megu, Tomoka]
party = premadeparty
enemyparty = [Dummy, Dummy1, Dummy2]
chargeonoroff = {True: "On", False: "Off"}



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
        checkifpartydefeat()
    skillrecovercooldown()
    skillrecovercooldownenemy()

    procendofturnstatus()

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

def resultdisplay(display):
    result = {"Poison": "from poison"}
    return result


def girlauto():
    for girls in party:
        if "KO" in girls.status and girls.command != 0:
            girls.command = 0
        if girls.command == "":
            girls.command = 1
    print(messagedisplay(9))


def girlcommand():
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


def bluepotionuse():
    i = 0
    for girls in party:
        if girls.currenthp < girls.hp:
            print(f"Healing {girls.name}")
            healed = round((girls.hp / 2))
            girls.currenthp = girls.currenthp + healed
            if girls.currenthp >= girls.hp:
                girls.currenthp = girls.hp
                print(f"{girls.name} is fully healed!")
            if girls.currenthp < girls.hp:
                print(f"{girls.name} recovers {healed} HP!")
        i = i + 1


def potionuse():
    choice = ""
    healed = 0
    while choice.upper() != "C":
        try:
            displaypartystats()
            choice = input(f"Heal who with green potion? C to go back to previous selection\n")
            if choice.upper() == 'C':
                displaypartystats()
                break
            if len(party) >= int(choice) > 0:
                i = 0
                tochoose = int(choice) - 1
                for girls in party:
                    if "KO" in girls.status and i == tochoose:
                        print(f"{girls.name} is knocked out, cannot heal!")
                        potionuse()
                        break
                    if tochoose == i and girls.currenthp >= girls.hp:
                        print(f"{girls.name} is already healthy.")
                        break
                    if tochoose == i and girls.currenthp < girls.hp:
                        print(f"Healing {girls.name}")
                        healed = round((girls.hp / 2))
                        girls.currenthp = girls.currenthp + healed
                        if girls.currenthp >= girls.hp:
                            girls.currenthp = girls.hp
                            print(f"{girls.name} is fully healed!")
                        if girls.currenthp < girls.hp:
                            print(f"{girls.name} recovers {healed} HP!")
                    i = i + 1
            else:
                print("no.")
        except ValueError:
            if choice.upper() != 'C':
                print("Enter a number please.")


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


#Update damage calc
def singletargetdamageskill(girls, skill):
    command = 0
    position = 0
    for enemies in enemyparty:
        position = position + 1
        print(f"{position} {enemies.getstats()}")
    while int(command) > 0 or int(command) <= len(enemyparty):
        try:
            command = int(input("Who are you targeting?\n"))
            damage = damagecalc(girls.attack * skill.power, enemyparty[command-1].defense)
            damageresult(enemyparty[command-1], damage)
            checkifenemydead()
            break
        except ValueError:
            print("Enter a valid selection please.")


def singletargetmultihitskill(girls, skill):
    command = 0
    position = 0
    hits = 0
    for enemies in enemyparty:
        position = position + 1
        print(f"{position} {enemies.getstats()}")
    while int(command) > 0 or int(command) <= len(enemyparty):
        try:
            command = int(input("Who are you targeting?\n"))
            for hits in range(skill.numberofhits):
                hits = hits + 1
                damage = damagecalc(girls.attack * skill.power, enemyparty[command-1].defense)
                damageresult(enemyparty[command-1], damage)
                checkifenemydead()
                if int(command) > len(enemyparty):
                    command = 0
            break
        except ValueError:
            print("Enter a valid selection please.")

def alltargetdamageskill(girls, skill):
    damage = 0
    for enemies in enemyparty:
        damage = damagecalc(girls.attack * skill.power, enemies.defense)
        damageresult(enemies, damage)
    checkifenemydead()
    checkifenemydead()


def singletargethealskill(girlss, skill):
    command = 0
    position = 0
    for girls in party:
        position = position + 1
        print(f"{position} {girls.getstats()}")
    while command > 0 or command <= len(party):
        try:
            command = int(input("Who are you healing?\n"))
            if "KO" not in party[command-1].status:
                healresult(party[command-1], skill.power)
                break
            else:
                print("Invalid target.")
        except ValueError:
            print("Enter a valid selection please.")


def alltargethealskill(girl, skill):
    for girls in party:
        if "KO" not in girls.status:
            healresult(girls, skill.power)

def attackmods(attacker):
    damagemultiplier = 1
    for i in attacker.status:
        if attackmodtier.get(i) is not None:
            damagemultiplier = damagemultiplier * attackmodtier.get(i)
    return damagemultiplier

attackmodtier = {"Rage" : 1.2,
                 "Rage2" : 1.4,
                 "Weakened" : 0.5}

def defensemods(defender):
    defensemultiplier = 1
    for i in defender.status:
        if defensemodtier.get(i) is not None:
            defensemultiplier = defensemultiplier * defensemodtier.get(i)
    return defensemultiplier

defensemodtier = {"Defense Down" : 0.8,
                  "Defense Break" : 0.7,
                  "Bulky" : 1.5}

def procendofturnstatus():
    for girls in party:
        if "Poison" in girls.status:
            print(f"{girls.name} suffers from Poison!")
            damageresult(girls, 5)
    for enemys in enemyparty:
        if "Poison" in enemys.status:
            print(f"{enemys.name} suffers from Poison!")
            damageresult(enemys, 5)



skillcalc = {
    1: singletargetdamageskill,
    2: alltargetdamageskill,
    3: singletargethealskill,
    4: alltargethealskill,
    7: singletargetmultihitskill,
                }

def singletargetdamageskillenemy(attacker, skill):
    pttarget = checkifvalidenemytarget(random.choice(party))
    print(f"{attacker.name} targets {pttarget.name}!")
    damage = damagecalc(round(attacker.attack * skill.power * attackmods(attacker)),
                        round(pttarget.defense * defensemods(pttarget)))
    if pttarget.command == 2:
        damage = round(damage / 2)
        print("Damage partially blocked!")
    damageresult(pttarget, damage)
    checkifpartydefeat()
    checkifpartydefeat()


def alltargetdamageskillenemy(attacker, skill):
    for girls in party:
        damage = damagecalc(round(attacker.attack * skill.power * attackmods(attacker)),
                            round(girls.defense * defensemods(girls)))
        if "KO" not in girls.status:
            damageresult(girls, damage)
    checkifpartydefeat()
    checkifpartydefeat()


def executeenemyskill(attacker):
    skillpick = random.choice(attacker.skill)
    print(f"{attacker.name} is using {skillpick.name}, a {targettype[skillpick.targets]}!")
    enemyskillcalc[skillpick.targets](attacker, skillpick)


enemyskillcalc = {
    1: singletargetdamageskillenemy,
    2: alltargetdamageskillenemy
                }



def skilllist(girls):
    command = 0
    actualcommand = 0
    numberofskills = len(girls.skill)
    print(f"{girls.name}'s skills (any number not in skill list returns to command list")
    while command > 0 or command <= numberofskills:
        position = 0
        for skills in girls.skill:
            position = position + 1
            print(f"{position} {skills.getskillinfo()}")
        command = int(input(messagedisplay(8)))
        actualcommand = command - 1
        if command > numberofskills or command <= 0:
            print("Returning to command list.")
            break
        if girls.skill[actualcommand].turnsleft > 0:
            print(
                f"{girls.name}'s {girls.skill[actualcommand].name} is on cooldown for "
                f"{girls.skill[actualcommand].turnsleft}"
                f" turns.")
        else:
            print(f"Using {girls.name}'s {girls.skill[actualcommand].name}")
            skillcalc[girls.skill[command - 1].targets](girls, girls.skill[actualcommand])
            girls.skill[actualcommand].turnsleft = girls.skill[actualcommand].turnsleft + girls.skill[actualcommand].cooldown

def action():
    choice = ""
    target = 0
    while choice.upper() != "A" and choice != "C":
        try:
            choice = input("[A] to execute all queued actions, "
                           "[C] to choose commands manually, "
                           "[P] to use green potions, "
                           "[B] to use blue potion, "
                           "Input number to manually choose a target\n")
            if choice.upper() == 'A':
                girlauto()
                return target
            if choice.upper() == 'C':
                girlcommand()
                return target
            if choice.upper() == 'P':
                potionuse()
            if choice.upper() == 'B':
                bluepotionuse()
            if len(enemyparty) >= int(choice) > 0:
                totarget = int(choice) - 1
                target = totarget
                print(f"Targeting {enemyparty[target].name} this turn.")
        except ValueError:
            print("Enter a valid selection please.")


execute = {'A': girlauto,
           'C': girlcommand,
           'P': potionuse}


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


def damagecalc(attack, defend):
    result = attack - defend
    return result


def damageresult(defender, finaldamage):
    if finaldamage <= 0:
        print(f"{defender.name} does not take any damage.")
    else:
        defender.currenthp = defender.currenthp - finaldamage
        print(f"{defender.name} takes {finaldamage} damage!")


def healresult(healed, healamount):
    if healamount <= 0:
        print(f"{healed.name} does not take any damage.")
    else:
        healed.currenthp = healed.currenthp + healamount
        if healed.currenthp >= healed.hp:
            healed.currenthp = healed.hp
            print(f"{healed.name} is fully healed!")
        else:
            print(f"{healed.name} recovers {healamount} HP!")


def chargegain(gainer, chargeamount):
    gainer.currentcharge = gainer.currentcharge + chargeamount


def girlattack(girls, partystarget):
    targetposition = 0
    for target in enemyparty:
        if girls.command == 1 and partystarget == targetposition:
            if girls.currentcharge == girls.chargecap and girls.togglecharge is True:
                girls.chargeattackused = True
                print(f"{girls.name} uses a charge attack!")
                setchargebarzero(girls)
                damage = (girls.attack * 3)
            else:
                print(f"{girls.name} attacks {target.name}!")
                chargegain(girls, 20)
                if girls.currentcharge > girls.chargecap: girls.currentcharge = girls.chargecap
                damage = damagecalc(round(girls.attack*attackmods(girls)), round(target.defense*defensemods(target)))
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
    if enemy.turnsleft == 0:
        print(f"{enemy.name} uses a skill!")
        executeenemyskill(enemy)
        enemy.turnsleft = enemy.turnsleft + enemy.cooldown
    else:
        pttarget = checkifvalidenemytarget(random.choice(party))
        print(f"{enemy.name} attacks {pttarget.name}!")
        enemyexecute(enemy, pttarget)


def checkifvalidenemytarget(pttarget):
    while "KO" in pttarget.status:
        pttarget = random.choice(party)
    return pttarget


def enemyexecute(enemy, pttarget):
    damage = damagecalc(round(enemy.attack * attackmods(enemy)), round(pttarget.defense * defensemods(pttarget)))
    if pttarget.command == 2:
        damage = round(damage / 2)
        print("Damage partially blocked!")
    damageresult(pttarget, damage)


def checkifpartydefeat():
    for girls in party:
        if girls.currenthp <= 0 and "KO" not in girls.status:
            girls.status.clear()
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
