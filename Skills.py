class Skills(object):
    def __init__(self, name, power, cooldown, effects, targets, numberofhits):
        self.name = name
        self.power = power
        self.cooldown = cooldown
        self.turnsleft = 0
        self.effects = effects
        self.targets = targets
        self.numberofhits = numberofhits
        self.targettype = {0: "self", 1: "one enemy", 2: "all enemies", 3: "one ally(heal)",
                      4: "whole party(heal)", 5: "random enemy",
                      6: "random ally", 7: "one enemy[multiple hits, carries over to other targets]"}

    def getskillinfo(self):
        return f"{self.name} | Power {self.power} | Cooldown {self.turnsleft} " \
               f" | Effects {self.effects}" \
               f"| Targets: {self.targettype.get(self.targets)}"

#SkillList
# Skills name, power, cooldown, effects, targets, numberofhits):
Bop = Skills("Bop (4x multiplier)", 4, 5, [], 1, 1)
Boppin = Skills("Boppin' (5x multiplier)", 5, 5, [], 2, 1)
Boppest = Skills("Boppest' (10x multiplier)", 10, 5, [], 3, 1)
HealAll = Skills("Heal All' (10x multiplier)", 20, 5, [], 4, 1)
Multibonk = Skills("Multibonk' (2x multiplier)", 2, 10, [], 7, 10)
MiserableMist = Skills("Miserable Mist", 0, 5, [1, 2], 1, 1)