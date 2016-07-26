#! /usr/local/dist/bin/python
# -*- coding: utf8 -*-

import DBnormalizer 
import random
EMPTY_SET_HTML="&empty;"
EMPTY_SET = "$"


def validateCandidateKeys(relation, fds, inputKeysString):
	keys = DBnormalizer.getKeys(relation, fds)
	inputKeysArray = inputKeysString.split()
	inputKeys = set("")
	for k in inputKeysArray:
		inputKeys.add(frozenset(k)|frozenset(EMPTY_SET))
	if not inputKeys:
		inputKeys.add(frozenset(EMPTY_SET))
	isCorrect = True
	for k in keys:
		if k not in inputKeys:
			isCorrect = False
	for k in inputKeys:
		if k not in keys:
			isCorrect = False
	return isCorrect


def validateLeftReduction(fds, leftSides):
	newfds = fds[:]
	for i, ls in enumerate(leftSides):
		newfds[i] = (ls, fds[i][1])
	validLeftReduction = True
	for i, fd in enumerate(fds):
		if DBnormalizer.closure(fd[0], newfds) != DBnormalizer.closure(fd[0], fds) or DBnormalizer.closure(leftSides[i], newfds) != DBnormalizer.closure(leftSides[i], fds) or not leftSides[i] <= fd[0]:
			validLeftReduction = False
	if validLeftReduction:
		if newfds != DBnormalizer.leftReduction(newfds):
			validLeftReduction = False
	if validLeftReduction:
		return newfds
	else:
		return []


def validateRightReduction(fds, rightSides):
	newfds = fds[:]
	for i, rs in enumerate(rightSides):
		newfds[i] = (fds[i][0], rs)
	validRightReduction = True
	for i, fd in enumerate(fds):
		if DBnormalizer.closure(fd[0], newfds) != DBnormalizer.closure(fd[0], fds) or not rightSides[i] <= fd[1]:
			validRightReduction = False
	if validRightReduction:
		if newfds != DBnormalizer.rightReduction(newfds):
			validRightReduction = False
	if validRightReduction:
		return newfds
	else:
		return []

def validateRemoveEmptyRight(fds, removeindices):
	emptyindices=[]
	newfds = []
	for i, fd in enumerate(fds):
		if fd[1] == set(EMPTY_SET):
			emptyindices.append(str(i))
		else:
			newfds.append(fd)
	if set(emptyindices[:]) == set(removeindices[:]):
		return newfds
	else:
		return []


def validateFinalCanonicalCoverFds(fds, fdinputstring):
	inputfds,inputmvds = DBnormalizer.parseInputFDsMVDs(fdinputstring)
	correctfds = DBnormalizer.collapseEqualLeftSides(fds[:])
	correct = True
	for fd in correctfds:
		if fd not in inputfds:
			correct = False
	for fd in inputfds:
		if fd not in correctfds:
			correct = False	
	if correct:
		return correctfds
	else:
		return []



def validateAddKeyRelation(originrelation, fds, relations, keyrelationstring):
	keys = DBnormalizer.getKeys(originrelation, fds)
	keyrelation = frozenset(keyrelationstring) | frozenset(EMPTY_SET)	
	newrelations = relations[:]
	if len(DBnormalizer.addRelationWithKey(relations[:], keys)) > len(relations):
		#key must be added
		if keyrelation in keys:
			newrelations.append(keyrelation)
			return newrelations
		else:
			return []
	else:
		#no key must be added
		if keyrelationstring == "":
			return newrelations
		else:
			return []

def validateRemoveRelations(relations, removeindices):
	redundantindices=[]
	newrelations = DBnormalizer.removeRedundantSchemas(relations)
	newrelationsuser = []
	for i, relation in enumerate(relations):
		if str(i) not in removeindices:
			newrelationsuser.append(relation)
	if sorted(newrelations[:]) == sorted(newrelationsuser[:]):
		return newrelations
	else:
		return []

def validatePrimaryKeys(relations, fds, primarykeys):
	keysAndFds = DBnormalizer.getKeysAndFDsMVDsOfRelations(relations, fds)
	valid = True
	for i, pk in enumerate(primarykeys):
		if pk not in keysAndFds[i]['keys']:
			valid=False
	return valid


def validateDecompositionEnd(relations, fds, mvds, targetnf):
	if targetnf == "BCNF":
		i,r = DBnormalizer.getFirstNonBCNFRelation(relations, fds)
	else:
		i,r = DBnormalizer.getFirstNon4NFRelation(relations, fds, mvds)
	if i==-1:
		return True
	else:
		return False


def validateDecompositionSplit(fds, mvds, splitrelation, newfirstrelation, newsecondrelation, targetnf):
	fdsInR = DBnormalizer.fdsInRelation(fds, splitrelation)
	mvdsInR = DBnormalizer.mvdsInRelation(mvds, splitrelation)
	normalforms = DBnormalizer.getNormalForms(splitrelation, fdsInR, mvdsInR)
	if targetnf == "BCNF":
		i=3
	else:
		i=4
	if not normalforms[i]:
		#splitrelation not in BCNF/4NF, user is correct so far
		return validateDecompositionSplitNewRelations(fdsInR, mvdsInR, splitrelation, newfirstrelation, newsecondrelation, targetnf)
	else:
		#splitrelation already in BCNF/4NF, user is wrong, relation must not be splitted
		return False


def validateDecompositionSplitNewRelations(fdsInR, mvdsInR, splitrelation, newfirstrelation, newsecondrelation, targetnf):
	possibleSplitFdsMvds = DBnormalizer.getAllNonBCNFfds(splitrelation, fdsInR)
	if targetnf == "4NF":
		possibleSplitFdsMvds.extend(DBnormalizer.getAllNon4NFmvds(splitrelation, fdsInR, mvdsInR))
	for fdmvd in possibleSplitFdsMvds:
		r1,r2 = DBnormalizer.splitRelationAtFdMvd(splitrelation, fdmvd)
		if r1 == newfirstrelation and r2 == newsecondrelation:
			return True
	return False




