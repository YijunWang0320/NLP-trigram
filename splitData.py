#! /usr/bin/python
import sys
import string

class  Classifier(object):
	"""Try to get the real class of the low-frequency words"""
	def __init__(self,  curtype = "single"):
		self.curtype = curtype;
		self.allType = ["allCapital","numberWithNoCharacter","nameAbr","_RARE_"];
	def numberWithNoCharacter(self,word):
		flag = False;
		for i in range(0,len(word)):
			if word[i] in string.digits:
				flag = True;
			elif word[i] in string.letters:
				return False;
		return flag;
	def getType(self, word):
		if self.curtype == "single":
			return "_RARE_";
		if self.numberWithNoCharacter(word):
			return "allCapital";
		elif len(word) == 2 and word[0] in string.ascii_uppercase and word[1] == '.':
			return "nameAbr";
		elif word.upper() == word:
			return "numberWithNoCharacter";
		else:
			return "_RARE_";


		
		
		