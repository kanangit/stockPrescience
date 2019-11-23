# This script
# (1) takes as input a folder of locally-stored HTML pages previously downloaded from the NY Times;
# (2) scrapes plain text from the article title and body of each article using BeautifulSoup 4;
# (3) and appends the text on an article-by-article basis in a Unicode harvester file called "text_harvest.txt"
# Text for individual articles are separated in the harvester file by line breaks and the string @@@@@@@@@@
# Customize path names in the following for your computer and development environment.

# import modules

import urllib2
from bs4 import BeautifulSoup
import codecs
import glob

# (Start of outer loop) Inputs folder of locally-stored HTML pages by
# using glob module to walk through folder and open each article.
# Then makes soup from each article (processes it in BeautifulSoup)

path = 'C:/workspace/downloaded_pages/*.html'   
files=glob.glob(path)   
for file in files:
    f=open(file, 'r')

    # (Start of inner loops) Uses BeautifulSoup) to scrape plain text of article title and body;
    #  then appends to text_harvest.txt file.

    soup = BeautifulSoup(f)

    # Use BeautifulSoup to find and extract NYT article title as plain text, appending to text_harvest.txt
    # (NYT articles put titles in a h1 tag that include the attribute class=story-heading)
    soup.find_all('h1',{'class':'story-heading'})
    for h1_tag in soup.find_all('h1'):
        with codecs.open("C:/workspace/text_harvest.txt", "a", "utf-8") as alltext:
            alltext.write(h1_tag.text)

    # Use BeautifulSoup to find and extract NYT article body as plain text, appending to text_harvest.txt
    # (NYT articles put the body of stories in a series of p tags, each of which includes the attribute class=story-body-text story content)
    soup.find_all('p',{'class':'story-body-text story-content'})
    for p_tag in soup.find_all('p'):
        with codecs.open("C:/workspace/text_harvest.txt", "a", "utf-8") as alltext:
            alltext.write(p_tag.text)
        alltext.close()

    # Add line break and the string @@@@@@@@@@ (ten ampersands) to above scrape of an individual article to indicate end-of-article division in the text-harvester.txt file
    with codecs.open("C:/workspace/text_harvest.txt", "a", "utf-8") as alltext:
        alltext.write("\n@@@@@@@@@@\n")
        
    # (Close of inner loops)
    
f.close() # (Close of outer loop)
