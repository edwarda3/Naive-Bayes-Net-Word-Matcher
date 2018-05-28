To run the program in flip:
$ python3 p3.py <trainingfile> <testfile>

The program does not function properly in python 2.x, use python3

The <trainingfile> parameter is the filename that we are using to train. 
The trainingSet.txt provided by the assignment was used.

The <testfile> parameter is the filename that we are using to test. 
The testSet.txt provided by the assignment was used.

Output:
result.txt shows the accuracy of the files run
preprocessed_train.txt shows the preprocessed text with the vocab in each sentence.
predictions-trainingSet.txt shows what the bayes net predicted, and if its wrong (for first file). This accuracy should be rather high.
predictions-testSet.txt shows what the bayes net predicted, and if its wrong (for second file). 