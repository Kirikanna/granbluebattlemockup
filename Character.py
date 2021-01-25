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
               f"Status {self.status}, Charge attack: {self.chargeonoroff.get(self.togglecharge)}"
