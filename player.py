class player:

    def __init__(self, name, bowlingTeam=False):
        self.captain = False
        self.keeper = False
        self.names = []
        self.bowlingTeam = bowlingTeam
        names = name.split()    #(c)  †  (c)†
        key = ['(c)', '(c)†', '†']
        self.captain = '(c)' in names or '(c)†' in names
        self.keeper = '†' in names or '(c)†' in names
        for name in names:
            if name not in key:
                self.names.append(name)

    def score(self, words):
        score = 0
        for word in words:
            if word in self.names:  #simple, consider with similarity
                score = score + 1
        return score

    def printout(self):
        print(' '.join(self.names), self.bowlingTeam)