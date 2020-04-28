# stockPrescience

Stock markets have been a constant presence in media coverage. Their ups and downs supply journalists with drama and action, which are considered to be the key ingredients of a newsworthy story. This means that, although financial news is likely to be saturated with informational “noise,” it can also provide potentially useful insights into the stock markets’ mood. Not only that – and this is the key question that motivates my project – this opens up an opportunity that the news media can not only reflect but also predict the upcoming changes in stock-market performance.

Paraphrasing the popular metaphor that describes the news media as a watchdog, my project asks: Can this watchdog sense an upcoming stock-market swing and start barking before the swing arrives?

As a result of this project, I plan to develop a tool that can be used by investors to predict a change in stock prices based on the features of the current news coverage. Specifically, the tool will predict the closing values of S&P 500 – as a commonly followed stock-market index – based on the analysis of the coverage in The New York Times, as the national newspaper of record.

The project is to be implemented in two steps.

At STEP 1 – which I preliminarily executed – I tested the hypothesis that the NYT coverage does, indeed, reflect the S&P 500’s current performance.

To do that, I used the NYT API to retrieve the meta information of the articles published in the newspapers’ financial articles, and then scraped the full-text versions of the articles from the newspaper’s website. This returned 911 articles, which I saved as a .csv file.

I then ran a topic-modeling analysis of the articles in R. The analysis infered 10 topics, or themes with statistically distinct patters of occurrence of words, which I validated by reading the articles identified by the algorithm as most indicative of each topic, and summarized with a substantive label. Topics included domestic partisan politics (with indicatives stems, or word root forms, such as "democrat," "republican," "polit," "state," "trump," "elect," "parti," "campaign"), changes in foreign, mostly European, politics ("world," "new," "first," "time," "merkel," "macron," "european"), trade politics with China ("china," "trade," "percent," "tariff," "deficit," "govern"), technology ("facebook," "alibaba," "bitcoin," "tesla," "amazon," "spotifi"), etc.

Then, for each article, I identified the salience of each topic, as a proportion of text that exhibited the “traces” of the respective topic. After that, for each day in the timeframe, an average salience of each topic in the news coverage was calculated. Finally, to see which of the 10 topics did the best job matching the dynamic of the S&P values, I created 10 time-series plots that mapped the S&P 500’s closing values versus the daily salience of each topic in the news. 

Figures 1 and 2 present two of them, which have provided the best match based on the preliminary visual analysis. Notably, both are related to political news, but appear to demonstrate different dynamics. An increase in foreign political coverage tended to coincide with the upward dynamic in S&P 500 prices ( see  [Figure 1](https://github.com/kanangit/stockPrescience/blob/master/Figure1_foreign.png) below). 

![Figure 1](https://github.com/kanangit/stockPrescience/blob/master/Figure1_foreign.png "Figure 1")

In contrast, the coverage of domestic news tended to behave countercyclically. With the notable exception on Nov. 6, the date of the midterm elections, when the journalists focused on partisan politics ( see  [Figure 2](https://github.com/kanangit/stockPrescience/blob/master/Figure2_domestic.png) below), this increase in coverage appears to have been accompanied by S&P 500’s poorer stock-market performance. 

![Figure 2](https://github.com/kanangit/stockPrescience/blob/master/Figure2_domestic.png "Figure 2")

At STEP 2, to be implemented later, I will subject this observation to more rigorous statistical testing, as well as will expand the sample beyond the financial news section. I will examine, specifically, which of the political topics that have not yet made their way to the financial news – where they would reflect concurrent price swings – have the biggest power in predicting the swings that’s yet to come. 

I will use the results of this analysis to formalize the predictive model that will be used in the tool. Given the features of the news content that are updated in real-time and the planning horizon, the tool will predict the likelihood and directionality of a swing in the S&P values.

