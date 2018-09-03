#Option 2 -- PyPoll Challenge for DU Data Bootcamp Homework 3
#raw data is saved in raw_data\election_data_1.csv  and election_data_2.csv

#In this challenge, you are tasked with helping a small, rural town modernize its vote-counting process. (Up until now, Uncle Cleetus had been trustfully tallying them one-by-one, but unfortunately, his concentration isn't what it used to be.)
#You will be given two sets of poll data (election_data_1.csv and election_data_2.csv). 
# Each dataset is composed of three columns: Voter ID, County, and Candidate. 
# Your task is to create a Python script that analyzes the votes and calculates each of the following:
###The total number of votes cast
###A complete list of candidates who received votes
###The percentage of votes each candidate won
###The total number of votes each candidate won
###The winner of the election based on popular vote.

#Your final script must be able to handle any such similarly-structured dataset in the future 
#-- so your script needs to work without massive re-writes. In addition, your final script
# should both print the analysis to the terminal and export a text file with the results.

import csv
from collections import defaultdict

#Read the CSV data from user path
#make sure the .csv file is saved to the subfolder raw_data
def read_csv_file(user_data_file):
    user_data_file_path = "raw_data\\{}".format(user_data_file)
    print(user_data_file_path)

    with open(user_data_file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip header row
        csv_data = list(reader)
        #print(csv_data[0:5])  #print first five rows to verify the data is being read - temporary
    return csv_data


#Calculates the election data - total # votes, list of candidates with total # votes 
# and % of vote and also declaring the overall winner
#csv_data must be a list of .csv rows 
#with each row having three values in a list of 'Voter ID', 'County', 'Candidate'
def calculate_election_data(csv_data):
    vote_totals_dict = defaultdict(int) #keys will be candidate, values will be vote tally
    total_votes_cast = 0
    winner_name = ""
    winner_votes = 0

    #calculate total votes for each candidate
    for row in csv_data:
        vote_totals_dict[row[2]] += 1
    #print(vote_totals_dict) #temporary check

    #calculate total votes cast
    for candidate, votes in vote_totals_dict.items():
        total_votes_cast += votes
    #print(total_votes_cast) #temporary check

    #determine winner
    for candidate, votes in vote_totals_dict.items():
        if votes > winner_votes:
            winner_votes = votes
            winner_name = candidate
    #print("Winner is {} with {} votes".format(winner_name, winner_votes)) #temporary check

    #return values
    return vote_totals_dict, total_votes_cast, winner_name

#Print info to Terminal
def print_terminal(vote_totals_dict, total_votes_cast, winner_name):
    print("\nElection Results \n--------------------------")
    print("Total Votes: {}".format(total_votes_cast))
    print("--------------------------")
    for candidate, votes in vote_totals_dict.items():
        #percent_vote = votes/total_votes_cast
        print("{}: {}% ({})".format(candidate, round(votes/total_votes_cast*100, 1), votes))
    print("--------------------------")
    print("Winner: {} \n--------------------------".format(winner_name))

#Print info to txt file
def print_text_file(user_data_file, vote_totals_dict, total_votes_cast, winner_name):
    user_output_file = "Election_Results_Output_" + user_data_file.strip(".csv") + ".txt"
    user_output_file_path = "text_output\\{}".format(user_output_file)
    with open(user_output_file_path, "w") as text_file:
        print("\nElection Results \n--------------------------", file=text_file)
        print("Total Votes: {}".format(total_votes_cast), file=text_file)
        print("--------------------------", file=text_file)
        for candidate, votes in vote_totals_dict.items():
            #percent_vote = votes/total_votes_cast
            print("{}: {}% ({})".format(candidate, round(votes/total_votes_cast*100, 1), votes), file=text_file)
        print("--------------------------", file=text_file)
        print("Winner: {} \n--------------------------\n\n".format(winner_name), file=text_file)

    print("*Results also printed to text file at {}\n\n\n".format(user_output_file_path))

#this is the main function that references all other functions
#make sure the .csv file is saved to the subfolder raw_data
def main(user_data_file):
    #user_data_file = input("What is the election .csv file name you are analyzing? (make sure it is saved to raw_data subfolder)")
    csv_data = read_csv_file(user_data_file)
    vote_totals_dict, total_votes_cast, winner_name = calculate_election_data(csv_data)
    print_terminal(vote_totals_dict, total_votes_cast, winner_name)
    print_text_file(user_data_file, vote_totals_dict, total_votes_cast, winner_name)



##RUN THE ACTUAL ELECTION FILES## could change code to run a user input by running main()
main("election_data_1.csv")
main("election_data_2.csv")
