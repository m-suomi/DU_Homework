
#Option 1 PyBank - Week 3 HW
#Try out jupyter and Pandas to solve option 1
#In this challenge, you are tasked with creating a Python script for analyzing the financial
#records of your company. You will be given two sets of revenue data (budget_data_1.csv and 
#budget_data_2.csv). Each dataset is composed of two columns: Date and Revenue. (Thankfully, 
#your company has rather lax standards for accounting so the records are simple.)

#Your task is to create a Python script that analyzes the records to calculate each of the following:
    #The total number of months included in the dataset
    #The total amount of revenue gained over the entire period
    #The average change in revenue between months over the entire period
    #The greatest increase in revenue (date and amount) over the entire period
    #The greatest decrease in revenue (date and amount) over the entire period


import pandas as pd

#function that calculates the monthly revenue change from previous month recursively
def revenue_change(revenue_list):
    previous_month = 0
    revenue_change_list = []
    for revenue in revenue_list:
        revenue_change_list.append(revenue - previous_month)
        previous_month = revenue
    return revenue_change_list


def process_budget(budget_data_file):
    file_path = "raw_data\\{}".format(budget_data_file)
    print(file_path)

    df = pd.read_csv(file_path)
    #df.head() temporary check

    total_months = df.Date.count()
    total_revenue = df.Revenue.sum()
 
    df['Revenue_Change'] = revenue_change(df.Revenue)
    #df.head() #temporary check

    average_monthly_revenue_change = df.Revenue_Change.mean()
    greatest_monthly_revenue_increase = df.Revenue_Change.max()
    greatest_monthly_revenue_decrease = df.Revenue_Change.min()
    month_max_inc = df[df.Revenue_Change == greatest_monthly_revenue_increase].iloc[0,0]
    month_max_dec = df[df.Revenue_Change == greatest_monthly_revenue_decrease].iloc[0,0]

    return (total_months, total_revenue, average_monthly_revenue_change, 
            greatest_monthly_revenue_increase, month_max_inc, 
            greatest_monthly_revenue_decrease, month_max_dec)

#Print info to Terminal
def print_terminal(tot_mon, tot_rev, avg_m_rev, max_inc_m_rev, max_inc_m, max_dec_m_rev, max_dec_m):
    print("\nFinancial Analysis \n--------------------------")
    print("Total Months: {}".format(tot_mon))
    print("Total Revenue: ${}".format(tot_rev))
    print("Average Monthly Revenue Change: ${}".format(round(avg_m_rev)))
    print("Greatest Increase in Revenue: {} (${})".format(max_inc_m, max_inc_m_rev))
    print("Greatest Decrease in Revenue: {} (${})".format(max_dec_m, max_dec_m_rev))
    print("--------------------------\n\n")

#Print info to txt file in folder text_output
def print_text_file(tot_mon, tot_rev, avg_m_rev, max_inc_m_rev, max_inc_m, max_dec_m_rev, max_dec_m, user_data_file):
    user_output_file = "Financial_Analysis_" + user_data_file.strip(".csv") + ".txt"
    user_output_file_path = "text_output\\{}".format(user_output_file)
    with open(user_output_file_path, "w") as text_file:  #in class, jeff showed that can do text_file.write(str(value))
        print("\nFinancial Analysis \n--------------------------", file=text_file)
        print("Total Months: {}".format(tot_mon), file=text_file)
        print("Total Revenue: ${}".format(tot_rev), file=text_file)
        print("Average Monthly Revenue Change: ${}".format(round(avg_m_rev)), file=text_file)
        print("Greatest Increase in Revenue: {} (${})".format(max_inc_m, max_inc_m_rev), file=text_file)
        print("Greatest Decrease in Revenue: {} (${})".format(max_dec_m, max_dec_m_rev), file=text_file)
        print("--------------------------\n\n", file=text_file)
    print("*Results also printed to text file at {}\n\n\n".format(user_output_file_path))

#main function that runs everything else
def main(budget_data_file_name):
    tot_mon, tot_rev, avg_m_rev, max_inc_m_rev, max_inc_m, max_dec_m_rev, max_dec_m = process_budget(budget_data_file_name)
    print_terminal(tot_mon, tot_rev, avg_m_rev, max_inc_m_rev, max_inc_m, max_dec_m_rev, max_dec_m)
    print_text_file(tot_mon, tot_rev, avg_m_rev, max_inc_m_rev, max_inc_m, max_dec_m_rev, max_dec_m, budget_data_file_name)   

##RUN THE ACTUAL BUDGET DATA##
main("budget_data_1.csv")
main("budget_data_2.csv")
