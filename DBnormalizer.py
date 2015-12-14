#! /usr/local/dist/bin/python
# -*- coding: utf8 -*-

import random 
import string
from datetime import datetime
import re
import views


EMPTY_SET = "$"
MAX_NUM_OF_ATTRIBUTES=20
UMLAUTS="äöüÄÖÜß"

#computes the attributhuelle of the attributes "huelle" for the given fds
def attributhuelle(huelle, fds):
	if len(huelle) > 0:
		huelleNeu = huelle.copy()
		first=True
		while (huelleNeu != huelle) or (first==True):
			huelle = huelleNeu.copy()
			first=False
			for number in range(len(fds)):
				if fds[number][0] <= huelleNeu:
					huelleNeu = huelleNeu | fds[number][1]
	return huelle


def isKey(attributes, relation, fds):
	return relation <= attributhuelle(attributes, fds)
	
	
#generate all permutations of all elements in the set of sets. used to first generate all combinations of attributes in order to check each one of then if it is a key
def makePermutations(setOfSets, relation, fds):
	newSetOfSets = setOfSets.copy()
	for element1 in setOfSets:
		for element2 in setOfSets:
			newSetOfSets.add(element1|element2)
	if relation in newSetOfSets:
		return newSetOfSets
	else:
		return makePermutations(newSetOfSets, relation, fds)			
	

#filters the keys from all permutations of all attributes. Thus, this function generates the superkeys
def filterKeys(permutations, relation, fds):
	superkeys = set(frozenset(""))
	for element in permutations:
		if isKey(element, relation, fds):
			superkeys.add(element)
	return superkeys
	
#prunes all subsets in the given set of sets (which are the superkeys). Only minimal keys will survive (the candidate keys)
def pruneSubsets(superkeys):
	prune = set(frozenset(""))
	for element1 in superkeys:
		for element2 in superkeys:
				if element1 < element2:
					prune.add(element2)
	return superkeys-prune
	
	
#set("ABCDEF")
#-->
#set([frozenset("A"), frozenset("B"),frozenset("C"),frozenset("D"),frozenset("E"),frozenset("F")])
def getSetOfSingleElementSets(relation):
	soses = set(frozenset(""))
	for element in relation:
		soses.add(frozenset(element))
	return soses
	
	
#computes all candidate keys for the relation (not very efficient). But it works.
def getKeysNotEfficient(relation, fds):
	relationSubsets = getSetOfSingleElementSets(relation)
	allCombinations = makePermutations(relationSubsets, relation, fds)
	superKeys = filterKeys(allCombinations, relation, fds)
	candidateKeys = pruneSubsets(superKeys)
	return candidateKeys


#computes all candidate keys for the relation quite efficient
def getKeys(relation, fds):
	ccover = canonicalCover(fds)[-1]
	l,r,b = getLRB(ccover)
	relationOnlyFDAttributes = l.union(r.union(b))
	if attributhuelle(l, fds) == relationOnlyFDAttributes:
		return  set((l.union(relation-relationOnlyFDAttributes),))
	else:
		#step 3, consider b
		#add attributes from b to l
		partkeys = findRestCandidateKeys(l,b,fds, relationOnlyFDAttributes)
		keys = set("")
		for key in partkeys:
			keys.add(key|(relation-relationOnlyFDAttributes))
		return pruneSubsets(keys)


#returns a sorted list of attributes
def getFirstKey(keys):
	keysList = []
	for key in keys:
		keysList.append(sorted(list(key)))
	return sorted(keysList)[0]


def convertEmptySetKeyToRelation(keys, relation):
	emptySet = set("")
	emptySet.add(frozenset(EMPTY_SET))	
	if keys == emptySet:
		relationSet = set("")
		relationSet.add(frozenset(relation))
		return relationSet
	else:
		return keys


def findRestCandidateKeys(l, b, fds, relation):
	keys =	set(frozenset(""))
	for battr in b:
		if attributhuelle(l | frozenset(battr), fds) == relation:
			#key
			keys.add(l | frozenset(battr))
		else:
			#here the new b (b-frozenset(battr)) contains possibly attributes that have been added as a key in the if.
			#thus we create superkeys here and have to prune them later
			keys=keys|(findRestCandidateKeys(l | frozenset(battr), b-frozenset(battr), fds, relation))
	return keys

#checks if the given attribute is contained in a key
def isKeyAttribute(attribute, keys):
	for attrSet in keys:
		if attribute in attrSet:
			return True
	return False


#returns a set of left (side=0) or right (side=1) side attributes
def getLeftOrRightSideAttributes(fds, side):
	attributes=EMPTY_SET
	for fd in fds:
		for attr in fd[side]:
			attributes=attributes+attr
	attributes = frozenset(attributes)
	return attributes


def getLeftSideAttributes(fds):
	return getLeftOrRightSideAttributes(fds, 0)

def getRightSideAttributes(fds):
	return getLeftOrRightSideAttributes(fds, 1)


def getLRB(fds):
	#those attributes that only occur on the left side (not on the right)
	l = getLeftSideAttributes(fds) - (getRightSideAttributes(fds)-frozenset(EMPTY_SET))
	#those attributes that only occur on the right side (not on the left)
	r = getRightSideAttributes(fds) - (getLeftSideAttributes(fds)-frozenset(EMPTY_SET))
	#those attributes that occur on both sides
	b = getLeftSideAttributes(fds) & getRightSideAttributes(fds)
	return (l,r,b)

#checks if Attribute appears on the right side of a fd
def isAttributeOnRightSide(attribute, fds):
	for fd in fds:
		for attr in fd:
			if attr == attribute:
				return True
	return False


	
#checks if all given attributes are contained in a key
def areAllKeyAttributes(attributes, keys):
	for attribute in attributes:
		if not(isKeyAttribute(attribute, keys)):
			return False
	return True
	
#checks if the given set of attributes is a proper subset of a key
def isProperSubsetOfKey(attributes, keys):
	for attrSet in keys:
		if attributes < attrSet:
			return True
	return False
	
#checks if the given fd is trivial	
def isTrivial(fd):
	return fd[1] <= fd[0]
	
	
def isTrivial4NF(mvd, relation):
	return isTrivial(mvd) or mvd[0]|mvd[1]==relation
	
#checks if the given set of attributes is a superkey
def isSuperKey(attributes, keys):
	for keySet in keys:
		if keySet <= attributes:
			return True
	return False

	
def isOneNF(relation, fds):
	return True
	

def isTwoNF(relation, fds):
	keys = getKeys(relation, fds)
	for fd in fds:
		for attribute in fd[1]:
			if (not(isKeyAttribute(attribute, keys))) & (isProperSubsetOfKey(fd[0], keys)):
				return False
	return True
	

def isThreeNF(relation, fds):
	keys = getKeys(relation, fds)
	for fd in fds:
		if (not(isTrivial(fd))) & (not(isSuperKey(fd[0], keys))) & (not(areAllKeyAttributes(fd[1], keys))):
			return False
	return True
	
	
def isBCNF(relation, fds):
	keys = getKeys(relation, fds)
	for fd in fds:
		if (not(isTrivial(fd))) & (not(isSuperKey(fd[0], keys))):
			return False
	return True
	
def isFourNF(relation, fds, mvds):
	keys = getKeys(relation, fds)
	for mvd in fds+mvds:
		if (not(isTrivial4NF(mvd, relation))) & (not(isSuperKey(mvd[0], keys))):
			return False
	return True

def leftReduction(fds):
	#new fds will be stored here
	newfds = fds[:]
	for i in range(len(fds)):
		leftSide=fds[i][0].copy()
		for attr in leftSide:
			#new fd with one less attribute on the right
			newFdTest = (newfds[i][0]-set(attr), newfds[i][1])
			#if the new FD passes the test, replace the old one
			if newFdTest[1] <= attributhuelle(newFdTest[0], fds):
				newfds[i]=newFdTest
	return newfds
	
	
	
def rightReduction(fds):
	#new fds will be stored here
	newfds = fds[:]
	for i in range(len(fds)):
		rightSide=fds[i][1].copy()
		for attr in rightSide:
			if attr != EMPTY_SET:
				#new fd with one less attribute on the right
				newFdTest = (newfds[i][0], newfds[i][1]-set(attr))
				#remember what we had so far
				oldFds = newfds[:]
				#add new test fd. Then, we check if we can keep it or whether we have to go back to the old state
				newfds[i]=newFdTest

				if attributhuelle(oldFds[i][0], newfds) != attributhuelle(oldFds[i][0], oldFds):
					newfds[i]=oldFds[i]
	return newfds

#removes fds ALPHA->[EMPTY]	
def removeEmptyRightSide(fds):
	newfds = []
	for fd in fds:
		if len(fd[1]) > 0 and fd[1] != set(EMPTY_SET):
			newfds.append(fd)
	return newfds
	
#merges fds with same left side
def collapseEqualLeftSides(fds):
	for i in range(len(fds)):
		for j in range(len(fds)):
			if i!=j and fds[i][0]==fds[j][0]:
				fds[i]=(fds[i][0],fds[i][1]|fds[j][1])
				fds[j]=(fds[i][0], set(""))
	return removeEmptyRightSide(fds)


#computes the canonical cover of the given fds	
def canonicalCover(fds):
	step1 = leftReduction(fds[:])
	step2 = rightReduction(step1[:])
	step3 = removeEmptyRightSide(step2[:])
	step4 = collapseEqualLeftSides(step3[:])
	return (step1, step2, step3, step4)

#generates relations from fds of the canonical cover
def generateNewRelations(canonicalCover):
	newRelations = []
	for fd in canonicalCover:
		newRelations.append(fd[0]|fd[1])
	return newRelations

	
def addRelationWithKey(relations, keys):
	keyFound = False
	for r in relations:
		for k in keys:
			if k <= r:
				keyFound=True
				break
	if not(keyFound):
		addKey = getFirstKey(keys)
		relations.append(set(addKey))
	return relations
	
def removeRedundantSchemas(relations):
	removeIndexes = set()
	
	for i in range(len(relations)):
		for j in range(len(relations)):
			if (i != j) and (relations[i] < relations[j]):
				removeIndexes.add(i)
			elif (i > j) and (relations[i] == relations[j]):
				removeIndexes.add(i)
	newRelations = []
	for i in range(len(relations)):
		if i not in removeIndexes:
			newRelations.append(relations[i])
	return newRelations
	
	

def synthesealgorithm(canonicalCover, keys, fds):
	#canonical cover
	step1 = canonicalCover[-1]
	step2 = generateNewRelations(step1[:])
	step2Keys = getKeysOfRelations(step2, fds)
	step3 = addRelationWithKey(step2[:], keys)
	step3Keys = getKeysOfRelations(step3, fds)
	step4 = removeRedundantSchemas(step3[:])
	step4Keys = getKeysOfRelations(step4, fds)
	#return result relations for each step together with their keys. For step 1, we return the canonical cover
	return (step1,(step2,step2Keys),(step3,step3Keys),(step4,step4Keys))
	

def getKeysOfRelations(relations, fds):
	keysOfRelations = []
	for r in relations:
		fdsInR = fdsInRelation(fds, r)
		keys = getKeys(r, fdsInR)
		keysOfRelations.append(keys)
	return keysOfRelations


def getFirstNonBCNFfd(relation, fds):
	keys = getKeys(relation, fds)
	for fd in fds:
		if not isTrivial(fd) and not isSuperKey(fd[0], keys):
			#just return the non-trivial part of this fd
			return (fd[0], fd[1]-fd[0]|set(EMPTY_SET))
	return ()
	
	
def getFirstNon4NFmvd(relation, fds, mvds):
	keys = getKeys(relation, fds)
	for mvd in fds+mvds:
		if not isTrivial4NF(mvd, relation) and not isSuperKey(mvd[0], keys):
			return mvd
	return ()
	
	
def fdsInRelation(fds, relation):
	fdsInRelation = []
	for fd in fds:
		for b in fd[1]:
			newfd = (fd[0], set(b))
			if (newfd[0]|newfd[1]) <= relation:
				fdsInRelation.append(newfd)
	return collapseEqualLeftSides(fdsInRelation)
	
	
def mvdsInRelation(mvds, relation):
	mvdsInRelation = []
	for mvd in mvds:
		if (mvd[0]|mvd[1]) <= relation:
			mvdsInRelation.append(mvd)
	return mvdsInRelation
	

	
def decompositionAlgorithm(fds, relation, mvds=None):
	collapseEqualLeftSides(fds)
	stepsString = ""
	resultString = ""
	if mvds is None:
		heading = "Schema in BCNF"
	else:
		heading = "Schema in 4NF"

	res =  decompositionAlgorithmRec(fds, relation, mvds)
	newRelations=res[0]
	for r in res[1]:
		stepsString = stepsString + r
	#resultString =  views.wrapInPanel(heading, res[2], 2)  
	for r in res[2]:
		resultString = resultString + r
		
	resultString =  views.wrapInPanel(heading, resultString, 2)  
	return (newRelations, stepsString, resultString)



def decompositionAlgorithmRec(fds, relation, mvds=None, relations=[], stepsString=[], resultString=[], i=""):
	fdsInR = fdsInRelation(fds, relation)

	if mvds is not None:
		mvdsInR = mvdsInRelation(mvds, relation)
		currentfd = getFirstNon4NFmvd(relation, fdsInR, mvdsInR)
	else:
		currentfd = getFirstNonBCNFfd(relation, fdsInR)

	keyOfRelation = getFirstKey(getKeys(relation,fdsInRelation(fds, relation)))
	relationString = views.relationToString(relation, i, keyOfRelation)+"<br/>"

	if currentfd != ():

		#remove the relation from the result string as this will be splitted now
		for x, r in enumerate(resultString):
			if r == relationString:
				del(resultString[x])


		#Split the relation into two relations based on the fd which hurts the BCNF (currentfd)
		#and test them again recursively
		r1 = currentfd[0]|currentfd[1]
		r2 = (relation - currentfd[1]) | set(EMPTY_SET)
		keyOfR1 = getFirstKey(getKeys(r1,fdsInRelation(fds, r1)))
		keyOfR2 = getFirstKey(getKeys(r2,fdsInRelation(fds, r2)))
		newStepString = views.wrapInPanel(views.relationToString(relation, i)+" aufspalten", views.relationToString(r1, i+"1", keyOfR1)+"<br/>"+views.relationToString(r2, i+"2", keyOfR2), 2)
		if newStepString not in stepsString:
			stepsString.append(newStepString)

		res = decompositionAlgorithmRec(fds, r1, mvds, relations, stepsString, resultString, i+"1")
		res2 = decompositionAlgorithmRec(fds, r2, mvds, relations, stepsString, resultString, i+"2")

		return (relations, stepsString, resultString)
	else:
		if relationString not in resultString:
			resultString.append(relationString)

		relations.append(relation)
		relations = removeRedundantSchemas(relations)
		return (relations, stepsString, resultString) 
	
	
#checks if all attributes in the fds and mvds are contained in the relation
def checkIfAllAttributesAreInRelation(fds, mvds, relation):
	for fd in fds+mvds:
		for attr in fd[0]|fd[1]:
			if attr not in relation and attr != EMPTY_SET:
				return False
	return True
	

	

def getNormalForms(relation, fds, mvds):
	normalForms = ()
	if isFourNF(relation, fds, mvds):
		normalForms = (True,True,True,True,True)
	elif isBCNF(relation, fds):
		normalForms = (True,True,True,True,False)
	elif isThreeNF(relation, fds):
		normalForms = (True,True,True,False,False)
	elif isTwoNF(relation, fds):
		normalForms = (True,True,False,False,False)
	elif isOneNF(relation, fds):
		normalForms = (True,False,False,False,False)
	else:
		normalForms = (True,False,False,False,False)
	return normalForms
	
def generateNewFD(relation):
		numberOfAttributesLeft = random.randint(1, 3)
		numberOfAttributesRight = random.randint(1, 4)
		newLeft = set("")
		newRight = set("")
		for i in range(0,numberOfAttributesLeft):
			newLeft = newLeft|set(random.sample(relation, 1))
		for i in range(0,numberOfAttributesRight):
			newRight = newRight|set(random.sample(relation, 1))
		newfd = (newLeft, newRight)
		return newfd
		
		
def generateFDs(relation):
	fds = []
	randomNumber = random.randint(1, 100)
	x = 125
	while(x >= randomNumber):
		#add FD
		newfd = generateNewFD(relation)
		fds.append(newfd)
		x=x-25	
	return fds
	
def generateMVDs(relation):
	mvds = []
	randomNumber = random.randint(1, 100)
	x = 75
	while(x >= randomNumber):
		#add MVD
		newmvd = generateNewFD(relation)
		mvds.append(newmvd)
		x=x-25
	return mvds
	
#generates relation
def generateNewRelation(numberOfAttributes):
	alphabet = list(string.ascii_uppercase)	
	return set(alphabet[:numberOfAttributes])


#generates relation with random german words as attribute names
def generateNewRelationFun(numberOfAttributes):
	resetDictionaries()
	lines = set("")
	attributes = set("")
	for i in range(0,numberOfAttributes):
		#pick random line numbers between 0 and 113643 (this is where the nouns in the ngerman file end)
		lines.add(random.randint(0,113643))
	f = open("static/dict/ngerman")
	try:
		for i, line in enumerate(f):
			if i in lines:
				attribute = line.replace("\n","")
				attributes.add(attribute)
				
	finally:
		f.close()
	return attributes

	

def generateNewProblem(numberOfAttributes, includeMvds, funMode):
	random.seed(datetime.now())
	if funMode==1:
		relation = generateNewRelationFun(int(numberOfAttributes))
	else:
		relation = generateNewRelation(int(numberOfAttributes))
	fds = generateFDs(relation)
	mvds = []
	if includeMvds:
		mvds = generateMVDs(relation)
	return (relation, fds, mvds)



def splitFdMvd(fdMvd, isFd):
	if isFd:
		delimiter = '->'
	else:
		delimiter = '->>'
	return re.split(delimiter, fdMvd, 1)

def parseFdMvd(fdMvd, isFd):
	newfdMvd = splitFdMvd(fdMvd, isFd)

	left = newfdMvd[0]
	right = newfdMvd[1]


	leftArray = left.split(",")
	rightArray = right.split(",")
	
	if longAttributeNamesUsed():
		#long attribute names are being used
		if left != "":
			left=""
			for attr in leftArray:
				next = dictionaryNameToRepl.get(attr)
				if not next:
					#this attribute does not appear in the relation
					#add something which is definitely not a attribute name, such that an error message will be displayed when validating
					left=left+"!"
				else:
					left = left + next
		if right.replace(" ","") != "":
			right=""
			for attr in rightArray:
				next = dictionaryNameToRepl.get(attr)
				if not next:
					right= right+"!"
				else:
					right = right + next
	
	left = left+EMPTY_SET
	right = right+EMPTY_SET	
	#add empty sets on both sides of the fd / mvd	
	return (set(left), set(right))


def parseInputFDsMVDs(inputString):
	fdsAndMvds = inputString.split()
	fds = []
	mvds = []
	for element in fdsAndMvds:
		if "->>" in element:
			mvds.append(parseFdMvd(element, False))
		elif "->" in element:		
			fds.append(parseFdMvd(element, True))
		elif not re.search("\s+", element):
			#Cannot parse this as it is no empty line and has no -> or ->> included
			return ([],[])
	return (fds,mvds)

def validateInput(relation, fds, mvds):
	if len(relation) >MAX_NUM_OF_ATTRIBUTES:
		return views.getErrorMessageBox("Bitte nicht mehr als "+str(MAX_NUM_OF_ATTRIBUTES)+" Attribute eingeben!")
	elif not checkIfAllAttributesAreInRelation(fds, mvds, relation):
		return views.getErrorMessageBox("Es gibt Attribute, die in FDs/MVDs vorkommen, aber nicht in der Relation!")
	elif fds==[] and mvds==[]:
		return views.getErrorMessageBox("Ich verstehe deine Eingabe nicht. Hast du die FDs/MVDs korrekt eingegeben?")
	else:
		return "OK"
	


#dictionaries to remember what we have replaced by what. We store this in both directions
dictionaryReplToName = {}
dictionaryNameToRepl = {}

def resetDictionaries():
	dictionaryReplToName = {}
	dictionaryNameToRepl = {}

#returns whether long attribute names are used or not
def longAttributeNamesUsed():
	if dictionaryReplToName or dictionaryNameToRepl:
		#long attribute names are used when the dictionaries are filled
		return True
	else:
		return False


#Input is of form [Relation][FD1 FD2...]
def parseInput(input):
	wordCharacters = "A-Za-z\s"+UMLAUTS
	#one character attribute names, i.e. in R(ABC)
	match = re.search("\[(["+wordCharacters+"]+)\]\[((["+wordCharacters+"]|\s|->{1,2})+)\]\[(.+)\]", input)
	#attribute names with multiple characters, like in R(Attr1,Attr2,Attr3)
	match2 = re.search("\[(["+wordCharacters+",]+)\]\[((["+wordCharacters+",]|\s|->{1,2})+)\]\[(.+)\]", input)
	resetDictionaries()
	if match or match2:
		if match:
			relationString = match.group(1).replace(" ", "")
			fdMvdString = match.group(2).replace(" ", "")
			numberOfAttributes = match.group(4)
		else:
			numberOfAttributes = match2.group(4)
			relationString = match2.group(1).replace(" ", "")
			relationStringArray = relationString.split(",")
			relationString = ""
			attributes = set("")
			alphabet = list(string.ascii_uppercase)	
			for attr in relationStringArray:
				if attr not in attributes:
					replacement = alphabet[len(attributes)]
					attributes.add(attr)
					dictionaryReplToName[replacement] = attr	
					dictionaryNameToRepl[attr] = replacement					
					relationString = relationString + replacement			
			fdMvdString = match2.group(2).replace(" ", "")		

		relation = set(relationString)
		fds, mvds = parseInputFDsMVDs(fdMvdString)

		inputCheck = validateInput(relation, fds, mvds)
		if inputCheck == "OK":
			return(relation, fds, mvds, numberOfAttributes)
		else:
			return (inputCheck,)
	else:
		return (views.getErrorMessageBox("Falsches Eingabeformat. Bitte überprüfe deine Eingabe!"),)





		
def computeEverything(relation, fds, mvds):
	relation.add(EMPTY_SET)
	keys = convertEmptySetKeyToRelation(getKeys(relation, fds), relation)
	normalForms = getNormalForms(relation, fds, mvds)
	cCover = canonicalCover(fds[:])
	schema3NF = synthesealgorithm(cCover, keys, fds)
	schemaBCNF = decompositionAlgorithm(fds, relation)
	schema4NF = decompositionAlgorithm(fds, relation, mvds)
	result = {"keys":keys, "normalForms":normalForms, "canonicalCover":cCover, "schema3NF":schema3NF, "schemaBCNF":schemaBCNF, "schema4NF":schema4NF}
	return result

	
"""	
#Some test data

#fds = [(set("D"),set("CA")), (set("C"),set("BA"))]
#fds = [(set("A"),set("B")), (set("C"),set("D")), (set("E"),set("AC")), (set("F"),set("CD")), (set("D"),set("BEF"))]
#fds = [(set("AD"),set("BC")), (set("DE"),set("BG")), (set("FCD"),set("A")), (set("AF"),set("DE")), (set("C"),set("AB"))]
#fds = [(set("B"),set("DA")), (set("DEF"),set("B")), (set("C"),set("EA"))]
fds = [(set("AB"),set("C"))]
mvds = [(set("A"),set("CD"))]

relation = set("ABCD")
#relation = set("ABCDEF")
#relation = set("ABCDEFGH")
#relation = set("ABCDEF")


#number of attributes of the random relation to be generated
numberOfAttributes=5

#generate new problem
#relation = generateNewRelation(numberOfAttributes)
#fds = generateFDs(relation)
#mvds = generateMVDs(relation)
	



("---- Relation ----")
print(relation)
print("------ FDs -------")
print(fds)
print("------ MVDs -------")
print(mvds)
	
	
	

keys = getKeys(relation, fds)
print("--- Candidate Keys ---")
print(keys)


synthesealgorithm(fds, keys)
#decompositionAlgorithm(fds, relation)
#decompositionAlgorithm4NF(fds, mvds, relation)
"""
