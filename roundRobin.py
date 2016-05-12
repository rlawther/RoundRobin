class RoundRobin:

    def __init__(self, numTeams):
        self.numTeams = numTeams

    def createYetToPlayDict(self, numTeams):
        yetToPlay = {}

        for i in range(1, numTeams + 1):
            yetToPlay[i] = range(1, numTeams + 1)
            yetToPlay[i].remove(i)

        return yetToPlay

    def readFixedDraw(self, filename):
        draw = []
        f = open(filename)
        for l in f.readlines():
            matchlist = []
            l = l.strip()
            if l.startswith('#'):
                continue
            if l == '':
                continue
            matches = l.split(',')
            for m in matches:
                m = m.strip()
                (home, away) = m.split('v')
                home = int(home.strip())
                away = int(away.strip())
                matchlist.append((home, away))
            draw.append(matchlist)

        print draw
        return draw

    def findOpponents(self, toPlayThisRound, toPlayThisTeam):
        opp = []
        for r in toPlayThisRound:
            if r in toPlayThisTeam:
                opp.append(r)

        return opp

    def createMatchupList(self, homeTeam, awayTeams):
        matchups = []
        for awayTeam in awayTeams:
            matchups.append((homeTeam, awayTeam))
        return matchups

    def selectMatchup(self, matchList, toPlay, yetToPlay):
        print "* Select matchup", matchList, toPlay, yetToPlay
        if self.foundValidRound:
            return
        if toPlay == []:
            self.foundValidRound = True
            self.validRound = matchList
            return
        homeTeam = toPlay[0]
        opponents = self.findOpponents(toPlay, yetToPlay[homeTeam])
        matchups = self.createMatchupList(homeTeam, opponents)
        print matchups
        for m in matchups:
            (home, away) = m
            print "Selecting", m
            mList = list(matchList)
            mList.append(m)
            tp = list(toPlay)
            tp.remove(home)
            tp.remove(away)
            self.selectMatchup(mList, tp, yetToPlay)
            if self.foundValidRound:
                break
            

    def matchlistToStrings(self, matchList):
        strings = []
        for (home, away) in matchList:
            strings.append('%d v %d' % (home, away))
        return strings

    def removeTeamsPlayed(self, matchlist, yetToPlay):
        for (home, away) in matchlist:
            yetToPlay[home].remove(away)
            yetToPlay[away].remove(home)

    def createRound(self, numTeams, yetToPlay):

        rnd = []
        toPlay = range(1, numTeams + 1)

        self.foundValidRound = False
        self.validRound = None
        self.selectMatchup([], toPlay, yetToPlay)

        if self.foundValidRound:
            self.removeTeamsPlayed(self.validRound, yetToPlay)
            return self.matchlistToStrings(self.validRound)
        else:
            print "**** Could not find valid round !!! ****"
            return []

    def roundRobinComplete(self, yetToPlay):
        complete = True
        for team in yetToPlay:
            if yetToPlay[team] != []:
                complete = False
        return complete

    def createRoundString(self, roundNum, rnd):
        return ("Round %d : " % roundNum) + ', '.join(rnd)

    def calc(self):
        yetToPlay = self.createYetToPlayDict(self.numTeams)
        print yetToPlay
        self.results = []
        fixedDraw = self.readFixedDraw('fixedDraw.txt')
        roundNum = 1
        for matchlist in fixedDraw:
            self.removeTeamsPlayed(matchlist, yetToPlay)
            res = self.createRoundString(roundNum, self.matchlistToStrings(matchlist))
            self.results.append("Fixed " + res)
            roundNum += 1
        while not self.roundRobinComplete(yetToPlay):
            rnd = self.createRound(self.numTeams, yetToPlay)
            res = self.createRoundString(roundNum, rnd)
            print res
            self.results.append(res)
            roundNum += 1

            print yetToPlay

    def printResults(self):
        print "** Results :"
        for r in self.results:
            print r

if __name__ == '__main__':

    rr = RoundRobin(numTeams=6)
    rr.calc()
    rr.printResults()

