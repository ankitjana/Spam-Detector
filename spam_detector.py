import os
from os import walk
import re
from math import log10


# current directory
dir = os.path.dirname(os.path.realpath(__file__))

# training files
training_path = os.path.join(dir, 'train')




'''
write model.txt file
p_ham is the probability of document being ham document
p_spam is the probability of document being spam document
word_dictionary contains a list of all words
ham_dict is a dictionary with the conditional probabilities of all ham words
spam_dict is a dictionary with the conditional probabilities of all spam words
'''


def write_to_file(word_dict, ham_dict, spam_dict, p_ham, p_spam):
    f = open("model.txt", "w+")
    counter = 0
    for word in word_dict:
        counter += 1
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
ham_dictionary = {}
spam_dictionary = {}

num_spam_docs = 0
num_ham_docs = 0

for file in training_files:
    if file.find("ham") != -1:
        num_ham_docs += 1
    if file.find("spam") != -1:
        num_spam_docs += 1

# the probability of document being ham or spam [prior probability]
prob_ham = num_ham_docs / (num_spam_docs + num_ham_docs)
prob_spam = num_spam_docs / (num_spam_docs + num_ham_docs)


for file in training_files:
    file_path = os.path.join(training_path, file)
    train_f = open(file_path, 'r', encoding="latin-1")
    for line in train_f:
        line = line.lower()
        # print(line, end=" -> ")
        words = re.split('[^a-zA-Z]',line)
        for word in words:
            # check for blank lines
            if len(word) == 0:
                continue

            # if the word is already in the word dictionary increment the frequency
            if word in word_dictionary:
                x = word_dictionary[word]
                x += 1
                word_dictionary[word] = x
            else:
                word_dictionary[word] = 1

            # check if the file is a ham file
            if file.find("ham") != -1:
                # if the word is already in the ham dictionary increment the frequency
                if word in ham_dictionary:
                    x = ham_dictionary[word]
                    x += 1
                    ham_dictionary[word] = x
                else:
                    ham_dictionary[word] = 1
                # word is also added to spam dictionary with 0 frequency if it does not exist in spam dict
                if word not in spam_dictionary:
                    spam_dictionary[word] = 0

            # if the file is a spam file
            if file.find("spam") != -1:
                # if the word is already in spam dictionary increment the frequency
                if word in spam_dictionary:
                    x = spam_dictionary[word]
                    x += 1
                    spam_dictionary[word] = x
                else:
                    spam_dictionary[word] = 1

                # word is also added to ham dictionary if it does not exist with 0 freq
                if word not in ham_dictionary:
                    ham_dictionary[word] = 0


# count the total frequency of words in both ham and spam files
total_words_count = 0
for i in word_dictionary:
    total_words_count += word_dictionary[i]

# count the total frequency of ham words only ham files
total_ham_words = 0
for i in ham_dictionary:
    total_ham_words += ham_dictionary[i]

# count the total frequency of spam words only in spam files
total_spam_words = 0
for i in spam_dictionary:
    total_spam_words += spam_dictionary[i]


# the probabilities of each word in its set
p_spam = {}
p_ham = {}

# size of vocabulary
vocab_size = len(word_dictionary)


# dictionary of ham word with conditional probabilities
# smoothing factor = 0.5
for i in ham_dictionary:
    p_ham[i] = (ham_dictionary[i] + 0.5) / (total_ham_words + 0.5 * total_words_count)

# dictionary of spam word with conditional probabilities
for j in spam_dictionary:
    p_spam[j] = (spam_dictionary[j] + 0.5) / (total_spam_words + 0.5 * total_words_count)

# sorts the word dictionary alphabetically
word_dictionary = sort_dictionary(word_dictionary)

# write model.txt file
write_to_file(word_dictionary, ham_dictionary, spam_dictionary, p_ham, p_spam)


# testing files
testing_path = os.path.join(dir, 'test')


test_files = []
ham_test_files = []
spam_test_files = []

for (dirpath, dirnames, test_filenames) in walk(testing_path):
    test_files.extend(test_filenames)

for i in test_files:
    if i.find("ham") != -1:
        ham_test_files.append(i)
    if i.find("spam") != -1:
        spam_test_files.append(i)


def print_result(summary):
    result_f = open("result.txt", "w+")

    # calculate accuracy of the classification
    wrongClassification = 0
    rightClassification = 0

    counter = 0
    for file_name in summary:
        counter += 1
        result_f.write(str(counter))
        result_f.write("  ")
        result_f.write(str(file_name))
        result_f.write("  ")
        result_f.write(str(summary[file_name]["classification"]))
        result_f.write("  ")
        result_f.write(str(summary[file_name]["ham_score"]))
        result_f.write("  ")
        result_f.write(str(summary[file_name]["spam_score"]))
        result_f.write("  ")
        result_f.write(str(summary[file_name]["result"]))
        result_f.write("\n")

        if summary[file_name]["result"] == "wrong":
            wrongClassification += 1
        elif summary[file_name]["result"] == "right":
            rightClassification += 1
        else:
            print("ERROR")
            break
    result_f.close()


def createWordList(file_path):
    result_words = []

    f_word_list = open(file_path, 'r', encoding="latin-1")
    for line in f_word_list:
        line = line.lower()
        # tokenizing the line. returns an array of lines ending by \n
        word_list = re.split('[^a-zA-Z]',line)

        for word_ in word_list:

            # ignore empty lines
            if len(word_) == 0:
                continue

            # is the word is already in our result dictionary increment frequency
            # else set frequency to 1
            result_words.append(word_)
    f_word_list.close()
    return result_words


confusion_matrix = [[0,0],[0,0]]

report = {}
for file_te in test_files:
    test_file_path = os.path.join(testing_path, file_te)
    words = createWordList(test_file_path)

    classification = ""
    actual_classification = ""
    # Initialize with the prior probability
    prob_email_spam = log10(prob_ham)
    prob_email_ham = log10(prob_spam)
    for word in words:
        if word not in word_dictionary:
            continue
        # need to calculate probabilities
        prob_email_spam += log10(p_spam[word])
        prob_email_ham += log10(p_ham[word])

    if prob_email_spam >= prob_email_ham:
        classification = "spam"
    else:
        classification = "ham"

    if file_te.find("ham") != -1:
        actual_classification = "ham"
    if file_te.find("spam") != -1:
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
    report[file_te] = {}
    report[file_te]['spam_score'] = prob_email_spam
    report[file_te]['ham_score'] = prob_email_ham
    report[file_te]['classification'] = classification
    report[file_te]['actual_classification'] = actual_classification
    report[file_te]['result'] = result

# print result.txt file
print_result(report)

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
