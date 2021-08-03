import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import pandas

def similarity(first, second):
    return SequenceMatcher(None, first, second).ratio()

class CricinfoScraper:
    def __init__(self, addressfile): #  give a filename to open to extract web addresses
        self.addresses = open(addressfile,'r').readlines()
        #  self.bowler_to_batter_to_outcome = []
        #  self.long_comments = []
        self.outcomeEmissions = {}  # dict of outcome: array of emissions
        self.outcomeSequence = []  # array of outcomes to use to do transition probabilities
        self.driver = webdriver.Chrome("C:/Users/sambe/chromedriver_win32/chromedriver.exe")
        for address in self.addresses:
            self.driver.get(address[:-1])
            self.content = self.driver.page_source
            #self.scrape() #  <=------------------------!!!!!!!!!!!!!!!!!!!!!!


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
                    break
            else:
                zeroCount = 0
            print(zeroCount)
            last = temp

    def getCommentBlocks(self):
        self.outcomeSequence.append('START ')
        self.soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        for a in self.soup.findAll('div', attrs={'class': 'match-comment-wrapper'}):
            shortComment = a.contents[0].text
            longComment = a.contents[1].text
            bowler, batter, outcome = self.extractBowlerBatterOutcome(shortComment)
            cleanedComment = self.cleanBowlerBatter(longComment, bowler, batter, handlePunctuation=False)
            self.outcomeSequence.append(outcome)
            if(outcome in self.outcomeEmissions):
                self.outcomeEmissions[outcome].append(cleanedComment)  # does this have affect?
            else:
                self.outcomeEmissions[outcome] = [cleanedComment]
            #print(f'Bowler: {bowler:20}   Batter: {batter:20}   Outcome: {outcome}')
            #if(bowler == 'Asitha Fernando'): print(cleanedComment) # shows that there is a need to check for both names
        self.outcomeSequence.append(' END')

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
        return bowler, batter, outcome

    def cleanBowlerBatter(self, longComment, bowler, batter, handlePunctuation=False):  # <--------- test, sort out first and surnames
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


    def getShortComments(self):  # being deprecated
        for a in self.soup.findAll('div', attrs={'class': 'match-comment-short-text'}):
            comment = a.text
            words = comment.split()
            split = words.index('to')
            end = len(words)
            i = 0
            bowler = ' '.join(words[0:split])
            batter = ''
            for word in words:
                if word[-1] == ',':
                    end = i
                    batter = word[0:len(word) - 1]
                i = i + 1
            outcome = ' '.join(words[end + 1:len(words)])
            self.bowler_to_batter_to_outcome.append([bowler, batter, outcome])

    def getLongComments(self): #  being deprecated
        i = 0
        for a in self.soup.findAll('div', attrs={'class': 'match-comment-long-text', 'itemprop': 'articleBody'}):
            long = a.text
            tokens = long.split()
            bowler = self.bowler_to_batter_to_outcome[i][0]
            batter = self.bowler_to_batter_to_outcome[i][1]
            j = 0
            for w in tokens:
                wbo = similarity(w, bowler)
                wba = similarity(w, batter)
                if wbo > 0.8:   #   can sort these out in a more nice way by preprocessing text and reformatting at end
                    if w[-2:] == '\'s':
                        tokens[j] = 'BOWLER\'s'
                    elif w[-1:] == ',':
                        tokens[j] = 'BOWLER,'
                    else:
                        tokens[j] = 'BOWLER'
                if wba > 0.8:
                    if w[-2:] == '\'s':
                        tokens[j] = 'BATTER\'s'
                    elif w[-1:] == ',':
                        tokens[j] = 'BATTER,'
                    else:
                        tokens[j] = 'BATTER'
                j = j + 1
            i = i + 1
            self.long_comments.append(' '.join(tokens))

    def scrape(self): #  scrape and clean the long and short comments
        self.scrollToBottom()

        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content, features="html.parser")

        self.getCommentBlocks() # <---

        #print('finished scraping first innings: ', len(self.bowler_to_batter_to_outcome), len(self.long_comments), 'balls')

        #  next innings
        self.driver.execute_script("window.scrollTo(0, " + str(500) + ")")
        self.switchInnings()
        self.scrollToBottom()

        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content, features="html.parser")

        self.getCommentBlocks() # <---

        #print('finished scraping second innings: ', len(self.bowler_to_batter_to_outcome), len(self.long_comments),
              #'balls')

        #with open('comments.txt','w') as f:
            #f.write('START1 START2 START3')
            #f.write(' END1 END2 END3 START1 START2 START3 '.join(self.long_comments) + ' END1 END2 END3')

    def switchInnings(self):
        time.sleep(2)
        actionChains = ActionChains(self.driver)
        consent_button = self.driver.find_element_by_id('onetrust-close-btn-container')
        actionChains.move_to_element(consent_button).click().perform()

        time.sleep(4)
        self.driver.execute_script("window.scrollTo(0, " + str(500) + ")")
        actionChains = ActionChains(self.driver)
        button = self.driver.find_element_by_class_name('comment-inning-dropdown')
        actionChains.move_to_element(button).click().perform()

        time.sleep(1)
        actionChains = ActionChains(self.driver)
        next_innings_button = self.driver.find_element_by_class_name('ci-dd__menu')
        actionChains.move_to_element_with_offset(next_innings_button, 20, 20).click().perform()


scraper = CricinfoScraper('safeAddresses')
scraper.scrape()
