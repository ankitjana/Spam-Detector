# COMP 6721 Applied Artificial Intelligence (Winter 2020)
Project Assignment #2
*Team members: (same as Project 1)*
A readme.txt (or readme.md) file that lists all submitted files with an explanation of their
content. It also must describe how to run your code for (a) training and (b) testing (including
generating the evaluation results provided in the report). If your instructions are incomplete and
your code cannot be run you might not receive any marks for your work.

## List of submitted files:
1.  model.txt: contains the training results. It includes a list of vocabulary words, their frequency, and smoothed conditional probability of each class ham and spam
2.  result.txt: contains the testing results. It includes the name of each test file, its label (spam or ham) done by the model, its spam and ham score, the expected label and whether the model's classification is right or wrong
3.  spam_detection.py: contains our code implementation for model training. The program processes all of the training files in the *train* directory, trains the model and outputs the training results to model.txt.
4.  model_evaluator.py: contains our code implementation for model testing. The program processes all of the testing files in the *test* directory and outputs the results to model.txt.
5.  project_report.pdf: contains the report of this project.
6.  readme.md: this readme file

## How to run the program
1.  To train the model, please run `spam_detector.py` using appropriate python command  
2.  To test the model, please run `model_evaluator.py` using appropriate python command
