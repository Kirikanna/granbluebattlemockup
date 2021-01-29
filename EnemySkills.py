class EnemySkills(object):
    def __init__(self, name, power, effects, targets):
        self.name = name
        self.power = power
        self.effects = effects
        self.targets = targets

#Create Enemy Skills
#   EnemySKill(self, name, power, effects, targets)
LumberingStrike = EnemySkills("Lumber Strike", 50, [], 2)
LumberingStrike2 = EnemySkills("Lumber Strikes", 100, [], 1)
LumberingStrike3 = EnemySkills("Lumbering Mist", 50, [1, 2], 1)