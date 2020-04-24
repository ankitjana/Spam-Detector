import os
from os import walk
import re
from math import log10

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

# the probability of document being ham or spam [prior probability]
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
                # word is also added to spam dictionary with 0 frequency if it does not exist in spam dict
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

                # word is also added to ham dictionary if it does not exist with 0 freq
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

# size of vocabulary
number_of_words = len(word_dictionary)


# dictionary of ham word with conditional probabilities
# smoothing factor = 0.5
for i in ham_word_dictionary:
    p_ham[i] = (ham_word_dictionary[i]+0.5)/(total_num_ham_words+0.5*total_words_count)

# dictionary of spam word with conditional probabilities
for j in spam_word_dictionary:
    p_spam[j] = (spam_word_dictionary[j]+0.5)/(total_num_spam_words+0.5*total_words_count)

# sorts the word dictionary alphabetically
word_dictionary = sort_dictionary(word_dictionary)

# testing files
testing_path = os.path.join(dir_path, 'test')


testing_files = []
ham_testing_files = []
spam_testing_files = []

for (dirpath, dirnames, filenames) in walk(testing_path):
    testing_files.extend(filenames)

for i in testing_files:
    if i.find("ham") != -1:
        ham_testing_files.append(i)
    if i.find("spam") != -1:
        spam_testing_files.append(i)

def print_result(report):
    #print_to_console = input("would you like to print file output to the console (0 for no 1 for yes) >")
    f = open("result.txt", "w+")

    # calculate accuracy of the classification
    wrongCounter = 0
    rightCounter = 0

    counter = 0
    for file_name in report:
        counter += 1

        '''
        if print_to_console == '1':
            print(counter, end="  ")
            print(file_name, end="  ")
            print(report[file_name]["classification"], end="  ")
            print(report[file_name]["ham_score"], end="  ")
            print(report[file_name]["spam_score"], end="  ")
            print(report[file_name]["result"])
        '''
        f.write(str(counter))
        f.write("  ")
        f.write(str(file_name))
        f.write("  ")
        f.write(str(report[file_name]["classification"]))
        f.write("  ")
        f.write(str(report[file_name]["ham_score"]))
        f.write("  ")
        f.write(str(report[file_name]["spam_score"]))
        f.write("  ")
        f.write(str(report[file_name]["result"]))
        f.write("\n")

        if report[file_name]["result"] == "wrong":
            wrongCounter += 1
        elif report[file_name]["result"] == "right":
            rightCounter += 1
        else:
            print("ERROR")
            break
    accuracy = rightCounter/(rightCounter + wrongCounter)
    print("--------------------------Accurracy--------------------------")
    print(accuracy*100, ' % ')
    print("--------------------------accurracy--------------------------")

    f.close()


def createWordList(file_path):
    result_words = []

    f = open(file_path, 'r', encoding="latin-1")
    for line in f:
        line = line.lower()
        # tokenizing the line. returns an array of lines ending by \n
        words = re.split('[^a-zA-Z]',line)

        for word in words:

            # ignore empty lines
            if len(word) == 0:
                continue

            # is the word is already in our result dictionary increment frequency
            # else set frequency to 1
            result_words.append(word)
    f.close()
    return result_words


confusion_matrix = [[0,0],[0,0]]

report = {}
for file in testing_files:
    path_to_file = os.path.join(testing_path, file)
    words = createWordList(path_to_file)

    classification = ""
    actual_classification = ""
    # Initialize with the prior probability
    probability_email_spam = log10(probability_ham)
    probability_email_ham = log10(probability_spam)
    for word in words:
        if word not in word_dictionary:
            continue
        # need to calculate probabilities
        probability_email_spam += log10(p_spam[word])
        probability_email_ham += log10(p_ham[word])

    if probability_email_spam >= probability_email_ham:
        classification = "spam"
    else:
        classification = "ham"

    if file.find("ham") != -1:
        actual_classification = "ham"
    if file.find("spam") != -1:
        actual_classification = "spam"

    result = "wrong"
    if actual_classification == classification:
        result = "right"

    # true positive
    if actual_classification=="spam" and classification=="spam":
        confusion_matrix[0][0] += 1

    # true negative
    if actual_classification=="ham" and classification=="ham":
        confusion_matrix[1][1] += 1

    # false positive
    if classification=="spam" and actual_classification=="ham":
        confusion_matrix[0][1] +=1

    # false negative
    if classification=="ham" and actual_classification=="spam":
        confusion_matrix[1][0] +=1

    # report storing necessary info like ham score, spam score
    report[file] = {}
    report[file]['spam_score'] = probability_email_spam
    report[file]['ham_score'] = probability_email_ham
    report[file]['classification'] = classification
    report[file]['actual_classification'] = actual_classification
    report[file]['result'] = result


print("confusion matrix")
print('       PREDICTED   ')
print('      SPAM |  HAM  ')
print('     --------------')
print('SPAM| %4d | %4d |' %(confusion_matrix[0][0], confusion_matrix[0][1]))
print('HAM | %4d | %4d |' %(confusion_matrix[1][0], confusion_matrix[1][1]))
print('     --------------')

true_positive = confusion_matrix[0][0]
false_positive = confusion_matrix[0][1]
false_negative = confusion_matrix[1][0]
true_negative = confusion_matrix[1][1]

print("True Positive: ", true_positive)
print("False Positive: ", false_positive)
print("False Negative: ", false_negative)
print("True Negative: ", true_negative)

total_emails = confusion_matrix[0][0] + confusion_matrix[0][1] + confusion_matrix[1][0] + confusion_matrix[1][1]

accuracy = (confusion_matrix[0][0] + confusion_matrix[1][1])/total_emails
print("Accuracy of the classification:  ", accuracy)

precision = true_positive/(true_positive+false_positive)
print("Precision of the classification:  ", precision )

recall = true_positive/(true_positive+false_negative)
print("Recall of the classification:  ", recall)

f1 = 2*(precision*recall)/(precision+recall)
print("f1 score of the classification:", f1)

if __name__ == "__main__":
    write_in_file(word_dictionary, ham_word_dictionary, spam_word_dictionary, p_ham, p_spam)
    print_result(report)
    '''
    print('Model training is done. Please run model_evaluator.py for testing')
    print("****************************************************************************")
    print("Total number of Spam Documents in the training files:", number_of_spam_documents)
    print("Total number of Ham Documents in the training files:", number_of_ham_documents)
    print("Probability of a document being a Spam", probability_spam)
    print("Probability of a document being a Ham", probability_ham)
    print('Total number of Spam words:', total_num_spam_words)
    print("Total number of Ham words:", total_num_ham_words)
    print("****************************************************************************")
    '''

