
# coding: utf-8

# In[1]:


import requests


# In[17]:


r = requests.get("https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key=ETOaFvpTJqixRiwvCFJn7j0652TX1hg4")


# In[12]:


r


# In[18]:


rjson = r.json()


# In[19]:


rjson


# In[20]:


rComment = requests.get("https://api.nytimes.com/svc/community/v3/user-content/url.json?api-key=vyk8e6eHS3dV0Un4RkS6RSccPkMnrbbo&offset=0&url=https%3A%2F%2Fwww.nytimes.com%2F2019%2F06%2F21%2Fscience%2Fgiant-squid-cephalopod-video.html")


# In[22]:


rcomJson=rComment.json()


# In[23]:


rcomJson

