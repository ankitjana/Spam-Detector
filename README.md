# COMP 6721 Applied Artificial Intelligence (Winter 2020)
Project Assignment #2 \
*Team members: (same as Project 1)*

## List of submitted files:
1.  model.txt: contains the training results. It includes a list of vocabulary words, their frequency, and smoothed conditional probability of each class ham and spam
2.  result.txt: contains the testing results. It includes the name of each test file, its label (spam or ham) done by the model, its spam and ham score, the expected label and whether the model's classification is right or wrong
3.  spam_detection.py: contains our code implementation for model training and testing. Firstly, the program processes all of the training files in the *train* directory, trains the model and outputs the training results to model.txt. Then it tests the model based on the test files in *test* directory. The test results are written to both the console and result.txt.
4.  project_report.pdf: contains the report of this project.
5.  readme.md: this readme file

## How to run the program
To train and test the model, please run `spam_detector.py` using appropriate python command