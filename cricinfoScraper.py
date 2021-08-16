import os
import time
import unicodedata

from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import pandas
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


from player import player


def similarity(first, second):
    return SequenceMatcher(None, first, second).ratio()

class CricinfoScraper:
    def __init__(self, addressfile, maxNgramLength): #  give a file of web addresses to open
        self.addresses = open(addressfile, 'r').readlines()
        self.maxNgramLength = maxNgramLength    # allows n START tokens to be added at beginning to facilatate ngrams
        self.outcomeEmissions = {}  # dict of outcome: array of emissions
        self.outcomeSequence = []  # array of outcomes to use to do transition probabilities
        self.driver = webdriver.Chrome("C:/Users/sambe/chromedriver_win32/chromedriver.exe")
        self.cookieClickNeeded = True
        self.totalBalls = 0
        self.inningsBalls = 0
        # self.teamA = []
        # self.teamB = []  # current teams - updated for each new link
        self.players = []
        self.allNames = []



    def translateOutcome(self, outcome):
        translations = {'FOUR runs':'4 runs', 'SIX runs':'6 runs', '(no ball) FOUR runs':'(no ball) 4 runs', '(no ball) SIX runs':'(no ball) 6 runs'}
        if outcome in translations:
            return translations[outcome]
        else:
            return outcome

    def extractOutcomeAndComment(self):
        self.inningsBalls = 0
        for i in range(self.maxNgramLength):
            self.outcomeSequence.append('START'+str(i))
        self.soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        for a in self.soup.findAll('div', attrs={'class': 'match-comment-wrapper'}):
            shortComment = a.contents[0].text
            self.inningsBalls = self.inningsBalls + 1
            if len(a.contents) < 2:
                longComment = ''        # rare case where there is no long comment div
            else:
                longComment = a.contents[1].text
            bowler, batter, outcome = self.extractBowlerBatterOutcome(shortComment)
            #bowler.printout()
            #batter.printout()
            outcome = self.translateOutcome(outcome)
            outcome = outcome.replace(' ', '_')
            #cleanedComment = self.cleanBowlerBatter(longComment, bowler, batter, handlePunctuation=False)  # v =-----
            cleanedComment = self.cleanBowlerBatterNew(longComment, bowler, batter)  # v =-----
            self.outcomeSequence.append(outcome)
            if outcome in self.outcomeEmissions:
                self.outcomeEmissions[outcome].append(cleanedComment)
            else:
                self.outcomeEmissions[outcome] = [cleanedComment]
        self.outcomeSequence.append('END')
        print('balls in innings :', self.inningsBalls)
        self.totalBalls = self.totalBalls + self.inningsBalls

    def createSequenceFiles(self):
        save_path = 'scrapedSequences/'
        address = os.getcwd()+'/scrapedSequences'
        for filename in os.listdir(address):
            with open(os.path.join(address, filename), 'w') as f:
                f.write('')

    def writeSequencesToFiles(self):
        save_path = 'scrapedSequences/'
        startSequence = ''
        endSequence = ' END'

        for i in range(self.maxNgramLength):
            startSequence = startSequence + 'START' + str(i) + ' '
        endAndStart = endSequence + ' ' + startSequence

        with open(save_path+'outcomes.txt', 'a') as f:
            f.write(' '.join(self.outcomeSequence) + ' ')

        for k in self.outcomeEmissions.keys():
            with open(save_path+k+'.txt', 'a') as f:
                f.write(startSequence)
                f.write(endAndStart.join(self.outcomeEmissions[k]) + endSequence)

    def extractBowlerBatterOutcome(self, shortComment):
        shortWords = shortComment.split()
        split = shortWords.index('to')
        end = len(shortWords)
        i = 0
        bowler = ' '.join(shortWords[0:split])
        batter = ''
        for word in shortWords:
            if word[-1] == ',':
                end = i
                batter = word[0:len(word) - 1]
                break
            i = i + 1
        outcome = ' '.join(shortWords[end + 1:len(shortWords)])
        bowlerP = self.findBestPlayerMatch(bowler.split())
        batterP = self.findBestPlayerMatch(batter.split())
        return bowlerP, batterP, outcome

    def cleanBowlerBatterNew(self, longComment, bowler, batter): # now bowler and batter are player objects
        longWords = nltk.word_tokenize(longComment)
        #print(longWords)
        cleanedWords = []
        buffer = []
        for word in longWords:
            if word in self.allNames:
                buffer.append(word)
            else:
                if len(buffer) > 0:
                    match = self.findBestPlayerMatch(buffer)
                    # find from match if bowler or batter, otherwise fielder (or non batting batter)
                    if match is None:
                        cleanedWords.append(buffer)
                    else:
                        if match == bowler and match.bowlingTeam:
                            cleanedWords.append('BOWLER')
                        elif match == batter and not match.bowlingTeam:
                            cleanedWords.append('BATTER')
                        else:
                            cleanedWords.append('FIELDER' if match.bowlingTeam else 'BATTER') # in this case BATTER should
                buffer = []
                cleanedWords.append(word)                                      # represent a batsman who is not currently in
        #print(cleanedWords)
        return ' '.join(cleanedWords)

    def findBestPlayerMatch(self, words):  # move all player things into a playerBase class?
        matchDict = {}
        best = 0
        for p in self.players:
            score = p.score(words)
            if score >= best:
                matchDict[score] = p
                best = score
        if best > 0:
            return matchDict[best]
        else:
            return None

    def cleanBowlerBatter(self, longComment, bowler, batter, handlePunctuation=False):  # being deprecated
        longWords = longComment.split()
        cleanedWords = []
        if(handlePunctuation):
            addApostrapheS = False
            addComma = False
            for word in longWords:
                cleanWord = word
                if word[-1:] == ',':
                    addComma = True
                    cleanWord = word[:-1]
                if cleanWord[-2:] == '\'s':
                    addApostrapheS = True
                    cleanWord = word[:-2]

                if similarity(cleanWord,bowler) > 0.8:
                    cleanWord = 'BOWLER'
                elif similarity(cleanWord,batter) > 0.8:
                    cleanWord = 'BATTER'

                cleanedWords.append(cleanWord)

                if addApostrapheS: cleanedWords.append('\'s')
                if addComma: cleanedWords.append(',')
                addComma = False
                addApostrapheS = False
        else:
            for word in longWords:
                wbo = similarity(word, bowler)
                wba = similarity(word, batter)
                if wbo > 0.8:  # can sort these out in a more nice way by preprocessing text and reformatting at end
                    if word[-3:] == '\'s,':
                        word = 'BOWLER\'s,'
                    elif word[-1:] == ',':
                        word = 'BOWLER,'
                    elif word[-2:] == '\'s':
                        word = 'BOWLER\'s'
                    else:
                        word = 'BOWLER'
                if wba > 0.8:  # can sort these out in a more nice way by preprocessing text and reformatting at end
                    if word[-3:] == '\'s,':
                        word = 'BATTER\'s,'
                    elif word[-1:] == ',':
                        word = 'BATTER,'
                    elif word[-2:] == '\'s':
                        word = 'BATTER\'s'
                    else:
                        word = 'BATTER'
                cleanedWords.append(word)
        return ' '.join(cleanedWords)

    def scrapeAll(self):
        i = 1
        self.createSequenceFiles()
        for address in self.addresses:
            if address == '':
                print('empty address')
                break
            print('scraping address ' + str(i) +  ' of ' + str(len(self.addresses)))
            self.scrapeTeamList(address[:-1]+'/full-scorecard')
            print(self.allNames)
            self.scrape(address[:-1]+'/ball-by-ball-commentary') #  <=------------------------!!!!!!!!!!!!!!!!!!!!!!
            self.writeSequencesToFiles()
            print('scraped data written to files')
            i = i + 1
        print('total balls: ', self.totalBalls)

    def scrapeTeamList(self, address):
        self.teams = [[], []]
        self.driver.get(address)
        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content, features="html.parser")

        innings = self.soup.findAll('table', attrs={'class':'batsman'})
        for i in range(len(innings)):
            rowsU = innings[i]
            if 'w-100' in rowsU.get_attribute_list('class'):
                break
            # in some way check so that class is table batsman not w-100 table batsman
            rows = rowsU.contents[1]
            for rowI in range(len(rows.contents)-1):
                if rowI%2 == 0:
                    b = rows.contents[rowI].contents[0].text
                    b = unicodedata.normalize("NFKD", b)
                    self.teams[i].append(b.lstrip().rstrip())
            if len(rows.contents) < 23:
                # print(i, 'innings batters that did not bat')
                footer = innings[i].contents[2]
                assert(len(footer.contents) > 2)
                didNotBat = footer.contents[1].text[13:]
                didNotBat = unicodedata.normalize("NFKD", didNotBat)
                nonBatters = (didNotBat.split(','))
                for b in nonBatters:
                    b = b.lstrip().rstrip()
                    self.teams[i].append(b)
        #print(self.teams[0])
        #print(self.teams[1])
        self.createTeams(self.teams)
        return self.teams

    def createTeams(self, playerNames):
        for playerName in playerNames[0]:
            p = player(playerName, True) # due to scraping order, this is correct way around
            for n in p.names:
                self.allNames.append(n)
            self.players.append(p)
        for playerName in playerNames[1]:
            p = player(playerName)
            for n in p.names:
                self.allNames.append(n)
            self.players.append(p)

    def playerSwitchInnings(self):
        for p in self.players:
            p.bowlingTeam = not p.bowlingTeam

    def scrape(self, address):  #  scrape and clean the long and short comments
        # reset the sequences for next page
        self.outcomeEmissions = {}
        self.outcomeSequence = []

        self.driver.get(address)
        self.content = self.driver.page_source

        self.scrollToBottom()
        self.soup = BeautifulSoup(self.content, features="html.parser")

        self.extractOutcomeAndComment() # <---

        #  next innings
        self.driver.execute_script("window.scrollTo(0, " + str(500) + ")")
        self.switchInnings()
        self.playerSwitchInnings()
        self.scrollToBottom()

        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content, features="html.parser")

        self.extractOutcomeAndComment() # <---

    def scrollToBottom(self):
        Y = 1000
        last = 0
        zeroCount = 0
        while True:
            self.driver.execute_script("window.scrollTo(0, " + str(Y) + ")")
            Y = Y + 2000
            self.content = self.driver.page_source
            soup = BeautifulSoup(self.content, features="html.parser")
            temp = len(soup.text)
            if temp - last == 0:
                zeroCount = zeroCount + 1
                if zeroCount > 10:
                    print('scrolling complete')
                    break
            else:
                zeroCount = 0
            last = temp

    def switchInnings(self):
        if self.cookieClickNeeded:
            time.sleep(2)
            actionChains = ActionChains(self.driver)
            consent_button = self.driver.find_element_by_id('onetrust-close-btn-container')
            actionChains.move_to_element(consent_button).click().perform()
            self.cookieClickNeeded = False

        time.sleep(4)
        self.driver.execute_script("window.scrollTo(0, " + str(500) + ")")
        actionChains = ActionChains(self.driver)
        button = self.driver.find_element_by_class_name('comment-inning-dropdown')
        actionChains.move_to_element(button).click().perform()

        time.sleep(1)
        actionChains = ActionChains(self.driver)
        next_innings_button = self.driver.find_element_by_class_name('ci-dd__menu')
        actionChains.move_to_element_with_offset(next_innings_button, 20, 20).click().perform()


scraper = CricinfoScraper('singleAddress.txt', 4)
# scraper.scrape()
# scraper.createSequenceFiles()
scraper.scrapeAll()


