import numpy as np
import pandas as pd
import time
import re
import requests
from bs4 import BeautifulSoup


# The code below is code by nimolne
# (https://github.com/nilmolne/Text-Mining-The-New-York-Times-Articles),
#modified for my needs


def parse_articles(articles):
    
    news = []
    
    for i in articles['response']['docs']:
        
        dic = {}
        dic['date'] = i['pub_date'][0:10] # cutting time of day.
        dic['atype'] = i['type_of_material']
        dic['url'] = i['web_url']
        dic['word_count'] = int(i['word_count'])
        dic['lead_par'] = i['lead_paragraph']
        news.append(dic)
        
    return news

def get_articles_url(api, start_day, end_day):
    
    all_articles = []
    all_nonparsed = []
    day = start_day
    
    print('Retrieving articles URL...'),
    
    #Loop through all years of interest
    while day != end_day:
        
        # Some pages might return a 'No JSON object could be decoded'
        # Example: country = Turkey, year = 1998, page 4
        # To keep this error from stopping the loop a try/except was used.
        for i in range(0,1):

            try:
                # Call API method with the parameters discussed on the README file
                articles = api.search(q = "resilience",
                    fq = {'source':['The New York Times'],                           
                          'section_name':('Business Day')}, 
                    begin_date = day, 
                    end_date = day, 
                    sort = 'oldest', page = str(i))
                
                # Check if page is empty
                if articles['response']['docs'] == []: break
                articles_nonparsed = articles
                print(articles_nonparsed)
                #all_nonparsed = all_nonparsed + articles_nonparsed
                print('--------------------------------------          ----------------------------------------------------------')
                articles = parse_articles(articles)
                all_articles = all_articles + articles
                print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                
                print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
                print(all_nonparsed)
                print('--------------------------------------')
                
            except Exception:

                pass
            
            # Avoid overwhelming the API
            time.sleep(1)
            
        day = get_nextday(day)
    
    # Copy all articles on the list to a Pandas dataframe
    articles_df = pd.DataFrame(all_articles)
    with open(r'D:\kananovich\personal\OneDrive\Documents\family\jobsAnton\dataIncubator\stage02\myproject\data\scrapped\dumpBusinessDay20191101-20191101resilience.txt', 'w') as f:
        for item in all_nonparsed:
            f.write("%s\n" % item)
    #nonparsed_df = pd.DataFrame(all_nonparsed)
    #Export = nonparsed_df.to_json(r'D:\kananovich\personal\OneDrive\Documents\family\jobsAnton\dataIncubator\stage02\myproject\data\scrapped\dumpBusinessDay20191101-20191101resilience.json')
    
    # Make sure we filter out non-news articles and remove 'atype' column
    #articles_df = articles_df.drop(articles_df[articles_df.atype != 'News'].index)
    #articles_df.drop('atype', axis = 1, inplace = True)
    
    # Discard non-working links (their number of word_count is 0).
    # Example: http://www.nytimes.com/2001/11/06/world/4-die-during-police-raid-in-istanbul.html
   # articles_df = articles_df[articles_df.word_count != 0]
    articles_df = articles_df.reset_index(drop = True)
    
    print('Done!')
    
    return(articles_df)


def scarp_articles_text(articles_df):
    
    # Unable false positive warning from Pandas dataframe manipulation
    pd.options.mode.chained_assignment = None
    
    articles_df['article_text'] = 'NaN'
    session = requests.Session()
    
    print('Scarping articles body text...'),
    
    for j in range(0, len(articles_df)):
        
        url = articles_df['url'][j]
        req = session.get(url)
        soup = BeautifulSoup(req.text, 'lxml')

        # Get only HTLM tags with article content
        # Articles through 1986 are found under different p tag 
        paragraph_tags = soup.find_all('p', class_= 'story-body-text story-content')
        if paragraph_tags == []:
            paragraph_tags = soup.find_all('p', itemprop = 'articleBody')

        # Put together all text from HTML p tags
        article = ''
        for p in paragraph_tags:
            article = article + ' ' + p.get_text()

        # Clean article replacing unicode characters
        article = article.replace(u'\u2018', u"'").replace(u'\u2019', u"'").replace(u'\u201c', u'"').replace(u'\u201d', u'"')

        # Copy article's content to the dataframe
        articles_df['article_text'][j] = article
    
    print('Done!')
    
    return articles_df


#The code below beongs to champerbarton
# (https://github.com/champebarton/NYTimesArticleAPI
# I had to use it explicitly instead of importing a module
# from nytimesarticle import articleAPI), because
# from imported module it doesn't work somehow

API_ROOT = 'http://api.nytimes.com/svc/search/v2/articlesearch.'

API_SIGNUP_PAGE = 'http://developer.nytimes.com/docs/reference/keys'

class NoAPIKeyException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class articleAPI(object):
    def __init__(self, key = None):
        """
        Initializes the articleAPI class with a developer key. Raises an exception if a key is not given.

        Request a key at http://developer.nytimes.com/docs/reference/keys

        :param key: New York Times Developer Key

        """
        self.key = key
        self.response_format = 'json'

        if self.key is None:
            raise NoAPIKeyException('Warning: Missing API Key. Please visit ' + API_SIGNUP_PAGE + ' to register for a key.')

    def _bool_encode(self, d):
        """
        Converts boolean values to lowercase strings

        """
        for k, v in d.items():
            if isinstance(v, bool):
                d[k] = str(v).lower()

        return d

    def _options(self, **kwargs):
        """
        Formats search parameters/values for use with API

        :param \*\*kwargs: search parameters/values

        """
        def _format_fq(d):
            for k,v in d.items():
                if isinstance(v, list):
                    d[k] = ' '.join(map(lambda x: '"' + x + '"', v))
                else:
                    d[k] = '"' + v + '"'
            values = []
            for k,v in d.items():
                value = '%s:(%s)' % (k,v)
                values.append(value)
            values = ' AND '.join(values)
            return values

        kwargs = self._bool_encode(kwargs)

        values = ''

        for k, v in kwargs.items():
            if k is 'fq' and isinstance(v, dict):
                v = _format_fq(v)
            elif isinstance(v, list):
                v = ','.join(v)
            values += '%s=%s&' % (k, v)

        return values

    def search(self,
                response_format = None,
                key = None,
                **kwargs):
        """
        Calls the API and returns a dictionary of the search results

        :param response_format: the format that the API uses for its response,
                                includes JSON (.json) and JSONP (.jsonp).
                                Defaults to '.json'.

        :param key: a developer key. Defaults to key given when the articleAPI class was initialized.

        """
        if response_format is None:
            response_format = self.response_format
        if key is None:
            key = self.key

        url = '%s%s?%sapi-key=%s' % (
            API_ROOT, response_format, self._options(**kwargs), key
        )

        self.req = requests.get(url)
        return self.req.json()


def get_nextday(today):
    todayStruct = time.strptime(today, '%Y%m%d')
    epochseconds = time.mktime(todayStruct)
    deltaDay = 60*60*24
    nextDayEpoch = epochseconds+deltaDay
    nexDayStruct = time.localtime(nextDayEpoch)
    nextDay= time.strftime('%Y%m%d', nexDayStruct)
    return nextDay

start_day = '20191101'
end_day = '20191102'
api = articleAPI('UC0yZec7sBIqmDUSCvPnRLQYFso1bocD')
articles_df = get_articles_url(api, start_day, end_day)
#articles_df.tail()

#articles_df = scarp_articles_text(articles_df)
#articles_df.tail()

export_csv = articles_df.to_csv (r'D:\kananovich\personal\OneDrive\Documents\family\jobsAnton\dataIncubator\stage02\myproject\data\scrapped\dumpBusinessDay20180101-20180110Full.csv', index = None, header=True) 