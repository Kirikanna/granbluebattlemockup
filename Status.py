class Status(object):
    def __init__(self, name, power, type, turnsleft):
        self.name = name
        self.power = power
        self.type = type
        self.turnsleft = turnsleft

#Create status
Knockout = Status("KO", 0, 0, 0)
Rage = Status("Rage", 1.2, 1, 4)
Poison = Status("Poison", 5, 3, 4)
DefenseBreak = Status("Defense Break", 0.8, 2, 5)
DefenseBreak2 = Status("Defense Breaker", 0.5, 2, 5)
AttackBreak = Status("Attack Break", 0.9, 1, 4)