import sys
import re
import math

#global variables.
#We keep out vocabulary, positive and negative sentence counts here.
pos=0
neg=0
vocab = [{},{}]

#training function. Simply runs through all sentences and adds the words of sentences based on the last word (1 or 0, answer)
#Omits the answer 1 or 0 as it makes the algorithm have perfect accuracy and is unrealistic.
#@param trainingfile File to parse and train with.
def train(trainingfile):
	file = open(trainingfile,'r')
	lines=file.readlines()
	global vocab
	global pos, neg
	for sentence in lines:
		words = re.sub("[^\w]"," ",sentence).split() #nifty little function, using the re library to convert sentence to words without punctuation
					
		if(words[len(words)-1]==str(1)):		#split for readability
			pos+=1
			for word in words:
				if(word != '1'):
					word = word.lower()
					if(word in vocab[1]):			#use a dictionary to store vocab, split into pos and neg reviews.
						vocab[1][word]+=1
					else:
						vocab[1][word]=1
		else:
			neg+=1
			for word in words:
				if(word != '0'):
					word = word.lower()
					if(word in vocab[0]):
						vocab[0][word]+=1
					else:
						vocab[0][word]=1
	
	file.close()
	
#prints preprocessed information
#prints all of vocab, and then what each sentence has... pretty difficult to read
#@param filein inputfile
#@param fileout output file
def printPre(filein,fileout):
	global vocab
	file = open(filein,'r')
	lines = file.readlines()
	file.close()
	
	total = {}
	for entry in sorted(vocab[0].keys()):
		total[entry]=vocab[0][entry]
	for entry in sorted(vocab[1].keys()):
		if(entry in total):
			total[entry]+=vocab[1][entry]
		else:
			total[entry]=vocab[1][entry]
	totalSorted = sorted(total)
	
	outfile = open(fileout,'w')
	for entry in totalSorted:
		outfile.write(entry+", ")
	outfile.write("classlabel")
	outfile.write("\n")
	for sentence in lines:	
		words = re.sub("[^\w]"," ",sentence).split()
		for entry in totalSorted:
			if(entry in words):
				outfile.write("1")
			else:
				outfile.write("0")
			outfile.write(", ")
		outfile.write("\n")

#returns the probability of a word in all of positive or all of negative. usually something like 3/325. 
#uses uniform dirichlet priors
def getPropWord(list,word):
	global vocab
	totalInList=0
	for entry in vocab[list]:			#gets the total amount of words in vocabulary
		totalInList+=vocab[list][entry]
	if(word in vocab[list]):			#gets the number of times a word showed up in the training
		return ((vocab[list][word.lower()]+1)/(totalInList+2))
	else:
		return ((1)/(totalInList+2))
	
#runs the prediction on all of the lines of a file.
def predictFile(testfile):
	file = open(testfile,'r')
	lines = file.readlines()
	file.close()
	outfile = open("predictions-"+testfile,'w')
	wrong = 0
	#run through all sentences and predict each line.
	for sentence in lines:
		prob = predict(sentence)
		if(prob[0]==1):
			wrong+=1
			outfile.write("WRONG --\t")		#we write the predictions that we made and if they were wrong on a separate file
		else: outfile.write("\t\t")
		if(prob[1]>prob[2]):
			outfile.write("POS: " + sentence)
		else:
			outfile.write("NEG: " + sentence)
	return 1-(wrong/len(lines))
	
def predict(sentence):
	words = re.sub("[^\w]"," ",sentence).split()
	#calculate the probability that it is positive
	global pos,neg
	posProb = pos/(pos+neg) #Start with the positive and negative probabilities: P(CD), P(~CD)
	negProb = 1-posProb
	for word in words:	
		if(word!='1' and word!='0'):
			posProb*=getPropWord(1,word)	#multiply the probability of each word in positive. P(CD)*P(w1|CD)*P(w2|CD)*...*P(wj|CD)
			negProb*=getPropWord(0,word)	#do this for all words in a sentence, along with negative
			
	if((posProb>negProb and words[len(words)-1]=='0') or (posProb<negProb and words[len(words)-1]=='1')):
		return [1,posProb,negProb]		#quick "wrongness" check, since we are given the answer. 
	return [0,posProb,negProb]
	
def main():
	train(sys.argv[1])
	trainedfiles = "Trained on "+sys.argv[1]
	printPre(sys.argv[1],"preprocessed_train.txt")
	file1 = predictFile(sys.argv[1])
	file2 = predictFile(sys.argv[2])
	outfile = open("result.txt",'w')
	outfile.write("Predictions on "+ sys.argv[1] + ", "+trainedfiles+", accuracy: " + str(file1))
	outfile.write("\n")
	outfile.write("Predictions on "+ sys.argv[2] + ", "+trainedfiles+", accuracy: " + str(file2))
	outfile.close()
	
main()