import os
from os import walk
import re
from math import log10
from spam_detector import word_dictionary, p_ham, p_spam, probability_ham, probability_spam

# current path
dir_path = os.path.dirname(os.path.realpath(__file__))

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
