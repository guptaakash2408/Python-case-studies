#!/usr/bin/env python
# coding: utf-8

# In[154]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[155]:


file_path= "C:/Users/DELL/Desktop/Python case studies/Credit card/"


# In[156]:


customer_acqusition= pd.read_csv(file_path+"Customer Acqusition.csv")
customer_acqusition.head()


# In[157]:


customer_acqusition.info()


# In[230]:


#Checking for duplicate customers 

customer_acqusition['Customer'].duplicated().sum()


# In[158]:


#Checking for duplicates in the customers table.

customer_acqusition.duplicated().sum()


# In[159]:


spend= pd.read_csv(file_path+"spend.csv")
spend.head()


# In[160]:


spend.info()


# In[161]:


# Converting the month column in dateset from object to datetime.
spend['Month']= pd.to_datetime(spend.Month)


# In[162]:


#Checking for duplicates in the spend table.

spend.duplicated().sum()


# In[163]:


repayment= pd.read_csv(file_path+"Repayment.csv")
repayment.head()


# In[164]:


repayment.info()


# In[165]:


# Converting the month column in dateset from object to datetime.
spend['Month']= pd.to_datetime(spend.Month)


# In[166]:


# Converting the month column in repayment dateset from object to datetime.
repayment['Month']= pd.to_datetime(repayment.Month)


# In[167]:


#Checking for duplicates in the repayment table.


repayment.duplicated().sum()


# ### 1. In the above dataset,
# ###  a. In case age is less than 18, replace it with mean of age values.

# In[168]:


# Checking for customers with age less than 18 years

customer_acqusition[customer_acqusition.Age<18]


# In[169]:


# Mean age of the customers

customer_acqusition.Age.mean()


# In[170]:


#Replacing the customers' age with age<18 with mean age of the dataset.  

customer_acqusition['Age']= pd.Series(np.where(customer_acqusition.Age<18, customer_acqusition.Age.mean(), customer_acqusition.Age ).astype(int))


# In[171]:


# Checking for customers with age less than 18 years

customer_acqusition[customer_acqusition.Age<18]


# In[172]:


print('Implies all customers\' ages with age less than 18 have been replaced with the mean age.')


# ###  b. In case spend amount is more than the limit, replace it with 50% of that customer’s limit. 
# ### (customer’s limit provided in acquisition table is the per transaction limit on his card)

# In[173]:


spend


# In[174]:


spend.dtypes


# In[175]:


q1_df = pd.merge(left=spend, right= customer_acqusition, how= 'left', on='Customer', indicator=True )


# In[176]:


q1_df[q1_df.Amount> q1_df.Limit]


# In[177]:


spend['Amount']=pd.Series(np.where(q1_df.Amount> q1_df.Limit, (1/2)*q1_df.Limit, q1_df.Amount ))


# In[178]:


#Also changing the amount in the q1_df dataframe

q1_df['Amount']=pd.Series(np.where(q1_df.Amount> q1_df.Limit, (1/2)*q1_df.Limit, q1_df.Amount ))


# In[179]:


spend.head()


# ###  c. Incase the repayment amount is more than the limit, replace the repayment with the limit.

# In[180]:


q1_df2= pd.merge(left=repayment, right= customer_acqusition, how= 'left', on='Customer', indicator=True )


# In[181]:


q1_df2[q1_df2.Amount> q1_df2.Limit]


# In[182]:


repayment['Amount']=pd.Series(np.where(q1_df2.Amount> q1_df2.Limit, q1_df.Limit, q1_df.Amount ))


# In[183]:


#Also changing the amount in q1_df2 dataframe.

q1_df2['Amount']=pd.Series(np.where(q1_df2.Amount> q1_df2.Limit, q1_df.Limit, q1_df.Amount ))


# In[184]:


repayment.head()


# ### 2. From the above dataset create the following summaries:
# ### a. How many distinct customers exist?

# In[186]:


customer_acqusition.Customer.nunique()


# ### b. How many distinct categories exist?

# In[187]:


print(f"{customer_acqusition.Product.nunique()} distinct categories exist which are:\n" )
print(customer_acqusition.Product.unique()) 


# ###  c. What is the average monthly spend by customers?

# In[233]:


round((spend.groupby([spend.Month.dt.month_name(),spend.Customer] )['Amount'].sum()).mean(),2)


# ###  d. What is the average monthly repayment by customers?

# In[238]:


round((repayment.groupby([repayment.Month.dt.month_name(),repayment.Customer])['Amount'].sum()).mean(),2)


# ###  e. If the monthly rate of interest is 2.9%, what is the profit for the bank for each month? 
# ### (Profit is defined as interest earned on Monthly Profit. Monthly Profit = Monthly repayment 
# ### '– Monthly spend. Interest is earned only on positive profits and not on negative amounts)

# In[259]:


repayment['year']=pd.Series(repayment.Month.dt.year)
repayment['Month_no']=pd.Series(repayment.Month.dt.month)
repayment['Month_name']=pd.Series(repayment.Month.dt.month_name())


# In[262]:


spend['year']=pd.Series(spend.Month.dt.year)
spend['Month_no']=pd.Series(spend.Month.dt.month)
spend['Month_name']=pd.Series(spend.Month.dt.month_name())


# In[274]:


df_repayment.head()


# In[268]:


df_repayment= repayment.groupby(['year','Month_no','Month_name'])['Amount'].sum().reset_index()


# In[270]:


df_spend= spend.groupby(['year','Month_no','Month_name'])['Amount'].sum().reset_index()


# In[276]:


df_repay_spend= pd.merge( left = df_repayment, right = df_spend, 
             how = 'inner', left_on = ['year', 'Month_no', 'Month_name'], right_on =['year', 'Month_no', 'Month_name'], indicator=True, suffixes=['_repayment', '_spend'])


# In[279]:


df_repay_spend.head()


# In[278]:


df_repay_spend['Profit']= pd.Series(df_repay_spend['Amount_repayment']-df_repay_spend['Amount_spend'])


# In[283]:


df_repay_spend['Monthly_interest']= round(pd.Series(np.where(df_repay_spend.Profit>0, (2.9/100)*df_repay_spend.Profit, 0 )),2)


# In[284]:


#The column of monthy interest is monthly profit

df_repay_spend.head() 


# ### f. What are the top 5 product types?

# In[193]:


#top 5 product types

q1_df.groupby('Type').Amount.sum().reset_index().sort_values('Amount', ascending=False).head(5)['Type']


# ###  g. Which city is having maximum spend?

# In[194]:


q2_df= q1_df.groupby('City')['Amount'].sum().reset_index()


# In[195]:


q2_df[q2_df.Amount==q2_df.Amount.max()].City.item()


# In[196]:


print(f'{q2_df[q2_df.Amount==q2_df.Amount.max()].City.item().capitalize()} has the maximum spend.')


# In[286]:


#Alternatively

(q1_df.groupby('City')['Amount'].sum().reset_index().sort_values('Amount', ascending=False)).head(1)['City'].item()


# ### h. Which age group is spending more money?

# In[198]:


q1_df.Age.max()


# In[199]:


q1_df['Age group']=pd.cut(q1_df.Age,  bins=[0, 1, 12, 19, 60, 100] , labels=['Infant', 'Kid', 'Teenager', 'Grownup', 'Senior Citizen'])
q1_df


# In[200]:


age_group=round(q1_df.groupby('Age group')['Amount'].sum()).reset_index().sort_values('Amount', ascending=False).head(1)['Age group'].item()
age_group


# In[201]:


print(f'{age_group}s are spending more money.')


# ### i. Who are the top 10 customers in terms of repayment?

# In[202]:


#Calculated the top 10 customers in trms of repayment by total amount repaid by these customers.

q1_df2.groupby('Customer')['Amount'].sum().reset_index().sort_values('Amount', ascending=False).head(10)['Customer']


# ### 3. Calculate the city wise spend on each product on yearly basis. Also include a graphical representation for the same.

# In[203]:


q3_df1=q1_df.pivot_table(index='City', columns=[ 'Product', q1_df.Month.dt.year], values='Amount', aggfunc='sum')
q3_df1


# In[204]:


#plotted a stacked bar graph 

q3_df1.plot(kind='bar', stacked=True, figsize=(10,7))
plt.legend( title='product, year', bbox_to_anchor=(1.04, 1), loc="upper left")
plt.show()


# ### 4. Create graphs for
# ### a. Monthly comparison of total spends, city wise

# In[205]:


summ = q1_df.pivot_table( index=[q1_df.Month.dt.month,q1_df.Month.dt.month_name()], columns='City', values='Amount', aggfunc='sum')
summ


# In[206]:


summ.plot(kind='line', stacked=True, title='Monthly comparison of city wise total spends', figsize=(20,10))
plt.legend( title='City', bbox_to_anchor=(1.04, 1), loc="upper left")
plt.legend( title='City', bbox_to_anchor=(1.04, 1), loc="upper left")


# In[207]:


plt.figure(figsize=(20,10))
q1_df.groupby(['City', q1_df.Month.dt.month,q1_df.Month.dt.month_name() ])['Amount'].sum().plot()


# ###  b. Comparison of yearly spend on air tickets

# In[208]:


q4b_df=q1_df.groupby([q1_df.Month.dt.year,'Type'])['Amount'].sum().reset_index()
q4b_df[q4b_df.Type=='AIR TICKET'].plot(x='Month', y='Amount', kind='bar')

From the graph it seems that the maximum ammount was spent in the year 2005.
# ### c. Comparison of monthly spend for each product (look for any seasonality that exists in terms of spend)

# In[209]:


q4c_df=q1_df.groupby([q1_df.Month.dt.month,q1_df.Month.dt.month_name(),'Product'])['Amount'].sum()
q4c_df.index.names=['Month No', 'Month', 'Product']
q4c_df=q4c_df.reset_index()
q4c_df
qc4_pivot=q4c_df.pivot_table(index=['Month No', 'Month'], columns='Product', values='Amount', aggfunc=sum).plot(figsize=(12,6))
plt.xlabel('Month')

From the above graph we can interpret that the spend using credit card was high for all three items during May and November. The sales also peaked for silver during March. 
# ### 5. Write user defined PYTHON function to perform the following analysis:
# ### You need to find top 10 customers for each city in terms of their repayment amount by different products and by different time periods i.e. year or month. The user should be able to specify the product (Gold/Silver/Platinum) and time period (yearly or monthly) and the function should automatically take these inputs while identifying the top 10 customers.

# In[295]:


#step 1= create a df with the product, month and year with repayment as left table

q1_df2['Month name']=pd.Series(q1_df2.Month.dt.month_name())
q1_df2['Year']=pd.Series(q1_df2.Month.dt.year)
q1_df2.head()


# In[311]:


def top10Customers(product_category,time_period):
    product_category=product_category.capitalize()
    time_period=time_period.capitalize()
    if time_period=='Yearly':
        time_period='Year'
    elif time_period=='Monthly':
        time_period='Month name'
    return q1_df2[(q1_df2.Product == product_category)].groupby(['Product',time_period,'City','Customer']).Amount.sum().reset_index().sort_values('Amount',ascending=False).head(10)


# In[325]:


product_category=str(input("Enter Product Category and product category should be in Gold/Silver/Platinum:  "))
time_period=str(input("Enter Time Period and time period should be in yearly/monthly: "))


# In[326]:


top10Customers(product_category,time_period)

