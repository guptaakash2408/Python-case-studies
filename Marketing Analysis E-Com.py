#!/usr/bin/env python
# coding: utf-8

# ### Required Packages

# In[58]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt


# ### Datasets

# In[2]:


cust = pd.read_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/CUSTOMERS.csv')
loc = pd.read_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/GEO_LOCATION.csv')
ord_item = pd.read_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/ORDER_ITEMS.csv')
ord_pay = pd.read_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/ORDER_PAYMENTS.csv')
ord_rate = pd.read_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/ORDER_REVIEW_RATINGS.csv')
order = pd.read_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/ORDERS.csv')
product = pd.read_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/PRODUCTS.csv')
seller = pd.read_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/SELLERS.csv')


# In[3]:


#df1 Order & Order Payment
df1 = pd.merge(left=order,right=ord_pay,how='left',left_on='order_id',right_on='order_id')


# In[4]:


#df2 Order Rating
df2 = pd.merge(left=df1,right=ord_rate,how='left',left_on=['order_id'],right_on=['order_id'])


# In[5]:


#df3 Order Items
df3 = pd.merge(left=df2,right=ord_item,how='left',left_on=['order_id'],right_on=['order_id'])


# In[6]:


#df4 Products
df4 = pd.merge(left=df3,right=product,how='left',left_on=['product_id'],right_on=['product_id'])


# In[7]:


#df5 sellers
df5 = pd.merge(left=df4,right=seller,how='left',left_on=['seller_id'],right_on=['seller_id'])


# In[8]:


#df6 Customers
df6 = pd.merge(left=df5,right=cust,how='left',left_on=['customer_id'],right_on=['customer_id'])


# In[9]:


#df7 sellers
df7 = pd.merge(left=df6,right=loc,how='left',left_on=['seller_zip_code_prefix'],right_on=['geolocation_zip_code_prefix'])


# In[10]:


#df8 sellers
df8 = pd.merge(left=df7,right=loc,how='left',left_on=['customer_zip_code_prefix'],right_on=['geolocation_zip_code_prefix'],suffixes=('_Seller','_Cust'))


# In[11]:


df8.to_csv('C:/Users/Nithin/Downloads/Python Foundation End to End Case Study E-Commerce Analytics Project/Datasets/Final.csv')


# In[12]:


df_final = df8.loc[:,['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp',
'order_approved_at', 'order_delivered_carrier_date',
'order_delivered_customer_date', 'order_estimated_delivery_date',
'payment_sequential', 'payment_type', 'payment_installments',
'payment_value', 'review_id', 'review_score', 'review_creation_date',
'review_answer_timestamp', 'order_item_id', 'product_id', 'seller_id',
'shipping_limit_date', 'price', 'freight_value',
'product_category_name', 'product_name_lenght',
'product_description_lenght', 'product_photos_qty', 'product_weight_g',
'product_length_cm', 'product_height_cm', 'product_width_cm',
'seller_zip_code_prefix','geolocation_lat_Seller','geolocation_lng_Seller' ,'seller_city', 'seller_state',
'customer_unique_id', 'customer_zip_code_prefix', 'customer_city',
'customer_state','geolocation_lat_Cust',
'geolocation_lng_Cust']]


# ### Data Preparation

# In[13]:


df_final.order_purchase_timestamp = pd.to_datetime(df_final.order_purchase_timestamp, format = '%m/%d/%Y %H:%M')
df_final.order_approved_at = pd.to_datetime(df_final.order_approved_at, format = '%m/%d/%Y %H:%M')
df_final.order_delivered_carrier_date = pd.to_datetime(df_final.order_delivered_carrier_date, format = '%m/%d/%Y %H:%M')
df_final.order_estimated_delivery_date = pd.to_datetime(df_final.order_estimated_delivery_date, format = '%m/%d/%Y %H:%M')
df_final.review_creation_date = pd.to_datetime(df_final.review_creation_date, format = '%m/%d/%Y %H:%M')
df_final.review_answer_timestamp = pd.to_datetime(df_final.review_answer_timestamp, format = '%m/%d/%Y %H:%M')
df_final.shipping_limit_date = pd.to_datetime(df_final.shipping_limit_date, format = '%m/%d/%Y %H:%M')


# ### 1.	Perform Detailed exploratory analysis
# 
# ##### a.	Define & calculate high level metrics like (Total Revenue, Total quantity, Total products, Total categories, Total sellers, Total locations, Total channels, Total payment methods etc…)
# 
# ##### b.	Understanding how many new customers acquired every month
# 
# ##### c.	Understand the retention of customers on month on month basis
# 
# ##### d.	How the revenues from existing/new customers on month on month basis
# 
# ##### e.	Understand the trends/seasonality of sales, quantity by category, location, month, week, day, time, channel, payment method etc…
# 
# ##### f.	Popular Products by month, seller, state, category.
# 
# ##### g.	Popular categories by state, month
# 
# ##### h.	List top 10 most expensive products sorted by price

# In[38]:


#a.

#Total Revenue
tot_rev = df_final['payment_installments'] * df_final['payment_value']
tot_rev.sum()

#Total Quantity
df_final.order_item_id.count()

#Total Products
df_final.product_id.nunique()

#Total Categories
df_final.product_category_name.nunique()

#Total Sellers
df_final.seller_id.nunique()

#Total Locations
loc.geolocation_zip_code_prefix.nunique()

#Total Payments
df_final.payment_type.nunique()


# In[42]:


df_final.columns


# In[78]:


#b

df9 = df_final.loc[:,['customer_id','order_purchase_timestamp']]
df9['Year_month'] = df9.order_purchase_timestamp.apply(lambda x : pd.Timestamp.strftime(x,format= '%Y/%m'))
df9.drop(columns = 'order_purchase_timestamp',inplace = True)
df10 = pd.DataFrame(df9.groupby('Year_month')['customer_id'].count())
df10


# In[72]:


df10.plot(kind = 'bar',figsize = (15,5))


# In[95]:


#c.

tot_cust = df_final.customer_id.count()


# In[112]:


#d.

df9['Revenue'] = df_final.price + df_final.freight_value
df9.groupby('Year_month').Revenue.sum().plot(kind= 'bar',figsize=(15,5))


# In[122]:


#e

df_final['year_month'] = df_final.order_purchase_timestamp.apply(lambda x : pd.Timestamp.strftime(x,format= '%Y/%m'))
df_final.groupby('year_month').aggregate({'product_id':'count','price':'sum'})


# In[123]:


df_final.groupby('product_category_name').aggregate({'product_id':'count','price':'sum'})


# In[136]:


#f

df_final.groupby(['year_month','product_category_name']).aggregate({'product_id':'count'})


# In[137]:


df_final.groupby(['seller_id','product_category_name']).agg({'product_id':'count'})


# In[148]:


#h.

pd.DataFrame(df_final.groupby('product_id').agg({'price':'sum'})).sort_values('price',ascending=False).head(10)


# ### 2.	Performing Customers/sellers Segmentation
# 
# ##### a.	Divide the customers into groups based on the revenue generated
# 
# ##### b.	Divide the sellers into groups based on the revenue generated

# In[173]:


#a.

df_final['Revenue'] = df_final.price + df_final.freight_value
df11 = pd.DataFrame(df_final.groupby('customer_id').Revenue.sum())
LC = df_final.groupby('customer_id').Revenue.sum().max()* 0.25


# In[174]:


df12 = pd.cut(df11.Revenue,bins=np.arange(0,15000,LC),
              labels=['Low','Avg','Good','High'])
df12


# In[175]:


#b.

df13 = pd.DataFrame(df_final.groupby('seller_id').Revenue.sum())
LC = df_final.groupby('customer_id').Revenue.sum().max()* 0.25


# In[176]:


df14 = pd.cut(df13.Revenue,bins=np.arange(0,15000,LC),
              labels=['Low','Avg','Good','High'])
df14


# ### 3.	Cross-Selling (Which products are selling together)
# 
# ##### Hint: We need to find which of the top 10 combinations of products are selling together in each transaction. (combination of 2 or 3 buying together)
# 

# In[189]:


df15 = df_final.loc[:,['customer_id','order_purchase_timestamp','product_id']].drop_duplicates().sort_values(['customer_id','order_purchase_timestamp'])


# ### 4.	Payment Behaviour
# 
# ##### a. How customers are paying?
# 
# ##### b. Which payment channels are used by most customers?

# In[221]:


#a.

df_final.payment_type.unique()


# In[223]:


#b.

df_final.groupby('payment_type').Revenue.sum().sort_values(ascending = False)


# ### 5.	Customer satisfaction towards category & product
# 
# ##### a.Which categories (top 10) are maximum rated & minimum rated ?
# ##### b.Which products (top10) are maximum rated & minimum rated ?
# ##### c.Average rating by location, seller, product, category, month etc.
# 

# In[240]:


#a

df17 = pd.DataFrame(df_final.groupby('product_category_name').review_score.sum()).sort_values('review_score',ascending=False)
df17.head(10)


# In[239]:


df17.tail(10)


# In[241]:


#b

df18 = pd.DataFrame(df_final.groupby('product_id').review_score.sum()).sort_values('review_score',ascending=False)
df18.head(10)


# In[242]:


df18.tail(10)


# In[245]:


#c

df_final.groupby('customer_state').review_score.mean().round(2)


# In[254]:


df_final.groupby('customer_state').review_score.mean().round(2).plot(kind = 'pie')


# In[248]:


df_final.groupby('seller_id').review_score.mean().round(2)


# In[253]:


df_final.groupby('product_category_name').review_score.mean().round(2)


# In[250]:


df_final.groupby('year_month').review_score.mean().round(2).plot(kind='bar')

