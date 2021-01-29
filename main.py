import Character
import Enemy
import EnemySkills
import Skills
import Status

import random

# battle variables

Character.Megu.skill.append(Skills.Bop)
Character.Megu.skill.append(Skills.Boppin)
Character.Megu.skill.append(Skills.Boppest)
Character.Megu.skill.append(Skills.HealAll)
Character.Megu.skill.append(Skills.Multibonk)
Character.Tomoka.status.append(Status.Rage)
Character.Tomoka.status.append(Status.Poison)
Character.Tomoka.skill.append(Skills.MiserableMist)
premadeparty = [Character.Megu, Character.Tomoka]
party = premadeparty

Enemy.Dummy.skill.append(EnemySkills.LumberingStrike)
Enemy.Dummy1.skill.append(EnemySkills.LumberingStrike)
Enemy.Dummy1.skill.append(EnemySkills.LumberingStrike2)
Enemy.Dummy1.skill.append(EnemySkills.LumberingStrike3)
Enemy.Dummy2.skill.append(EnemySkills.LumberingStrike3)
Enemy.Dummy.status.append(Status.DefenseBreak)
enemyparty = [Enemy.Dummy, Enemy.Dummy1, Enemy.Dummy2]

battle = False
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
    statusturncountdown()
    enemystatusturncountdown()

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


def inflictstatus(skill, target):
    for status in skill.effects:
        if status == 1 and Status.DefenseBreak not in target.status:
            target.status.append(Status.DefenseBreak)
            print(f"Inflicted {target.name} with {Status.DefenseBreak.name}")
        if status == 2 and Status.AttackBreak not in target.status:
            target.status.append(Status.AttackBreak)
            print(f"Inflicted {target.name} with {Status.AttackBreak.name}")


def statusturncountdown():
    for girls in party:
        for status in girls.status:
            if Status.Knockout not in girls.status:
                status.turnsleft = status.turnsleft - 1
                removestatus(girls, status)


def enemystatusturncountdown():
    for enemies in enemyparty:
        for status in enemies.status:
            if Status.Knockout not in enemies.status:
                status.turnsleft = status.turnsleft - 1
                removestatus(enemies, status)


def removestatus(inflicted, thestatus):
    if thestatus.turnsleft <= 0:
        print(f"{inflicted.name}'s {thestatus.name} has subsided.")
        inflicted.status.remove(thestatus)


def displayenemystats():
    print("Enemy status")
    position = 0
    for enemies in enemyparty:
        position = position + 1
        print(f"{position} {enemies.getstats()}")


def actiondisplay(display):
    actions = {0: "doing nothing", 1: "attacking", 2: "defending", 3: "skill", 4: "execute action"}
    return actions.get(display)


def girlauto():
    for girls in party:
        if Status.Knockout in girls.status and girls.command != 0:
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
                    if Status.Knockout in girls.status and i == tochoose:
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
                    if Status.Knockout in girls.status and i == tochoose:
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


def singletargetdamageskill(attacker, skill):
    command = 0
    position = 0
    for enemies in enemyparty:
        position = position + 1
        print(f"{position} {enemies.getstats()}")
    while int(command) > 0 or int(command) <= len(enemyparty):
        try:
            command = int(input("Who are you targeting?\n"))
            skilltarget = enemyparty[command-1]
            damage = damagecalc(attacker.attack * skill.power, skilltarget.defense)
            damageresult(skilltarget, damage)
            inflictstatus(skill, skilltarget)
            checkifenemydead()
            break
        except ValueError:
            print("Enter a valid selection please.")


def singletargetmultihitskill(attacker, skill):
    command = 0
    position = 0
    for enemies in enemyparty:
        position = position + 1
        print(f"{position} {enemies.getstats()}")
    while int(command) > 0 or int(command) <= len(enemyparty):
        try:
            command = int(input("Who are you targeting?\n"))
            target = enemyparty[command-1]
            for hits in range(skill.numberofhits):
                damage = damagecalc(attacker.attack * skill.power, target.defense)
                damageresult(target, damage)
                checkifenemydead()
                if int(command) > len(enemyparty):
                    command = 0
            break
        except ValueError:
            print("Enter a valid selection please.")


def alltargetdamageskill(attacker, skill):
    for enemies in enemyparty:
        damage = damagecalc(attacker.attack * skill.power, enemies.defense)
        damageresult(enemies, damage)
        inflictstatus(skill, enemies)
    checkifenemydead()


def singletargethealskill(healer, skill):
    command = 0
    position = 0
    for girls in party:
        position = position + 1
        print(f"{position} {girls.getstats()}")
    while command > 0 or command <= len(party):
        try:
            command = int(input("Who are you healing?\n"))
            toheal = party[command - 1]
            if Status.Knockout not in toheal.status:
                healresult(toheal, skill.power * healer.attack)
                break
            else:
                print("Invalid target.")
        except ValueError:
            print("Enter a valid selection please.")


def alltargethealskill(healer, skill):
    for girls in party:
        if Status.Knockout not in girls.status:
            healresult(girls, skill.power * healer.power)


def attackmods(attacker):
    damagemultiplier = 1
    for mods in attacker.status:
        if mods.type == 1:
            damagemultiplier = damagemultiplier * mods.power
    return damagemultiplier


def defensemods(defender):
    defensemultiplier = 1
    for mods in defender.status:
        if mods.type == 2:
            defensemultiplier = defensemultiplier * mods.power
    return defensemultiplier


def procendofturnstatus():
    for girls in party:
        for effects in girls.status:
            if effects.type == 3:
                print(f"{girls.name} suffers from {effects.name}!")
                damageresult(girls, effects.power)
    for enemys in enemyparty:
        for effects in enemys.status:
            if effects.type == 3:
                print(f"{enemys.name} suffers from {effects.name}!")
                damageresult(enemys, effects.power)
                damageresult(enemys, effects.power)


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
    inflictstatus(skill, pttarget)
    checkifpartydefeat()
    checkifpartydefeat()


def alltargetdamageskillenemy(attacker, skill):
    for girls in party:
        damage = damagecalc(round(attacker.attack * skill.power * attackmods(attacker)),
                            round(girls.defense * defensemods(girls)))
        if Status.Knockout not in girls.status:
            damageresult(girls, damage)
            inflictstatus(skill, girls)
    checkifpartydefeat()
    checkifpartydefeat()


def executeenemyskill(attacker):
    skillpick = random.choice(attacker.skill)
    print(f"{attacker.name} is using {skillpick.name}!")
    enemyskillcalc[skillpick.targets](attacker, skillpick)


enemyskillcalc = {
    1: singletargetdamageskillenemy,
    2: alltargetdamageskillenemy
                }


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
        actualcommand = command - 1
        girlskilltouse = girls.skill[actualcommand]
        if command > numberofskills or command <= 0:
            print("Returning to command list.")
            break
        if girlskilltouse.turnsleft > 0:
            print(
                f"{girls.name}'s {girlskilltouse.name} is on cooldown for "
                f"{girlskilltouse.turnsleft}"
                f" turns.")
        else:
            print(f"Using {girls.name}'s {girlskilltouse.name}")
            skillcalc[girlskilltouse.targets](girls, girlskilltouse)
            girlskilltouse.turnsleft = girlskilltouse.turnsleft + girlskilltouse.cooldown


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
            if skills.turnsleft > 0:
                skills.turnsleft = skills.turnsleft - 1
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
            enemy.status.append(Status.Knockout)
    for enemy in enemyparty:
        if Status.Knockout in enemy.status:
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
    while Status.Knockout in pttarget.status:
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
        if girls.currenthp <= 0 and Status.Knockout not in girls.status:
            girls.status.clear()
            girls.status.append(Status.Knockout)
            girls.currenthp = 0
            print(f"{girls.name} was knocked out.")
            checkifwiped()


def checkifwiped():
    for girls in party:
        if Status.Knockout not in girls.status:
            checkbattlefinish(False)
    print(messagedisplay(6))
    checkbattlefinish(True)


battleturn(party, enemyparty)
