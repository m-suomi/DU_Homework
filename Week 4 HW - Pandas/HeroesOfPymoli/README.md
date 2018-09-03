
## Heroes of Pymolia - Final Data Analysis
#### By: Mike Suomi 6/3/2018

- Observed Trend 1: The Normalized Purchase Total per user is the lowest for the 15-24 age range, but this is our largest user demographic so targeting this range to increase more multiple purchases would help our profit the most. 


- Observed Trend 2: We need to figure out how to entice our users to make multiple purchases. Only six of our users have more than three purchases and the vast majority of our users only have one purchase.  How can we get them playing longer and/or entice them to buy more add-ons to increase the longevity of our game and long-term revenue?


- Observed Trend 3: How do we increase the sale of our top sellers? Out of 780 purchases, our two top sellers only have 11 purchases each (and these are relatively cheap items at around 2.30).  If we can't successfully increase the frequency of top sellers, than we should increase purchase price for many of our items, because our largest revenue items are those that have a higher purchase price and still relatively low purchase count (around 4.00 and 6 to 9 purchases).


```python
import pandas as pd
import numpy as np
```


```python
#import json file to dataframe
json_file_path = 'purchase_data.json'

df = pd.read_json(json_file_path)
```

### Player Count


```python
player_count = len(df.SN.unique())  #the json data is all purchases, so make sure have unique SNs
pd.DataFrame({'Total Unique Players': [player_count]})
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Unique Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>573</td>
    </tr>
  </tbody>
</table>
</div>



### Purchasing Analysis (Total)


```python
num_unique_items_purchased = len(df['Item ID'].unique())
average_purchase_price = df.Price.mean()
total_num_purchases = df.Price.count()
total_revenue = df.Price.sum()
purchasing_totals_df = pd.DataFrame([[num_unique_items_purchased,
                                    average_purchase_price,
                                    total_num_purchases,
                                    total_revenue]],
                                    columns = ['Number of Unique Items',
                                                'Average Purchase Price',
                                                'Total Number of Purchases',
                                                'Total Revenue'])

purchasing_totals_df['Average Purchase Price'] = purchasing_totals_df[
                                                'Average Purchase Price'].apply('${:.2f}'.format)
purchasing_totals_df['Total Revenue'] = purchasing_totals_df[
                                                'Total Revenue'].apply('${:.2f}'.format)

purchasing_totals_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Number of Unique Items</th>
      <th>Average Purchase Price</th>
      <th>Total Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>183</td>
      <td>$2.93</td>
      <td>780</td>
      <td>$2286.33</td>
    </tr>
  </tbody>
</table>
</div>



### Gender Demographics


```python
df_unique_users = df.drop_duplicates(subset=['SN'])[['SN','Age','Gender']] #get a df with only unique users

gender_counts = df_unique_users.Gender.value_counts()

df_gender_counts = pd.DataFrame(gender_counts) #convert gender counts to df
df_gender_counts.rename(columns = {'Gender':'Total Count'}, inplace=True)

df_gender_counts['% of Players'] = (df_gender_counts['Total Count'] / df_gender_counts['Total Count'].sum())*100
df_gender_counts['% of Players'] = df_gender_counts['% of Players'].apply('{:.2f}%'.format)

df_gender_counts = df_gender_counts[['% of Players','Total Count']] #reverse column order

gender_counts  = gender_counts.to_dict()  #store the gender user counts to a dictionary for later use

df_gender_counts
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>% of Players</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>81.15%</td>
      <td>465</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>17.45%</td>
      <td>100</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>1.40%</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>



### Purchasing Analysis (Gender)


```python
gender_analysis = df.groupby('Gender').agg({'Age': np.count_nonzero, 
                                           'Price': np.mean})
gender_analysis.rename(columns = {'Age':'Purchase Count', 'Price': 'Average Purchase Price'}, inplace=True) 

gender_analysis['Total Purchase Value'] = df.groupby('Gender')['Price'].sum()

#normalized totals is looking for average purchase total per user (instead of per purchase)
#create a list of values that can then be passed into dataframe column
num_rows_in_gender_analysis = len(gender_analysis['Total Purchase Value'])
gender_norm_tot = [gender_analysis['Total Purchase Value'][row] / #lookup total purchase value
                 gender_counts[gender_analysis.index[row]] #lookup the user count based on gender index
                 for row in range(0, num_rows_in_gender_analysis)]

gender_analysis['Normalized Totals'] = gender_norm_tot

gender_analysis[['Average Purchase Price', 'Total Purchase Value', 'Normalized Totals']]=gender_analysis[
                ['Average Purchase Price', 'Total Purchase Value', 'Normalized Totals']].applymap(
                                                                                '${:.2f}'.format)
gender_analysis
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>136</td>
      <td>$2.82</td>
      <td>$382.91</td>
      <td>$3.83</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>633</td>
      <td>$2.95</td>
      <td>$1867.68</td>
      <td>$4.02</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>11</td>
      <td>$3.25</td>
      <td>$35.74</td>
      <td>$4.47</td>
    </tr>
  </tbody>
</table>
</div>



### Age Demographics


```python
min_age = df_unique_users.Age.min()
max_age = df_unique_users.Age.max()

bins = list(range(9,max_age,5)) #starts with first bin edge at 9 and then counts up by 5 until one before max
labels = [str(bins[idx]+1)+"-"+str(bins[idx+1]) for idx in range(0,len(bins)-1)] #names the labels for the bin range (inclusive)

#insert the starting and ending bins/labels to capture all data
bins.insert(0,0)
labels.insert(0,'<10')
bins.append(max_age)
labels.append(str(bins[-2]+1)+"+")
#print(bins) # temporary check
#print(labels) # temporary check

#add bins cut to both the unique users df and the overall df for later use
df_unique_users['Age Group'] = pd.cut(df_unique_users['Age'], bins=bins, labels=labels)
df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

age_group_counts = df_unique_users['Age Group'].value_counts(sort=False)

df_age_group_counts = pd.DataFrame(age_group_counts) #convert age counts to df
df_age_group_counts.rename(columns = {'Age Group':'Total Count'}, inplace=True)

df_age_group_counts['% of Players'] = (df_age_group_counts['Total Count'] / df_age_group_counts['Total Count'].sum())*100
df_age_group_counts['% of Players'] = df_age_group_counts['% of Players'].apply('{:.2f}%'.format)
df_age_group_counts = df_age_group_counts[['% of Players','Total Count']] #reverse column order

age_group_counts  = age_group_counts.to_dict() #convert age group counts to dict for later use

df_age_group_counts
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>% of Players</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>3.32%</td>
      <td>19</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>4.01%</td>
      <td>23</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>17.45%</td>
      <td>100</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>45.20%</td>
      <td>259</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>15.18%</td>
      <td>87</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>8.20%</td>
      <td>47</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>4.71%</td>
      <td>27</td>
    </tr>
    <tr>
      <th>40-44</th>
      <td>1.75%</td>
      <td>10</td>
    </tr>
    <tr>
      <th>45+</th>
      <td>0.17%</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



### Purchasing Analysis (Age)


```python
age_analysis = df.groupby('Age Group').agg({'Age': np.count_nonzero, 
                                           'Price': np.mean})
age_analysis.rename(columns = {'Age':'Purchase Count', 'Price': 'Average Purchase Price'}, inplace=True) 

age_analysis['Total Purchase Value'] = df.groupby('Age Group')['Price'].sum()

#normalized totals is looking for average purchase total per user (instead of per purchase)
#create a list of values that can then be passed into dataframe column
num_rows_in_age_analysis = len(age_analysis['Total Purchase Value'])
age_norm_tot = [age_analysis['Total Purchase Value'][row] / #lookup total purchase value
                 age_group_counts[age_analysis.index[row]] #lookup the user count based on age group index
                 for row in range(0, num_rows_in_age_analysis)]

age_analysis['Normalized Totals'] = age_norm_tot

age_analysis[['Average Purchase Price', 'Total Purchase Value', 'Normalized Totals']]=age_analysis[
                ['Average Purchase Price', 'Total Purchase Value', 'Normalized Totals']].applymap(
                                                                                '${:.2f}'.format)
age_analysis
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Age Group</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>28</td>
      <td>$2.98</td>
      <td>$83.46</td>
      <td>$4.39</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>35</td>
      <td>$2.77</td>
      <td>$96.95</td>
      <td>$4.22</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>133</td>
      <td>$2.91</td>
      <td>$386.42</td>
      <td>$3.86</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>336</td>
      <td>$2.91</td>
      <td>$978.77</td>
      <td>$3.78</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>125</td>
      <td>$2.96</td>
      <td>$370.33</td>
      <td>$4.26</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>64</td>
      <td>$3.08</td>
      <td>$197.25</td>
      <td>$4.20</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>42</td>
      <td>$2.84</td>
      <td>$119.40</td>
      <td>$4.42</td>
    </tr>
    <tr>
      <th>40-44</th>
      <td>16</td>
      <td>$3.19</td>
      <td>$51.03</td>
      <td>$5.10</td>
    </tr>
    <tr>
      <th>45+</th>
      <td>1</td>
      <td>$2.72</td>
      <td>$2.72</td>
      <td>$2.72</td>
    </tr>
  </tbody>
</table>
</div>



### Top Spenders


```python
user_spending = df.groupby('SN').agg({'Item Name': np.count_nonzero, 
                                           'Price': np.mean})
user_spending.rename(columns = {'Item Name':'Purchase Count', 'Price': 'Average Purchase Price'}, inplace=True) 

user_spending['Total Purchase Value'] = df.groupby('SN')['Price'].sum()

#get top 5 values by total purchase value before formatting changes to strings
user_spending_top5 = user_spending.nlargest(5, 'Total Purchase Value')
user_spending_top5
user_spending_top5[['Average Purchase Price', 'Total Purchase Value']]=user_spending_top5[
               ['Average Purchase Price', 'Total Purchase Value']].applymap('${:.2f}'.format)

user_spending_top5
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Undirrala66</th>
      <td>5</td>
      <td>$3.41</td>
      <td>$17.06</td>
    </tr>
    <tr>
      <th>Saedue76</th>
      <td>4</td>
      <td>$3.39</td>
      <td>$13.56</td>
    </tr>
    <tr>
      <th>Mindimnya67</th>
      <td>4</td>
      <td>$3.18</td>
      <td>$12.74</td>
    </tr>
    <tr>
      <th>Haellysu29</th>
      <td>3</td>
      <td>$4.24</td>
      <td>$12.73</td>
    </tr>
    <tr>
      <th>Eoda93</th>
      <td>3</td>
      <td>$3.86</td>
      <td>$11.58</td>
    </tr>
  </tbody>
</table>
</div>



### Most Popular Items


```python
popular_items = df.groupby(['Item ID', 'Item Name']).agg({'SN': np.count_nonzero, 
                                                       'Price': np.mean})
popular_items.rename(columns = {'SN':'Purchase Count', 'Price': 'Item Price'}, inplace=True) 

popular_items['Total Purchase Value'] = df.groupby(['Item ID','Item Name'])['Price'].sum()
#popular_items

#get top 5 purchased items by purchase count before formatting changes to strings
popular_items_top5 = popular_items.nlargest(5, 'Purchase Count')
#popular_items_top5
popular_items_top5[['Item Price', 'Total Purchase Value']]=popular_items_top5[
                    ['Item Price', 'Total Purchase Value']].applymap('${:.2f}'.format)

popular_items_top5
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <th>Betrayal, Whisper of Grieving Widows</th>
      <td>11</td>
      <td>$2.35</td>
      <td>$25.85</td>
    </tr>
    <tr>
      <th>84</th>
      <th>Arcane Gem</th>
      <td>11</td>
      <td>$2.23</td>
      <td>$24.53</td>
    </tr>
    <tr>
      <th>13</th>
      <th>Serenity</th>
      <td>9</td>
      <td>$1.49</td>
      <td>$13.41</td>
    </tr>
    <tr>
      <th>31</th>
      <th>Trickster</th>
      <td>9</td>
      <td>$2.07</td>
      <td>$18.63</td>
    </tr>
    <tr>
      <th>34</th>
      <th>Retribution Axe</th>
      <td>9</td>
      <td>$4.14</td>
      <td>$37.26</td>
    </tr>
  </tbody>
</table>
</div>



### Most Profitable Items


```python
#can use most popular data frame and just sort out top 5 profitable items
profitable_items_top5 = popular_items.nlargest(5, 'Total Purchase Value')
#profitable_items_top5
profitable_items_top5[['Item Price', 'Total Purchase Value']]=profitable_items_top5[
                    ['Item Price', 'Total Purchase Value']].applymap('${:.2f}'.format)

profitable_items_top5
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34</th>
      <th>Retribution Axe</th>
      <td>9</td>
      <td>$4.14</td>
      <td>$37.26</td>
    </tr>
    <tr>
      <th>115</th>
      <th>Spectral Diamond Doomblade</th>
      <td>7</td>
      <td>$4.25</td>
      <td>$29.75</td>
    </tr>
    <tr>
      <th>32</th>
      <th>Orenmir</th>
      <td>6</td>
      <td>$4.95</td>
      <td>$29.70</td>
    </tr>
    <tr>
      <th>103</th>
      <th>Singed Scalpel</th>
      <td>6</td>
      <td>$4.87</td>
      <td>$29.22</td>
    </tr>
    <tr>
      <th>107</th>
      <th>Splitter, Foe Of Subtlety</th>
      <td>8</td>
      <td>$3.61</td>
      <td>$28.88</td>
    </tr>
  </tbody>
</table>
</div>


