# define the Character class

class Character(object):
    def __init__(self, name, hp, attack, defense, chargecap):
        self.name = name
        self.hp = hp
        self.currenthp = self.hp
        self.attack = attack
        self.defense = defense
        self.chargecap = chargecap
        self.currentcharge = 0
        self.status = []
        self.statusdisplay = []
        self.command = ""
        self.position = 0
        self.targeting = 1
        self.chargeattackused = False
        self.skill = []
        self.togglecharge = True
        self.chargeonoroff = {True: "On", False: "Off"}

    def __bool__(self):
        if "KO" in self.status:
            return False
        return True

    def __str__(self):
        return self.name



    def getstats(self):
        return f"{self.name}: HP {self.currenthp}/{self.hp}, Attack {self.attack} " \
               f"Defense {self.defense}, Charge {self.currentcharge}/{self.chargecap}, " \
               f"Status {self.getstatus(self.status)}, Charge attack: {self.chargeonoroff.get(self.togglecharge)}"

    def getstatus(self, status):
        statusdisplay = []
        for whatstat in status:
            statusdisplay.append(whatstat.name + self.displayturns(whatstat.turnsleft))
        return statusdisplay

    def displayturns(self, turnsleft):
        if turnsleft == 0:
            return ""
        turnsleft = f" [{turnsleft} turns left]"
        return turnsleft

#Create Characters
# Character(name, maxhp, attack, defense, chargecap
Megu = Character("Megu", 99999, 15, 0, 100)
Tomoka = Character("Tomoka", 99999, 20, 0, 100)