import Character

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


    def __str__(self):
        return self.name


    def getstats(self):
        return f"{self.name}: HP {self.currenthp}/{self.hp}, Attack {self.attack} " \
               f"Defense {self.defense}, Status {self.getstatus(self.status)}, Turns before using Skill: {self.turnsleft}"


    def getstatus(self, status):
        statusdisplay = []
        for whatstat in status:
            statusdisplay.append(whatstat.name)
        return statusdisplay

