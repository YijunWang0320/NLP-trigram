#! /usr/bin/python
import sys
from collections import defaultdict
from splitData import Classifier
import string

if __name__ == '__main__':
	'''
	This Replace.py just replace the low-frequency words with other words.
	The first part is parsing the input of the program.
	single: only one class for the low-frequency words "_RARE_"
	notSingle: four classes for the low-frequency words "allCapital","numberWithNoCharacter","nameAbr","_RARE_"
	'''
	if len(sys.argv) > 2:
		print "Too much arguments " + str(len(sys.argv));
		sys.exit(1);
	elif len(sys.argv) == 1:
		thisType = "single";
	else:
		if sys.argv[1].upper() == "NOTSINGLE":
			thisType = "notSingle";
		else:
			thisType = "single";
	COUNTFILE = "ner.counts";
	INPUTFILE = "ner_train.dat";
	OUTPUTFILE = "ner_train2.dat";
	'''
	This is the classifier
	'''
	classifier = Classifier(thisType);
 	mycol = dict();
 	fp=open(COUNTFILE,"r");
 	for eachline in fp:
 		st = eachline[:len(eachline)-1].split(" ");
 		if st[1] != "WORDTAG":
 			break;
 		if mycol.has_key(st[3]):
 			mycol[st[3]] = int(mycol[st[3]]) + int(st[0]);
 		else:
 			mycol[st[3]] = st[0];
 	fp.close();
 	fp = open(INPUTFILE,"r");
 	wp = open(OUTPUTFILE,"w");
 	for eachline in fp:
 		if eachline == "\n":
 			wp.write("\n");
 			continue;
 		st = eachline[:len(eachline)-1].split(" ");
 		if  int(mycol[st[0]]) < 5:
 			'''
 			Replace the low-frequency words
 			'''
 			wp.write(classifier.getType(st[0]));
 		else:
 			wp.write(st[0]);
 		wp.write(" ");
 		wp.write(st[1]);
 		wp.write("\n");
 	fp.close();
 	wp.close();


