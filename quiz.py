#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import views
import DBnormalizer
import quizForms
import inputValidation
import re
form = cgi.FieldStorage()


EMPTY_SET = "$"

print """
	<html>
		<head>
			<meta charset="utf-8">
			<title>DBnormalizer</title>
			<link rel="stylesheet" type="text/css" href="http://home.in.tum.de/~becher/static/css/bootstrapcosmo.min.css" />
			<script src="http://home.in.tum.de/~becher/static/js/jquery-1.11.3.min.js"></script>
			<script src="http://home.in.tum.de/~becher/static/js/bootstrap.min.js"></script>
		</head>
	<body>
	<div class="panel panel-default">
  	<div class="panel-body">
		<div class="row">
			<div class="col-md-6">
				<h1><big><a href="index.py" style="text-decoration:none;">DB->normalizer</a></big><small id="dasquiz">Das Quiz</small></h1>
			</div>
		</div>
		<br/>
		<div class="panel panel-default">
			<div class="panel-body">
			<span class="label label-success">DB-Fragen? DB fragen:</span> <a href="mailto:david.becher@mytum.de">david.becher@mytum.de</a>
			</div>
		</div>
		<br/>
"""


def htmlend():
	html = """
	<script>
		$(document).ready(function(){
   		 $('[data-toggle="tooltip"]').tooltip();   
		});
	</script>
	<script>
		$('[data-toggle="popover"]').each(function(){
   		 $(this).popover(
				{
				trigger: 'hover',
				container:$(this)
				}
			);   
		});
	</script>
</body>
		</html>
"""
	return html





try:
	relationString = str(form['relation'].value).replace(" ", "").replace("\n", "").replace("\r", "")
	relation = set(relationString)|set(EMPTY_SET)
	fdsString = re.sub("(\r\n)*", "", str(form['fds'].value), 1)
	fds,mvds = DBnormalizer.parseInputFDsMVDs(fdsString)
	additionalFds = []
	step = str(form['step'].value).replace(" ", "").replace("\n", "").replace("\r", "")
	candidatekeys = DBnormalizer.getKeys(relation, fds)
	alert = ""
	info = ""
	inputpanel = views.inputToString(relation, fds, mvds, additionalFds, "default")
	quizform = ""
	
	try:
		numberOfTries = int(form['numberOfTries'].value)
		numberOfSteps = int(form['numberOfSteps'].value)
	except KeyError:
		numberOfTries = 0
		numberOfSteps = 0
	numberOfTries = numberOfTries + 1
	if (step=='1'):
		#candidate keys
		numberOfSteps = numberOfSteps + 1
		quizform = quizForms.candidateKeys(numberOfTries, numberOfSteps, relationString, fdsString) + htmlend()
	if (step=='2'):
		#validate candidate keys
		try:
			inputCandidateKeys= str(form['candidatekeys'].value).replace(" ", "")
		except KeyError:
			inputCandidateKeys = ""
		if inputValidation.validateCandidateKeys(relation, fds, inputCandidateKeys):
			alert =  views.getSuccessMessageBox("Richtig!")
			inputpanel = views.inputToString(relation, fds,mvds, additionalFds, "default", candidatekeys)
			numberOfSteps = numberOfSteps + 1
			quizform = quizForms.normalForm(numberOfTries, numberOfSteps, relationString, fdsString) + htmlend()
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.candidateKeys(numberOfTries, numberOfSteps, relationString, fdsString) + htmlend()
	if (step=='3-1'):
		#validate normal form
		selectedNF = str(form['normalform'].value)
		if DBnormalizer.getHighestNormalForm(relation, fds, mvds) == selectedNF:
			alert =  views.getSuccessMessageBox("Richtig!")
			numberOfSteps = numberOfSteps + 1
			quizform = quizForms.canonicalCoverLeftReduction(numberOfTries, numberOfSteps, relationString, fdsString, fds)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.normalForm(numberOfTries, numberOfSteps, relationString, fdsString) + htmlend()
		inputpanel = views.inputToString(relation, fds,mvds, additionalFds, "default", candidatekeys)
	if (step=='3-2'):
		#validate left reduction
		leftSides = []
		for i in range(len(fds)):
			try:
				leftSide = set(str(form['fd'+str(i)].value))|set(EMPTY_SET)
			except KeyError:
				leftSide = set(EMPTY_SET)
			leftSides.append(leftSide)
		leftReduction = inputValidation.validateLeftReduction(fds, leftSides)
		if leftReduction:
			alert =  views.getSuccessMessageBox("Richtig!")
			inputpanel = views.inputToString(relation, leftReduction,mvds, additionalFds, "default", candidatekeys)
			numberOfSteps = numberOfSteps + 1
			quizform = quizForms.canonicalCoverRightReduction(numberOfTries, numberOfSteps, relationString, fdsString, leftReduction)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.canonicalCoverLeftReduction(numberOfTries, numberOfSteps, relationString, fdsString, fds)
			inputpanel = views.inputToString(relation, fds,mvds, additionalFds, "default", candidatekeys)
	if (step=='3-3'):
		currentfds, currentmvds = DBnormalizer.parseInputFDsMVDs(str(form['currentfds'].value))
		#validate right reduction
		rightSides = []
		for i in range(len(fds)):
			try:
				rightSide = set(str(form['fd'+str(i)].value))|set(EMPTY_SET)
			except KeyError:
				rightSide = set(EMPTY_SET)
			rightSides.append(rightSide)
		rightReduction = inputValidation.validateRightReduction(currentfds, rightSides)
		if rightReduction:
			alert =  views.getSuccessMessageBox("Richtig!")
			inputpanel = views.inputToString(relation, rightReduction,mvds, additionalFds, "default", candidatekeys)
			numberOfSteps = numberOfSteps + 1
			quizform = quizForms.canonicalCoverRemoveEmptyRight(numberOfTries, numberOfSteps, relationString, fdsString, rightReduction)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.canonicalCoverRightReduction(numberOfTries, numberOfSteps, relationString, fdsString, currentfds)
			inputpanel = views.inputToString(relation, currentfds,mvds, additionalFds, "default", candidatekeys)

	if (step=='3-4'):
		currentfds, currentmvds = DBnormalizer.parseInputFDsMVDs(str(form['currentfds'].value))
		#validate removal of fds
		try:
			removeindices = form.getvalue('removeindices')
			if removeindices is None:
				removeindices = []
			elif not isinstance(removeindices, list):
				removeindices = [removeindices]
		except KeyError:
			removeindices = []
		newfds = inputValidation.validateRemoveEmptyRight(currentfds, removeindices)
		if newfds:
			alert =  views.getSuccessMessageBox("Richtig!")
			numberOfSteps = numberOfSteps + 1
			quizform = quizForms.canonicalCoverCollapse(numberOfTries, numberOfSteps, relationString, fdsString, newfds)
			inputpanel = views.inputToString(relation, newfds,mvds, additionalFds, "default", candidatekeys)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.canonicalCoverRemoveEmptyRight(numberOfTries, numberOfSteps, relationString, fdsString, currentfds)
			inputpanel = views.inputToString(relation, currentfds,mvds, additionalFds, "default", candidatekeys)
	if (step=='4'):
		currentfds, currentmvds = DBnormalizer.parseInputFDsMVDs(str(form['currentfds'].value))
		#validate final fds
		try:
			finalfdinput = str(form['finalfds'].value)
		except KeyError:
			finalfdinput = ""
		canonicalcover = inputValidation.validateFinalCanonicalCoverFds(currentfds, finalfdinput)
		if canonicalcover:
			alert =  views.getSuccessMessageBox("Richtig!")
			relations = DBnormalizer.generateNewRelations(canonicalcover)
			numberOfTries = numberOfTries - 1
			quizform = quizForms.formRelationSchemas(numberOfTries, numberOfSteps, relationString, fdsString, canonicalcover, relations)
			inputpanel = views.inputToString(relation, canonicalcover,mvds, additionalFds, "default", candidatekeys)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.canonicalCoverCollapse(numberOfTries, numberOfSteps, relationString, fdsString, currentfds)
			inputpanel = views.inputToString(relation, currentfds,mvds, additionalFds, "default", candidatekeys)
	if (step=='5'):
		currentfds, currentmvds = DBnormalizer.parseInputFDsMVDs(str(form['currentfds'].value))
		relations = DBnormalizer.generateNewRelations(currentfds)
		numberOfSteps = numberOfSteps + 1
		quizform = quizForms.addKeyRelation(numberOfTries, numberOfSteps, relationString, fdsString, currentfds, relations)
		inputpanel = views.inputToString(relation, currentfds,mvds, additionalFds, "default", candidatekeys)
		if DBnormalizer.getNormalForms(relation, fds, mvds)[2]:
			info = views.getInfoMessageBox("Die Relation ist zwar schon in 3NF, führe den Algorithmus zur Übung trotzdem aus...")
	if (step=='6'):
		currentfds, currentmvds = DBnormalizer.parseInputFDsMVDs(str(form['currentfds'].value))
		#validate addition of relation with key
		try:
			addkeyrelation = form.getvalue('addkeyrelation')
			keyrelation = str(form['newrelation'].value).replace(" ", "")
		except KeyError:
			keyrelation = ""
		relations = DBnormalizer.generateNewRelations(currentfds)
		newrelations = inputValidation.validateAddKeyRelation(relation, fds, relations, keyrelation)
		if newrelations:
			alert =  views.getSuccessMessageBox("Richtig!")
			numberOfSteps = numberOfSteps + 1
			quizform = quizForms.removeRedundantRelations(numberOfTries, numberOfSteps, relationString, fdsString, currentfds, newrelations, keyrelation)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.addKeyRelation(numberOfTries, numberOfSteps, relationString, fdsString, currentfds, relations)
		inputpanel = views.inputToString(relation, currentfds,mvds, additionalFds, "default", candidatekeys)
	if (step=='7'):
		currentfds, currentmvds = DBnormalizer.parseInputFDsMVDs(str(form['currentfds'].value))
		#validate removal of relations
		try:
			removeindices = form.getvalue('removeindices')
			if removeindices is None:
				removeindices = []
			elif not isinstance(removeindices, list):
				removeindices = [removeindices]
		except KeyError:
			removeindices = []
		relations = DBnormalizer.generateNewRelations(currentfds)
		keyrelationstring = str(form['keyrelation'].value).replace("\r", "").replace("\n", "")
		if keyrelationstring != "":
			keyrelation = set(keyrelationstring)|set(EMPTY_SET)
			relations.append(keyrelation)
		newrelations = inputValidation.validateRemoveRelations(relations, removeindices)
		if newrelations:
			alert =  views.getSuccessMessageBox("Richtig!")
			numberOfSteps = numberOfSteps + 1
			quizform = quizForms.choosePrimaryKeys(numberOfTries, numberOfSteps, relationString, fdsString, currentfds, newrelations)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.removeRedundantRelations(numberOfTries, numberOfSteps, relationString, fdsString, currentfds, relations, keyrelationstring)
		inputpanel = views.inputToString(relation, currentfds, mvds, additionalFds, "default", candidatekeys)
	if (step=='8'):
		currentfds, currentmvds = DBnormalizer.parseInputFDsMVDs(str(form['currentfds'].value))
		#validate relation primary keys
		primarykeys = []
		relations = []
		currentrelationsStrings = str(form['currentrelations'].value).split(",")
		for r in currentrelationsStrings:
			relations.append(views.stringToRelation(r))
		relations = DBnormalizer.removeRedundantSchemas(relations[:])
		for i in range(len(relations)):
			try:
				primarykey = set(str(form['pk'+str(i)].value))|set(EMPTY_SET)
			except KeyError:
				primarykey = set(EMPTY_SET)
			primarykeys.append(primarykey)
		if inputValidation.validatePrimaryKeys(relations, currentfds, primarykeys):
			alert =  views.getSuccessMessageBox("Richtig!")
			keysAndFDs = DBnormalizer.getKeysAndFDsMVDsOfRelations(relations, currentfds)
			numberOfTries = numberOfTries - 1
			quizform = quizForms.formResultSyntheseAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, currentfds, relations, keysAndFDs, primarykeys)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.choosePrimaryKeys(numberOfTries, numberOfSteps, relationString, fdsString, currentfds, relations)
		inputpanel = views.inputToString(relation, currentfds, mvds, additionalFds, "default", candidatekeys)
	if (step=='9'):
		additionalFds = DBnormalizer.getAdditionalFDs(fds)
		fds.extend(additionalFds)
		try:
			targetnf = str(form['targetnf'].value).replace(" ", "").replace("\r", "").replace("\n", "")
		except KeyError:
			targetnf = "BCNF"
		try:
			splitrelationIndex = int(form['splitrelation'].value)
			relationnumbers = str(form['relationnumbers'].value).split(",")
			currentrelationsStrings = str(form['currentrelations'].value).split(",")
			currentrelations = []
			for r in currentrelationsStrings:
				currentrelations.append(views.stringToRelation(r))
			if splitrelationIndex == -1:
				if inputValidation.validateDecompositionEnd(currentrelations, fds, mvds, targetnf):
					alert =  views.getSuccessMessageBox("Richtig!")
					numberOfSteps = numberOfSteps + 1
					quizform =  quizForms.choosePrimaryKeys(numberOfTries, numberOfSteps, relationString, fdsString, fds, currentrelations, targetnf, relationnumbers)
				else:
					alert =  views.getErrorMessageBox("Leider falsch!")
					quizform =  quizForms.decompositionAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, currentrelations, relationnumbers, targetnf)
			else:
				try:
					newfirstrelation = views.stringToRelation(str(form['first'+str(splitrelationIndex)].value))
					newsecondrelation = views.stringToRelation(str(form['second'+str(splitrelationIndex)].value))
					splitrelation = currentrelations[splitrelationIndex]
					if inputValidation.validateDecompositionSplit(fds, mvds, splitrelation, newfirstrelation, newsecondrelation, targetnf):
						splitrelationnumber = relationnumbers[splitrelationIndex].strip()
						del(currentrelations[splitrelationIndex])
						del(relationnumbers[splitrelationIndex])
						currentrelations.append(newfirstrelation)
						currentrelations.append(newsecondrelation)
						relationnumbers.append(splitrelationnumber+"1")
						relationnumbers.append(splitrelationnumber+"2")
						alert =  views.getSuccessMessageBox("Richtig!")
						numberOfSteps = numberOfSteps + 1
						quizform =  quizForms.decompositionAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, currentrelations, relationnumbers, targetnf)
					else:
						alert =  views.getErrorMessageBox("Leider falsch!")
						quizform =  quizForms.decompositionAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, currentrelations, relationnumbers, targetnf)
				except KeyError:
					alert =  views.getErrorMessageBox("Du musst neue Relationen eingeben!")
					numberOfTries = numberOfTries - 1
					quizform =  quizForms.decompositionAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, currentrelations, relationnumbers, targetnf)
		except KeyError:
			#init
			relations = [set(relationString)|set(EMPTY_SET)]
			relationnumbers = ['']
			numberOfSteps = numberOfSteps + 1
			quizform =  quizForms.decompositionAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, relations, relationnumbers, targetnf)
			if targetnf == "BCNF":
				nfindex = 3
				if additionalFds:
					info = views.getInfoMessageBox("Ich habe noch FDs hinzugefügt, die mithilfe der Armstrong-Axiome hergeleitet werden können.")
			else:
				nfindex = 4
			if DBnormalizer.getNormalForms(relation, fds, mvds)[nfindex]:
				info = views.getInfoMessageBox("Die Relation ist zwar schon in "+targetnf+", führe den Algorithmus zur Übung trotzdem aus...") + info
		inputpanel = views.inputToString(relation, fds,mvds, additionalFds, "default", candidatekeys)
	if (step=='10'):
		additionalFds = DBnormalizer.getAdditionalFDs(fds)
		fds.extend(additionalFds)
		try:
			targetnf = str(form['targetnf'].value).replace(" ", "").replace("\r", "").replace("\n", "")
		except KeyError:
			targetnf = "BCNF"
		#validate relation primary keys
		primarykeys = []
		relations = []
		currentrelationsStrings = str(form['currentrelations'].value).split(",")
		relationnumbers = str(form['relationnumbers'].value).replace(" ", "").split(",")
		for r in currentrelationsStrings:
			relations.append(views.stringToRelation(r))
		for i in range(len(relations)):
			try:
				primarykey = set(str(form['pk'+str(i)].value))|set(EMPTY_SET)
			except KeyError:
				primarykey = set(EMPTY_SET)
			primarykeys.append(primarykey)
		if inputValidation.validatePrimaryKeys(relations, fds, primarykeys):
			alert =  views.getSuccessMessageBox("Richtig!")
			numberOfTries = numberOfTries - 1
			keysAndFDsMVDs = DBnormalizer.getKeysAndFDsMVDsOfRelations(relations, fds, mvds)
			quizform = quizForms.formResultDecompositionAlgorithm(numberOfTries, numberOfSteps, relationString, fdsString, mvds, relations, relationnumbers, keysAndFDsMVDs, primarykeys, targetnf)
		else:
			alert =  views.getErrorMessageBox("Leider falsch!")
			quizform = quizForms.choosePrimaryKeys(numberOfTries, numberOfSteps, relationString, fdsString, fds, relations, targetnf, relationnumbers)
		inputpanel = views.inputToString(relation, fds, mvds, additionalFds, "default", candidatekeys)
	if (step=='11'):
		numberOfTries = numberOfTries - 1
		quizform = quizForms.quizFinal(numberOfTries, numberOfSteps, relationString, fdsString)
		inputpanel = ""
	print alert
	print info
	print inputpanel
	print quizform
except KeyError:
    	print views.getErrorMessageBox("Upsi, da ist wohl irgendwas schiefgelaufen!")

print htmlend()
