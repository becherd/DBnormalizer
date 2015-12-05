# -*- coding: utf8 -*-

import random 
import string
from datetime import datetime
import re
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
def makePermutations(setOfSets, relation):
	newSetOfSets = setOfSets.copy()
	for element1 in setOfSets:
		for element2 in setOfSets:
				newSetOfSets.add(element1|element2)
	if relation in newSetOfSets:
		return newSetOfSets
	else:
		return makePermutations(newSetOfSets, relation)			
	

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
	
	
#computes all candidate keys for the relation	
def getKeys(relation, fds):
	relationSubsets = getSetOfSingleElementSets(relation)
	allCombinations = makePermutations(relationSubsets, relation)
	superKeys = filterKeys(allCombinations, relation, fds)
	candidateKeys = pruneSubsets(superKeys)
	return candidateKeys
	
#checks if the given attribute is contained in a key
def isKeyAttribute(attribute, keys):
	for attrSet in keys:
		if attribute in attrSet:
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
			#remember what we had so far
			oldFds = newfds[:]
			#add new test fd. Then, we check if we can keep it or whether we have to go back to the old state
			newfds[i]=newFdTest
			if attributhuelle(newFdTest[0], oldFds) != attributhuelle(leftSide, oldFds):
				newfds[i]=oldFds[i]
	return newfds
	
	
	
def rightReduction(fds):
	#new fds will be stored here
	newfds = fds[:]
	for i in range(len(fds)):
		rightSide=fds[i][1].copy()
		for attr in rightSide:
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
		if len(fd[1]) > 0:
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


	
def canonicalCover(fds):
	newfds = leftReduction(fds)
	newfds = rightReduction(newfds)
	newfds = removeEmptyRightSide(newfds)
	newfds = collapseEqualLeftSides(newfds)
	return newfds

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
		addKey = []
		for attr in random.sample(keys, 1)[0]:
			addKey.append(attr)
		relations.append(set(addKey))
	return relations
	
def removeRedundantSchemas(relations):
	removeIndexes = set()
	
	for i in range(len(relations)):
		for j in range(len(relations)):
			if (i != j) and (relations[i] <= relations[j]):
				removeIndexes.add(i)
	newRelations = []
	for i in range(len(relations)):
		if i not in removeIndexes:
			newRelations.append(relations[i])
	return newRelations
	
	

def synthesealgorithm(fds, keys):
	print "-----------------------"
	print "---Synthesealgorithm---"
	print "-----------------------"
	ccover= canonicalCover(fds)
	print "--- Canonical Cover ---"
	print ccover
	newRelations = generateNewRelations(ccover)
	newRelations = addRelationWithKey(newRelations, keys)
	newRelations = removeRedundantSchemas(newRelations)
	print "---  New Relations ---"
	print newRelations
	return newRelations
	

def getFirstNonBCNFfd(relation, fds):
	keys = getKeys(relation, fds)
	for fd in fds:
		if (not(isTrivial(fd))) & (not(isSuperKey(fd[0], keys))):
			return fd
	return ()
	
	
def getFirstNon4NFmvd(relation, fds, mvds):
	keys = getKeys(relation, fds)
	for mvd in fds+mvds:
		if (not(isTrivial4NF(mvd, relation))) & (not(isSuperKey(mvd[0], keys))):
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
	return collapseEqualLeftSides(mvdsInRelation)
	

	
def decompositionAlgorithm(fds, relation):
	print "------------------------"
	print "---Dekomposition Algo---"
	print "------------------------"
	collapseEqualLeftSides(fds)
	newRelations =  decompositionAlgorithmRec(fds, relation, []) if not isBCNF(relation, fds) else relation
	print "---  New Relations ---"
	print newRelations
	return newRelations if type(newRelations) == list else [newRelations]


def decompositionAlgorithmRec(fds, relation, relations):
	fdsInR = fdsInRelation(fds, relation)
	
	currentfd = getFirstNonBCNFfd(relation, fdsInR)

	if currentfd != ():
		#Split the relation into two relations based on the fd which hurts the BCNF (currentfd)
		#and test them again recursively
		r1 = currentfd[0]|currentfd[1]
		r2 = relation - currentfd[1]
		decompositionAlgorithmRec(fds, r1, relations)
		decompositionAlgorithmRec(fds, r2, relations)
		return relations
	else:
		return relations.append(relation) 
		
	
def decompositionAlgorithm4NF(fds, mvds, relation):
	print "-----------------------------"
	print "---Dekomposition Algo 4NF ---"
	print "-----------------------------"
	collapseEqualLeftSides(fds)
	newRelations =  decompositionAlgorithmRec4NF(fds, mvds, relation, []) if not isFourNF(relation, fds, mvds) else relation
	print "---  New Relations ---"
	print newRelations
	return newRelations if type(newRelations) == list else [newRelations]


	
def decompositionAlgorithmRec4NF(fds, mvds, relation, relations):
	fdsInR = fdsInRelation(fds, relation)
	mvdsInR = mvdsInRelation(mvds, relation)

	currentmvd = getFirstNon4NFmvd(relation, fdsInR, mvdsInR)

	if currentmvd != ():
		#Split the relation into two relations based on the mvd which hurts the 4NF (currentmvd)
		#and test them again recursively
		r1 = currentmvd[0]|currentmvd[1]
		r2 = relation - currentmvd[1]
		decompositionAlgorithmRec4NF(fds, mvds, r1, relations)
		decompositionAlgorithmRec4NF(fds, mvds, r2, relations)
		return relations
	else:
		return relations.append(relation) 
	
#checks if all attributes in the fds and mvds are contained in the relation
def checkIfAllAttributesAreInRelation(fds, mvds, relation):
	for fd in fds+mvds:
		for attr in fd[0]|fd[1]:
			if attr not in relation:
				return False
	return True
	

	
def printNormalForms(relation, fds, mvds):
	print "--- Normal Forms ---"
	if isOneNF(relation, fds):
		print("1NF")
	else:
		print("Not even 1NF")
	if isTwoNF(relation, fds):
		print("2NF")
	if isThreeNF(relation, fds):
		print("3NF")
	if isBCNF(relation, fds):
		print("BCNF")		
	if isFourNF(relation, fds, mvds):
		print("4NF")	
	return True

def getNormalForms(relation, fds, mvds):
	normalForms = []
	if isOneNF(relation, fds):
		normalForms.append("1NF")
	if isTwoNF(relation, fds):
		normalForms.append("2NF")
	if isThreeNF(relation, fds):
		normalForms.append("3NF")
	if isBCNF(relation, fds):
		normalForms.append("BCNF")
	if isFourNF(relation, fds, mvds):
		normalForms.append("4NF")
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
	random.seed(datetime.now())
	fds = []
	randomNumber = random.randint(1, 100)
	x = 125
	while(x >= randomNumber):
		#add FD
		newfd = generateNewFD(relation)
		fds.append(newfd)
		x=x-25	
	return fds
	
def generateMVDs (relation):
	random.seed(datetime.now())
	mvds = []
	randomNumber = random.randint(1, 100)
	x = 75
	while(x >= randomNumber):
		#add MVD
		newmvd = generateNewFD(relation)
		mvds.append(newmvd)
		x=x-25
	return mvds
	
def generateNewRelation(numberOfAttributes):
	random.seed(datetime.now())
	alphabet = list(string.ascii_uppercase)	
	return set(alphabet[:numberOfAttributes])	


def parseInputFDsMVDs(inputString):
	fdsAndMvds = inputString.splitlines()
	fds = []
	mvds = []
	for element in fdsAndMvds:
		if "->>" in element:
			newmvd = (re.split('->>', element, 1))
			mvds.append((set(newmvd[0]), set(newmvd[1])))
		elif "->" in element:
			newfd = (re.split('->', element, 1))
			fds.append((set(newfd[0]), set(newfd[1])))
		else:
			print("Cannot parse this!")
			exit()
	return (fds,mvds)

def validateInput(relation, fds, mvds):
	if not checkIfAllAttributesAreInRelation(fds, mvds, relation):
		return "There are attributes in FDs/MVDs which do not appear in the Relation!"
	else:
		return "OK"
	

#Input is of form [Relation][FD1 FD2...]
def parseInput(input):
	print input
	#match = re.search("\\[([A-Za-z]+)\\]\\[([[A-Za-z]\s->]+)\\]", input)
	match = re.search("\[([A-Za-z]+)\]\[(([A-Za-z]|\n|->{1,2})+)\]\[(.+)\]", input)
	if match:
		relation = set(match.group(1))
		fds, mvds = parseInputFDsMVDs(match.group(2).replace(" ", "\n"))
		targetNf = match.group(4)
		inputCheck = validateInput(relation, fds, mvds)
		if inputCheck == "OK":
			return(relation, fds, mvds, targetNf)
		else:
			return (inputCheck,)
	else:
		return ("Wrong Format",)

		
def computeEverything(relation, fds, mvds, targetNf):
	keys = getKeys(relation, fds)
	normalForms = getNormalForms(relation, fds, mvds)
	newSchema = []
	if targetNf == "3NF":
		newSchema = synthesealgorithm(fds, keys)
	elif targetNf == "BCNF":
		newSchema = decompositionAlgorithm(fds, relation)
	elif targetNf == "4NF":
		newSchema = decompositionAlgorithm4NF(fds, mvds, relation)	
	return (keys, normalForms, newSchema)

	
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
	

print("---- Relation ----")
print(relation)
print("------ FDs -------")
print(fds)
print("------ MVDs -------")
print(mvds)
	
	
	

keys = getKeys(relation, fds)
print("--- Candidate Keys ---")
print(keys)

printNormalForms(relation, fds, mvds)

synthesealgorithm(fds, keys)
#decompositionAlgorithm(fds, relation)
#decompositionAlgorithm4NF(fds, mvds, relation)
"""