from selenium import webdriver
from bs4 import BeautifulSoup
#  import pandas
from difflib import SequenceMatcher


def similarity(first, second):
    return SequenceMatcher(None, first, second).ratio()


driver = webdriver.Chrome("C:/Users/sambe/chromedriver_win32/chromedriver.exe")
driver.get("https://www.espncricinfo.com/series/sri-lanka-in-england-2021-1239532/england-vs-sri-lanka-2nd-odi-1239535/"
           "ball-by-ball-commentary")
content = driver.page_source

Y = 1000
last = 0
zeroCount = 0
while True:
    driver.execute_script("window.scrollTo(0, " + str(Y) + ")")
    Y = Y + 2000
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    temp = len(soup.text)
    if temp - last == 0:
        zeroCount = zeroCount + 1
        if zeroCount > 10:
            break
    else:
        zeroCount = 0
    print(zeroCount)
    last = temp

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

bowler_to_batter_to_outcome = []
short_comments = []
long_comments = []
long_comments_a = []

for a in soup.findAll('div', attrs={'class': 'match-comment-short-text'}):
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
    bowler_to_batter_to_outcome.append([bowler, batter, outcome])
    short_comments.append(a.text)

i = 0
for a in soup.findAll('div', attrs={'class': 'match-comment-long-text'}):
    if len(a['class']) == 1:
        long_comments.append(a.text)
        long = a.text
        tokens = long.split()
        bowler = bowler_to_batter_to_outcome[i][0]
        batter = bowler_to_batter_to_outcome[i][1]
        j = 0
        for w in tokens:
            wbo = similarity(w, bowler)
            wba = similarity(w, batter)
            if wbo > 0.8:
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
        long_comments_a.append(' '.join(tokens))

if len(short_comments) == len(long_comments):
    for i in range(len(short_comments)):
        #  print(bowler_to_batter_to_outcome[i][0], 'to', bowler_to_batter_to_outcome[i][1], '\n' + bowler_to_batter_to_
        #  outcome[i][2], '\n')
        #  print(short_comments[i], '\n',long_comments[i],'\n\n')
        print(long_comments_a[i])

#  now we have extracted bowler and batter names, replace in long text using string similarity
