class player:

    def __init__(self, name, bowlingTeam=False):
        self.captain = False
        self.keeper = False
        self.names = []
        self.bowlingTeam = bowlingTeam
        names = name.split()    #(c)  †  (c)†
        key = ['(c)', '(c)†', '†']
        self.captain = names.contains('(c)') or names.contains('(c)†')
        self.keeper = names.contains('†') or names.contains('(c)†')
        for name in names:
            if name not in key:
                self.names.append(name)

    def score(self, word):
        if word in self.names:
            return True

