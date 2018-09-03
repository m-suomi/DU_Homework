#Option 4: PyParagraph for Homework 3
#In this challenge, you get to play the role of chief linguist at a local learning academy.
# As chief linguist, you are responsible for assessing the complexity of various passages 
# of writing, ranging from the sophomoric Twilight novel to the nauseatingly high-minded
# research article. Having read so many passages, you've since come up with a fairly simple 
# set of metrics for assessing complexity.

#Your task is to create a Python script to automate the analysis of any such passage using
# these metrics. Your script will need to do the following:
    ##Import a text file filled with a paragraph of your choosing.
    ##Assess the passage for each of the following:
        ##Approximate word count
        ##Approximate sentence count
        ##Approximate letter count (per word)
        ##Average sentence length (in words)


import re

##reads the text file to one long string
def read_text_file(paragraph_text_file):
    user_txt_file_path = "raw_data\\{}".format(paragraph_text_file)
    print(user_txt_file_path)

    with open(user_txt_file_path, 'r') as f:
        paragraph_string = f.read()
    
    ##clean up the paragraph string so reads better with later scripts
    clean_paragraph_string = paragraph_string.replace("\n\n", " ") #take out any double returns
    clean_paragraph_string = paragraph_string.replace("\n", " ") #take out any single returns
    clean_paragraph_string = clean_paragraph_string.strip() #take out any trailing or leading spaces on paragraph string
    clean_paragraph_string = clean_paragraph_string.replace("  ", " ") #take out an double spaces
    #print(clean_paragraph_string) #temporary check
    return clean_paragraph_string

##makes calculations on paragraph string for word count, sentence count, letter count, avg sent length
##and prints results to terminal
def paragraph_metrics_terminal(clean_paragraph_string):         
    ##word count and count letters per word avg
    words = clean_paragraph_string.split(" ")
    #print(words) #temporary check
    word_count = len(words)
    letters_per_word = [len(word) for word in words] #this is slightly off as will count punctuation
    avg_letters_per_word = sum(letters_per_word)/len(letters_per_word)
    
    ##sentence count and avg sentence word length
    sentences = re.split("\.|\?|!", clean_paragraph_string) #note this does add a sentence if someone has abbrevation Anne V. Coates
    sentences.remove('') #remove blank sentence that re.split seems to put at the end
    #print(sentences) #temporary check
    words_in_sentence = [sentence.split() for sentence in sentences]
    #print(words_in_sentence) #temporary check
    number_words_in_sentence = [len(row) for row in words_in_sentence]
    avg_words_per_sentence = sum(number_words_in_sentence)/len(number_words_in_sentence)
    sentence_count = len(sentences)
    
    ##print results to terminal(word_count, sentence_count, avg_letters_per_word, avg_words_per_sentence) #temporary check
    print("\nParagraph Analysis \n--------------------------")
    print("Approximate Word Count: {}".format(word_count))
    print("Approximate Sentence Count: {}".format(sentence_count))
    print("Approximate Average Letters per Word: {}".format(round(avg_letters_per_word, 1)))
    print("Approximate Average Words per Sentence: {}\n\n".format(round(avg_words_per_sentence, 1)))


#this is the main function that references all other functions
#make sure the .txt file is saved to the subfolder raw_data
def main(paragraph_text_file):
    paragraph_text_string = read_text_file(paragraph_text_file)
    paragraph_metrics_terminal(paragraph_text_string)
    

##RUN THE ACTUAL PARAGRAPH FILES PROVIDED##
main("paragraph_1.txt")
main("paragraph_2.txt")