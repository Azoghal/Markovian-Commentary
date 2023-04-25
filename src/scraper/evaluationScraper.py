import json
import time

import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

import cricinfoScraper

class evaluationScraper:

    def __init__(self):
        self.driver = self.driver = webdriver.Chrome("C:/Users/sambe/chromedriver_win32/chromedriver.exe")
        self.content = None
        self.actionChains = ActionChains(self.driver)
        self.match_links = []
        self.summaries = []
        self.year_links = []
        self.cookie_click_needed =True
        # TODO: evaluation data needed:
        # TODO: distribution of totals
        # TODO: distribution of wickets
        # TODO: scatter of total/wickets pairs
        # TODO: distribution of fours and sixes
        # TODO: distribution of extras?
        # TODO: distribution of innings length
        # TODO: worms

        # start on archive page
        # visit each year and each series
        # was thinking just world cups but too far back and there isn't ball by ball
        # expand series
        # scrape total/wicket pairs (and legal balls?) directly
        # scrape scorecard link, replace the end with full-commentary and save to file
        # run cricinfoscraper (outcomes only?) on the file of evaluation links
        # can extract from that file (one innings between start tokens) the stats
        # fours, wickets, extras, total balls
        # need to run through a pared back match simulation just for it to keep track of runs and overs
        # to give us the worm data

    def find_ODI_and_expand_series(self,link):
        self.driver.get(link)
        self.content = self.driver.page_source
        # first need to find the one day international header (always the next one after tests?)
        # current plan is to find the titles from the soup
        # and all the elements
        # and then filter the elements by which ones have matching text
        # and then only click through those
        # hopefully
        #TODO!!! make faster by expanding and closing. info stays in html
        soup = BeautifulSoup(self.content, features="html.parser")
        root = soup.findAll('div', attrs={'class': 'match-section-head'})[1]
        print('expandning one day section', root.text)
        ODI_container = root.next_sibling.next_sibling
        filter = []
        for ODI_series in ODI_container.contents:
            if type(ODI_series) is bs4.element.Tag:
                title = ODI_series.section.div.div.text
                filter.append(title)
            #print(ODI_series.contents[0].contents[0].contents[0].text)
        self.click_cookies()
        filtered = []
        time.sleep(1)
        elements = self.driver.find_elements_by_class_name('series-summary-block')
        for element in elements:
            series_name = element.text.split('\n')[0]
            if series_name in filter and element not in filtered:
                filtered.append(element)
        print(len(filtered),' ODI series found to expand')
        actionChains = ActionChains(self.driver)
        for i, element in enumerate(filtered):
            actionChains.move_to_element(element).click().perform()
            #double click should be faster but has problems with highlighting header and clicking that instead
            #actionChains.move_to_element(element).click().pause(0.1).click().move_to_element(element).perform()

    def click_cookies(self):
        if self.cookie_click_needed:
            time.sleep(2)
            actionChains = ActionChains(self.driver)
            consent_button = self.driver.find_element_by_id('onetrust-close-btn-container')
            actionChains.move_to_element(consent_button).click().perform()
            self.cookie_click_needed = False

    def scrape_total_wickets_and_links(self):
        print('starting match summary scrape')
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        summaries = []
        all_summaries = soup.findAll('div', attrs={'class': ['innings-info-1', 'innings-info-2']})
        for summary in all_summaries:
            summaries.append(str(summary.span.text))
        links = []
        match_articles = soup.findAll('div', attrs={'class': 'match-articles'})
        for match_article in match_articles:
            if match_article.previous_sibling.previous_sibling.span.text not in ['Match abandoned without a ball bowled','No result (abandoned with a toss)', 'No result (abandoned with a toss)']:
                link = match_article.a.get('href')
                links.append(link)
        print(len(links),'match summaries and links gathered')
        self.summaries = self.summaries + summaries
        self.match_links = self.match_links + links

    def save_scores(self, to_save):
        with open('saved_scores.txt','w') as f:
            json.dump({'scores': to_save}, f)

    def load_scores(self):
        with open('saved_scores.txt', 'r') as f:
            d = json.load(f)
            return d['scores']

    def save_match_links(self):
        with open('match_links.txt', 'a') as f:
            for link in self.match_links:
                f.write(link + '\n')

    def load_match_links(self):
        self.match_links = []
        with open('match_links.txt','r') as f:
            v = f.readline()
            while v:
                self.match_links.append(v)
                v = f.readline()

    def save_score_wicket_files(self, to_save): # made additive
        scores, wickets = to_save
        with open('scores.txt','a') as f:
            for score in scores:
                f.write(score+'\n')
        with open('wickets.txt','a') as f:
            for wicket in wickets:
                f.write(wicket+'\n')

    def wipe_files(self):
        print('clearing files')
        with open('scores.txt', 'w') as f:
            f.write('')
        with open('wickets.txt', 'w') as f:
            f.write('')
        with open('match_links.txt', 'w') as f:
            f.write('')

    def parse_total_wicket_text(self):#TODO check for empties
        texts = self.summaries
        scores = []
        wickets = []
        for text in texts:
            if text not in ['']:
                score_pair = text.split(' ')[0]
                split_pair = score_pair.split('/')
                wicket = '10' if len(split_pair) < 2 else split_pair[1]
                score = split_pair[0]
                #print(text, '--->', score, 'for', wickets)
                scores.append(score)
                wickets.append(wicket)
        return scores, wickets

    def scrape_n_year_links_back_from_2018(self,n):
        archive_link = 'https://www.espncricinfo.com/ci/engine/series/index.html'
        start_year = 2018
        end_year = start_year-n
        # open in webdriver and copy links to years into list
        year_links = []
        print('loading archive page')
        self.driver.get(archive_link)
        self.content = self.driver.page_source
        print('archive page loaded')
        soup = BeautifulSoup(self.content, features="html.parser")
        print('archive page souped')
        break_flag = False
        for decade in soup.findAll('section', attrs={'class': 'season-links'}):
            if break_flag:
                break
            for season in decade:
                if type(season) is bs4.Tag:
                    year_name = season.text[0:4]
                    second_year_name = season.text[5:7]
                    second_year_name = year_name[0:2]+second_year_name
                    year_1 = int(year_name)
                    year_2 = int(second_year_name) if len(second_year_name)>2 else 0
                    if year_1 <= start_year and year_2 <= start_year:
                        if year_1 < end_year:
                            break_flag=True
                            break
                        link = season.get('href')
                        link = 'https://www.espncricinfo.com' + link
                        year_links.append(link)
        print(len(year_links),' season links gathered')
        print(year_links)
        self.year_links = year_links
        return year_links

    def scrape_from_year_links(self):
        scores = []
        wickets = []
        for i, link in enumerate(self.year_links):
            print(i)
            self.find_ODI_and_expand_series(link)
            self.scrape_total_wickets_and_links()
            a,b = self.parse_total_wicket_text()
            scores.append(a)
            wickets.append(b)
        self.save_score_wicket_files((scores,wickets))
        return None

    def scrape_outcome_sequences_from_commentary(self,n=0):
        CS = cricinfoScraper.CricinfoScraper(None, 4, driver=self.driver)
        all_outcome_sequences = []
        for i, link in enumerate(self.match_links[n:]):
            print(i+n)
            self.driver.get(link)
            ##self.click_cookies()
            self.content = self.driver.page_source
            soup = BeautifulSoup(self.driver.page_source, features="html.parser")
            tabs = soup.findAll('a', attrs={'class': 'widget-tab-link'})
            for tab in tabs:
                if tab.div.text == 'Commentary':
                    commentary_link = 'https://www.espncricinfo.com' + tab.get('href')
                    print(commentary_link)
                    CS.scrape(commentary_link, outcomes_only=True)
                    outcome_sequence = CS.outcomeSequence
                    total_balls = CS.totalBalls
                    seq = ' '.join(outcome_sequence)+'\n'
                    all_outcome_sequences.append(seq)
                     #TODO save the outcomes to files for reading in and making plots
                    with open('evaluation_outcomes.txt', 'a') as f:
                        f.write(seq)
                    break
        print('find neccessary link first')

    def close_window(self):
        time.sleep(5)
        self.driver.close()

if __name__=="__main__":
    ES = evaluationScraper()
    #ES.wipe_files()
    ES.scrape_n_year_links_back_from_2018(4)
    ES.scrape_from_year_links()
    #ES.save_match_links()

    #ES2 = evaluationScraper()
    #ES2.load_match_links()
    #ES2.scrape_outcome_sequences_from_commentary(720)


