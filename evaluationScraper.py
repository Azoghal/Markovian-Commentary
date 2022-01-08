import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

class evaluationScraper:

    def __init__(self):
        self.driver = self.driver = webdriver.Chrome("C:/Users/sambe/chromedriver_win32/chromedriver.exe")
        self.content = None
        self.soup=None
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

    def scrape_n_years_back_from_2018(self,n):
        archive_link = 'https://www.espncricinfo.com/ci/engine/series/index.html'
        end_year = 2018-n
        # open in webdriver and copy links to years into list
        year_links = []
        print('loading page')
        self.driver.get(archive_link)
        self.content = self.driver.page_source
        print('page loaded')
        self.soup = BeautifulSoup(self.content, features="html.parser")
        print('page souped')
        break_flag = False
        for decade in self.soup.findAll('section', attrs={'class': 'season-links'}):
            if break_flag:
                break
            for season in decade:
                if type(season) is bs4.Tag:
                    year_name = season.text[0:4]
                    second_year_name = season.text[5:7]
                    second_year_name = year_name[0:2]+second_year_name
                    year_1 = int(year_name)
                    year_2 = int(second_year_name) if len(second_year_name)>2 else 0
                    if year_1 <= 2018 and year_2 <= 2018:
                        if year_1 < end_year:
                            break_flag=True
                            break
                        link = season.get('href')
                        link = 'https://www.espncricinfo.com' + link
                        year_links.append(link)
        print(year_links)
        return year_links

ES = evaluationScraper()
ES.scrape_n_years_back_from_2018(4)