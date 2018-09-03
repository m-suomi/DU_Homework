#In this challenge, you get to be the boss. You oversee hundreds of employees across
#the country developing Tuna 2.0, a world-changing snack food based on canned tuna fish.
#Alas, being the boss isn't all fun, games, and self-adulation. The company recently
#decided to purchase a new HR system, and unfortunately for you, the new system requires
#employee records be stored completely differently.

#Your task is to help bridge the gap by creating a Python script able to convert your
# employee records to the required format. Your script will need to do the following:
#Import the employee_data1.csv and employee_data2.csv files, which currently holds
# employee records like the below:
        #Emp ID,Name,DOB,SSN,State
        #214,Sarah Simpson,1985-12-04,282-01-8166,Florida
        #15,Samantha Lara,1993-09-08,848-80-7526,Colorado
        #411,Stacy Charles,1957-12-20,658-75-8526,Pennsylvania
#Then convert and export the data to use the following format instead:
        #Emp ID,First Name,Last Name,DOB,SSN,State
        #214,Sarah,Simpson,12/04/1985,***-**-8166,FL
        #15,Samantha,Lara,09/08/1993,***-**-7526,CO
        #411,Stacy,Charles,12/20/1957,***-**-8526,PA
#In summary, the required conversions are as follows:
    #The Name column should be split into separate First Name and Last Name columns.
    #The DOB data should be re-written into MM/DD/YYYY format.
    #The SSN data should be re-written such that the first five numbers are hidden from view.
    #The State data should be re-written as simple two-letter abbreviations.

import csv
import datetime

#dictionary to convert states - is there an easier way to import this code rather than just paste it here?
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'}

#Read the CSV data from user path
#make sure the .csv file is saved to the subfolder raw_data
def read_csv_file(user_data_file):
    user_data_file_path = "raw_data\\{}".format(user_data_file)
    print("Imported original file from: {}".format(user_data_file_path))

    with open(user_data_file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip header row
        csv_data = list(reader)
        #print(csv_data[2])  #print third row to verify the data is being read/compare - temporary
    return csv_data

#split the columns into separate lists, make conversions necessary, then rejoin them
def convert_employee_data(original_csv_data):
    emp_ids = []
    first_names = []
    last_names = []
    dobs_m_d_y = []
    ssns_hidden = []
    state_abbrevs = []
    converted_csv_data = []
    
    #split columns, split first and last names, change SSN
    for row in original_csv_data:
        emp_ids.append(row[0])
        #split first and last names
        full_name = row[1]
        first_name, last_name = full_name.split()[0], full_name.split()[1]
        first_names.append(first_name)
        last_names.append(last_name)
        #change the date format from 1985-12-04 to 12/04/1985
        dob_orig_str = row[2]
        dob_py = datetime.datetime.strptime(dob_orig_str, '%Y-%m-%d')
        dob_m_d_y = datetime.datetime.strftime(dob_py, '%m/%d/%Y')
        dobs_m_d_y.append(dob_m_d_y)
        #change SSN to hidden first 5 characters
        ssn = row[3]
        ssn_hidden = "***-**-" + ssn.rpartition('-')[2]
        ssns_hidden.append(ssn_hidden)
        #change state name to state abbreviation
        state = row[4]
        state_abbrev = us_state_abbrev.get(state)
        state_abbrevs.append(state_abbrev)
    #print(emp_ids[2], first_names[2], last_names[2], dobs_m_d_y[2], ssns_hidden[2], state_abbrevs[2]) #temporary check

    converted_csv_data = list(zip(emp_ids, first_names, last_names, dobs_m_d_y, ssns_hidden, state_abbrevs))
    return converted_csv_data
    #print(converted_csv_data[2]) #temporary print check
    #print(type(converted_csv_data)) #temporary print check

#export converted data back to csv file in the folder csv_output
def export_converted_data_to_csv(original_employee_data_file, converted_csv_data):
    converted_data_file = "converted_{}".format(original_employee_data_file)
    converted_data_file_path = "csv_output\\{}".format(converted_data_file)
       
    with open(converted_data_file_path, 'w', newline='') as f:
        converted_headers = ['Emp ID', 'First Name', 'Last Name', 'DOB', 'SSN', 'State']
        writer = csv.writer(f)
        writer.writerow(converted_headers)
        for row in converted_csv_data:
            writer.writerow(row)
            
    print("Exported converted file to: {}\n\n".format(converted_data_file_path))


#this is the main function that references all other functions
#make sure the .csv file is saved to the subfolder raw_data
def main(original_employee_data_file):
    original_csv_data = read_csv_file(original_employee_data_file)
    converted_csv_data = convert_employee_data(original_csv_data)
    export_converted_data_to_csv(original_employee_data_file, converted_csv_data)
    

##RUN THE ACTUAL BOSS DATA##
main("employee_data1.csv")
main("employee_data2.csv")