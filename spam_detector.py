import os
from os import walk
import re

# current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# training files
training_path = os.path.join(dir_path, 'train')




'''
p_ham is the probability of document being ham document
p_spam is the probability of document being spam document
word_dictionary contains a list of all words
ham_dict is a dictionary with the conditional probabilities of all ham words
spam_dict is a dictionary with the conditional probabilities of all spam words
'''


def write_in_file(word_dict, ham_dict, spam_dict, p_ham, p_spam):
    # print_to_console = input("would you like to print file output to the console (0 for no 1 for yes) >")
    f = open("model.txt", "w+")
    counter = 0
    for word in word_dict:
        counter += 1
        '''
        if print_to_console == '1':
            print(counter, end="  ")
            print(word, end="  ")
            print(ham_dict[word], end="  ")
            print(p_ham[word], end="  ")
            print(spam_dict[word], end="  ")
            print(p_spam[word])
        '''
        f.write(str(counter))
        f.write("  ")
        f.write(str(word))
        f.write("  ")
        f.write(str(ham_dict[word]))
        f.write("  ")
        f.write(str(p_ham[word]))
        f.write("  ")
        f.write(str(spam_dict[word]))
        f.write("  ")
        f.write(str(p_spam[word]))
        f.write("\n")
    f.close()


'''
sort the dictionary in alphabetical order
'''


def sort_dictionary(dictionary):
    result = {}
    dictionary.keys()
    sorted(dictionary.keys())
    for key in sorted(dictionary.keys()) :
        result[key] = dictionary[key]

    return result



training_files = []

for (dirpath, dirnames, filenames) in walk(training_path):
    training_files.extend(filenames)

word_dictionary = {}
ham_word_dictionary = {}
spam_word_dictionary = {}

number_of_spam_documents = 0
number_of_ham_documents = 0

for file in training_files:
    if file.find("ham") != -1:
        number_of_ham_documents += 1
    if file.find("spam") != -1:
        number_of_spam_documents += 1

# the probabilty of document being ham or spam [prior probabilty]
probability_ham = number_of_ham_documents/(number_of_spam_documents+number_of_ham_documents)
probability_spam = number_of_spam_documents/(number_of_spam_documents+number_of_ham_documents)


for file in training_files:
    path_to_file = os.path.join(training_path, file)
    f = open(path_to_file, 'r', encoding="latin-1")
    for line in f:
        line = line.lower()
        # print(line, end=" -> ")
        words = re.split('[^a-zA-Z]',line)
        # print(words)
        for word in words:
            # print(word , end=" - >")
            # print(word)
            #check for blank lines
            if len(word) == 0:
                continue

            #if the word is already in the word dictionary increment the frequency
            if word in word_dictionary:
                x = word_dictionary[word]
                x += 1
                word_dictionary[word] = x
            else:
                word_dictionary[word] = 1

            # check if the file is a ham file
            if file.find("ham") != -1:
                # if the word is already in the ham dictionary increment the frequency
                if word in ham_word_dictionary:
                    x = ham_word_dictionary[word]
                    x += 1
                    ham_word_dictionary[word] = x
                else:
                    ham_word_dictionary[word] = 1
                # word is also added to spam dictionary if it does not exist with 0 probability
                if word not in spam_word_dictionary:
                    spam_word_dictionary[word] = 0

            # if the file is a spam file
            if file.find("spam") != -1:
                # if the word is already in spam dictionary increment the frequency
                if word in spam_word_dictionary:
                    x = spam_word_dictionary[word]
                    x += 1
                    spam_word_dictionary[word] = x
                else:
                    spam_word_dictionary[word] = 1

                # word is also added to ham dictionary if it does not exist with 0 probability
                if word not in ham_word_dictionary:
                    ham_word_dictionary[word] = 0


# count the total frequency of words in both ham and spam files
total_words_count = 0
for i in word_dictionary:
    total_words_count += word_dictionary[i]

# print("total number of words:", total_words_count)

# count the total frequency of ham words only ham files
total_num_ham_words = 0
for i in ham_word_dictionary:
    total_num_ham_words += ham_word_dictionary[i]

# count the total frequency of spam words only in spam files
total_num_spam_words = 0
for i in spam_word_dictionary:
    total_num_spam_words += spam_word_dictionary[i]


# the probabilities of each word in its set
p_spam = {}
p_ham = {}

# total number of unique words
number_of_words = len(word_dictionary)


# dictionary of ham word with conditional probabilites
# smoothing factor = 0.5
for i in ham_word_dictionary:
    p_ham[i] = (ham_word_dictionary[i]+0.5)/(total_num_ham_words+0.5*total_words_count)

# dictionary of spam word with conditional probabilites
for j in spam_word_dictionary:
    p_spam[j] = (spam_word_dictionary[j]+0.5)/(total_num_spam_words+0.5*total_words_count)

# sorts the word dictionary alphabetically
word_dictionary = sort_dictionary(word_dictionary)

if __name__ == "__main__":
    write_in_file(word_dictionary, ham_word_dictionary, spam_word_dictionary, p_ham, p_spam)
    '''
    print("****************************************************************************")
    print("Total number of Spam Documents in the training files:", number_of_spam_documents)
    print("Total number of Ham Documents in the training files:", number_of_ham_documents)
    print("Probability of a document being a Spam", probability_spam)
    print("Probability of a document being a Ham", probability_ham)
    print('Total number of Spam words:', total_num_spam_words)
    print("Total number of Ham words:", total_num_ham_words)
    print("****************************************************************************")
    '''
