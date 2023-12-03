#!/usr/bin/env python
# coding: utf-8

# ### 1. Import claims_data.csv and cust_data.csv which is provided to you and combine the two datasets appropriately to create a 360-degree view of the data. Use the same for the subsequent questions.

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import datetime as dt


# In[3]:


file_path='C:/Users/DELL/Desktop/Python case studies/Insurance'


# In[4]:


claims= pd.read_csv(file_path+'/claims.csv')


# In[5]:


claims.head()


# In[6]:


#checking for duplicates in the claims table

claims.duplicated().sum()


# In[7]:


cust= pd.read_csv(file_path+'/cust_demographics.csv')


# In[8]:


cust.head()


# In[9]:


#checking for duplicates in the cust table
cust.duplicated().sum()


# In[10]:


cust_claims= pd.merge(left=claims, right= cust, how= 'left', left_on='customer_id',right_on='CUST_ID', indicator=True )


# In[11]:


cust_claims.head()


# ### 2. Perform a data audit for the datatypes and find out if there are any mismatch within the current datatypes of the columns and their business significance.

# In[12]:


cust_claims.dtypes

From above we can see that claim_date, DateofBirth are objects instedof date time, also claim ammount is a string due to the addition of $ which would prevent us from doing any calculations like average claim ammount,average monthly/yearly number of claims, or average monthly/yearly claim ammount. 
# In[13]:


# Converting the claim date column in dateset from object to datetime.
cust_claims['claim_date']=pd.to_datetime(cust_claims.claim_date)


# In[14]:


# Converting the DateOfBirth column in dateset from object to datetime.
cust_claims['DateOfBirth']= pd.to_datetime(cust_claims.DateOfBirth)


# In[15]:


cust_claims.dtypes


# ### 3. Convert the column claim_amount to numeric. Use the appropriate modules/attributes to remove the $ sign.

# In[16]:


cust_claims['claim_amount']=cust_claims['claim_amount'].str.replace('$','').astype(float)


# In[17]:


cust_claims.claim_amount.dtype


# ### 4. Of all the injury claims, some of them have gone unreported with the police. Create an alert flag (1,0) for all such claims.

# In[18]:


cust_claims['Alert Flag']= np.where( (cust_claims.claim_type.str.lower().str.contains('injury')) & (cust_claims.police_report!='Yes'),1,0)


# In[19]:


cust_claims.head(7)


# ### 5. One customer can claim for insurance more than once and in each claim, multiple categories of claims can be involved. However, customer ID should remain unique. Retain the most recent observation and delete any duplicated records in the data based on the customer ID column.

# In[20]:


cust_claims.sort_values('claim_date', ascending=False, inplace=True)


# In[21]:


cust_claims.drop_duplicates(subset=['customer_id'], inplace=True)


# In[22]:


cust_claims.customer_id.duplicated().sum()


# ### 6. Check for missing values and impute the missing values with an appropriate value. (mean for continuous and mode for categorical)

# In[23]:


cust_claims.dtypes


# In[24]:


# Out of the given columns in cust_claims only claim_amount is a continuous variable. Therefore we will do outlier treatment
# for claim_amount before we start with missing value treatment.

p0 = cust_claims.claim_amount.min()
p100 = cust_claims.claim_amount.max()
q2 = cust_claims.claim_amount.quantile( 0.5 )
q1 = cust_claims.claim_amount.quantile( 0.25 )
q3 = cust_claims.claim_amount.quantile( 0.75 )

iqr = q3 - q1

lc = q1 - 1.5 * iqr
uc = q3 + 1.5 * iqr

print( p0, p100, lc, uc )


# In[25]:


cust_claims.claim_amount.plot(kind = 'box')

From the above box plot we can see that there are no outliers in claim_amount column. So we can start the missing value imputation of this column now.
# In[26]:


cust_claims['total_policy_claims']


# In[27]:


# Missing value treatment

cust_claims.isna().sum()

With the above missing values we can see that there are 15 customers who claimed amount but are not mentioned in the customer database. So for these records we can't find Date of birth, contact. We can impute, gender, state, segment as mode but this data only forms 15/1093*100= 1.37 percent of the total data, in which case it is better to remove it. 
# In[28]:


15/1093*100


# In[29]:


cust_claims.dropna(subset=['CUST_ID'], inplace=True)


# In[30]:


cust_claims.isna().sum()


# In[31]:


#imputing missing claim amount to mean claim amount

cust_claims.claim_amount.fillna(cust_claims.claim_amount.mean(), inplace=True)


# In[147]:


mode_1=cust_claims.total_policy_claims.mode().item()
mode_1


# In[148]:


#imputing missing total policy claims to mode of total policy claims

cust_claims.total_policy_claims.fillna(value=mode_1, inplace=True)


# In[149]:


#no there are no missing values 

cust_claims.isna().sum()


# In[36]:


# cust_claims[cust_claims.total_policy_claims.isna()]


# ### 7. Calculate the age of customers in years. Based on the age, categorize the customers according to the below criteria
# ### Children < 18
# ### Youth 18-30
# ### Adult 30-60
# ### Senior > 60

# In[37]:


# q1_df['Age group']=pd.cut(q1_df.Age,  bins=[0, 1, 12, 19, 60, 100] , labels=['Infant', 'Kid', 'Teenager', 'Grownup', 'Senior Citizen'])


# In[38]:


# Calcuting customers age 

cust_claims['Age']= pd.Timestamp.now().year- cust_claims.DateOfBirth.dt.year


# In[39]:


#Negative ages are not possible and it's probably a human error that the years have been entered as 2067 insead of 1967

cust_claims.loc[cust_claims.Age<0]


# In[40]:


cust_claims['Age']= np.where(cust_claims.Age<0, (pd.Timestamp.now().year- ((cust_claims.DateOfBirth- pd.offsets.DateOffset(years=100)).dt.year)), cust_claims.Age) 


# In[41]:


#Also updating the years in Date of birth column
cust_claims['DateOfBirth']= np.where(cust_claims.Age<0, (cust_claims.DateOfBirth- pd.offsets.DateOffset(years=100)), cust_claims.DateOfBirth) 


# In[42]:


cust_claims['Age group']=pd.cut(cust_claims.Age,  bins=[0,18, 30, 60, 100] , labels=['Children', 'Youth', 'Adult', 'Senior'])


# In[43]:


cust_claims.head()


# ### 8. What is the average amount claimed by the customers from various segments?

# In[44]:


round(cust_claims.groupby(cust_claims.Segment)['claim_amount'].mean(),2)


# ### 9. What is the total claim amount based on incident cause for all the claims that have been done at least 20 days prior to 1st of October, 2018.

# In[45]:


q9_df= cust_claims[cust_claims.claim_date<pd.to_datetime('10-01-2018')- pd.offsets.DateOffset(days=20)]


# In[46]:


q9_df.groupby(q9_df.incident_cause)['claim_amount'].sum()


# ### 10. How many adults from TX, DE and AK claimed insurance for driver related issues and causes?

# In[47]:


cust_claims[(cust_claims.State.isin(['TX','DE','AK'])) & (cust_claims['Age group']=='Adult') & (cust_claims.incident_cause.str.lower().str.contains('driver'))].shape[0]


# ### 11. Draw a pie chart between the aggregated value of claim amount based on gender and segment. Represent the claim amount as a percentage on the pie chart.

# In[48]:


# cust_claims.groupby(['Segment','gender'])['claim_amount'].sum()


# In[49]:


seg_gen= cust_claims.pivot_table(index='Segment',columns='gender', values='claim_amount', aggfunc=sum)


# In[50]:


seg_gen


# In[51]:


seg_gen.T.plot(kind='pie', subplots=True, figsize=(15,8),legend=False, autopct='%1.1f%%')


# ### 12. Among males and females, which gender had claimed the most for any type of driver related issues? E.g. This metric can be compared using a bar chart.

# In[52]:


cust_claims[cust_claims.incident_cause.str.lower().str.contains('driver')].groupby('gender')['claim_id'].count().plot(kind='bar',ylabel= 'number of driver related claims')

Clearly Males have claimed more for any driver related issues. 
# ### 13. Which age group had the maximum fraudulent policy claims? Visualize it on a bar chart.

# In[53]:


cust_claims[cust_claims.fraudulent.str.lower()=='yes'].groupby('Age group')['claim_id'].count().plot(kind='bar', ylabel= 'Number of fradulent claims')

Clearly Adults have claimed maxium number of fradulent poilicies follwed by youth and seniors.Children have no fradulaent claims.
# ### 14. Visualize the monthly trend of the total amount that has been claimed by the customers. Ensure that on the “month” axis, the month is in a chronological order not alphabetical order.

# In[54]:


cust_claims.groupby([cust_claims.claim_date.dt.month, cust_claims.claim_date.dt.month_name()])['claim_amount'].sum().plot(kind='bar',xlabel='Month', ylabel='total claim amount')

Most claims have been made in October and least in November. 
# ### 15. What is the average claim amount for gender and age categories and suitably represent the above using a facetted bar chart, one facet that represents fraudulent claims and the other for non-fraudulent claims. 

# In[140]:


fraud_age_gender_amt= pd.DataFrame(cust_claims[cust_claims.fraudulent.str.lower()=='yes'].groupby(["gender","Age group"])[["claim_amount"]].mean().add_prefix("Fraud_"))
fraud_age_gender_amt


# In[144]:


authentic_age_gender_amt=pd.DataFrame(cust_claims[cust_claims.fraudulent.str.lower()!='yes'].groupby(["gender","Age group"])[["claim_amount"]].mean().add_prefix("Authentic_"))
authentic_age_gender_amt


# In[145]:


fraud_authentic_amt= round(pd.merge(fraud_age_gender_amt,authentic_age_gender_amt, on=["gender","Age group"]),2)
fraud_authentic_amt


# In[146]:


fraud_authentic_amt.plot(kind="bar", subplots= True, legend= True,figsize=(10,10))
plt.show()


# ### Based on the conclusions from exploratory analysis as well as suitable statistical tests, answer the below questions. Please include a detailed write-up on the parameters taken into consideration, the Hypothesis testing steps, conclusion from the p-values and the business implications of the statements.

# In[60]:


import scipy.stats as stats


# ### 16. Is there any similarity in the amount claimed by males and females?

# In[61]:


cust_claims.groupby('gender')['claim_amount'].sum()

to check whether there is a similarity between the ammount claimed by males and females, we will compare means of amount claimed by males anf females. 

Ho- mean(males)= mean(females)
H1- mean(males)<> mean(females) 
# In[62]:


amount = 'claim_amount'

male_spend = cust_claims.loc[ cust_claims.gender == 'Male', amount ]
female_spend = cust_claims.loc[ cust_claims.gender == 'Female', amount ]

print( 'mean of male spend: ', round(male_spend.mean(),2), '| mean of female spend: ', round(female_spend.mean(),2) )

H0 - u1 = u2
Ha - u1 <> u2

CI - 95%
p - 0.05
# #### Using t test to check the relation 

# In[63]:


stats.ttest_ind( male_spend, female_spend )


# In[118]:


# p value of the test

p_16 = stats.ttest_ind( male_spend, female_spend ).pvalue
p_16


# In[119]:


# Checking if p value is greater than or less than 0.05.

if(p_16<0.05):
    print('We reject null hypothesis')
else:
    print('We fail to reject null hypothesis')

Business conclusion- The amounts claimed by men and women are similar, implying gender doesn't impact claimed amount. 
# ### 17. Is there any relationship between age category and segment?

# #### Using Chi Square test to check the relationship because age category and segment because these are two categorical variables. 
H0 - No relationship
Ha - There is a relationship among the variables

CI - 95%
p - 0.05
# In[66]:


obs_freq = pd.crosstab( cust_claims['Age group'], cust_claims['Segment'])


# In[67]:


obs_freq


# In[68]:


stats.chi2_contingency(obs_freq)


# In[120]:


p_17= stats.chi2_contingency(obs_freq)[1]
p_17


# In[121]:


# Checking if p value is greater than or less than 0.05.

if(p_17<0.05):
    print('We reject null hypothesis')
else:
    print('We fail to reject null hypothesis')

Business conclusion: The age category does not impact the segment the customer belongs to. 
# ### 18. The current year has shown a significant rise in claim amounts as compared to 2016-17 fiscal average which was $10,000.
H0: u=10000
H1: u>10000

CI: 95%
p value= 0.05
# In[71]:


s1= cust_claims.loc[cust_claims.claim_date.dt.year==2018, 'claim_amount']


# In[72]:


s1.mean()


# In[73]:


stats.ttest_1samp(s1,10000)


# In[122]:


p_18= stats.ttest_1samp(s1,10000).pvalue
p_18


# In[123]:


# Checking if p value is greater than or less than 0.05.

if(p_18<0.05):
    print('We reject null hypothesis')
else:
    print('We fail to reject null hypothesis')

Business conclusion: The claim amounts have significantly risen in the current year.
# ### 19. Is there any difference between age groups and insurance claims?

# In[74]:


cust_claims['Age group'].value_counts()


# In[75]:


s1_19=cust_claims.loc[cust_claims['Age group']=='Adult', 'total_policy_claims']
s2_19=cust_claims.loc[cust_claims['Age group']=='Youth', 'total_policy_claims']
s3_19=cust_claims.loc[cust_claims['Age group']=='Senior', 'total_policy_claims']
s4_19=cust_claims.loc[cust_claims['Age group']=='Children', 'total_policy_claims']


# In[76]:


cust_claims.shape


# In[77]:


print( 'mean s1_19:', s1_19.mean(), '| mean s2_19:', s2_19.mean(), '| mean s3_19:', s3_19.mean(), '| mean s4_19:', s4_19.mean())

H0 - No difference between age groups and insurance claims (means are from same population)
Ha - difference between age groups and insurance claims (means are from different population) 

CI - 95%
p - 0.05
# In[78]:


# Performing f-test or ANOVA 

stats.f_oneway(s1_19,s2_19,s3_19)


# In[124]:


# p value of the f test 

p_19=stats.f_oneway(s1_19,s2_19,s3_19).pvalue
p_19


# In[126]:


# Checking if p value is greater than or less than 0.05.

if(p_19<0.05):
    print('We reject null hypothesis')
else:
    print('We fail to reject null hypothesis')

Business conclusion: Age groups do not impact the number of insurance claims. 
# ### 20. Is there any relationship between total number of policy claims and the claimed amount?

# ####  Creating m saples of different number of total policy claims to use ANOVA to test the claim

# In[105]:


list1=[]
for i in cust_claims.total_policy_claims.unique():
    list1.append(cust_claims.loc[cust_claims['total_policy_claims']==i, 'claim_amount' ])

H0 - No relationship between number of policy claims and claimed amount. (means are from same population)
Ha - There is a relationship between number of policy claims and claimed amount. (means are from different population) 

CI - 95%
p - 0.05
# In[108]:


stats.f_oneway(list1[0],list1[1],list1[2],list1[3],list1[4],list1[5],list1[6],list1[7])


# In[111]:


p= stats.f_oneway(list1[0],list1[1],list1[2],list1[3],list1[4],list1[5],list1[6],list1[7]).pvalue
p


# In[112]:


# Checking if p value is greater than or less than 0.05.

if(p<0.05):
    print('We reject null hypothesis')
else:
    print('We fail to reject null hypothesis')

Business conclusion: Number of policy claims do not impact the amount claimed
# #### Treating the number of policy claims as a ordinal categorical variable, using spearsman rank to test the relationship between claimed amount and number of policy claims
H0 - No relationship between number of policy claims and claimed amount. (means are from same population)
Ha - There is a relationship between number of policy claims and claimed amount. (means are from different population) 

CI - 95%
p - 0.05
# In[113]:


stats.spearmanr(cust_claims.total_policy_claims,cust_claims.claim_amount)


# In[114]:


p= stats.spearmanr(cust_claims.total_policy_claims,cust_claims.claim_amount).pvalue
p


# In[116]:


# Checking if p value is greater than or less than 0.05.

if(p<0.05):
    print('We reject null hypothesis')
else:
    print('We fail to reject null hypothesis')

Business conclusion: Number of policy claims do not impact the amount claimed
# In[ ]:




