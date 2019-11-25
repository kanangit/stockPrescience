
# In[10]:


tm_df = pd.read_csv(tmFilePath)


# In[11]:


tm_df.head()


# In[12]:


result_df = pd.concat([full_df, tm_df], axis=1, sort=False)


# In[13]:


result_df.head()


# In[14]:


print(len(result_df))


# In[15]:


set_dates = set(list(result_df['date']))


# In[16]:


print(len(set_dates))


# In[17]:


l_dates = [str(x) for x in set_dates]


# In[18]:


l_dates.sort()
l_dates.pop(len(l_dates)-1)


# In[19]:


print(l_dates)


# In[20]:


time_list = [[time.mktime(time.strptime(date,'%m/%d/%y')), date] for date in l_dates]


# In[22]:


time_list = sort_by_column(time_list,0,desc = False)


# In[24]:


sub_df = result_df[result_df.date == time_list[5][1]]


# In[25]:


sub_df.head()


# In[26]:


sub_df.reset_index(drop = True)


# In[29]:


def get_dateMean(date_list, data_df, dateName, colName):
    out_list = []
    for date in date_list:
        sub_df = data_df[data_df[dateName] == date]
        sub_df.reset_index(drop = True)
        curMean = sub_df[colName].mean()
        out_list.append([date, curMean])
    return out_list
    


# In[30]:


d_list = [row[1] for row in time_list]


# In[31]:


check_list = get_dateMean(d_list,result_df,'date','V5')


# In[32]:


allDates = [matplotlib.dates.epoch2num(time[0]) for time in time_list ]


# In[33]:


ytemp = [row[1] for row in check_list]


# In[34]:


matplotlib.pyplot.plot_date(allDates, ytemp, '-')


# In[36]:


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

