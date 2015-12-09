#! /usr/local/dist/bin/python
# -*- coding: utf8 -*-

import DBnormalizer 


def keysToString(keys):
	keyString=""
	for key in keys:
		keyString = keyString + "{"
		for attr in key:
			if attr != DBnormalizer.EMPTY_SET:
				keyString = keyString + attr
		keyString = keyString + "}<br/>"
	return keyString
	
	
def setOfAttributesToString(attributes):
	setOfAttributesString=""
	for attr in attributes:
		if attr != DBnormalizer.EMPTY_SET:
			setOfAttributesString = setOfAttributesString + attr
	return setOfAttributesString
	
def relationToString(relation, i):
	relationString="R<sub>"+i+"</sub>:={"
	relationString=relationString+setOfAttributesToString(relation)
	relationString = relationString + "}"
	return relationString
	
	
def fdsToString(fds):
	fdString=""
	for fd in fds:
		for attr in fd[0]:
			if attr == DBnormalizer.EMPTY_SET:
				if len(fd[0])==1:
					#this attribute (which is empty set) is the only one -> display empty set
					attr = "&empty;"
				else:
					#remove the EMPTY_SET place holder
					attr=""
			fdString = fdString + attr
		fdString = fdString + "->"
		for attr in fd[1]:
			if attr == DBnormalizer.EMPTY_SET:
				if len(fd[1])==1:
					#this attribute (which is empty set) is the only one -> display empty set
					attr = "&empty;"
				else:
					#remove the EMPTY_SET place holder
					attr=""
			fdString = fdString + attr
		fdString = fdString + "\n"
	return fdString

	
def fdsToHtmlString(fds):
	return fdsToString(fds).replace("\n", "<br/>")
	
	
def mvdsToString(mvds):
	mvdString=""
	for mvd in mvds:
		for attr in mvd[0]:
			if attr == DBnormalizer.EMPTY_SET:
				if len(mvd[0])==1:
					#this attribute (which is empty set) is the only one -> display empty set
					attr = "&empty;"
				else:
					#remove the EMPTY_SET place holder
					attr=""
			mvdString = mvdString + attr
		mvdString = mvdString + "->>"
		for attr in mvd[1]:
			if attr == DBnormalizer.EMPTY_SET:
				if len(mvd[1])==1:
					#this attribute (which is empty set) is the only one -> display empty set
					attr = "&empty;"
				else:
					#remove the EMPTY_SET place holder
					attr=""
			mvdString = mvdString + attr
		mvdString = mvdString + "\n"
	return mvdString

def mvdsToHtmlString(mvds):
        return mvdsToString(mvds).replace("\n", "<br/>")

	
def normalFormsToString(normalForms):
	nfString = ""
	for nf in normalForms:
		nfString = nfString + nf + "<br/>"
	return nfString

	
def schemaToString(schema):
	schemaString=""
	i=0
	for relation in schema:
		i=i+1
		schemaString = schemaString + relationToString(relation, str(i)) + "<br/>"
	return schemaString	


def numberOfAttributesOptions(x):
	options=""
	for i in range(3,8):
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
		return "<div class=\"container\"><div class=\"col-md-8\"><div class=\"alert alert-danger\" role=\"alert\"><span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span><span class=\"sr-only\">Error:</span> "+message+"</div></div></div>"
	



def canonicalCoverToString(algorithmResult):
	numberOfColumns = 4
	resultString = """<br/><div class="panel panel-default"><div class="panel-heading"><h4>Kanonische Überdeckung</h4></div></div><div class="row">"""
	resultString =  resultString+wrapInPanel("&#x2460; Linksreduktion", fdsToHtmlString(algorithmResult[0]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2461; Rechtsreduktion", fdsToHtmlString(algorithmResult[1]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2462; a&rarr;&empty; entfernen", fdsToHtmlString(algorithmResult[2]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2463; FDs zusammenfassen", fdsToHtmlString(algorithmResult[3]),numberOfColumns)
	resultString =  resultString + """</div>"""
	return resultString



def synthesealgorithmToString(algorithmResult):
	numberOfColumns = 4
	resultString = """<br/><div class="panel panel-default"><div class="panel-heading"><h4>Synthesealgorithmus (überführt R in 3NF)</h4></div></div><div class="row">"""
	resultString =  resultString+wrapInPanel("&#x2460; Kanonische Überdeckung", fdsToHtmlString(algorithmResult[0]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2461; Relationsschemata formen", schemaToString(algorithmResult[1]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2462; Schlüssel hinzufügen", schemaToString(algorithmResult[2]),numberOfColumns)
	resultString =  resultString+wrapInPanel("&#x2463; Redundante Schemata eliminieren", schemaToString(algorithmResult[3]),numberOfColumns)
	resultString =  resultString + """</div>"""
	return resultString

def decompositionAlgorithmToString(algorithmResult, normalForm):
	numberOfColumns = 1
	resultString = """<br/><div class="panel panel-default"><div class="panel-heading"><h4>Dekompositionsalgorithmus (überführt R in """+normalForm+""")</h4></div></div><div class="row">"""
	resultString = resultString+ wrapInPanel("Schema in "+normalForm, schemaToString(algorithmResult),numberOfColumns)
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
	newschema3NFPanel = synthesealgorithmToString(result['schema3NF'])
	canonicalCoverPanel = canonicalCoverToString(result['canonicalCover'])
	newschemaBCNFPanel = decompositionAlgorithmToString(result['schemaBCNF'], "BCNF")
	newschema4NFPanel = decompositionAlgorithmToString(result['schema4NF'], "4NF")

	return """<div class="panel-body"><h2>Eingabe</h2><div class="panel panel-default"><div class="panel-body"><div class="row">"""+relationPanel + fdsPanel + mvdsPanel + """</div></div></div><br/><h2>Ergebnis</h2><div class="panel panel-default"><div class="panel-body"><div class="row">"""+ keysPanel  + normalformsPanel+ """</div>"""+canonicalCoverPanel+newschema3NFPanel+newschemaBCNFPanel+newschema4NFPanel+ """</div></div></div>"""
