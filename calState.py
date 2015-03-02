#! /usr/bin/python

import sys
from collections import defaultdict
from splitData import Classifier
import string
import math

def getProb(twoGramMap, threeGramMap):
	probMap = dict();
	keyList = threeGramMap.keys();
	for tuples in keyList:
		probMap[tuples] = math.log(threeGramMap[tuples]/twoGramMap[(tuples[0],tuples[1])],2);
	return probMap;

def getEmiss(emissList,typeNumber):
	emiss = dict();
	for key in emissList.keys():
		tList = emissList[key];
		for pairs in tList:
			emiss[(pairs[1],pairs[0])] = math.log(pairs[2]/typeNumber[pairs[1]],2);
	return emiss;


def printToFile(fileName,probMap):
	wp = open(fileName,"w");
	for tuples in probMap.keys():
		wp.write(tuples[0]);
		wp.write(" ");
		wp.write(tuples[1]);
		wp.write(" ");
		wp.write(tuples[2]);
		wp.write(" ");
		wp.write(str(probMap[tuples]));
		wp.write("\n");
	wp.close();
	return;
def getSenList(rankFile):
	fp = open(rankFile,"r");
	sentenceList = [];
	sentence = [];
	for eachline in fp:
		if eachline == "\n":
			sentenceList.append(list(sentence));
			del sentence[:];
			continue;
		sentence.append(eachline.strip());
	sentenceList.append(sentence);
	fp.close();
	return sentenceList;


def viterbi(allType,wordList,emiss,probMap,thisType,rankFile):
	#The part that I modified for Question 6:
	classifier = Classifier(thisType);
	#End of the part
	wp = open("new_prediction.dat","w");
	'''
	parse the whole file into sentences. 
	We are gonna do the tagging based on the sentences, it's more reasonable.
	'''
	sentenceList = getSenList(rankFile);
	for sentence in sentenceList:
		pai = dict();
		bp = dict();
		yp = dict();
		length = len(sentence);
		pai[(0,"*","*")] = 0;
		for i in range(1,length+1):
			if i == 1:
				for v in allType:
					x = sentence[i-1];
					if x not in wordList:
						#This is also where I made modification
						#x = "_RARE_";
						x = classifier.getType(x); 
						#modification ends
					pai[(i,"*",v)] = -sys.maxint;
					bp[(i,"*",v)] = "O";
					if emiss.has_key((v,x)) and probMap.has_key(("*","*",v)) and pai[(i,"*",v)] < pai[(i-1,"*","*")] + probMap[("*","*",v)] + emiss[(v,x)]:
						pai[(i,"*",v)] = pai[(i-1,"*","*")] + probMap[("*","*",v)] + emiss[(v,x)];
						bp[(i,"*",v)] = "*";
			elif i == 2:
				for u in allType:
					for v in allType:
						x = sentence[i-1];
						if x not in wordList:
							#This is also where I made modification
							#x = "_RARE_";
							x = classifier.getType(x); 
							#modification ends
						pai[(i,u,v)] = -sys.maxint;
						bp[(i,u,v)] = "O";
						if emiss.has_key((v,x)) and probMap.has_key(("*",u,v)) and pai[(i,u,v)] < pai[(i-1,"*",u)] + probMap[("*",u,v)] + emiss[(v,x)]:
							pai[(i,u,v)] = pai[(i-1,"*",u)] + probMap[("*",u,v)] + emiss[(v,x)];
							bp[(i,u,v)] = "*";
			else:
				for u in allType:
					for v in allType:
						x = sentence[i-1];
						if x not in wordList:
							#This is also where I made modification
							#x = "_RARE_";
							x = classifier.getType(x); 
							#modification ends
						pai[(i,u,v)] = -sys.maxint;
						bp[(i,u,v)] = "O";
						for w in allType:
							if emiss.has_key((v,x)) and probMap.has_key((w,u,v)) and pai[(i,u,v)] < pai[(i-1,w,u)] + probMap[(w,u,v)] + emiss[(v,x)]:
								pai[(i,u,v)] = pai[(i-1,w,u)] + probMap[(w,u,v)] + emiss[(v,x)];
								bp[(i,u,v)] = w;
		'''
		Find the y1...yn from the back pointers.
		'''
		tempMax = -sys.maxint-1;
		yp[length-1] = "O";
		yp[length] = "O";
		for u in allType:
			for v in allType:
				if length >= 2 and probMap.has_key((u,v,"STOP")) and pai[(length,u,v)] + probMap[(u,v,"STOP")] > tempMax:
					tempMax =  pai[(length,u,v)] + probMap[(u,v,"STOP")];
					yp[length-1] = u;
					yp[length] = v;
		for k in range(length-2,0,-1):
			yp[k] = bp[(k+2,yp[k+1],yp[k+2])];

		'''
		Print out the result to new_prediction.dat.
		'''
		for k in range(1,length+1):
			wp.write(sentence[k-1] + " " + yp[k] + " ");
			if k == 1:
				wp.write(str(pai[(k,"*",yp[k])]));
			else:
				wp.write(str(pai[(k,yp[k-1],yp[k])]));
			wp.write("\n");
		wp.write("\n");
	wp.close();
		

	
if __name__ == '__main__':
	'''
	This calState.py is for Question 5 and Question 6.
	This file use the viterbi algoritm to perfrom the tagging.

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
	OUTPUTFILE = "state_trigram_result";
	COUNTFILE = "ner2.counts";
	RANKFILE = "ner_dev.dat";
	twoGramMap = dict();
	threeGramMap = dict();
	allType = list();
	reverseType = dict();
	wordList = set();
	emissList = defaultdict(list);
	typeNumber = dict();
	fp = open(COUNTFILE,"r");

	for eachline in fp:
		st = eachline[:len(eachline)-1].split(" ");
		if len(st) < 4:
			if ~reverseType.has_key(st[2]):
				allType.append(st[2]);
				reverseType[st[2]] = len(allType)-1;
		elif st[1] == "WORDTAG":
			wordList.add(st[3]);
		elif st[1] == "2-GRAM":
			twoGramMap[(st[2],st[3])] = float(st[0]);
		elif st[1] == "3-GRAM":
			threeGramMap[(st[2],st[3],st[4])] = float(st[0]);
		else:
			print "something wrong, there are other kind of tags?";
			sys.exit();
	fp.close();
	'''
	It get's the conditional probability of trigrams.
	The sequence is that probMap(w,u,v) = q(v | w,u).
	'''
	probMap = getProb(twoGramMap,threeGramMap);
	printToFile(OUTPUTFILE,probMap);
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
		emissList[st[3]].append((st[3],st[2],float(st[0])));
	fp.close();
	'''
	emiss:
	This is the emission probability list
	The order is e (y, x) for e (x | y)
	The condition is in front
	'''
	emiss = getEmiss(emissList,typeNumber); 
	'''
	Clear from the name, this is the viterbi algorithm.
	It prints to new_prediction.dat.
	'''
	viterbi(allType,wordList,emiss,probMap,thisType,RANKFILE);
