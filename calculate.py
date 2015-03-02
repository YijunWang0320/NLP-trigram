#! /usr/bin/python
import sys
from collections import defaultdict
import string
import math

def getEmiss(emissList,typeNumber):
	emiss = dict();
	for key in emissList.keys():
		tList = emissList[key];
		for pairs in tList:
			emiss[(pairs[1],pairs[0])] = math.log(pairs[2]/typeNumber[pairs[1]],2);
	return emiss;

def simpleNLP(emiss, wordList, inputfile,outputfile):
	'''
	BASELINE
	This calculate.py is the only doing tagging based on the emission probability.
	y = (for each y) argmax e(x | y)
	'''
	fp = open(inputfile,"r");
	wp = open(outputfile,"w");
	alltype = ["I-MISC", "I-ORG","I-LOC", "I-PER", "O", "B-MISC", "B-ORG", "B-LOC", "B-PER"];
	for eachline in fp:
		if eachline == "\n":
			wp.write("\n");
			continue;
		st = eachline[:len(eachline)-1];
		temp = st;
		if st not in wordList:
			st = "_RARE_";
		maxNum = -sys.maxint;
		maxType = "O";
		for tps in alltype:
			if emiss.has_key((tps,st)):
				if maxNum < emiss[(tps,st)]:
					maxNum = emiss[(tps,st)];
					maxType = tps;
		wp.write(temp + " " + maxType + " " + str(maxNum));
		wp.write("\n");
	fp.close();
	wp.close();


if __name__ == '__main__':
	COUNTFILE = "ner2.counts";
	INPUTFILE = "ner_dev.dat";
	OUTPUTFILE = "prediction.dat";
	wordList = set();
	typeNumber = dict();
	emissList = defaultdict(list);
	fp = open(COUNTFILE,"r");
	for eachline in fp:
		if eachline == "\n":
			continue;
		st = eachline[:len(eachline)-1].split(" ");
		if st[1] != "WORDTAG":
			break;
		if typeNumber.has_key(st[2]):
			typeNumber[st[2]] = typeNumber[st[2]] + int(st[0]);
		else:
			typeNumber[st[2]] = int(st[0]);
		wordList.add(st[3]);
		emissList[st[3]].append((st[3],st[2],float(st[0])));
	fp.close();
	'''
	emiss:
	This is the emission probability list
	The order is e (y, x) for e (x | y)
	The condition is in front
	'''
	emiss = getEmiss(emissList,typeNumber); 
	simpleNLP(emiss, wordList, INPUTFILE, OUTPUTFILE);