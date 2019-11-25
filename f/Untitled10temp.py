
snp500_df = pd.read_csv(snp500FilePath)


# In[37]:


snp500_df.head()


# In[38]:


epochStart = time.mktime(time.strptime('2018-01-01','%Y-%m-%d'))


# In[39]:


epochEnd =time.mktime(time.strptime('2018-12-31','%Y-%m-%d')) 


# In[40]:


l_snp_dates = list(snp500_df['Date'])


# In[41]:


epoch_list = [time.mktime(time.strptime(date,'%Y-%m-%d')) for date in l_snp_dates]


# In[42]:


epoch_df = pd.DataFrame(epoch_list, columns = ['Epoch'])


# In[43]:


snp500_df = pd.concat([snp500_df, epoch_df], axis=1, sort=False)


# In[44]:


snp500_2018_df = snp500_df[snp500_df['Epoch'] >= epochStart]


# In[45]:


snp500_2018_df.reset_index(drop = True);


# In[46]:


snp500_2018_df = snp500_df[snp500_df['Epoch'] <= epochEnd]


# In[47]:


snp500_2018_df.reset_index(drop = True)


# In[48]:


l_dates = list(snp500_2018_df['Epoch'])


# In[49]:


l_snp = list(snp500_df['Close'])


# In[50]:


allDatesSnp = [matplotlib.dates.epoch2num(time) for time in l_dates ]


# In[51]:


matplotlib.pyplot.plot_date(l_dates, l_snp, '-')

