#! /usr/local/dist/bin/python
# -*- coding: utf8 -*-

import DBnormalizer 
import random

EMPTY_SET_HTML="&empty;"

def keysToString(keys):
	keyString=""
	for key in keys:
		keyString = keyString + "{"
		keyString = keyString + setOfAttributesToString(key)
		keyString = keyString + "}<br/>"
	return keyString
	
	
def setOfAttributesToString(attributes, key=None):
	setOfAttributesString=""
	delimiter=""
	for i,attr in enumerate(attributes):
		if attr != DBnormalizer.EMPTY_SET:
			if key is not None and attr in key:
				underlineAttribute=True
			else:
				underlineAttribute=False

			if DBnormalizer.longAttributeNamesUsed():
				attr = DBnormalizer.dictionaryReplToName[attr]
				if i < len(attributes)-2:
					delimiter=", "
				else:
					delimiter=""
			elif len(attr)>1:
				#fun mode
				if DBnormalizer.EMPTY_SET in attributes:
					offset = 2
				else:
					offset=1
				if i < len(attributes)-offset :
					delimiter=", "
				else:
					delimiter=""

			setOfAttributesString = setOfAttributesString + underlineString(attr, underlineAttribute) + delimiter
	return setOfAttributesString


def underlineString(string, underline):
	if underline:
		return "<u>"+string+"</u>"
	else:
		return string

	
def relationToString(relation, i, key = None):
	relationString="R<sub>"+i+"</sub>:={"
	relationString=relationString+setOfAttributesToString(relation, key)
	relationString = relationString + "}"
	return relationString
	
	
def fdsToString(fds):
	return fdsMvdsToString(fds, True)

	
def fdsToHtmlString(fds):
	return fdsToString(fds).replace("\n", "<br/>")
	


def mvdsToString(mvds):
	return fdsMvdsToString(mvds, False)

def mvdsToHtmlString(mvds):
        return mvdsToString(mvds).replace("\n", "<br/>")



def fdsMvdsToString(fdMvds, isFds):
	if isFds:
		delimiter="->"
	else:
		delimiter="->>"
	fdMvdString=""
	for fdMvd in fdMvds:
		left = setOfAttributesToString(fdMvd[0])
		right = setOfAttributesToString(fdMvd[1])
		if left == "":
			left = EMPTY_SET_HTML
		if right == "":
			right = EMPTY_SET_HTML
		fdMvdString = fdMvdString + left
		fdMvdString = fdMvdString + delimiter
		fdMvdString = fdMvdString + right
		fdMvdString = fdMvdString + "\n"
	return fdMvdString



	


	
def normalFormsToString(normalForms):
	allNormalForms = ["1NF", "2NF", "3NF", "BCNF", "4NF"]
	nfString = ""
	for i in range(len(allNormalForms)):
		nfString = nfString+"""<span class="label label-"""
		if(normalForms[i]):
			label="success"
			glyphicon = "ok"
		else:
			label="danger"
			glyphicon = "flash"
		nfString = nfString+label+"""">"""+allNormalForms[i]+""" <span class="glyphicon glyphicon-"""+glyphicon+"""" aria-hidden=" """+glyphicon+""""></span></span>   """
	return nfString

	
def schemaToString(schema, keys=None):
	schemaString=""
	i=0
	for relation in schema:
		i=i+1
		if keys is not None:
			x = keys[i-1]
			key = random.sample(x,1)[0]
		else:
			key = None
		#print "KEY:"+str(isinstance(keys,list))
		schemaString = schemaString + relationToString(relation, str(i), key) + "<br/>"
	return schemaString	


def numberOfAttributesOptions(x):
	options=""
	for i in range(3,DBnormalizer.MAX_NUM_OF_ATTRIBUTES+1):
		options = options + "<option"
		if i==int(x):
			options = options + " selected"
		options = options + ">"+str(i)+"</option>"
	return options
		
		
def wrapInPanel(heading, content, numberOfColumns):
	if numberOfColumns == 1:
		x = 12
	elif numberOfColumns == 2:
		x = 6
	elif numberOfColumns == 3:
		x = 4
	else:
		x = 3
	panelString = "<div class=\"col-xs-8 col-sm-6 col-md-"+str(x)+"\"><div class=\"panel panel-primary\"><div class=\"panel-heading\"><h3 class=\"panel-title\">"+heading+"</h3></div><div class=\"panel-body\">"+content+"</div></div></div>"
	return panelString
	
	
def getErrorMessageBox(message):
		return """<div class="row"><div class="col-md-12"><div class="alert alert-danger" role="alert"><span class="glyphicon glyphicon-exclamation-sign" aria-hidden="exclamation"></span><span class="sr-only">Error:</span> """+message+"""</div></div></div>"""
	



def canonicalCoverToString(algorithmResult):
	if DBnormalizer.longAttributeNamesUsed():
		numberOfColumns = 2
	else:
		numberOfColumns = 4
	resultString = """<br/><div class="panel panel-default"><div class="panel-heading"><h4>Kanonische Überdeckung</h4></div></div><div class="row">"""
	resultString =  resultString+wrapInPanel("&#x2460; Linksreduktion", fdsToHtmlString(algorithmResult[0]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2461; Rechtsreduktion", fdsToHtmlString(algorithmResult[1]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2462; a&rarr;&empty; entfernen", fdsToHtmlString(algorithmResult[2]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2463; FDs zusammenfassen", fdsToHtmlString(algorithmResult[3]),numberOfColumns)
	resultString =  resultString + """</div>"""
	return resultString



def infoNFwasAlreadySatisfied(normalForm):
	return """<span class="label label-danger"><span class="glyphicon glyphicon-info-sign" aria-hidden="info"></span> Das ursprüngliche Schema war bereits in """+normalForm+"""!</span>"""


def synthesealgorithmToString(algorithmResult, satisfiedNormalForms):
	if DBnormalizer.longAttributeNamesUsed():
		numberOfColumns = 2
	else:
		numberOfColumns = 4

	if satisfiedNormalForms[2]:
		#original schema was already in 3NF. Let the user know this
		info = infoNFwasAlreadySatisfied("3NF")
	else:
		info = ""

	resultString = """<br/><div class="panel panel-default"><div class="panel-heading">"""+info+"""<h4>Synthesealgorithmus (überführt R in 3NF)</h4></div></div><div class="row">"""
	resultString =  resultString+wrapInPanel("&#x2460; Kanonische Überdeckung", fdsToHtmlString(algorithmResult[0]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2461; Relationsschemata formen", schemaToString(algorithmResult[1][0]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2462; Schlüssel hinzufügen", schemaToString(algorithmResult[2][0]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2463; Redundante Schemata eliminieren", schemaToString(algorithmResult[3][0], algorithmResult[3][1]),numberOfColumns)
	resultString =  resultString + """</div>"""
	return resultString

def decompositionAlgorithmToString(algorithmResult, normalForm, satisfiedNormalForms):
	numberOfColumns = 1
	if normalForm == "BCNF" and satisfiedNormalForms[3]:
		#original schema was already in 3NF. Let the user know this
		info = infoNFwasAlreadySatisfied("BCNF")
	elif normalForm == "4NF" and satisfiedNormalForms[4]:
		#original schema was already in 3NF. Let the user know this
		info = infoNFwasAlreadySatisfied("4NF")
	else:
		info = ""
	
	if normalForm=="BCNF":
        	algoResultString = algorithmResult[1]+algorithmResult[2]
	else:
		algoResultString =  wrapInPanel("Schema in "+normalForm, schemaToString(algorithmResult),numberOfColumns)


	resultString = """<br/><div class="panel panel-default"><div class="panel-heading">"""+info+"""<h4>Dekompositionsalgorithmus (überführt R in """+normalForm+""")</h4></div></div><div class="row">"""
	resultString = resultString+ algoResultString
	resultString = resultString+ """</div>"""
	return resultString


	
def resultToString(relation, fds, mvds, result) :
	if mvds != []:
		#MVDs available
		numberOfColumns = 3
		mvdsPanel = wrapInPanel("MVDs", mvdsToHtmlString(mvds),numberOfColumns)
	else:
		#no MVDs, just FDs
		numberOfColumns = 2
		mvdsPanel= ""
	relationPanel = wrapInPanel("Relation", relationToString(relation,""),numberOfColumns)
	fdsPanel = wrapInPanel("FDs", fdsToHtmlString(fds),numberOfColumns)

	numberOfColumns = 2
	keysPanel = wrapInPanel("Kandidatenschlüssel", keysToString(result['keys']),numberOfColumns)
	normalformsPanel = wrapInPanel("Normalformen", normalFormsToString(result['normalForms']),numberOfColumns)
	newschema3NFPanel = synthesealgorithmToString(result['schema3NF'], result['normalForms'])
	canonicalCoverPanel = canonicalCoverToString(result['canonicalCover'])
	newschemaBCNFPanel = decompositionAlgorithmToString(result['schemaBCNF'], "BCNF", result['normalForms'])
	newschema4NFPanel = decompositionAlgorithmToString(result['schema4NF'], "4NF", result['normalForms'])

	return """<div class="panel-body"><h2>Eingabe</h2><div class="panel panel-default"><div class="panel-body"><div class="row">"""+relationPanel + fdsPanel + mvdsPanel + """</div></div></div><br/><h2>Ergebnis</h2><div class="panel panel-default"><div class="panel-body"><div class="row">"""+ keysPanel  + normalformsPanel+ """</div>"""+canonicalCoverPanel+newschema3NFPanel+newschemaBCNFPanel+newschema4NFPanel+ """</div></div></div>"""
